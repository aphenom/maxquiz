import json
import random

from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (GameConfig, Player, Question, AdCampaign,
                     GameSession, Answer, JokerUse, Withdrawal)

TRAINING_COUNT = 6
MIN_HUMAN_MS = 800  # bonne réponse plus rapide = suspect


def _player(request):
    pid = request.session.get("player_id")
    return Player.objects.filter(id=pid).first() if pid else None


def _difficulty_for_index(cfg, i, total):
    """Courbe de difficulté : les % du mix découpent la partie en tranches."""
    mix = cfg.difficulty_mix
    bounds, acc = [], 0
    for lvl in ("1", "2", "3", "4"):
        acc += int(mix.get(lvl, 0))
        bounds.append((acc * total / 100.0, int(lvl)))
    for bound, lvl in bounds:
        if i < bound:
            return lvl
    return 4


def _build_deck(cfg, total):
    """Tire des questions aléatoires PAR JOUEUR, difficulté croissante.
    Si une difficulté manque de questions, on complète avec les niveaux voisins."""
    pools = {d: list(Question.objects.filter(active=True, difficulty=d)) for d in (1, 2, 3, 4)}
    for p in pools.values():
        random.shuffle(p)
    deck, used = [], set()

    def draw(level):
        for lvl in [level] + [l for l in (1, 2, 3, 4) if l != level]:
            while pools[lvl]:
                q = pools[lvl].pop()
                if q.id not in used:
                    used.add(q.id)
                    return q
        return None

    for i in range(total):
        q = draw(_difficulty_for_index(cfg, i, total))
        if q is None:
            break  # banque épuisée : la partie sera plus courte
        deck.append(q)
    return deck


def home(request):
    """Routeur d'accueil : un membre d'établissement connecté atterrit sur son
    espace personnel ; sinon, défi public du jour (voir aussi public_daily)."""
    verified_id = request.session.get("verified_player_id")
    if verified_id and Membership.objects.filter(player_id=verified_id).exists():
        return redirect("account_home")
    return public_daily(request)


def public_daily(request):
    cfg = GameConfig.get()
    player = _player(request)
    today = timezone.localdate()
    session = None
    if player:
        session = GameSession.objects.filter(player=player, mode="daily", day=today).first()
    finishers = GameSession.objects.filter(mode="daily", day=today, status="finished").count()
    return render(request, "game/home.html", {
        "cfg": cfg, "player": player, "session": session,
        "finishers": finishers, "tab": "home",
    })


@require_POST
def start(request):
    cfg = GameConfig.get()
    mode = request.POST.get("mode", "daily")
    if mode not in ("daily", "training"):
        mode = "daily"

    player = _player(request)
    if not player:
        return redirect("public_daily")

    total = cfg.daily_question_count if mode == "daily" else TRAINING_COUNT
    deck = _build_deck(cfg, total)
    if not deck:
        return redirect("home")

    try:
        session = GameSession.objects.create(
            player=player, mode=mode, question_ids=[q.id for q in deck])
    except IntegrityError:
        return redirect("home")

    ads = list(AdCampaign.objects.filter(active=True, is_video=False))
    video_ads = list(AdCampaign.objects.filter(active=True, is_video=True)) or ads
    random.shuffle(ads)
    AdCampaign.objects.filter(id__in=[a.id for a in ads]).update(impressions=F("impressions") + 1)

    payload = {
        "session_id": session.id,
        "mode": mode,
        "total": len(deck),
        "ad_every": cfg.ad_every,
        "timers": cfg.timer_by_difficulty,
        "joker": {
            "paid": cfg.joker_paid_enabled,
            "ad": cfg.joker_ad_enabled,
            "max": cfg.joker_max_per_game if cfg.rewards_enabled else 0,
            "prices": cfg.joker_price_by_difficulty,
        },
        "balance": player.balance,
        "rewards_enabled": cfg.rewards_enabled,
        "pot": cfg.daily_pot if cfg.rewards_enabled else 0,
        "pot_sponsor": cfg.pot_sponsor,
        "questions": [
            {"id": q.id, "cat": q.get_category_display(), "difficulty": q.difficulty,
             "text": q.text, "options": q.options(),
             "explanation": q.explanation if mode == "training" else ""}
            for q in deck
        ],
        "ads": [{"brand": a.brand, "tagline": a.tagline, "pitch": a.pitch,
                 "emoji": a.emoji, "color": a.color} for a in ads] or
               [{"brand": "Votre marque ici", "tagline": "Espace partenaire MaxQuiz",
                 "pitch": "Les publicités financent la cagnotte des joueurs.",
                 "emoji": "📣", "color": "#F2790F"}],
        "video_ads": [{"brand": a.brand, "tagline": a.tagline, "pitch": a.pitch,
                       "emoji": a.emoji, "color": a.color, "aid": a.id} for a in video_ads] or
                     [{"brand": "Partenaire vidéo", "tagline": "Votre spot ici",
                       "pitch": "15 secondes d'attention totale pour votre marque.",
                       "emoji": "🎬", "color": "#0B9A5C", "aid": None}],
    }
    return render(request, "game/play.html", {"payload": payload, "cfg": cfg})


@require_POST
def answer(request):
    """Valide une réponse. Mode survie : une erreur = élimination (sauf joker)."""
    cfg = GameConfig.get()
    player = _player(request)
    data = json.loads(request.body)
    session = get_object_or_404(GameSession, id=data["session_id"],
                                player=player, status="playing")
    question = get_object_or_404(Question, id=data["question_id"])

    if question.id not in session.question_ids:
        return JsonResponse({"error": "question hors partie"}, status=400)
    if session.answers.filter(question=question).exists():
        return JsonResponse({"error": "déjà répondu"}, status=400)

    idx = session.question_ids.index(question.id)
    timer_s = int(cfg.timer_by_difficulty.get(str(question.difficulty), 15))
    choice = int(data.get("choice", -1))
    time_ms = min(int(data.get("time_ms", timer_s * 1000)), timer_s * 1000)
    is_correct = (choice == question.correct)

    Answer.objects.create(session=session, question=question, choice=choice,
                          time_ms=time_ms, is_correct=is_correct)
    session.total_time_ms += time_ms
    if is_correct and time_ms < MIN_HUMAN_MS:
        session.flagged = True

    resp = {"correct": is_correct, "correct_index": question.correct,
            "explanation": question.explanation, "reached": session.reached,
            "status": "playing", "done": False}

    if is_correct:
        session.reached = idx + 1
        resp["reached"] = session.reached
        if session.reached >= len(session.question_ids):
            session.status = "finished"
            session.finished_at = timezone.now()
            resp["status"] = "finished"
            resp["done"] = True
    else:
        if session.mode == "training":
            # pas d'élimination en entraînement
            session.reached = idx + 1
            resp["reached"] = session.reached
            if session.reached >= len(session.question_ids):
                session.status = "finished"
                session.finished_at = timezone.now()
                resp["status"] = "finished"
                resp["done"] = True
        else:
            # ÉLIMINATION — proposer un joker si possible (récompenses/jokers activés)
            price = int(cfg.joker_price_by_difficulty.get(str(question.difficulty), 500))
            can_joker = cfg.rewards_enabled and session.jokers_used < cfg.joker_max_per_game
            resp["status"] = "eliminated_pending"
            resp["joker_offer"] = {
                "available": can_joker and (cfg.joker_paid_enabled or cfg.joker_ad_enabled),
                "paid": cfg.joker_paid_enabled and can_joker,
                "ad": cfg.joker_ad_enabled and can_joker,
                "price": price,
                "balance": player.balance,
                "remaining": cfg.joker_max_per_game - session.jokers_used,
            }
    # cohérence temporelle globale
    if session.status == "finished":
        elapsed = (session.finished_at - session.started_at).total_seconds() * 1000
        if session.total_time_ms > elapsed * 1.5:
            session.flagged = True
    session.save()
    return JsonResponse(resp)


