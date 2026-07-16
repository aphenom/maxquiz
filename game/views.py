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
    pseudo = request.POST.get("pseudo", "").strip()[:30]
    mode = request.POST.get("mode", "daily")
    if mode not in ("daily", "training"):
        mode = "daily"

    player = _player(request)
    if not player:
        if not pseudo:
            return redirect("home")
        player = Player.objects.create(pseudo=pseudo)
        request.session["player_id"] = player.id
    elif pseudo and player.pseudo != pseudo:
        player.pseudo = pseudo
        player.save(update_fields=["pseudo"])

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
            "max": cfg.joker_max_per_game,
            "prices": cfg.joker_price_by_difficulty,
        },
        "balance": player.balance,
        "pot": cfg.daily_pot,
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
            # ÉLIMINATION — proposer un joker si possible
            price = int(cfg.joker_price_by_difficulty.get(str(question.difficulty), 500))
            can_joker = session.jokers_used < cfg.joker_max_per_game
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
                                player=player, status="playing", mode="daily")
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
            if not cfg.joker_ad_enabled:
                return JsonResponse({"error": "joker pub désactivé"}, status=400)
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


def leaderboard(request):
    today = timezone.localdate()
    rows = (GameSession.objects
            .filter(mode="daily", day=today, flagged=False)
            .exclude(status="playing")
            .select_related("player")
            .order_by("-status", "-reached", "total_time_ms")[:50])
    # tri : finished > eliminated, puis question atteinte, puis temps total
    rows = sorted(rows, key=lambda s: (s.status != "finished", -s.reached, s.total_time_ms))
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
from .models import Space


def _space(slug):
    return get_object_or_404(Space, slug=slug, active=True)


def space_home(request, slug):
    space = _space(slug)
    player = _player(request)
    today = timezone.localdate()
    already = bool(player and space.one_per_day and GameSession.objects.filter(
        player=player, space=space, day=today).exists())
    return render(request, "game/space_home.html", {
        "space": space, "player": player, "already": already,
    })


@require_POST
def space_start(request, slug):
    space = _space(slug)
    if space.access_code and request.POST.get("access_code", "").strip() != space.access_code:
        return render(request, "game/space_home.html", {
            "space": space, "player": _player(request),
            "error": "Code d'accès incorrect.", "already": False,
        })
    pseudo = request.POST.get("pseudo", "").strip()[:30]
    phone = request.POST.get("phone", "").strip()[:20]
    consent = request.POST.get("consent") == "on"

    player = _player(request)
    if not player:
        if not pseudo:
            return redirect("space_home", slug=slug)
        existing = Player.objects.filter(phone=phone).first() if phone else None
        player = existing or Player.objects.create(pseudo=pseudo, phone=phone or None)
        request.session["player_id"] = player.id
    if phone and not player.phone:
        player.phone = phone
        player.save(update_fields=["phone"])

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
                  "reward": space.reward_text},
        "questions": [
            {"id": q.id, "cat": q.get_category_display(), "difficulty": q.difficulty,
             "kind": q.kind, "text": q.text, "options": q.options(), "explanation": ""}
            for q in deck
        ],
        "ads": [], "video_ads": [],
    }
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

    eliminated = (question.kind == "quiz" and not is_correct
                  and session.space.elimination)
    if not eliminated:
        session.reached = idx + 1
    done = eliminated or session.reached >= len(session.question_ids)
    if done:
        session.status = "eliminated" if eliminated else "finished"
        session.finished_at = timezone.now()
    session.save()

    return JsonResponse({
        "correct": is_correct, "survey": question.kind == "survey",
        "correct_index": question.correct if question.kind == "quiz" else choice,
        "explanation": "", "reached": session.reached,
        "status": session.status if done else "playing", "done": done,
    })


def space_dashboard(request, slug):
    """Tableau de bord client, protégé par un code simple (MVP)."""
    space = _space(slug)
    code = request.GET.get("code") or request.session.get(f"dash_{space.id}")
    if code != space.dashboard_code:
        if request.method == "POST" and request.POST.get("code") == space.dashboard_code:
            request.session[f"dash_{space.id}"] = space.dashboard_code
            return redirect("space_dashboard", slug=slug)
        return render(request, "game/dashboard_login.html", {"space": space})
    request.session[f"dash_{space.id}"] = space.dashboard_code

    sessions = GameSession.objects.filter(space=space, flagged=False).exclude(status="playing")
    total = sessions.count()
    finished = sessions.filter(status="finished").count()
    consented = sessions.filter(consent=True).values("player").distinct().count()

    # Taux de réussite par question quiz → produits mal maîtrisés en premier
    quiz_stats = []
    for q in Question.objects.filter(space=space, kind="quiz", active=True):
        agg = Answer.objects.filter(question=q, session__in=sessions).aggregate(
            n=Count("id"), ok=Count("id", filter=Q(is_correct=True)))
        if agg["n"]:
            quiz_stats.append({"q": q, "n": agg["n"],
                               "pct": round(100 * agg["ok"] / agg["n"])})
    quiz_stats.sort(key=lambda x: x["pct"])

    # Répartition des réponses par sondage
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

    # Export CSV des contacts consentants
    if request.GET.get("export") == "contacts":
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="contacts-{space.slug}.csv"'
        w = csv.writer(resp)
        w.writerow(["pseudo", "telephone", "meilleur_score", "parties"])
        for p in Player.objects.filter(sessions__space=space, sessions__consent=True).distinct():
            ps = sessions.filter(player=p)
            best = max((s.reached for s in ps), default=0)
            w.writerow([p.pseudo, p.phone or "", best, ps.count()])
        return resp

    top = sorted(sessions.select_related("player"),
                 key=lambda s: (-s.reached, s.total_time_ms))[:10]
    return render(request, "game/dashboard.html", {
        "space": space, "total": total, "finished": finished,
        "completion": round(100 * finished / total) if total else 0,
        "consented": consented, "quiz_stats": quiz_stats,
        "survey_stats": survey_stats, "top": top,
    })