@require_POST
def joker(request):
    """Utiliser un joker après une mauvaise réponse : payant ou pub vidéo."""
    cfg = GameConfig.get()
    player = _player(request)
    data = json.loads(request.body)
    session = get_object_or_404(GameSession, id=data["session_id"],
                                player=player, status="playing", mode__in=["daily", "space"])
    kind = data.get("kind")
    last = session.answers.order_by("-id").first()
    if not last or last.is_correct or last.saved_by_joker:
        return JsonResponse({"error": "aucun joker à utiliser ici"}, status=400)
    if session.jokers_used >= cfg.joker_max_per_game:
        return JsonResponse({"error": "maximum de jokers atteint"}, status=400)

    idx = session.question_ids.index(last.question_id)
    price = int(cfg.joker_price_by_difficulty.get(str(last.question.difficulty), 500))

    with transaction.atomic():
        if kind == "paid":
            if session.mode != "daily":
                return JsonResponse({"error": "joker payant réservé au jeu public"}, status=400)
            if not cfg.joker_paid_enabled:
                return JsonResponse({"error": "joker payant désactivé"}, status=400)
            p = Player.objects.select_for_update().get(id=player.id)
            if p.balance < price:
                return JsonResponse({"error": "solde insuffisant", "balance": p.balance}, status=402)
            p.balance -= price
            p.save(update_fields=["balance"])
            JokerUse.objects.create(session=session, question_index=idx, kind="paid", price=price)
            balance = p.balance
        elif kind == "ad":
            if session.mode == "daily" and not cfg.joker_ad_enabled:
                return JsonResponse({"error": "joker pub désactivé"}, status=400)
            if session.mode == "space" and not _jokers_ok(session.space, session.quiz):
                return JsonResponse({"error": "joker désactivé pour ce quiz"}, status=400)
            ad = AdCampaign.objects.filter(id=data.get("ad_id")).first()
            if ad:
                AdCampaign.objects.filter(id=ad.id).update(impressions=F("impressions") + 1)
            JokerUse.objects.create(session=session, question_index=idx, kind="ad", ad=ad)
            balance = player.balance
        else:
            return JsonResponse({"error": "type de joker inconnu"}, status=400)

        last.saved_by_joker = True
        last.save(update_fields=["saved_by_joker"])
        session.jokers_used += 1
        session.reached = idx + 1  # la question ratée est franchie grâce au joker
        done = session.reached >= len(session.question_ids)
        if done:
            session.status = "finished"
            session.finished_at = timezone.now()
        session.save()

    return JsonResponse({"ok": True, "balance": balance,
                         "jokers_left": cfg.joker_max_per_game - session.jokers_used,
                         "reached": session.reached,
                         "status": session.status, "done": done})


@require_POST
def give_up(request):
    """Le joueur refuse le joker : élimination définitive pour la journée."""
    player = _player(request)
    data = json.loads(request.body)
    session = get_object_or_404(GameSession, id=data["session_id"],
                                player=player, status="playing")
    session.status = "eliminated"
    session.finished_at = timezone.now()
    session.save()
    return JsonResponse({"ok": True, "reached": session.reached})


def _ranked(sessions):
    """Trie des sessions par performance : finaliste > éliminé, puis question
    atteinte, puis temps total — utilisé pour tous les classements du site."""
    return sorted(sessions, key=lambda s: (s.status != "finished", -s.reached, s.total_time_ms))


def leaderboard(request):
    today = timezone.localdate()
    rows = (GameSession.objects
            .filter(mode="daily", day=today, flagged=False)
            .exclude(status="playing")
            .select_related("player")
            .order_by("-status", "-reached", "total_time_ms")[:50])
    rows = _ranked(rows)
    finishers = sum(1 for s in rows if s.status == "finished")
    cfg = GameConfig.get()
    share = cfg.daily_pot // finishers if finishers else cfg.daily_pot
    return render(request, "game/leaderboard.html", {
        "rows": rows, "player": _player(request), "today": today,
        "cfg": cfg, "finishers": finishers, "share": share, "tab": "board",
    })


def wallet(request):
    player = _player(request)
    if not player:
        return redirect("home")
    if request.method == "POST":
        amount = int(request.POST.get("amount", 0))
        momo = request.POST.get("momo", "").strip()[:20]
        if 0 < amount <= player.balance and momo:
            with transaction.atomic():
                p = Player.objects.select_for_update().get(id=player.id)
                if amount <= p.balance:
                    p.balance -= amount
                    p.save(update_fields=["balance"])
                    Withdrawal.objects.create(player=p, amount=amount, momo_number=momo)
            return redirect("wallet")
    withdrawals = player.withdrawals.order_by("-created_at")[:10]
    player.refresh_from_db()
    return render(request, "game/wallet.html", {
        "player": player, "withdrawals": withdrawals, "tab": "wallet",
    })


# ============================================================
# ESPACES ENTREPRISES (multi-tenant)
# ============================================================
import csv
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils.text import slugify
from .models import Space, Category, SubCategory, Quiz, Membership, OTPCode, License, REWARD_TYPES


def _space(slug):
    return get_object_or_404(Space, slug=slug, active=True)


def _match_membership(space, phone, player):
    """Associe automatiquement un joueur à une entrée de la base établissement
    (Membership) déjà présente pour ce téléphone mais pas encore appariée."""
    if phone:
        Membership.objects.filter(space=space, phone=phone, player__isnull=True).update(
            player=player, matched_at=timezone.now())


def _post_int(post, key):
    """Convertit un champ POST en entier pour filter(id=...), sans planter sur
    une valeur vide (ex. option « Aucune » d'un select) ou absente."""
    val = post.get(key)
    return int(val) if val and val.isdigit() else None


def _unique_slug(scoped_qs, name):
    """Slug unique dans le queryset déjà filtré au bon parent (espace ou catégorie)."""
    base = slugify(name)[:56] or "item"
    slug, i = base, 2
    while scoped_qs.filter(slug=slug).exists():
        slug = f"{base}-{i}"[:60]
        i += 1
    return slug


def _dashboard_gate(request, space):
    """Vérifie le code d'accès au tableau de bord client. Renvoie une réponse à
    retourner directement si l'accès n'est pas encore accordé, sinon None."""
    code = request.GET.get("code") or request.session.get(f"dash_{space.id}")
    if code != space.dashboard_code:
        if request.method == "POST" and request.POST.get("code") == space.dashboard_code:
            request.session[f"dash_{space.id}"] = space.dashboard_code
            return redirect(request.path)
        return render(request, "game/dashboard_login.html", {"space": space})
    request.session[f"dash_{space.id}"] = space.dashboard_code
    return None


def _quiz_dashboard_stats(space, sessions):
    """Taux de bonne réponse par question quiz (pires en premier) et répartition
    des sondages, pour un ensemble de sessions donné."""
    quiz_stats = []
    for q in Question.objects.filter(space=space, kind="quiz", active=True):
        agg = Answer.objects.filter(question=q, session__in=sessions).aggregate(
            n=Count("id"), ok=Count("id", filter=Q(is_correct=True)))
        if agg["n"]:
            quiz_stats.append({"q": q, "n": agg["n"],
                               "pct": round(100 * agg["ok"] / agg["n"])})
    quiz_stats.sort(key=lambda x: x["pct"])

    survey_stats = []
    for q in Question.objects.filter(space=space, kind="survey", active=True):
        answers = Answer.objects.filter(question=q, session__in=sessions, choice__gte=0)
        n = answers.count()
        if n:
            dist = []
            for i, opt in enumerate(q.options()):
                c = answers.filter(choice=i).count()
                dist.append({"opt": opt, "n": c, "pct": round(100 * c / n)})
            survey_stats.append({"q": q, "n": n, "dist": dist})
    return quiz_stats, survey_stats


def space_home(request, slug):
    space = _space(slug)
    player = _player(request)
    today = timezone.localdate()
    already = bool(player and space.one_per_day and GameSession.objects.filter(
        player=player, space=space, day=today).exists())

    # Catégorie/sous-catégorie du profil du joueur dans cet espace : union de
    # toutes ses adhésions (licence en cours ou passée) — (category_id, sub_category_id)
    # avec sub_category_id=None pour un membre affecté à une catégorie sans détail.
    my_pairs = set()
    if player:
        for m in Membership.objects.filter(space=space, player=player):
            if m.sub_category_id:
                my_pairs.add((m.category_id, m.sub_category_id))
            elif m.category_id:
                my_pairs.add((m.category_id, None))
    show_all = request.GET.get("all") == "1" or not my_pairs

    # Arbre de découverte des quiz (facultatif) : catégorie > sous-catégorie > quiz.
    # Un membre au profil connu (catégorie/sous-catégorie) ne voit que ce qui le
    # concerne, pas tout le catalogue — sauf s'il demande explicitement à tout voir.
    categories, orphan_quizzes = [], []
    has_catalog = space.quizzes.filter(active=True).exists()
    if has_catalog:
        for cat in space.categories.prefetch_related("subcategories"):
            subs = []
            for sub in cat.subcategories.all():
                if not show_all and (cat.id, sub.id) not in my_pairs:
                    continue
                qs = list(sub.quizzes.filter(active=True))
                if qs:
                    subs.append({"sub": sub, "quizzes": qs})
            direct = []
            if show_all or (cat.id, None) in my_pairs:
                direct = list(cat.quizzes.filter(active=True, sub_category__isnull=True))
            if subs or direct:
                categories.append({"category": cat, "subs": subs, "direct": direct})
        if show_all:
            orphan_quizzes = list(space.quizzes.filter(active=True, category__isnull=True))

    played_quiz_ids = set()
    if player and has_catalog:
        played_quiz_ids = set(Quiz.objects.filter(sessions__player=player, space=space)
                              .values_list("id", flat=True))

    reward_text, reward_type = _effective_reward(space)
    return render(request, "game/space_home.html", {
        "space": space, "player": player, "already": already,
        "categories": categories, "orphan_quizzes": orphan_quizzes,
        "reward_text": reward_text, "reward_type": reward_type,
        "profile_filtered": bool(my_pairs) and not show_all,
        "show_all": show_all,
        "has_catalog": has_catalog,
        "played_quiz_ids": played_quiz_ids,
    })


@require_POST
def space_start(request, slug):
    space = _space(slug)
    if space.access_code and request.POST.get("access_code", "").strip() != space.access_code:
        return render(request, "game/space_home.html", {
            "space": space, "player": _player(request),
            "error": "Code d'accès incorrect.", "already": False,
        })
    consent = (request.POST.get("consent") == "on") if space.consent_required else True

    player = _player(request)
    if not player:
        return redirect("space_home", slug=slug)
    _match_membership(space, player.phone, player)

    today = timezone.localdate()
    if space.one_per_day and GameSession.objects.filter(
            player=player, space=space, day=today).exists():
        return redirect("space_home", slug=slug)

    # Deck : quiz de l'espace (difficulté croissante) + sondages intercalés
    quiz_pool = list(Question.objects.filter(space=space, active=True, kind="quiz"))
    surveys = list(Question.objects.filter(space=space, active=True, kind="survey"))
    random.shuffle(quiz_pool)
    random.shuffle(surveys)
    quiz_pool.sort(key=lambda q: q.difficulty)
    quiz_pool = quiz_pool[:space.question_count]
    deck = []
    for i, q in enumerate(quiz_pool, 1):
        deck.append(q)
        if space.survey_every and i % space.survey_every == 0 and surveys:
            deck.append(surveys.pop())
    if not deck:
        return redirect("space_home", slug=slug)

    cfg = GameConfig.get()
    session = GameSession.objects.create(
        player=player, mode="space", space=space, consent=consent,
        question_ids=[q.id for q in deck])

    reward_text, reward_type = _effective_reward(space)
    payload = {
        "session_id": session.id,
        "mode": "space",
        "elimination": space.elimination,
        "total": len(deck),
        "ad_every": 0,  # pas de pub tierce dans l'espace d'une marque
        "timers": cfg.timer_by_difficulty,
        "joker": {"paid": False, "ad": False, "max": 0, "prices": {}},
        "balance": 0, "pot": 0, "pot_sponsor": "",
        "brand": {"name": space.name, "emoji": space.emoji,
                  "primary": space.color_primary, "accent": space.color_accent,
                  "reward": reward_text, "reward_type": reward_type},
        "questions": [
            {"id": q.id, "cat": q.get_category_display(), "difficulty": q.difficulty,
             "kind": q.kind, "text": q.text, "options": q.options(), "explanation": ""}
            for q in deck
        ],
        "ads": [], "video_ads": [],
    }
    return render(request, "game/play.html", {"payload": payload, "cfg": cfg})


def _quiz_locked(player, quiz, today):
    """Verrou de rejouabilité selon Quiz.replay_policy : aucun verrou (unlimited),
    une fois par jour (daily, par défaut), ou définitivement après une 1ère
    tentative comptée (once). Une partie abandonnée (statut "playing", jamais
    finie) ne compte jamais comme une tentative — sinon un onglet fermé en
    cours de route bloquerait le joueur pour rien."""
    if not player or quiz.replay_policy == "unlimited":
        return False
    sessions = GameSession.objects.filter(player=player, quiz=quiz, flagged=False).exclude(status="playing")
    if quiz.replay_policy == "once":
        return sessions.exists()
    return sessions.filter(day=today).exists()


def quiz_home(request, slug, quiz_slug):
    """Page d'accueil d'un quiz précis (lien direct partagé par l'entité)."""
    space = _space(slug)
    quiz = get_object_or_404(Quiz, space=space, slug=quiz_slug, active=True)
    player = _player(request)
    today = timezone.localdate()
    already = _quiz_locked(player, quiz, today)
    played_before = bool(player and GameSession.objects.filter(
        player=player, quiz=quiz, flagged=False).exclude(status="playing").exists())
    reward_text, reward_type = _effective_reward(space, quiz)
    return render(request, "game/quiz_home.html", {
        "space": space, "quiz": quiz, "player": player, "already": already,
        "played_before": played_before,
        "reward_text": reward_text, "reward_type": reward_type,
    })


@require_POST
def quiz_start(request, slug, quiz_slug):
    space = _space(slug)
    quiz = get_object_or_404(Quiz, space=space, slug=quiz_slug, active=True)
    if space.access_code and request.POST.get("access_code", "").strip() != space.access_code:
        return render(request, "game/quiz_home.html", {
            "space": space, "quiz": quiz, "player": _player(request),
            "error": "Code d'accès incorrect.", "already": False,
        })
    consent = (request.POST.get("consent") == "on") if space.consent_required else True

    player = _player(request)
    if not player:
        return redirect("quiz_home", slug=slug, quiz_slug=quiz_slug)
    _match_membership(space, player.phone, player)

    today = timezone.localdate()
    if _quiz_locked(player, quiz, today):
        return redirect("quiz_home", slug=slug, quiz_slug=quiz_slug)

    # Deck scopé à la sous-catégorie (ou catégorie) du quiz + sondages de l'espace
    if quiz.sub_category_id:
        quiz_pool = list(Question.objects.filter(
            space=space, active=True, kind="quiz", sub_category=quiz.sub_category))
    elif quiz.category_id:
        quiz_pool = list(Question.objects.filter(
            space=space, active=True, kind="quiz", sub_category__category=quiz.category))
    else:
        quiz_pool = list(Question.objects.filter(space=space, active=True, kind="quiz"))
    surveys = list(Question.objects.filter(space=space, active=True, kind="survey"))
    random.shuffle(quiz_pool)
    random.shuffle(surveys)
    quiz_pool.sort(key=lambda q: q.difficulty)
    quiz_pool = quiz_pool[:quiz.question_count]
    deck = []
    for i, q in enumerate(quiz_pool, 1):
        deck.append(q)
        if quiz.survey_every and i % quiz.survey_every == 0 and surveys:
            deck.append(surveys.pop())
    if not deck:
        return redirect("quiz_home", slug=slug, quiz_slug=quiz_slug)

    cfg = GameConfig.get()
    session = GameSession.objects.create(
        player=player, mode="space", space=space, quiz=quiz, consent=consent,
        question_ids=[q.id for q in deck])

    jokers_ok = _jokers_ok(space, quiz)
    reward_text, reward_type = _effective_reward(space, quiz)
    payload = {
        "session_id": session.id,
        "mode": "space",
        "elimination": quiz.elimination,
        "total": len(deck),
        "ad_every": 0,
        "timers": cfg.timer_by_difficulty,
        "joker": {"paid": False, "ad": jokers_ok, "max": cfg.joker_max_per_game if jokers_ok else 0, "prices": {}},
        "balance": 0, "pot": 0, "pot_sponsor": "",
        "brand": {"name": space.name, "emoji": space.emoji,
                  "primary": space.color_primary, "accent": space.color_accent,
                  "reward": reward_text, "reward_type": reward_type},
        "questions": [
            {"id": q.id, "cat": q.sub_category.name if q.sub_category else q.get_category_display(),
             "difficulty": q.difficulty, "kind": q.kind, "text": q.text,
             "options": q.options(), "explanation": ""}
            for q in deck
        ],
        "ads": [],
        "video_ads": [{"brand": a.brand, "tagline": a.tagline, "pitch": a.pitch,
                       "emoji": a.emoji, "color": a.color, "aid": a.id}
                      for a in AdCampaign.objects.filter(active=True, is_video=True)] if jokers_ok else [],
    }
    if jokers_ok and not payload["video_ads"]:
        payload["video_ads"] = [{"brand": "Partenaire vidéo", "tagline": "Votre spot ici",
                                 "pitch": "15 secondes d'attention totale pour votre marque.",
                                 "emoji": "🎬", "color": "#0B9A5C", "aid": None}]
    return render(request, "game/play.html", {"payload": payload, "cfg": cfg})


@require_POST
def space_answer(request):
    """Réponse dans un espace : sondage toujours accepté, quiz noté,
    élimination seulement si l'espace l'active."""
    player = _player(request)
    data = json.loads(request.body)
    session = get_object_or_404(GameSession, id=data["session_id"], player=player,
                                mode="space", status="playing")
    question = get_object_or_404(Question, id=data["question_id"])
    if question.id not in session.question_ids:
        return JsonResponse({"error": "question hors partie"}, status=400)
    if session.answers.filter(question=question).exists():
        return JsonResponse({"error": "déjà répondu"}, status=400)

    cfg = GameConfig.get()
    idx = session.question_ids.index(question.id)
    timer_s = int(cfg.timer_by_difficulty.get(str(question.difficulty), 15))
    choice = int(data.get("choice", -1))
    time_ms = min(int(data.get("time_ms", timer_s * 1000)), timer_s * 1000)

    if question.kind == "survey":
        is_correct = choice >= 0  # toute opinion exprimée est « valide »
    else:
        is_correct = (choice == question.correct)
        if is_correct and time_ms < MIN_HUMAN_MS:
            session.flagged = True

    Answer.objects.create(session=session, question=question, choice=choice,
                          time_ms=time_ms, is_correct=is_correct)
    session.total_time_ms += time_ms

    space_elimination = session.quiz.elimination if session.quiz_id else session.space.elimination
    eliminated = (question.kind == "quiz" and not is_correct and space_elimination)

    # Joker « pub vidéo » : nécessite un quiz dont la licence de l'espace l'autorise
    joker_offer = None
    if eliminated:
        can_joker = _jokers_ok(session.space, session.quiz) and session.jokers_used < cfg.joker_max_per_game
        if can_joker:
            joker_offer = {
                "available": True, "paid": False, "ad": True, "price": 0,
                "balance": player.balance, "remaining": cfg.joker_max_per_game - session.jokers_used,
            }

    if joker_offer:
        status, done = "eliminated_pending", False
    elif eliminated:
        session.status = "eliminated"
        session.finished_at = timezone.now()
        status, done = "eliminated", True
    else:
        session.reached = idx + 1
        done = session.reached >= len(session.question_ids)
        if done:
            session.status = "finished"
            session.finished_at = timezone.now()
        status = session.status if done else "playing"
    session.save()

    resp = {
        "correct": is_correct, "survey": question.kind == "survey",
        "correct_index": question.correct if question.kind == "quiz" else choice,
        "explanation": "", "reached": session.reached,
        "status": status, "done": done,
    }
    if joker_offer:
        resp["joker_offer"] = joker_offer
    return JsonResponse(resp)


def _quiz_row(sessions, quiz):
    qs = sessions.filter(quiz=quiz)
    t = qs.count()
    f = qs.filter(status="finished").count()
    return {"quiz": quiz, "total": t, "finished": f,
            "completion": round(100 * f / t) if t else 0}


def _build_quiz_tree(space, sessions):
    """Arbre Catégorie > Sous-catégorie > Quiz avec compteurs de participation,
    pour la vue d'ensemble du tableau de bord."""
    quizzes = list(space.quizzes.select_related("category", "sub_category").filter(active=True))
    rows = [_quiz_row(sessions, qz) for qz in quizzes]
    tree = []
    for cat in space.categories.all():
        cat_rows = [r for r in rows if r["quiz"].category_id == cat.id]
        if not cat_rows:
            continue
        subs, seen = [], set()
        for r in cat_rows:
            sub = r["quiz"].sub_category
            if sub.id in seen:
                continue
            seen.add(sub.id)
            sub_rows = [x for x in cat_rows if x["quiz"].sub_category_id == sub.id]
            subs.append({"sub": sub, "rows": sub_rows,
                        "total": sum(x["total"] for x in sub_rows)})
        direct_rows = [r for r in cat_rows if r["quiz"].sub_category_id is None]
        tree.append({"category": cat, "subs": subs, "direct_rows": direct_rows,
                    "total": sum(r["total"] for r in cat_rows)})
    orphan_rows = [r for r in rows if r["quiz"].category_id is None]
    return tree, orphan_rows


def space_dashboard(request, slug):
    """Tableau de bord client, protégé par un code simple (MVP)."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    sessions = GameSession.objects.filter(space=space, flagged=False).exclude(status="playing")
    total = sessions.count()
    finished = sessions.filter(status="finished").count()
    consented = sessions.filter(consent=True).values("player").distinct().count()
    has_quizzes = space.quizzes.exists()

    tree, orphan_rows = _build_quiz_tree(space, sessions)
    # Bucket « Général » : sessions hors quiz (jeu à plat, ou espaces sans catégorie)
    general_sessions = sessions.filter(quiz__isnull=True) if has_quizzes else sessions
    quiz_stats, survey_stats = _quiz_dashboard_stats(space, general_sessions)

    # Export CSV des contacts consentants
    if request.GET.get("export") == "contacts":
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="contacts-{space.slug}.csv"'
        resp.write("﻿")  # BOM : Excel n'auto-détecte pas l'UTF-8 sans lui (accents affichés en charabia)
        w = csv.writer(resp)
        w.writerow(["pseudo", "telephone", "meilleur_score", "parties"])
        for p in Player.objects.filter(sessions__space=space, sessions__consent=True).distinct():
            ps = sessions.filter(player=p)
            best = max((s.reached for s in ps), default=0)
            w.writerow([p.pseudo, p.phone or "", best, ps.count()])
        return resp

    top = _ranked(sessions.select_related("player"))[:10]
    return render(request, "game/dashboard.html", {
        "space": space, "total": total, "finished": finished,
        "completion": round(100 * finished / total) if total else 0,
        "consented": consented, "has_quizzes": has_quizzes,
        "tree": tree, "orphan_rows": orphan_rows,
        "quiz_stats": quiz_stats, "survey_stats": survey_stats, "top": top,
    })


def dashboard_categories(request, slug):
    """Gestion des catégories / sous-catégories de l'espace."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_category":
            name = request.POST.get("name", "").strip()[:80]
            if name:
                cat_slug = _unique_slug(space.categories, name)
                Category.objects.create(space=space, name=name, slug=cat_slug,
                                        order=space.categories.count())
        elif action == "rename_category":
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            name = request.POST.get("name", "").strip()[:80]
            if cat and name:
                cat.name = name
                cat.save(update_fields=["name"])
        elif action == "delete_category":
            space.categories.filter(id=_post_int(request.POST, "category_id")).delete()
        elif action == "add_subcategory":
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            name = request.POST.get("name", "").strip()[:80]
            if cat and name:
                sub_slug = _unique_slug(cat.subcategories, name)
                SubCategory.objects.create(category=cat, name=name, slug=sub_slug,
                                           order=cat.subcategories.count())
        elif action == "rename_subcategory":
            sub = SubCategory.objects.filter(id=_post_int(request.POST, "subcategory_id"),
                                             category__space=space).first()
            name = request.POST.get("name", "").strip()[:80]
            if sub and name:
                sub.name = name
                sub.save(update_fields=["name"])
        elif action == "delete_subcategory":
            SubCategory.objects.filter(id=_post_int(request.POST, "subcategory_id"),
                                       category__space=space).delete()
        return redirect("dashboard_categories", slug=slug)

    categories = space.categories.prefetch_related("subcategories")
    return render(request, "game/dashboard_categories.html", {
        "space": space, "categories": categories,
    })


def dashboard_quizzes(request, slug):
    """Liste + création des quiz (chacun avec son lien direct partageable)."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_quiz":
            name = request.POST.get("name", "").strip()[:100]
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            sub = cat.subcategories.filter(id=_post_int(request.POST, "subcategory_id")).first() if cat else None
            if name:
                quiz_slug = _unique_slug(space.quizzes, name)
                replay_policy = request.POST.get("replay_policy")
                if replay_policy not in dict(Quiz.REPLAY_POLICIES):
                    replay_policy = "daily"
                Quiz.objects.create(
                    space=space, category=cat, sub_category=sub, slug=quiz_slug, name=name,
                    question_count=int(request.POST.get("question_count") or space.question_count),
                    survey_every=int(request.POST.get("survey_every") or space.survey_every),
                    elimination=request.POST.get("elimination") == "on",
                    replay_policy=replay_policy,
                    **_quiz_reward_joker_fields(request.POST))
        elif action == "toggle_quiz":
            qz = space.quizzes.filter(id=_post_int(request.POST, "quiz_id")).first()
            if qz:
                qz.active = not qz.active
                qz.save(update_fields=["active"])
        elif action == "delete_quiz":
            space.quizzes.filter(id=_post_int(request.POST, "quiz_id")).delete()
        return redirect("dashboard_quizzes", slug=slug)

    base_sessions = GameSession.objects.filter(space=space, flagged=False).exclude(status="playing")
    quizzes = list(space.quizzes.select_related("category", "sub_category"))
    for qz in quizzes:
        qz.total = base_sessions.filter(quiz=qz).count()
    categories = space.categories.prefetch_related("subcategories")
    current_license = _current_license(space)
    return render(request, "game/dashboard_quizzes.html", {
        "space": space, "quizzes": quizzes, "categories": categories,
        "jokers_allowed": bool(current_license and current_license.jokers_allowed),
        "reward_types": REWARD_TYPES, "replay_policies": Quiz.REPLAY_POLICIES,
    })


def dashboard_quiz_detail(request, slug, quiz_slug):
    """Détail des stats (questions + sondages) d'un quiz précis."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    quiz = get_object_or_404(Quiz, space=space, slug=quiz_slug)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "edit_quiz":
            name = request.POST.get("name", "").strip()[:100]
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            sub = cat.subcategories.filter(id=_post_int(request.POST, "subcategory_id")).first() if cat else None
            if name:
                quiz.name = name
                quiz.category = cat
                quiz.sub_category = sub
                quiz.question_count = int(request.POST.get("question_count") or space.question_count)
                quiz.survey_every = int(request.POST.get("survey_every") or space.survey_every)
                quiz.elimination = request.POST.get("elimination") == "on"
                replay_policy = request.POST.get("replay_policy")
                if replay_policy in dict(Quiz.REPLAY_POLICIES):
                    quiz.replay_policy = replay_policy
                for field, value in _quiz_reward_joker_fields(request.POST).items():
                    setattr(quiz, field, value)
                quiz.save()
        elif action == "toggle_quiz":
            quiz.active = not quiz.active
            quiz.save(update_fields=["active"])
        elif action == "delete_quiz":
            quiz.delete()
            return redirect("dashboard_quizzes", slug=slug)
        return redirect("dashboard_quiz_detail", slug=slug, quiz_slug=quiz.slug)

    sessions = GameSession.objects.filter(space=space, quiz=quiz, flagged=False).exclude(status="playing")

    if request.GET.get("export") == "answers":
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="reponses-{quiz.slug}.csv"'
        resp.write("﻿")  # BOM : Excel n'auto-détecte pas l'UTF-8 sans lui (accents affichés en charabia)
        w = csv.writer(resp)

        sessions_list = list(sessions.select_related("player").prefetch_related("answers__question"))
        question_ids = {a.question_id for s in sessions_list for a in s.answers.all()}
        questions = list(Question.objects.filter(id__in=question_ids).order_by("kind", "difficulty", "id"))

        w.writerow(["participant", "telephone", "score", "statut", "temps_total_ms"]
                  + [q.text for q in questions])
        for s in sessions_list:
            anonymize = space.consent_required and not s.consent
            name = "Anonyme" if anonymize else s.player.pseudo
            phone = "" if anonymize else (s.player.phone or "")
            answers_by_question = {a.question_id: a for a in s.answers.all()}
            row = [name, phone, s.reached, s.get_status_display(), s.total_time_ms]
            for q in questions:
                a = answers_by_question.get(q.id)
                if not a:
                    row.append("")
                elif a.choice < 0:
                    row.append("(temps écoulé)")
                elif q.kind == "survey":
                    row.append(q.options()[a.choice])
                else:
                    row.append(f"{q.options()[a.choice]} ({'oui' if a.is_correct else 'non'})")
            w.writerow(row)
        return resp

    total = sessions.count()
    finished = sessions.filter(status="finished").count()
    quiz_stats, survey_stats = _quiz_dashboard_stats(space, sessions)
    top = _ranked(sessions.select_related("player"))[:10]
    categories = space.categories.prefetch_related("subcategories")
    current_license = _current_license(space)
    reward_text, reward_type = _effective_reward(space, quiz)
    return render(request, "game/dashboard_quiz_detail.html", {
        "space": space, "quiz": quiz, "total": total, "finished": finished,
        "completion": round(100 * finished / total) if total else 0,
        "quiz_stats": quiz_stats, "survey_stats": survey_stats, "top": top,
        "categories": categories,
        "jokers_allowed": bool(current_license and current_license.jokers_allowed),
        "reward_types": REWARD_TYPES, "replay_policies": Quiz.REPLAY_POLICIES,
        "reward_text": reward_text, "reward_type": reward_type,
    })


def _question_fields_from_post(space, post):
    kind = post.get("kind") if post.get("kind") in ("quiz", "survey") else "quiz"
    sub = SubCategory.objects.filter(id=_post_int(post, "sub_category_id"), category__space=space).first()
    return dict(
        kind=kind,
        sub_category=sub,
        difficulty=int(post.get("difficulty") or 1),
        text=post.get("text", "").strip(),
        option_a=post.get("option_a", "").strip()[:200],
        option_b=post.get("option_b", "").strip()[:200],
        option_c=post.get("option_c", "").strip()[:200],
        option_d=post.get("option_d", "").strip()[:200],
        correct=int(post.get("correct") or 0) if kind == "quiz" else 0,
        explanation=post.get("explanation", "").strip(),
        active=post.get("active") == "on",
    )


def dashboard_questions(request, slug):
    """Gestion des questions (quiz + sondages) de l'espace, avec filtres."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    if request.method == "POST":
        action = request.POST.get("action")
        question_id = request.POST.get("question_id") or 0
        if action in ("add_question", "edit_question"):
            fields = _question_fields_from_post(space, request.POST)
            if fields["text"] and fields["option_a"] and fields["option_b"]:
                if action == "add_question":
                    Question.objects.create(space=space, category="cg", **fields)
                else:
                    Question.objects.filter(id=question_id, space=space).update(**fields)
        elif action == "toggle_question":
            q = Question.objects.filter(id=question_id, space=space).first()
            if q:
                q.active = not q.active
                q.save(update_fields=["active"])
        elif action == "delete_question":
            Question.objects.filter(id=question_id, space=space).delete()
        return redirect(f"{request.path}?{request.GET.urlencode()}")

    cat_id = _post_int(request.GET, "category_id")
    sub_id = _post_int(request.GET, "subcategory_id")
    kind = request.GET.get("kind") or ""

    questions = Question.objects.filter(space=space).select_related("sub_category", "sub_category__category")
    if kind in ("quiz", "survey"):
        questions = questions.filter(kind=kind)
    if sub_id:
        questions = questions.filter(sub_category_id=sub_id)
    elif cat_id:
        questions = questions.filter(sub_category__category_id=cat_id)
    questions = questions.order_by("sub_category__category__order", "sub_category__order", "-id")

    categories = space.categories.prefetch_related("subcategories")
    return render(request, "game/dashboard_questions.html", {
        "space": space, "questions": questions, "categories": categories,
        "f_category": cat_id, "f_subcategory": sub_id, "f_kind": kind,
    })


def _member_fields(post, space):
    return {
        "full_name": post.get("full_name", "").strip()[:120],
        "phone": post.get("phone", "").strip()[:20],
        "external_ref": post.get("external_ref", "").strip()[:60],
        "category": space.categories.filter(id=_post_int(post, "category_id")).first(),
        "sub_category": SubCategory.objects.filter(id=_post_int(post, "subcategory_id"),
                                                    category__space=space).first(),
    }


def _current_license(space):
    return space.licenses.filter(active=True).first()


def _effective_reward(space, quiz=None):
    """Résout la récompense à afficher : quiz > espace > licence courante > aucune."""
    for obj in (quiz, space, _current_license(space)):
        if obj and obj.reward_text:
            return obj.reward_text, obj.reward_type
    return "", ""


def _jokers_ok(space, quiz):
    lic = _current_license(space)
    return bool(quiz and quiz.joker_enabled and lic and lic.jokers_allowed)


def _quiz_reward_joker_fields(post):
    reward_type = post.get("reward_type", "")
    if reward_type not in dict(REWARD_TYPES):
        reward_type = ""
    return {
        "reward_type": reward_type,
        "reward_text": post.get("reward_text", "").strip()[:200],
        "joker_enabled": post.get("joker_enabled") == "on",
    }


def _seat_check(space, license_obj):
    """None si un siège est disponible, sinon le message d'erreur à afficher."""
    if not license_obj or license_obj.billing_mode != "per_seat" or not license_obj.seat_count:
        return None
    used = Membership.objects.filter(space=space, license=license_obj).count()
    if used >= license_obj.seat_count:
        return (f"Limite de sièges atteinte pour la licence {license_obj.period_label} "
               f"({license_obj.seat_count} sièges) — contactez MQ Technologies pour l'étendre.")
    return None


def dashboard_members(request, slug):
    """Base des personnes identifiées par l'établissement : liste + import CSV + ajout.
    L'édition détaillée d'un membre se fait sur sa fiche (dashboard_member_detail)."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    current_license = _current_license(space)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "import_csv" and request.FILES.get("csv_file"):
            raw = request.FILES["csv_file"].read().decode("utf-8-sig", errors="ignore")
            created, matched, skipped = 0, 0, 0
            for row in csv.reader(raw.splitlines()):
                if not row or len(row) < 2:
                    continue
                full_name, phone = row[0].strip()[:120], row[1].strip()[:20]
                external_ref = row[2].strip()[:60] if len(row) > 2 else ""
                if not full_name or not phone or not phone[0].isdigit():
                    continue  # ignore l'en-tête éventuelle et les lignes vides
                existing = Membership.objects.filter(space=space, phone=phone, license=current_license).first()
                if not existing and _seat_check(space, current_license):
                    skipped += 1
                    continue
                member, is_new = Membership.objects.get_or_create(
                    space=space, phone=phone, license=current_license,
                    defaults={"full_name": full_name, "external_ref": external_ref})
                created += is_new
                existing_player = Player.objects.filter(phone=phone).first()
                if existing_player and not member.player_id:
                    member.player = existing_player
                    member.matched_at = timezone.now()
                    member.save(update_fields=["player", "matched_at"])
                    matched += 1
            msg = f"{created} membre(s) importé(s), {matched} déjà apparié(s)."
            if skipped:
                msg += f" {skipped} ignoré(s) faute de sièges disponibles."
            messages.success(request, msg)
        elif action == "add_member":
            f = _member_fields(request.POST, space)
            if not f["full_name"] or not f["phone"]:
                messages.error(request, "Nom et téléphone sont obligatoires.")
            else:
                seat_error = _seat_check(space, current_license)
                if seat_error:
                    messages.error(request, seat_error)
                else:
                    member, created = Membership.objects.get_or_create(
                        space=space, phone=f["phone"], license=current_license, defaults={
                            "full_name": f["full_name"], "external_ref": f["external_ref"],
                            "category": f["category"], "sub_category": f["sub_category"]})
                    if not created:
                        messages.error(request, f"Un membre existe déjà avec le téléphone {f['phone']}.")
                    else:
                        existing_player = Player.objects.filter(phone=f["phone"]).first()
                        if existing_player:
                            member.player = existing_player
                            member.matched_at = timezone.now()
                            member.save(update_fields=["player", "matched_at"])
        return redirect("dashboard_members", slug=slug)

    members = space.members.select_related("player", "category", "sub_category").order_by("-matched_at", "full_name")
    return render(request, "game/dashboard_members.html", {
        "space": space, "members": members, "current_license": current_license,
    })


def dashboard_member_detail(request, slug, member_id):
    """Fiche d'un membre : infos, édition, historique de quiz et réponses."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate
    member = get_object_or_404(Membership, id=member_id, space=space)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "edit_member":
            f = _member_fields(request.POST, space)
            if not f["full_name"] or not f["phone"]:
                messages.error(request, "Nom et téléphone sont obligatoires.")
            elif space.members.exclude(id=member.id).filter(phone=f["phone"]).exists():
                messages.error(request, f"Un autre membre utilise déjà le téléphone {f['phone']}.")
            else:
                member.full_name = f["full_name"]
                member.phone = f["phone"]
                member.external_ref = f["external_ref"]
                member.category = f["category"]
                member.sub_category = f["sub_category"]
                member.save()
        elif action == "delete_member":
            member.delete()
            return redirect("dashboard_members", slug=slug)
        return redirect("dashboard_member_detail", slug=slug, member_id=member.id)

    sessions_stats = []
    history = []
    if member.player_id:
        sessions = (GameSession.objects.filter(space=space, player_id=member.player_id, flagged=False)
                    .exclude(status="playing").select_related("quiz")
                    .prefetch_related("answers__question").order_by("-started_at"))
        for s in sessions:
            rank, total = None, None
            if s.quiz_id:
                ranked = _ranked(GameSession.objects.filter(
                    quiz_id=s.quiz_id, flagged=False).exclude(status="playing"))
                if s in ranked:
                    rank, total = ranked.index(s) + 1, len(ranked)
            sessions_stats.append({"session": s, "rank": rank, "total": total, "answers": s.answers.all()})

        history = (Membership.objects.filter(space=space, player_id=member.player_id)
                  .exclude(id=member.id).select_related("license", "category", "sub_category")
                  .order_by("license__start_date"))

    categories = space.categories.prefetch_related("subcategories")
    return render(request, "game/dashboard_member_detail.html", {
        "space": space, "member": member, "sessions_stats": sessions_stats,
        "categories": categories, "history": history,
    })


# ============================================================
# COMPTES UTILISATEURS (connexion OTP, historique, classements)
# ============================================================
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

OTP_VALIDITY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5


def _send_otp(phone):
    """Génère et « envoie » un code OTP. Stub dev : loggué console (point de
    branchement pour un vrai fournisseur SMS plus tard)."""
    code = f"{random.randint(0, 999999):06d}"
    OTPCode.objects.create(phone=phone, code=code)
    print(f"[OTP] {phone} -> {code}")
    return code


def account_login(request):
    space_slug = request.GET.get("space") or request.POST.get("space") or ""
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    space = Space.objects.filter(slug=space_slug, active=True).first() if space_slug else None
    dev_code = None
    error = None
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()[:20]
        if space and space.access_code and request.POST.get("access_code", "").strip() != space.access_code:
            error = "Code d'accès incorrect."
        elif phone:
            dev_code = _send_otp(phone)
            request.session["otp_phone"] = phone
            request.session["otp_space"] = space_slug
            request.session["otp_next"] = next_url
            url = reverse("account_verify")
            if settings.DEBUG:
                url += f"?dev_code={dev_code}"
            return redirect(url)
    return render(request, "game/account_login.html", {
        "space": space, "space_slug": space_slug, "next": next_url, "error": error,
    })


def account_verify(request):
    phone = request.session.get("otp_phone")
    space_slug = request.session.get("otp_space") or ""
    space = Space.objects.filter(slug=space_slug, active=True).first() if space_slug else None
    if not phone:
        return redirect("account_login")

    error = None
    if request.method == "POST":
        submitted = request.POST.get("code", "").strip()
        otp = OTPCode.objects.filter(phone=phone, consumed=False).order_by("-created_at").first()
        expired = not otp or otp.created_at < timezone.now() - timedelta(minutes=OTP_VALIDITY_MINUTES)
        if not otp or expired:
            error = "Code expiré — demande un nouveau code."
        elif otp.attempts >= OTP_MAX_ATTEMPTS:
            error = "Trop de tentatives — demande un nouveau code."
        elif submitted != otp.code:
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            error = "Code incorrect."
        else:
            otp.consumed = True
            otp.save(update_fields=["consumed"])
            player, created = Player.objects.get_or_create(phone=phone, defaults={"pseudo": ""})
            request.session["player_id"] = player.id
            request.session["verified_player_id"] = player.id
            Membership.objects.filter(phone=phone, player__isnull=True).update(
                player=player, matched_at=timezone.now())
            if not player.full_name:
                matched = Membership.objects.filter(player=player).exclude(
                    full_name="").order_by("-created_at").first()
                if matched:
                    player.full_name = matched.full_name
                    player.save(update_fields=["full_name"])
            request.session.pop("otp_phone", None)
            if created or not player.pseudo:
                return redirect("account_register")
            next_url = request.session.pop("otp_next", "") or ""
            request.session["otp_space"] = ""
            if next_url:
                return redirect(next_url)
            if space:
                return redirect("space_confirm", slug=space.slug)
            return redirect("account_home")

    dev_code = request.GET.get("dev_code") if settings.DEBUG else None
    return render(request, "game/account_verify.html", {
        "space": space, "phone": phone, "error": error, "dev_code": dev_code,
    })


def account_register(request):
    """Complète le profil lors de la 1ère vérification OTP — uniquement les infos
    manquantes : le nom complet est déjà connu s'il vient d'une fiche membre
    d'établissement appariée par téléphone (voir account_verify)."""
    player_id = request.session.get("verified_player_id")
    player = Player.objects.filter(id=player_id).first() if player_id else None
    if not player:
        return redirect("account_login")

    need_name = not player.full_name
    error = None
    if request.method == "POST":
        pseudo = request.POST.get("pseudo", "").strip()[:30]
        full_name = request.POST.get("full_name", "").strip()[:80] if need_name else player.full_name
        city = request.POST.get("city", "").strip()[:50]
        if not pseudo or (need_name and not full_name):
            error = "Le pseudo" + (" et le nom complet sont obligatoires." if need_name else " est obligatoire.")
        else:
            player.pseudo = pseudo
            player.full_name = full_name
            player.city = city
            player.save(update_fields=["pseudo", "full_name", "city"])
            space_slug = request.session.pop("otp_space", "") or ""
            next_url = request.session.pop("otp_next", "") or ""
            space = Space.objects.filter(slug=space_slug, active=True).first() if space_slug else None
            if next_url:
                return redirect(next_url)
            if space:
                return redirect("space_confirm", slug=space.slug)
            return redirect("account_home")

    return render(request, "game/account_register.html", {
        "player": player, "error": error, "need_name": need_name,
    })


def account_logout(request):
    for key in ("player_id", "verified_player_id", "otp_phone", "otp_space", "otp_next"):
        request.session.pop(key, None)
    return redirect("home")


def _session_pct(session):
    """Taux de bonne réponse (questions type quiz uniquement) pour une session."""
    qs = session.answers.filter(question__kind="quiz")
    n = qs.count()
    return round(100 * qs.filter(is_correct=True).count() / n) if n else None


def account_home(request):
    """« Mes quiz » : historique, scores, classements et détail des réponses du joueur connecté."""
    player_id = request.session.get("verified_player_id")
    player = Player.objects.filter(id=player_id).first() if player_id else None
    if not player:
        return redirect("account_login")

    public_sessions = list(GameSession.objects.filter(player=player, space__isnull=True)
                           .order_by("-day", "-started_at"))
    for s in public_sessions:
        s.pct = _session_pct(s)

    finished_answers = Answer.objects.filter(session__player=player, question__kind="quiz")
    overall_n = finished_answers.count()
    overall_pct = round(100 * finished_answers.filter(is_correct=True).count() / overall_n) if overall_n else None
    total_quizzes = GameSession.objects.filter(
        player=player, flagged=False).exclude(status="playing").count()

    # Espaces où le joueur a déjà joué OU est inscrit (membre) sans avoir encore joué
    played_space_ids = set(GameSession.objects.filter(player=player)
                           .exclude(space__isnull=True).values_list("space_id", flat=True))
    member_space_ids = set(Membership.objects.filter(player=player).values_list("space_id", flat=True))
    spaces = Space.objects.filter(id__in=played_space_ids | member_space_ids)

    space_blocks = []
    for sp in spaces:
        memberships = list(Membership.objects.filter(space=sp, player=player)
                           .select_related("license", "category", "sub_category")
                           .order_by("-created_at"))
        current_license = _current_license(sp)
        membership = next((m for m in memberships if m.license_id == current_license.id), None) \
            if current_license else None
        if not membership:
            membership = memberships[0] if memberships else None
        history = [m for m in memberships if membership is None or m.id != membership.id]

        quiz_rows = []
        played_quiz_ids = set()
        for qz in Quiz.objects.filter(sessions__player=player, space=sp).distinct():
            played_quiz_ids.add(qz.id)
            all_sessions = _ranked(GameSession.objects.filter(
                quiz=qz, flagged=False).exclude(status="playing"))
            mine = [s for s in all_sessions if s.player_id == player.id]
            if not mine:
                continue
            best = mine[0]
            reward_text, reward_type = _effective_reward(sp, qz)
            quiz_rows.append({
                "quiz": qz, "session": best,
                "rank": all_sessions.index(best) + 1, "total": len(all_sessions),
                "pct": _session_pct(best), "date": best.finished_at or best.started_at,
                "answers": best.answers.select_related("question").all(),
                "reward_text": reward_text, "reward_type": reward_type,
                "reward_eligible": bool(reward_text) and best.status == "finished",
            })
        quiz_rows.sort(key=lambda r: r["date"], reverse=True)

        space_answers = Answer.objects.filter(session__player=player, session__space=sp, question__kind="quiz")
        space_n = space_answers.count()
        space_pct = round(100 * space_answers.filter(is_correct=True).count() / space_n) if space_n else None

        # Points forts / points faibles par catégorie · sous-catégorie (matière) :
        # la moyenne globale de l'espace masque où sont réellement les lacunes.
        sub_totals = {}
        for a in space_answers.select_related("question__sub_category__category"):
            sub = a.question.sub_category
            if not sub:
                continue
            row = sub_totals.setdefault(sub.id, {"sub": sub, "n": 0, "correct": 0})
            row["n"] += 1
            row["correct"] += 1 if a.is_correct else 0
        sub_breakdown = sorted((
            {"sub_category": r["sub"], "n": r["n"], "pct": round(100 * r["correct"] / r["n"])}
            for r in sub_totals.values()
        ), key=lambda r: r["pct"])

        priority = None
        if len(sub_breakdown) > 1 and sub_breakdown[0]["pct"] < 70:
            weak_sub = sub_breakdown[0]["sub_category"]
            quiz = Quiz.objects.filter(space=sp, active=True, sub_category=weak_sub).exclude(
                id__in=played_quiz_ids).first() or Quiz.objects.filter(
                space=sp, active=True, sub_category=weak_sub).first()
            if quiz:
                priority = {"sub_category": weak_sub, "pct": sub_breakdown[0]["pct"], "quiz": quiz}

        # Quiz correspondant à l'établissement + catégorie/sous-catégorie de CHAQUE
        # adhésion du joueur (licence en cours ou passée) : un quiz d'une année
        # antérieure reste utile en révision, pas seulement l'année en cours.
        assigned_quizzes = []
        seen_quiz_ids = set()
        for m in memberships:
            if not (m.sub_category_id or m.category_id):
                continue
            qs = Quiz.objects.filter(space=sp, active=True)
            qs = qs.filter(sub_category=m.sub_category) if m.sub_category_id \
                else qs.filter(category=m.category, sub_category__isnull=True)
            for q in qs:
                if q.id in played_quiz_ids or q.id in seen_quiz_ids:
                    continue
                seen_quiz_ids.add(q.id)
                assigned_quizzes.append({
                    "quiz": q,
                    "current": bool(membership and m.id == membership.id),
                    "period_label": m.license.period_label if m.license_id else "",
                })

        flat_count = GameSession.objects.filter(
            space=sp, quiz__isnull=True, player=player, flagged=False).exclude(status="playing").count()
        space_blocks.append({"space": sp, "membership": membership, "history": history,
                            "assigned_quizzes": assigned_quizzes, "space_pct": space_pct,
                            "quiz_rows": quiz_rows, "flat_count": flat_count,
                            "has_quizzes": sp.quizzes.filter(active=True).exists(),
                            "sub_breakdown": sub_breakdown, "priority": priority})

    return render(request, "game/account_home.html", {
        "player": player, "public_sessions": public_sessions, "space_blocks": space_blocks,
        "tab": "account", "overall_pct": overall_pct, "total_quizzes": total_quizzes,
        "space_count": len(spaces),
    })


def space_confirm(request, slug):
    """Page de confirmation brandée juste après une connexion OTP initiée
    depuis le lien d'un établissement."""
    space = _space(slug)
    player_id = request.session.get("verified_player_id")
    player = Player.objects.filter(id=player_id).first() if player_id else None
    if not player:
        return redirect(f"{reverse('account_login')}?space={slug}")
    return render(request, "game/space_confirm.html", {"space": space, "player": player})
