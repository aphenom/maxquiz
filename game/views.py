import json
import random
import re

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (GameConfig, Player, Question, AdCampaign,
                     GameSession, Answer, JokerUse, Withdrawal)
from .subscriptions import access_status

TRAINING_COUNT = 6
MIN_HUMAN_MS = 800  # bonne réponse plus rapide = suspect


def _player(request):
    pid = request.session.get("player_id")
    return Player.objects.filter(id=pid).first() if pid else None


def _pick_by_difficulty(pool, n):
    """Tire n questions réparties sur TOUTES les difficultés présentes (tour à tour
    1, 2, 3, 4…), puis les range par difficulté croissante. Évite qu'un chapitre
    riche en questions faciles ne serve que des difficultés 1."""
    by_d = {}
    for q in pool:
        by_d.setdefault(q.difficulty, []).append(q)
    for lst in by_d.values():
        random.shuffle(lst)
    picked, levels = [], sorted(by_d)
    while len(picked) < n and any(by_d[d] for d in levels):
        for d in levels:
            if by_d[d] and len(picked) < n:
                picked.append(by_d[d].pop())
    picked.sort(key=lambda q: q.difficulty)
    return picked


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
    pools = {d: list(Question.objects.filter(active=True, difficulty=d, kind="quiz",
                                             space__isnull=True, quiz__isnull=True))
             for d in (1, 2, 3, 4)}
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


def _pending_quizzes(player):
    """Quiz assignés (catégorie/sous-catégorie de l'adhésion en cours) pas
    encore joués, tous établissements confondus — mis en avant sur l'accueil,
    avant le défi public, pour un membre connecté."""
    if not player:
        return []
    pending = []
    space_ids = Membership.objects.filter(player=player).values_list("space_id", flat=True)
    for sp in Space.objects.filter(id__in=set(space_ids), active=True):
        current_license = _current_license(sp)
        memberships = list(Membership.objects.filter(space=sp, player=player).order_by("-created_at"))
        membership = next((m for m in memberships if current_license and m.license_id == current_license.id), None) \
            or (memberships[0] if memberships else None)
        if not membership or not (membership.sub_category_id or membership.category_id):
            continue
        if _license_expired(membership.license):
            # Licence passée : plus rien à proposer pour cet établissement,
            # seuls les résultats déjà obtenus restent visibles sur /compte/.
            continue
        # Filtré par l'espace de la SESSION (pas Quiz.space) : un quiz partagé
        # (space=None) joué via cet espace doit quand même compter comme fait.
        played_ids = set(GameSession.objects.filter(player=player, space=sp, quiz__isnull=False)
                         .values_list("quiz_id", flat=True))
        days_left = _license_days_left(membership.license)
        qs = _quizzes_for_membership(sp, membership)
        for q in qs:
            if q.id not in played_ids:
                pending.append({"space": sp, "quiz": q, "days_left": days_left})
    # Les quiz dont la licence expire bientôt remontent en premier — un quiz
    # qui va disparaître de la liste mérite d'être vu avant celui qui a tout
    # son temps, plutôt que d'être signalé au même rang qu'eux.
    pending.sort(key=lambda p: p["days_left"] if p["days_left"] is not None else 9999)
    return pending


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
        "pending_quizzes": _pending_quizzes(player),
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
    if idx != session.reached:
        # Réponses strictement dans l'ordre : interdit de sauter à la dernière
        # question, et de continuer après une erreur éliminatoire sans joker.
        return JsonResponse({"error": "question hors séquence"}, status=400)
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


def _session_elimination(s):
    """Le mode élimination détermine ce qui distingue les joueurs : en mode
    survie, une seule erreur élimine, donc la question atteinte est le signal
    utile. Sans élimination (la plupart des quiz d'évaluation), tout le monde
    va jusqu'au bout du quiz quel que soit son score — la question atteinte
    ne distingue plus rien, il faut se baser sur le taux de bonne réponse."""
    if s.mode == "daily":
        return True
    if s.quiz_id:
        return s.quiz.elimination
    return bool(s.space_id and s.space.elimination)


def _ranked(sessions):
    """Trie des sessions par performance pour tous les classements du site :
    finaliste > éliminé, puis (en mode survie) question atteinte, sinon taux
    de bonne réponse, puis temps total en départage."""
    sessions = list(sessions)
    def key(s):
        if _session_elimination(s):
            return (s.status != "finished", -s.reached, s.total_time_ms)
        return (s.status != "finished", -(_session_pct(s) or 0), s.total_time_ms)
    return sorted(sessions, key=key)


def leaderboard(request):
    today = timezone.localdate()
    rows = (GameSession.objects
            .filter(mode="daily", day=today, flagged=False)
            .exclude(status="playing")
            .select_related("player")
            .order_by("-status", "-reached", "total_time_ms")[:50])
    rows = _ranked(rows)
    for s in rows:
        s.pct = _session_pct(s)
    finishers = sum(1 for s in rows if s.status == "finished")
    cfg = GameConfig.get()
    share = cfg.daily_pot // finishers if finishers else cfg.daily_pot

    player = _player(request)
    my_quiz_ranks = []
    if player:
        quiz_ids = (GameSession.objects.filter(player=player, quiz__isnull=False, flagged=False)
                   .exclude(status="playing").values_list("quiz_id", flat=True).distinct())
        for qz in Quiz.objects.filter(id__in=quiz_ids).select_related("space"):
            all_sessions = _ranked(GameSession.objects.filter(
                quiz=qz, flagged=False).exclude(status="playing"))
            mine = next((s for s in all_sessions if s.player_id == player.id), None)
            if not mine:
                continue
            reward_text, reward_type = _effective_reward(mine.space, qz)
            my_quiz_ranks.append({
                "quiz": qz, "space": mine.space,
                "rank": all_sessions.index(mine) + 1, "total": len(all_sessions),
                "pct": _session_pct(mine),
                "reward_text": reward_text, "reward_type": reward_type,
                "reward_eligible": bool(reward_text) and mine.status == "finished",
            })

    return render(request, "game/leaderboard.html", {
        "rows": rows, "player": player, "today": today,
        "cfg": cfg, "finishers": finishers, "share": share, "tab": "board",
        "my_quiz_ranks": my_quiz_ranks,
    })


def quiz_leaderboard(request, slug, quiz_slug):
    """Classement d'un quiz d'établissement précis, accessible au joueur."""
    space = _space(slug)
    quiz = _resolve_quiz(space, quiz_slug)
    if not quiz:
        raise Http404("Quiz introuvable pour cet espace.")
    player = _player(request)
    rows = _ranked(GameSession.objects.filter(quiz=quiz, space=space, flagged=False)
                   .exclude(status="playing").select_related("player"))[:50]
    for s in rows:
        s.pct = _session_pct(s)
    reward_text, reward_type = _effective_reward(space, quiz)
    return render(request, "game/quiz_leaderboard.html", {
        "space": space, "quiz": quiz, "rows": rows, "player": player,
        "reward_text": reward_text, "reward_type": reward_type, "tab": "board",
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
import io

import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils.text import slugify
from .models import Space, Category, SubCategory, Theme, Quiz, Membership, OTPCode, License, REWARD_TYPES, AuditLog


def _space(slug):
    return get_object_or_404(Space, slug=slug, active=True)


_LABEL_SYNONYMS = {
    "troisieme": "3eme", "quatrieme": "4eme", "cinquieme": "5eme", "sixieme": "6eme",
    "seconde": "2nde", "premiere": "1ere", "terminale": "tle", "term": "tle",
    "maths": "mathematiques", "math": "mathematiques",
    "pc": "physiquechimie", "spc": "physiquechimie", "sciencesphysiques": "physiquechimie",
    "svt": "sciencesdelavieetdelaterre", "hg": "histoiregeographie", "histgeo": "histoiregeographie",
}


def label_key(label):
    """Clé de rapprochement d'un libellé de niveau ou de matière entre le contenu
    MQ et une école : sans accents, casse, espaces ni ponctuation, avec synonymes
    courants (« 3e », « 3ème 2 », « Troisième » -> « 3eme » ; « Maths » ->
    « mathematiques »). Un numéro ou une lettre de classe est ignoré."""
    import unicodedata
    s = unicodedata.normalize("NFKD", str(label or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]", "", s)
    m = re.match(r"^([3-6])(e|eme|ieme)", s)            # 3e, 3eme, 3eme1, 3emea, 3ieme…
    if m:
        return f"{m.group(1)}eme"
    for word, key in _LABEL_SYNONYMS.items():
        if s == word or (word in ("troisieme", "quatrieme", "cinquieme", "sixieme") and s.startswith(word)):
            return key
    return s


def _global_quizzes_for(category, sub_category=None):
    """Quiz partagés (contenu MQ, sans espace) dont le niveau/matière correspond à
    cette catégorie/sous-catégorie d'un espace, rapprochés par label_key() et non
    par égalité stricte des libellés (« 3e » = « 3ème » = « Troisième »)."""
    lvl = label_key(category.name)
    sub = label_key(sub_category.name) if sub_category else ""
    ids = [q.id for q in Quiz.objects.filter(space__isnull=True, active=True)
           .only("id", "shared_level_name", "shared_subject_name")
           if label_key(q.shared_level_name) == lvl and label_key(q.shared_subject_name) == sub]
    return Quiz.objects.filter(id__in=ids)


def shared_match(space, quiz):
    """Sous-catégorie (ou catégorie si le quiz n'a pas de matière) de l'espace
    qui reçoit ce quiz partagé, ou None."""
    lvl, sub = label_key(quiz.shared_level_name), label_key(quiz.shared_subject_name)
    for cat in Category.objects.filter(space=space).prefetch_related("subcategories"):
        if label_key(cat.name) != lvl:
            continue
        if not sub:
            return cat
        for sc in cat.subcategories.all():
            if label_key(sc.name) == sub:
                return sc
    return None



def _answer_subject(question, space, cache=None):
    """Matière d'une question pour les « points faibles » : sa sous-catégorie, ou,
    pour une question de quiz partagé (contenu MQ, sans espace), la sous-catégorie
    de CET espace qui porte le niveau/matière du quiz partagé."""
    if question.sub_category_id:
        return question.sub_category
    qz = question.quiz
    if not qz or not qz.shared_subject_name:
        return None
    cache = {} if cache is None else cache
    if qz.id not in cache:                      # 1 recherche par quiz partagé, pas par réponse
        cache[qz.id] = shared_match(space, qz)
    return cache[qz.id]


def _answer_theme(question, space, cache=None):
    """Thématique (chapitre) : le Theme de la question, ou, pour un quiz partagé,
    le quiz lui-même (un quiz partagé = un chapitre, cf. import_questions --shared)."""
    from types import SimpleNamespace
    if question.theme_id:
        th = question.theme
        return SimpleNamespace(key=f"t{th.id}", name=th.name, sub_category=th.sub_category)
    qz = question.quiz
    sub = _answer_subject(question, space, cache) if qz else None
    if not qz or not sub:
        return None
    return SimpleNamespace(key=f"q{qz.id}", name=qz.name, sub_category=sub)


def _resolve_quiz(space, quiz_slug):
    """Retrouve un quiz par slug dans le contexte d'un espace : d'abord parmi
    les quiz propres à l'espace, sinon parmi les quiz partagés dont le
    niveau/matière correspond à l'une des catégories/sous-catégories de cet
    espace (voir _global_quizzes_for)."""
    quiz = Quiz.objects.filter(space=space, slug=quiz_slug, active=True).first()
    if quiz:
        return quiz
    quiz = Quiz.objects.filter(space__isnull=True, slug=quiz_slug, active=True).first()
    if not quiz:
        return None
    return quiz if shared_match(space, quiz) else None


def _quizzes_for_membership(space, membership):
    """Quiz (propres à l'espace + partagés correspondants) auxquels une
    adhésion donne accès : une matière précise si sub_category est renseignée,
    sinon TOUTES les matières du niveau — une adhésion à un niveau seul ne
    doit pas cloisonner l'élève aux seuls quiz sans matière du tout."""
    cat = membership.category
    if not cat:
        return []
    if membership.sub_category_id:
        sub = membership.sub_category
        return (list(Quiz.objects.filter(space=space, active=True, sub_category=sub))
                + list(_global_quizzes_for(cat, sub)))
    quizzes = (list(Quiz.objects.filter(space=space, active=True, category=cat))
              + list(_global_quizzes_for(cat)))
    for sub in cat.subcategories.all():
        quizzes += list(_global_quizzes_for(cat, sub))
    return quizzes


def _quiz_still_playable(player, space, quiz):
    """Une fois la licence d'une adhésion passée, seuls les résultats déjà
    obtenus restent consultables — le quiz ne doit plus pouvoir être
    (re)lancé sur la seule base de cette adhésion expirée. On bloque
    uniquement si TOUTES les adhésions du joueur qui donnaient accès à ce
    quiz sont désormais expirées ; un visiteur sans adhésion concernée par ce
    quiz n'est pas affecté (comportement actuel inchangé)."""
    memberships = list(Membership.objects.filter(space=space, player=player)
                       .select_related("license", "category", "sub_category"))
    matching = [m for m in memberships if quiz in _quizzes_for_membership(space, m)]
    if not matching:
        return True
    return any(not _license_expired(m.license) for m in matching)


def _match_membership(space, phone, player):
    """Associe automatiquement un joueur à une entrée de la base établissement
    (Membership) déjà présente pour ce téléphone mais pas encore appariée."""
    _match_by_phone(Membership.objects.filter(space=space), phone, player)


def _match_by_phone(memberships, phone, player):
    """Relie au joueur les fiches non appariées portant ce téléphone, sauf
    ambiguïté : une fiche avec code PIN se relie par la connexion matricule +
    PIN, et un téléphone partagé par plusieurs fiches d'un même espace (fratrie
    sur le numéro d'un parent) n'est jamais apparié automatiquement."""
    if not phone:
        return
    ids = [m.id for m in memberships.filter(phone=phone, player__isnull=True, pin_hash="")
           if Membership.objects.filter(space_id=m.space_id, license_id=m.license_id,
                                        phone=phone).count() == 1]
    if ids:
        Membership.objects.filter(id__in=ids).update(player=player, matched_at=timezone.now())


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
    """Vérifie que la session est authentifiée pour ce tableau de bord (voir
    dashboard_login_common, page de connexion commune à tous les
    établissements). Renvoie une redirection vers cette connexion si ce n'est
    pas le cas, sinon None."""
    if request.session.get(f"dash_{space.id}") == space.dashboard_code:
        return None
    login_url = f"{reverse('dashboard_login_common')}?next={request.path}"
    return redirect(login_url)


def dashboard_login_common(request):
    """Connexion unique à tous les tableaux de bord établissement : un
    identifiant et un mot de passe, créés par MQ Technologies et communiqués
    à l'établissement — modifiables ensuite par celui-ci depuis son tableau
    de bord (dashboard_change_password). L'identifiant est volontairement
    distinct du slug de l'espace (public, visible dans les liens `/e/slug/`)."""
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    error = None
    if request.method == "POST":
        identifiant = request.POST.get("identifiant", "").strip()
        password = request.POST.get("password", "")
        space = Space.objects.filter(dashboard_username=identifiant, active=True).first()
        teacher = None
        if not space:
            # Compte individuel d'un enseignant (direction ou professeur)
            from .models import Teacher
            teacher = Teacher.objects.filter(username__iexact=identifiant, active=True,
                                             space__active=True).select_related("space").first()
        if teacher:
            if not teacher.check_password(password):
                error = "Identifiant ou mot de passe incorrect."
            else:
                request.session["teacher_id"] = teacher.id
                if teacher.role == "direction":
                    request.session[f"dash_{teacher.space_id}"] = teacher.space.dashboard_code
                    return redirect(next_url or reverse("space_dashboard", args=[teacher.space.slug]))
                return redirect("school_resources", slug=teacher.space.slug)
        elif not space or password != space.dashboard_code:
            error = "Identifiant ou mot de passe incorrect."
        else:
            request.session[f"dash_{space.id}"] = space.dashboard_code
            if next_url:
                return redirect(next_url)
            return redirect("space_dashboard", slug=space.slug)
    return render(request, "game/dashboard_login.html", {
        "next": next_url, "error": error,
    })


def dashboard_change_password(request, slug):
    """Permet à l'établissement de changer lui-même le mot de passe de son
    tableau de bord (créé initialement par l'admin) — l'ancien mot de passe
    doit être confirmé avant d'en enregistrer un nouveau. L'admin reste par
    ailleurs libre de le réinitialiser à tout moment depuis l'admin Django."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate
    error = None
    saved = False
    if request.method == "POST":
        current = request.POST.get("current_password", "")
        pw1 = request.POST.get("password1", "")
        pw2 = request.POST.get("password2", "")
        if current != space.dashboard_code:
            error = "Mot de passe actuel incorrect."
        elif len(pw1) < 4:
            error = "Le nouveau mot de passe doit contenir au moins 4 caractères."
        elif pw1 != pw2:
            error = "Les deux mots de passe ne correspondent pas."
        else:
            space.dashboard_code = pw1
            space.save(update_fields=["dashboard_code"])
            request.session[f"dash_{space.id}"] = space.dashboard_code
            saved = True
    return render(request, "game/dashboard_change_password.html", {
        "space": space, "error": error, "saved": saved,
    })


def dashboard_logout(request, slug):
    """Déconnecte uniquement ce tableau de bord établissement — n'affecte pas
    une éventuelle session élève active en parallèle dans le même navigateur."""
    space = _space(slug)
    request.session.pop(f"dash_{space.id}", None)
    request.session.pop("teacher_id", None)
    return redirect("dashboard_login_common")


def _quiz_dashboard_stats(space, sessions):
    """Taux de bonne réponse par question (pires en premier) et répartition des
    sondages, calculés à partir des RÉPONSES des sessions — couvre donc aussi les
    quiz partagés (questions sans espace, rattachées à Question.quiz)."""
    quiz_agg = (Answer.objects.filter(session__in=sessions, question__kind="quiz", question__active=True)
               .values("question_id")
               .annotate(n=Count("id"), ok=Count("id", filter=Q(is_correct=True))))
    quiz_agg_by_q = {a["question_id"]: a for a in quiz_agg}
    questions = Question.objects.in_bulk(list(quiz_agg_by_q))
    quiz_stats = [{"q": questions[qid], "n": a["n"], "pct": round(100 * a["ok"] / a["n"])}
                  for qid, a in quiz_agg_by_q.items() if a["n"] and qid in questions]
    quiz_stats.sort(key=lambda x: x["pct"])

    survey_agg = (Answer.objects.filter(session__in=sessions, question__kind="survey",
                                        question__active=True, choice__gte=0)
                 .values("question_id", "choice").annotate(c=Count("id")))
    counts_by_q = {}
    for row in survey_agg:
        counts_by_q.setdefault(row["question_id"], {})[row["choice"]] = row["c"]
    survey_questions = Question.objects.in_bulk(list(counts_by_q))
    survey_stats = []
    for qid, qcounts in counts_by_q.items():
        q = survey_questions.get(qid)
        n = sum(qcounts.values())
        if q and n:
            dist = [{"opt": opt, "n": qcounts.get(i, 0), "pct": round(100 * qcounts.get(i, 0) / n)}
                    for i, opt in enumerate(q.options())]
            survey_stats.append({"q": q, "n": n, "dist": dist})
    return quiz_stats, survey_stats


def space_home(request, slug):
    space = _space(slug)
    player = _player(request)
    today = timezone.localdate()
    already = bool(player and space.one_per_day and GameSession.objects.filter(
        player=player, space=space, day=today).exists())

    # Catégorie/sous-catégorie du profil du joueur dans cet espace : seulement
    # l'adhésion EN COURS (licence active), pas l'historique — parcourir le
    # catalogue doit refléter le niveau actuel, pas mélanger d'anciennes années
    # (celles-ci restent visibles, étiquetées, dans « Quiz à faire » sur /compte/).
    current_license = _current_license(space)
    current_membership = None
    if player:
        memberships = list(Membership.objects.filter(space=space, player=player).order_by("-created_at"))
        current_membership = next((m for m in memberships if current_license and m.license_id == current_license.id), None) \
            or (memberships[0] if memberships else None)
    # Une adhésion à une matière précise (sub_category renseignée) cloisonne à
    # cette seule matière. Une adhésion à un niveau SANS matière précisée ne
    # cloisonne à rien : l'élève doit avoir accès à toutes les matières de ce
    # niveau, pas seulement aux quiz qui n'ont pas de matière du tout.
    my_full_categories = set()
    my_specific_pairs = set()
    if current_membership and current_membership.category_id:
        if current_membership.sub_category_id:
            my_specific_pairs.add((current_membership.category_id, current_membership.sub_category_id))
        else:
            my_full_categories.add(current_membership.category_id)
    my_category_ids = my_full_categories | {c for c, s in my_specific_pairs}
    # Sans profil déterminé (visiteur, ou membre sans catégorie renseignée), on
    # n'a rien à filtrer : le catalogue complet reste le seul repli possible.
    # Avec un profil, le filtre est strict — voir d'autres niveaux ne sert à
    # rien à l'élève, ce qui lui est utile (son parcours) est sur /compte/.
    no_profile = not my_category_ids

    # Arbre de découverte : quiz propres à l'espace + quiz partagés (créés
    # depuis l'admin, sans espace) dont le niveau/matière correspond par nom à
    # une catégorie/sous-catégorie de cet espace — automatiquement mêlés au
    # catalogue, sans configuration de la part de l'établissement.
    all_categories = list(space.categories.prefetch_related("subcategories"))
    categories, orphan_quizzes = [], []
    for cat in all_categories:
        subs = []
        for sub in cat.subcategories.all():
            if not no_profile and cat.id not in my_full_categories \
                    and (cat.id, sub.id) not in my_specific_pairs:
                continue
            qs = list(sub.quizzes.filter(active=True).select_related("theme")) \
                + list(_global_quizzes_for(cat, sub))
            if not qs:
                continue
            # À l'intérieur d'une matière, regrouper les quiz par thématique
            # (ex. « Conjugaison ») ; ceux sans thématique restent « généraux »
            # (un quiz partagé n'a jamais de thématique propre à un espace).
            themed, seen = [], set()
            for q in qs:
                if not q.theme_id or q.theme_id in seen:
                    continue
                seen.add(q.theme_id)
                themed.append({"theme": q.theme, "quizzes": [x for x in qs if x.theme_id == q.theme_id]})
            general = [q for q in qs if not q.theme_id]
            subs.append({"sub": sub, "themed": themed, "general": general, "count": len(qs)})
        direct = []
        if no_profile or cat.id in my_category_ids:
            direct = list(cat.quizzes.filter(active=True, sub_category__isnull=True)) \
                + list(_global_quizzes_for(cat))
        if subs or direct:
            categories.append({"category": cat, "subs": subs, "direct": direct})
    if no_profile:
        orphan_quizzes = list(space.quizzes.filter(active=True, category__isnull=True))
    has_catalog = bool(categories or orphan_quizzes)
    # Une seule matière au total (cas courant : profil cloisonné à une seule
    # sous-catégorie) : pas besoin d'accordion, ça n'ajoute qu'un clic pour
    # rien. Dès qu'il y en a plusieurs (profil niveau-seul avec accès à
    # toutes les matières, ou catalogue complet pour un visiteur), chaque
    # matière est repliée dans son propre accordion pour rester lisible.
    total_subs = sum(len(c["subs"]) for c in categories)

    played_quiz_ids = set()
    if player and has_catalog:
        # Filtré par l'espace de la SESSION (pas Quiz.space) : un quiz partagé
        # (space=None) joué via cet espace doit quand même être marqué « déjà joué ».
        played_quiz_ids = set(GameSession.objects.filter(player=player, space=space, quiz__isnull=False)
                              .values_list("quiz_id", flat=True))

    reward_text, reward_type = _effective_reward(space)
    # Un élève sans fiche établissement (personne n'a chargé son numéro) peut se
    # déclarer lui-même — seulement s'il y a un niveau à choisir, et seulement
    # tant que l'établissement n'a rien réglé pour lui (no_profile).
    can_declare_level = bool(player and no_profile and all_categories and not space.members_only)
    return render(request, "game/space_home.html", {
        "space": space, "player": player, "already": already,
        "categories": categories, "orphan_quizzes": orphan_quizzes,
        "reward_text": reward_text, "reward_type": reward_type,
        "profile_filtered": bool(my_category_ids),
        "has_catalog": has_catalog,
        "played_quiz_ids": played_quiz_ids,
        "multi_subject": total_subs > 1,
        "all_categories": all_categories,
        "can_declare_level": can_declare_level,
        "access": access_status(space, player) if player else None,
        "tab": "home",
    })


@require_POST
def space_declare_level(request, slug):
    """Auto-déclaration du niveau/matière par un élève sans fiche établissement
    (personne n'a chargé son numéro) : crée ou complète sa Membership pour la
    période en cours, sans jamais écraser une fiche déjà réglée par
    l'établissement. Celui-ci reste libre de la corriger ensuite depuis son
    tableau de bord — cette déclaration n'est qu'un point de départ."""
    space = _space(slug)
    player = _player(request)
    if not player or space.members_only:
        # Espace réservé : seule l'école crée les fiches (sinon n'importe qui
        # occuperait un siège facturé en se déclarant lui-même).
        return redirect("space_home", slug=slug)
    category = Category.objects.filter(space=space, id=_post_int(request.POST, "category")).first()
    if not category:
        return redirect("space_home", slug=slug)
    sub_category = category.subcategories.filter(id=_post_int(request.POST, "sub_category")).first()

    current_license = _current_license(space)
    existing = Membership.objects.filter(space=space, phone=player.phone, license=current_license).first()
    if existing:
        if not existing.category_id:
            existing.category = category
            existing.sub_category = sub_category
            existing.player = existing.player or player
            existing.matched_at = existing.matched_at or timezone.now()
            existing.save(update_fields=["category", "sub_category", "player", "matched_at"])
    elif not _seat_check(space, current_license):
        Membership.objects.create(
            space=space, phone=player.phone, license=current_license,
            full_name=player.full_name or player.pseudo, player=player,
            category=category, sub_category=sub_category, matched_at=timezone.now())
    return redirect("space_home", slug=slug)


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
    if not access_status(space, player)["ok"]:
        return redirect("space_subscribe", slug=slug)

    today = timezone.localdate()
    if space.one_per_day and GameSession.objects.filter(
            player=player, space=space, day=today).exists():
        return redirect("space_home", slug=slug)

    # Deck : quiz de l'espace (difficulté croissante) + sondages intercalés
    quiz_pool = list(Question.objects.filter(space=space, active=True, kind="quiz"))
    surveys = list(Question.objects.filter(space=space, active=True, kind="survey"))
    random.shuffle(surveys)
    quiz_pool = _pick_by_difficulty(quiz_pool, space.question_count)
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
        "playful": space.playful_fx,
        "home_url": reverse("space_home", args=[space.slug]),
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
    """Page d'accueil d'un quiz précis (lien direct partagé par l'entité, ou
    quiz partagé rattaché par niveau/matière — voir _resolve_quiz)."""
    space = _space(slug)
    quiz = _resolve_quiz(space, quiz_slug)
    if not quiz:
        raise Http404("Quiz introuvable pour cet espace.")
    player = _player(request)
    today = timezone.localdate()
    already = _quiz_locked(player, quiz, today)
    played_before = bool(player and GameSession.objects.filter(
        player=player, quiz=quiz, flagged=False).exclude(status="playing").exists())
    expired = bool(player) and not _quiz_still_playable(player, space, quiz)
    reward_text, reward_type = _effective_reward(space, quiz)
    return render(request, "game/quiz_home.html", {
        "space": space, "quiz": quiz, "player": player, "already": already,
        "played_before": played_before, "expired": expired,
        "reward_text": reward_text, "reward_type": reward_type,
        "access": access_status(space, player) if player else None,
        "tab": "home",
    })


@require_POST
def quiz_start(request, slug, quiz_slug):
    space = _space(slug)
    quiz = _resolve_quiz(space, quiz_slug)
    if not quiz:
        raise Http404("Quiz introuvable pour cet espace.")
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

    if not _quiz_still_playable(player, space, quiz):
        return render(request, "game/quiz_home.html", {
            "space": space, "quiz": quiz, "player": player, "expired": True,
            "error": "La période de licence liée à ce quiz est terminée — il n'est plus jouable, "
                    "mais tes résultats passés restent visibles sur ton compte.",
        })

    access = access_status(space, player)
    if not access["ok"]:
        return redirect("space_subscribe", slug=slug)

    today = timezone.localdate()
    if _quiz_locked(player, quiz, today):
        return redirect("quiz_home", slug=slug, quiz_slug=quiz_slug)

    if quiz.space_id is None:
        # Quiz partagé (sans espace) : banque de questions qui lui est
        # dédiée, indépendante des catégories/sous-catégories de l'espace.
        quiz_pool = list(Question.objects.filter(quiz=quiz, active=True, kind="quiz"))
    else:
        # Deck scopé à la thématique (si renseignée), sinon sous-catégorie ou
        # catégorie du quiz + sondages de l'espace. Repli automatique si pas
        # assez de questions taguées à la thématique : on complète avec le
        # reste de la matière plutôt que de bloquer le quiz (même philosophie
        # que _build_deck pour la difficulté).
        if quiz.sub_category_id:
            fallback_pool = Question.objects.filter(
                space=space, active=True, kind="quiz", sub_category=quiz.sub_category)
        elif quiz.category_id:
            fallback_pool = Question.objects.filter(
                space=space, active=True, kind="quiz", sub_category__category=quiz.category)
        else:
            fallback_pool = Question.objects.filter(space=space, active=True, kind="quiz")

        if quiz.theme_id:
            quiz_pool = list(Question.objects.filter(space=space, active=True, kind="quiz", theme=quiz.theme))
            if len(quiz_pool) < quiz.question_count:
                themed_ids = {q.id for q in quiz_pool}
                quiz_pool += [q for q in fallback_pool if q.id not in themed_ids]
        else:
            quiz_pool = list(fallback_pool)
    surveys = list(Question.objects.filter(space=space, active=True, kind="survey"))
    random.shuffle(surveys)
    quiz_pool = _pick_by_difficulty(quiz_pool, quiz.question_count)
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
        "playful": space.playful_fx,
        "home_url": reverse("space_home", args=[space.slug]),
        "board_url": reverse("quiz_leaderboard", args=[space.slug, quiz.slug]),
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
    if idx != session.reached:
        return JsonResponse({"error": "question hors séquence"}, status=400)
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


def _quiz_participation_counts(sessions):
    """Total et terminé par quiz en une seule requête groupée — évite une paire
    de requêtes par quiz (N+1) sur les pages qui en listent beaucoup."""
    rows = (sessions.exclude(quiz__isnull=True).values("quiz_id")
            .annotate(total=Count("id"), finished=Count("id", filter=Q(status="finished"))))
    return {r["quiz_id"]: r for r in rows}


def _quiz_row(counts, quiz):
    c = counts.get(quiz.id, {"total": 0, "finished": 0})
    t, f = c["total"], c["finished"]
    return {"quiz": quiz, "total": t, "finished": f,
            "completion": round(100 * f / t) if t else 0}


def _build_quiz_tree(space, sessions):
    """Arbre Catégorie > Sous-catégorie > Quiz avec compteurs de participation,
    pour la vue d'ensemble du tableau de bord — quiz propres à l'espace et
    quiz partagés (admin, sans espace) dont le niveau/matière correspond,
    inclus en lecture seule pour que l'établissement suive la participation
    de ses membres même à un contenu qu'il ne gère pas lui-même."""
    counts = _quiz_participation_counts(sessions)
    quizzes = list(space.quizzes.select_related("category", "sub_category", "theme").filter(active=True))
    tree = []
    for cat in space.categories.prefetch_related("subcategories"):
        cat_quizzes = [q for q in quizzes if q.category_id == cat.id]
        subs = []
        for sub in cat.subcategories.all():
            sub_quizzes = [q for q in cat_quizzes if q.sub_category_id == sub.id] \
                + list(_global_quizzes_for(cat, sub))
            if not sub_quizzes:
                continue
            sub_rows = [_quiz_row(counts, q) for q in sub_quizzes]
            subs.append({"sub": sub, "rows": sub_rows,
                        "total": sum(x["total"] for x in sub_rows)})
        direct_quizzes = [q for q in cat_quizzes if q.sub_category_id is None] + list(_global_quizzes_for(cat))
        direct_rows = [_quiz_row(counts, q) for q in direct_quizzes]
        if subs or direct_rows:
            tree.append({"category": cat, "subs": subs, "direct_rows": direct_rows,
                        "total": sum(r["total"] for s in subs for r in s["rows"])
                                + sum(r["total"] for r in direct_rows)})
    orphan_rows = [_quiz_row(counts, q) for q in quizzes if q.category_id is None]
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
    unique_participants = sessions.values("player").distinct().count()
    consented = sessions.filter(consent=True).values("player").distinct().count()

    tree, orphan_rows = _build_quiz_tree(space, sessions)
    # Un quiz partagé (admin, sans espace) compte aussi comme quiz pour cet
    # espace s'il correspond par nom à l'une de ses catégories/sous-catégories.
    has_quizzes = space.quizzes.exists() or bool(tree or orphan_rows)
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

    # « Meilleurs participants » n'a de sens comme classement par score que si
    # tout le monde affronte le même jeu (pool à plat, ex. Banque Horizon) —
    # comparer la question atteinte entre des quiz de longueurs différentes
    # (courant dès qu'il y a plusieurs quiz) n'aurait pas de sens. Dès qu'il y a
    # des quiz structurés, on bascule sur un classement par assiduité
    # (nombre de participations), comparable quel que soit le quiz joué ; le
    # score par quiz reste consultable sur la page de détail de chaque quiz.
    if has_quizzes:
        top_active = (Player.objects.filter(sessions__space=space, sessions__flagged=False)
                     .exclude(sessions__status="playing")
                     .annotate(n=Count("sessions", filter=Q(sessions__space=space, sessions__flagged=False)
                                       & ~Q(sessions__status="playing")))
                     .order_by("-n")[:10])
        consenting_ids = set(Player.objects.filter(sessions__space=space, sessions__consent=True)
                             .values_list("id", flat=True))
        top = [{"player": p, "n": p.n, "consent": p.id in consenting_ids} for p in top_active]
        top_mode = "active"
    else:
        top = _ranked(sessions.select_related("player"))[:10]
        for s in top:
            s.pct = _session_pct(s)
        top_mode = "score"

    avg_participation = round(total / unique_participants, 1) if unique_participants else 0
    return render(request, "game/dashboard.html", {
        "space": space, "total": total, "finished": finished,
        "completion": round(100 * finished / total) if total else 0,
        "unique_participants": unique_participants, "avg_participation": avg_participation,
        "consented": consented, "has_quizzes": has_quizzes,
        "tree": tree, "orphan_rows": orphan_rows,
        "quiz_stats": quiz_stats, "survey_stats": survey_stats,
        "top": top, "top_mode": top_mode,
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
                cat = Category.objects.create(space=space, name=name, slug=cat_slug,
                                              order=space.categories.count())
                _log_action(space, "create", cat)
        elif action == "rename_category":
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            name = request.POST.get("name", "").strip()[:80]
            if cat and name:
                old_name = cat.name
                cat.name = name
                cat.save(update_fields=["name"])
                _log_action(space, "update", cat, f"renommée depuis « {old_name} »")
        elif action == "delete_category":
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            if cat:
                _soft_delete_category(space, cat)
        elif action == "add_subcategory":
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            name = request.POST.get("name", "").strip()[:80]
            if cat and name:
                sub_slug = _unique_slug(cat.subcategories, name)
                sub = SubCategory.objects.create(category=cat, name=name, slug=sub_slug,
                                                 order=cat.subcategories.count())
                _log_action(space, "create", sub)
        elif action == "rename_subcategory":
            sub = SubCategory.objects.filter(id=_post_int(request.POST, "subcategory_id"),
                                             category__space=space).first()
            name = request.POST.get("name", "").strip()[:80]
            if sub and name:
                old_name = sub.name
                sub.name = name
                sub.save(update_fields=["name"])
                _log_action(space, "update", sub, f"renommée depuis « {old_name} »")
        elif action == "delete_subcategory":
            sub = SubCategory.objects.filter(id=_post_int(request.POST, "subcategory_id"),
                                             category__space=space).first()
            if sub:
                _soft_delete_subcategory(space, sub)
        elif action == "add_theme":
            sub = SubCategory.objects.filter(id=_post_int(request.POST, "subcategory_id"),
                                             category__space=space).first()
            name = request.POST.get("name", "").strip()[:80]
            if sub and name:
                theme_slug = _unique_slug(sub.themes, name)
                theme = Theme.objects.create(sub_category=sub, name=name, slug=theme_slug,
                                             order=sub.themes.count())
                _log_action(space, "create", theme)
        elif action == "rename_theme":
            theme = Theme.objects.filter(id=_post_int(request.POST, "theme_id"),
                                         sub_category__category__space=space).first()
            name = request.POST.get("name", "").strip()[:80]
            if theme and name:
                old_name = theme.name
                theme.name = name
                theme.save(update_fields=["name"])
                _log_action(space, "update", theme, f"renommée depuis « {old_name} »")
        elif action == "delete_theme":
            theme = Theme.objects.filter(id=_post_int(request.POST, "theme_id"),
                                         sub_category__category__space=space).first()
            if theme:
                _soft_delete_theme(space, theme)
        return redirect("dashboard_categories", slug=slug)

    q = request.GET.get("q", "").strip()
    categories_qs = space.categories.prefetch_related("subcategories__themes")
    if q:
        categories_qs = categories_qs.filter(name__icontains=q)
    paginator = Paginator(categories_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "game/dashboard_categories.html", {
        "space": space, "page_obj": page_obj, "total_matching": paginator.count, "q": q,
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
            theme = sub.themes.filter(id=_post_int(request.POST, "theme_id")).first() if sub else None
            if name:
                quiz_slug = _unique_slug(space.quizzes, name)
                replay_policy = request.POST.get("replay_policy")
                if replay_policy not in dict(Quiz.REPLAY_POLICIES):
                    replay_policy = "daily"
                quiz = Quiz.objects.create(
                    space=space, category=cat, sub_category=sub, theme=theme, slug=quiz_slug, name=name,
                    question_count=int(request.POST.get("question_count") or space.question_count),
                    survey_every=int(request.POST.get("survey_every") or space.survey_every),
                    elimination=request.POST.get("elimination") == "on",
                    replay_policy=replay_policy,
                    **_quiz_reward_joker_fields(request.POST))
                _log_action(space, "create", quiz)
        elif action == "toggle_quiz":
            qz = space.quizzes.filter(id=_post_int(request.POST, "quiz_id")).first()
            if qz:
                qz.active = not qz.active
                qz.save(update_fields=["active"])
                _log_action(space, "toggle", qz, "activé" if qz.active else "désactivé")
        elif action == "delete_quiz":
            qz = space.quizzes.filter(id=_post_int(request.POST, "quiz_id")).first()
            if qz:
                _soft_delete_quiz(space, qz)
        return redirect("dashboard_quizzes", slug=slug)

    q = request.GET.get("q", "").strip()
    quizzes_qs = space.quizzes.select_related("category", "sub_category", "theme").order_by("-id")
    if q:
        quizzes_qs = quizzes_qs.filter(name__icontains=q)
    paginator = Paginator(quizzes_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    base_sessions = GameSession.objects.filter(space=space, flagged=False).exclude(status="playing")
    counts = _quiz_participation_counts(base_sessions)
    for qz in page_obj:
        qz.total = counts.get(qz.id, {"total": 0})["total"]

    categories = space.categories.prefetch_related("subcategories__themes")
    current_license = _current_license(space)
    return render(request, "game/dashboard_quizzes.html", {
        "space": space, "page_obj": page_obj, "total_matching": paginator.count, "q": q,
        "categories": categories,
        "jokers_allowed": bool(current_license and current_license.jokers_allowed),
        "reward_types": REWARD_TYPES, "replay_policies": Quiz.REPLAY_POLICIES,
    })


def dashboard_quiz_detail(request, slug, quiz_slug):
    """Détail des stats (questions + sondages) d'un quiz précis."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    quiz = _resolve_quiz(space, quiz_slug)
    if not quiz:
        raise Http404("Quiz introuvable pour cet espace.")
    is_own_quiz = quiz.space_id == space.id

    if request.method == "POST" and not is_own_quiz:
        # Quiz partagé (admin, sans espace) : consultation uniquement, pas de
        # gestion depuis le tableau de bord établissement — ce n'est pas son quiz.
        return redirect("dashboard_quiz_detail", slug=slug, quiz_slug=quiz.slug)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "edit_quiz":
            name = request.POST.get("name", "").strip()[:100]
            cat = space.categories.filter(id=_post_int(request.POST, "category_id")).first()
            sub = cat.subcategories.filter(id=_post_int(request.POST, "subcategory_id")).first() if cat else None
            theme = sub.themes.filter(id=_post_int(request.POST, "theme_id")).first() if sub else None
            if name:
                quiz.name = name
                quiz.category = cat
                quiz.sub_category = sub
                quiz.theme = theme
                quiz.question_count = int(request.POST.get("question_count") or space.question_count)
                quiz.survey_every = int(request.POST.get("survey_every") or space.survey_every)
                quiz.elimination = request.POST.get("elimination") == "on"
                replay_policy = request.POST.get("replay_policy")
                if replay_policy in dict(Quiz.REPLAY_POLICIES):
                    quiz.replay_policy = replay_policy
                quiz.show_corrections = request.POST.get("show_corrections") == "on"
                for field, value in _quiz_reward_joker_fields(request.POST).items():
                    setattr(quiz, field, value)
                quiz.save()
                _log_action(space, "update", quiz)
        elif action == "toggle_quiz":
            quiz.active = not quiz.active
            quiz.save(update_fields=["active"])
            _log_action(space, "toggle", quiz, "activé" if quiz.active else "désactivé")
        elif action == "delete_quiz":
            _soft_delete_quiz(space, quiz)
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
    for s in top:
        s.pct = _session_pct(s)
    categories = space.categories.prefetch_related("subcategories__themes")
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
        "is_own_quiz": is_own_quiz,
    })


def _question_fields_from_post(space, post):
    kind = post.get("kind") if post.get("kind") in ("quiz", "survey") else "quiz"
    sub = SubCategory.objects.filter(id=_post_int(post, "sub_category_id"), category__space=space).first()
    theme = sub.themes.filter(id=_post_int(post, "theme_id")).first() if sub else None
    return dict(
        kind=kind,
        sub_category=sub,
        theme=theme,
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
                    q = Question.objects.create(space=space, category="cg", **fields)
                    _log_action(space, "create", q)
                else:
                    q = Question.objects.filter(id=question_id, space=space).first()
                    if q:
                        Question.objects.filter(id=question_id, space=space).update(**fields)
                        _log_action(space, "update", q)
        elif action == "toggle_question":
            q = Question.objects.filter(id=question_id, space=space).first()
            if q:
                q.active = not q.active
                q.save(update_fields=["active"])
                _log_action(space, "toggle", q, "activée" if q.active else "désactivée")
        elif action == "delete_question":
            q = Question.objects.filter(id=question_id, space=space).first()
            if q:
                _soft_delete_one(space, q)
        elif action in ("bulk_activate", "bulk_deactivate", "bulk_delete"):
            selected = request.POST.getlist("selected_ids")
            selected_qs = list(Question.objects.filter(space=space, id__in=selected))
            if action == "bulk_activate":
                for q in selected_qs:
                    q.active = True
                    q.save(update_fields=["active"])
                    _log_action(space, "toggle", q, "activée (lot)")
            elif action == "bulk_deactivate":
                for q in selected_qs:
                    q.active = False
                    q.save(update_fields=["active"])
                    _log_action(space, "toggle", q, "désactivée (lot)")
            else:
                for q in selected_qs:
                    _soft_delete_one(space, q, action="bulk_delete")
        return redirect(f"{request.path}?{request.GET.urlencode()}")

    cat_id = _post_int(request.GET, "category_id")
    sub_id = _post_int(request.GET, "subcategory_id")
    theme_id = _post_int(request.GET, "theme_id")
    kind = request.GET.get("kind") or ""
    q = request.GET.get("q", "").strip()

    questions = Question.objects.filter(space=space).select_related(
        "sub_category", "sub_category__category", "theme")
    if kind in ("quiz", "survey"):
        questions = questions.filter(kind=kind)
    if theme_id:
        questions = questions.filter(theme_id=theme_id)
    elif sub_id:
        questions = questions.filter(sub_category_id=sub_id)
    elif cat_id:
        questions = questions.filter(sub_category__category_id=cat_id)
    if q:
        questions = questions.filter(text__icontains=q)
    questions = questions.order_by("sub_category__category__order", "sub_category__order", "-id")

    # Chaque question s'affiche en carte-formulaire complète (4 options,
    # difficulté...) : nettement plus lourd qu'une carte membre, d'où une
    # pagination plus serrée dès qu'il y a une grosse banque de questions.
    paginator = Paginator(questions, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = space.categories.prefetch_related("subcategories__themes")
    return render(request, "game/dashboard_questions.html", {
        "space": space, "page_obj": page_obj, "total_matching": paginator.count,
        "categories": categories, "q": q,
        "f_category": cat_id, "f_subcategory": sub_id, "f_theme": theme_id, "f_kind": kind,
    })


def _rows_from_upload(f):
    """Normalise un fichier d'import (.xlsx généré par dashboard_members_template,
    ou .csv classique) en lignes de valeurs texte — pour que le reste de l'import
    n'ait pas à se soucier du format d'origine."""
    if (f.name or "").lower().endswith(".xlsx"):
        wb = openpyxl.load_workbook(f, data_only=True)
        ws = wb["Import"] if "Import" in wb.sheetnames else wb.worksheets[0]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row and any(v is not None for v in row):
                yield ["" if v is None else str(v).strip() for v in row]
    else:
        data = f.read()
        try:
            raw = data.decode("utf-8-sig")
        except UnicodeDecodeError:              # « CSV (point-virgule) » d'Excel FR = Windows-1252
            raw = data.decode("cp1252", errors="replace")
        delim = ";" if raw.split("\n", 1)[0].count(";") > raw.split("\n", 1)[0].count(",") else ","
        for row in csv.reader(raw.splitlines(), delimiter=delim):
            yield row


def _resolve_category_by_name(space, cat_name, sub_name):
    """Résout catégorie/sous-catégorie par nom (import CSV/Excel) plutôt que par
    id (formulaire) — comparaison insensible à la casse et aux espaces, pour
    tolérer les petites variations de saisie dans un fichier rempli à la main."""
    cat_name = (cat_name or "").strip()
    sub_name = (sub_name or "").strip()
    category = space.categories.filter(name__iexact=cat_name).first() if cat_name else None
    sub_category = None
    if category and sub_name:
        sub_category = category.subcategories.filter(name__iexact=sub_name).first()
    return category, sub_category


def _member_fields(post, space):
    return {
        "full_name": post.get("full_name", "").strip()[:120],
        "phone": normalize_phone(post.get("phone", "")) or "",
        "external_ref": post.get("external_ref", "").strip()[:60],
        "parent_phone": normalize_phone(post.get("parent_phone", "")) or "",
        "category": space.categories.filter(id=_post_int(post, "category_id")).first(),
        "sub_category": SubCategory.objects.filter(id=_post_int(post, "subcategory_id"),
                                                    category__space=space).first(),
    }


def _current_license(space):
    return space.licenses.filter(active=True).first()


def _license_expired(license_obj):
    """Une licence est « passée » si elle a été désactivée ou si sa date de
    fin est dépassée. Pas de licence du tout = pas de notion d'expiration
    (comportement inchangé pour les espaces qui n'utilisent pas ce système)."""
    if not license_obj:
        return False
    if not license_obj.active:
        return True
    return license_obj.end_date < timezone.localdate()


def _license_days_left(license_obj):
    """Jours restants avant la fin d'une licence active (None si pas de
    licence, licence désactivée, ou déjà expirée — ces cas n'ont pas de
    compte à rebours à afficher, le quiz est simplement retiré de la liste)."""
    if not license_obj or not license_obj.active:
        return None
    days = (license_obj.end_date - timezone.localdate()).days
    return days if days >= 0 else None


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


# ============================================================
# JOURNAL D'ACTIVITÉ ET SUPPRESSION DOUCE
# ============================================================
# Rien n'est jamais réellement effacé par une action du tableau de bord
# établissement : chaque modèle géré ici (Category, SubCategory, Theme, Quiz,
# Question, Membership) utilise SoftDeleteManager (voir models.py) — une
# « suppression » ne fait que renseigner deleted_at, la ligne reste en base et
# reste restaurable. Chaque action est en plus journalisée (AuditLog) pour
# pouvoir toujours remonter à ce qui a été fait, quand, par quel tableau de
# bord — ni panne (pas de cascade réelle qui casserait des données liées), ni
# perte d'information.
RESTORABLE_MODELS = {"Category": Category, "SubCategory": SubCategory, "Theme": Theme,
                     "Quiz": Quiz, "Question": Question, "Membership": Membership}


def _log_action(space, action, obj, details=""):
    AuditLog.objects.create(
        space=space, actor=space.dashboard_username, action=action,
        model_name=obj.__class__.__name__, object_id=obj.id,
        object_repr=str(obj)[:200], details=details[:300])


def _soft_delete_one(space, obj, action="delete", details=""):
    """Marque un objet supprimé (sans l'effacer) et journalise l'action."""
    _log_action(space, action, obj, details)
    obj.deleted_at = timezone.now()
    obj.save(update_fields=["deleted_at"])


def _soft_delete_theme(space, theme, action="delete"):
    _soft_delete_one(space, theme, action)


def _soft_delete_subcategory(space, sub, action="delete"):
    for theme in sub.themes.all():
        _soft_delete_theme(space, theme, action)
    _soft_delete_one(space, sub, action)


def _soft_delete_category(space, category, action="delete"):
    for sub in category.subcategories.all():
        _soft_delete_subcategory(space, sub, action)
    _soft_delete_one(space, category, action)


def _soft_delete_quiz(space, quiz, action="delete"):
    # Un quiz partagé (space=None) a sa propre banque de questions dédiée
    # (Question.quiz) — la CASCADE réelle les aurait effacées avec le quiz ;
    # en douceur, on les marque supprimées avec lui pour rester cohérent.
    for q in quiz.own_questions.all():
        _soft_delete_one(space, q, action)
    _soft_delete_one(space, quiz, action)


def dashboard_restore(request, slug):
    """Annule une suppression (douce) : remet deleted_at à vide sur l'objet visé,
    retrouvé par type + id depuis une entrée du journal d'activité. Toujours
    possible puisque la suppression n'a jamais réellement effacé la ligne."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate
    if request.method == "POST":
        model_name = request.POST.get("model_name", "")
        object_id = _post_int(request.POST, "object_id")
        model = RESTORABLE_MODELS.get(model_name)
        if model:
            obj = model.all_objects.filter(id=object_id).first()
            # Vérification d'appartenance à cet espace avant de restaurer,
            # propre à chaque modèle (Membership/Category/Quiz ont un champ
            # space direct, SubCategory/Theme remontent par leur parent).
            belongs = False
            if obj is not None:
                if hasattr(obj, "space_id"):
                    belongs = obj.space_id == space.id
                elif model is SubCategory:
                    belongs = obj.category.space_id == space.id
                elif model is Theme:
                    belongs = obj.sub_category.category.space_id == space.id
            if obj is not None and belongs:
                obj.deleted_at = None
                obj.save(update_fields=["deleted_at"])
                _log_action(space, "restore", obj)
    return redirect(f"{reverse('dashboard_audit_log', args=[slug])}?{request.GET.urlencode()}")


def dashboard_audit_log(request, slug):
    """Journal d'activité de l'espace : toutes les actions du tableau de bord,
    les plus récentes d'abord, avec restauration en un clic pour les
    suppressions (l'objet reste en base — voir SoftDeleteManager)."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    logs = AuditLog.objects.filter(space=space).order_by("-created_at")
    action_filter = request.GET.get("action") or ""
    if action_filter:
        logs = logs.filter(action=action_filter)
    paginator = Paginator(logs, 40)
    page_obj = paginator.get_page(request.GET.get("page"))

    # Pour chaque entrée de suppression affichée, sait-on si l'objet est
    # toujours supprimé (bouton « Restaurer » utile) ou déjà restauré depuis
    # (bouton inutile, l'objet est de nouveau actif) ?
    for log in page_obj:
        log.can_restore = False
        if log.action in ("delete", "bulk_delete") and log.object_id:
            model = RESTORABLE_MODELS.get(log.model_name)
            if model:
                obj = model.all_objects.filter(id=log.object_id).first()
                log.can_restore = bool(obj and obj.deleted_at is not None)

    return render(request, "game/dashboard_audit_log.html", {
        "space": space, "page_obj": page_obj, "total_matching": paginator.count,
        "action_filter": action_filter, "actions": AuditLog.ACTIONS,
    })


def dashboard_members_template(request, slug):
    """Modèle de fichier d'import (Excel), personnalisé à l'établissement :
    colonnes aux libellés propres à l'espace, listes déroulantes de vérification
    pour la catégorie/sous-catégorie (évite les fautes de frappe qui
    empêcheraient l'appariement au bon niveau/matière à l'import), et une feuille
    de référence listant les catégories/sous-catégories valides."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate is not None:
        return gate

    categories = list(space.categories.prefetch_related("subcategories").order_by("order", "name"))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Import"
    headers = ["Nom complet*", "Téléphone (élève)", "Matricule",
              space.category_label or "Catégorie", space.subcategory_label or "Sous-catégorie",
              "Téléphone du parent"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for i, width in enumerate([26, 18, 20, 22, 22, 20], start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.freeze_panes = "A2"
    for r in range(2, 501):                    # colonnes téléphone au format Texte : garde le 0 initial
        ws.cell(row=r, column=2).number_format = "@"
        ws.cell(row=r, column=6).number_format = "@"

    ref_name = "Catégories disponibles"
    ref = wb.create_sheet(ref_name)
    ref.append([space.category_label or "Catégorie", space.subcategory_label or "Sous-catégorie"])
    for cell in ref[1]:
        cell.font = Font(bold=True)
    row_i = 2
    for cat in categories:
        subs = list(cat.subcategories.all())
        if subs:
            for sub in subs:
                ref.cell(row=row_i, column=1, value=cat.name)
                ref.cell(row=row_i, column=2, value=sub.name)
                row_i += 1
        else:
            ref.cell(row=row_i, column=1, value=cat.name)
            row_i += 1
    ref.column_dimensions["A"].width = 22
    ref.column_dimensions["B"].width = 22
    last_row = max(row_i - 1, 2)

    if categories:
        cat_dv = DataValidation(type="list", formula1=f"'{ref_name}'!$A$2:$A${last_row}",
                                allow_blank=True, showDropDown=False)
        cat_dv.error = "Choisis une valeur dans la liste (feuille « Catégories disponibles »)."
        cat_dv.errorTitle = "Valeur invalide"
        ws.add_data_validation(cat_dv)
        cat_dv.add("D2:D500")

        sub_dv = DataValidation(type="list", formula1=f"'{ref_name}'!$B$2:$B${last_row}",
                                allow_blank=True, showDropDown=False)
        sub_dv.error = "Choisis une valeur dans la liste (feuille « Catégories disponibles »)."
        sub_dv.errorTitle = "Valeur invalide"
        ws.add_data_validation(sub_dv)
        sub_dv.add("E2:E500")

    buf = io.BytesIO()
    wb.save(buf)
    resp = HttpResponse(buf.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="modele-import-{space.slug}.xlsx"'
    return resp


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
            created, matched, skipped = 0, 0, 0
            rejected = []  # lignes refusées, affichées à l'école au lieu de disparaître
            duplicates, seen_in_file, already = [], {}, 0
            for line_no, row in enumerate(_rows_from_upload(request.FILES["csv_file"]), start=1):
                if not row or len(row) < 2:
                    continue
                full_name = (row[0] or "").strip()[:120]
                if not full_name or (line_no == 1 and full_name.lower().startswith("nom")):
                    continue  # en-tête et lignes vides
                raw_phone = (row[1] or "").strip()
                phone = normalize_phone(raw_phone) or ""
                external_ref = (row[2] or "").strip()[:60] if len(row) > 2 else ""
                if external_ref.endswith(".0") and external_ref[:-2].isdigit():
                    external_ref = external_ref[:-2]          # matricule numérique lu par Excel
                cat_name = row[3] if len(row) > 3 else ""
                sub_name = row[4] if len(row) > 4 else ""
                parent_phone = normalize_phone(row[5]) or "" if len(row) > 5 else ""
                if raw_phone and not phone:
                    rejected.append(f"{full_name} ({raw_phone})")
                    continue
                if not phone and not external_ref:
                    rejected.append(f"{full_name} (ni téléphone ni matricule)")
                    continue
                key = ("ref", external_ref) if external_ref else ("tel", phone)
                if key in seen_in_file:
                    what = "même matricule" if external_ref else "même téléphone"
                    duplicates.append(f"{full_name} ({what} que {seen_in_file[key]})")
                    continue
                seen_in_file[key] = full_name
                category, sub_category = _resolve_category_by_name(space, cat_name, sub_name)
                lookup = ({"external_ref": external_ref} if external_ref
                          else {"phone": phone, "external_ref": ""})
                existing = Membership.objects.filter(space=space, license=current_license, **lookup).first()
                if existing:
                    already += 1
                    if parent_phone and not existing.parent_phone:
                        existing.parent_phone = parent_phone
                        existing.save(update_fields=["parent_phone"])
                    continue
                if _seat_check(space, current_license):
                    skipped += 1
                    continue
                member = Membership.objects.create(
                    space=space, license=current_license, full_name=full_name, phone=phone,
                    external_ref=external_ref, parent_phone=parent_phone,
                    category=category, sub_category=sub_category)
                created += 1
                _log_action(space, "create", member, "import")
                # Appariement automatique par téléphone, sauf si ce téléphone est
                # partagé par plusieurs élèves (fratrie) : chacun se connecte
                # alors avec son matricule et son code PIN.
                existing_player = Player.objects.filter(phone=phone).first() if phone else None
                if existing_player and not Membership.objects.filter(
                        space=space, license=current_license, phone=phone).exclude(id=member.id).exists():
                    member.player = existing_player
                    member.matched_at = timezone.now()
                    member.save(update_fields=["player", "matched_at"])
                    matched += 1
            msg = f"{created} membre(s) importé(s), {matched} déjà apparié(s)."
            if already:
                msg += f" {already} déjà inscrit(s), inchangé(s)."
            if skipped:
                msg += f" {skipped} ignoré(s) faute de sièges disponibles."
            messages.success(request, msg)
            if duplicates:
                messages.error(request, f"{len(duplicates)} ligne(s) en double dans le fichier, non créée(s) : "
                               + ", ".join(duplicates[:20]) + ("…" if len(duplicates) > 20 else "")
                               + ". Renseigne un matricule par élève : des frères et sœurs peuvent alors "
                                 "partager le même téléphone.")
            if rejected:
                messages.error(request, f"{len(rejected)} ligne(s) refusée(s) : "
                               + ", ".join(rejected[:20]) + ("…" if len(rejected) > 20 else ""))
        elif action == "add_member":
            f = _member_fields(request.POST, space)
            if not f["full_name"] or not (f["phone"] or f["external_ref"]):
                messages.error(request, "Le nom et un téléphone ou un matricule sont obligatoires.")
            else:
                seat_error = _seat_check(space, current_license)
                if seat_error:
                    messages.error(request, seat_error)
                else:
                    lookup = ({"external_ref": f["external_ref"]} if f["external_ref"]
                              else {"phone": f["phone"], "external_ref": ""})
                    member, created = Membership.objects.get_or_create(
                        space=space, license=current_license, **lookup, defaults={
                            "full_name": f["full_name"], "phone": f["phone"],
                            "parent_phone": f["parent_phone"],
                            "category": f["category"], "sub_category": f["sub_category"]})
                    if not created:
                        messages.error(request, "Un membre existe déjà avec ce "
                                       + ("matricule." if f["external_ref"] else "téléphone."))
                    else:
                        _log_action(space, "create", member)
                        existing_player = (Player.objects.filter(phone=f["phone"]).first()
                                           if f["phone"] and not space.members.filter(
                                               license=current_license, phone=f["phone"]).exclude(
                                               id=member.id).exists() else None)
                        if existing_player:
                            member.player = existing_player
                            member.matched_at = timezone.now()
                            member.save(update_fields=["player", "matched_at"])
        elif action == "bulk_delete":
            selected = request.POST.getlist("selected_ids")
            for m in space.members.filter(id__in=selected):
                _soft_delete_one(space, m, action="bulk_delete")
            return redirect(f"{request.path}?{request.GET.urlencode()}")
        return redirect("dashboard_members", slug=slug)

    q = request.GET.get("q", "").strip()
    # Le compteur de sièges ne porte que sur la licence en cours : par défaut la
    # liste s'y limite aussi (pour rester la réponse directe à « qui compte dans
    # ces sièges »), avec un sélecteur pour voir une autre période ou tout le
    # monde — plutôt qu'une liste à plat mélangeant toutes les années, illisible
    # dès qu'il y a beaucoup de membres.
    license_filter = request.GET.get("periode") or ("current" if current_license else "all")

    members = space.members.select_related("player", "category", "sub_category", "license")
    if license_filter == "current" and current_license:
        members = members.filter(license=current_license)
    elif license_filter == "none":
        members = members.filter(license__isnull=True)
    elif license_filter not in ("current", "all"):
        members = members.filter(license_id=license_filter)
    # "all" (ou licence courante absente) : pas de filtre par période.
    members = members.order_by("-matched_at", "full_name")

    if q:
        members = members.filter(Q(full_name__icontains=q) | Q(phone__icontains=q)
                                 | Q(external_ref__icontains=q))

    paginator = Paginator(members, 30)
    page_obj = paginator.get_page(request.GET.get("page"))

    other_licenses = space.licenses.exclude(id=current_license.id if current_license else None).order_by(
        "-start_date")
    has_unlicensed = space.members.filter(license__isnull=True).exists()

    return render(request, "game/dashboard_members.html", {
        "space": space, "current_license": current_license, "page_obj": page_obj,
        "total_matching": paginator.count, "q": q, "license_filter": license_filter,
        "other_licenses": other_licenses, "has_unlicensed": has_unlicensed,
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
            others = space.members.exclude(id=member.id).filter(license=member.license)
            if not f["full_name"] or not (f["phone"] or f["external_ref"]):
                messages.error(request, "Le nom et un téléphone ou un matricule sont obligatoires.")
            elif f["external_ref"] and others.filter(external_ref=f["external_ref"]).exists():
                messages.error(request, f"Un autre membre a déjà le matricule {f['external_ref']}.")
            elif not f["external_ref"] and others.filter(phone=f["phone"], external_ref="").exists():
                messages.error(request, f"Un autre membre utilise déjà le téléphone {f['phone']}.")
            else:
                member.full_name = f["full_name"]
                member.phone = f["phone"]
                member.external_ref = f["external_ref"]
                member.parent_phone = f["parent_phone"]
                member.category = f["category"]
                member.sub_category = f["sub_category"]
                member.save()
                _log_action(space, "update", member)
        elif action == "delete_member":
            _soft_delete_one(space, member)
            return redirect("dashboard_members", slug=slug)
        return redirect("dashboard_member_detail", slug=slug, member_id=member.id)

    sessions_stats = []
    history = []
    overall_pct = None
    sub_breakdown, theme_breakdown, assigned_quizzes = [], [], []
    if member.player_id:
        sessions = (GameSession.objects.filter(space=space, player_id=member.player_id, flagged=False)
                    .exclude(status="playing").select_related("quiz")
                    .prefetch_related("answers__question").order_by("-started_at"))
        played_quiz_ids = set()
        for s in sessions:
            rank, total = None, None
            if s.quiz_id:
                played_quiz_ids.add(s.quiz_id)
                ranked = _ranked(GameSession.objects.filter(
                    quiz_id=s.quiz_id, flagged=False).exclude(status="playing"))
                if s in ranked:
                    rank, total = ranked.index(s) + 1, len(ranked)
            reward_text, reward_type = _effective_reward(space, s.quiz) if s.quiz_id else (None, None)
            sessions_stats.append({
                "session": s, "rank": rank, "total": total, "answers": s.answers.all(),
                "pct": _session_pct(s), "reward_text": reward_text,
                "reward_eligible": bool(reward_text) and s.status == "finished",
            })

        history = (Membership.objects.filter(space=space, player_id=member.player_id)
                  .exclude(id=member.id).select_related("license", "category", "sub_category")
                  .order_by("license__start_date"))

        # Points forts / à travailler par matière puis par thématique — même
        # calcul que sur /compte/ côté élève, ici scopé à ce membre précis :
        # utile pour un enseignant qui veut savoir où cet élève a besoin d'aide.
        space_answers = Answer.objects.filter(session__player_id=member.player_id, session__space=space,
                                              question__kind="quiz")
        overall_n = space_answers.count()
        overall_pct = round(100 * space_answers.filter(is_correct=True).count() / overall_n) if overall_n else None

        sub_totals, shared_cache = {}, {}
        for a in space_answers.select_related("question__sub_category__category", "question__quiz"):
            sub = _answer_subject(a.question, space, shared_cache)
            if not sub:
                continue
            row = sub_totals.setdefault(sub.id, {"sub": sub, "n": 0, "correct": 0})
            row["n"] += 1
            row["correct"] += 1 if a.is_correct else 0
        sub_breakdown = sorted((
            {"sub_category": r["sub"], "n": r["n"], "pct": round(100 * r["correct"] / r["n"])}
            for r in sub_totals.values()
        ), key=lambda r: r["pct"])

        theme_totals = {}
        for a in space_answers.select_related("question__theme__sub_category", "question__quiz"):
            th = _answer_theme(a.question, space, shared_cache)
            if not th:
                continue
            row = theme_totals.setdefault(th.key, {"theme": th, "n": 0, "correct": 0})
            row["n"] += 1
            row["correct"] += 1 if a.is_correct else 0
        theme_breakdown = sorted((
            {"theme": r["theme"], "n": r["n"], "pct": round(100 * r["correct"] / r["n"])}
            for r in theme_totals.values()
        ), key=lambda r: r["pct"])

        # Quiz encore à faire pour ce membre, toutes ses adhésions confondues
        # (licence en cours comme passées) — même logique que /compte/, pour
        # que l'établissement voie ce qu'il reste à cet élève sans lui demander.
        all_memberships = list(Membership.objects.filter(space=space, player_id=member.player_id)
                               .select_related("license", "category", "sub_category"))
        seen_quiz_ids = set()
        for m in all_memberships:
            if not m.category_id or _license_expired(m.license):
                continue
            days_left = _license_days_left(m.license)
            for q in _quizzes_for_membership(space, m):
                if q.id in played_quiz_ids or q.id in seen_quiz_ids:
                    continue
                seen_quiz_ids.add(q.id)
                assigned_quizzes.append({
                    "quiz": q, "period_label": m.license.period_label if m.license_id else "",
                    "days_left": days_left,
                })
        assigned_quizzes.sort(key=lambda a: a["days_left"] if a["days_left"] is not None else 9999)

    categories = space.categories.prefetch_related("subcategories")
    return render(request, "game/dashboard_member_detail.html", {
        "space": space, "member": member, "sessions_stats": sessions_stats,
        "categories": categories, "history": history, "overall_pct": overall_pct,
        "sub_breakdown": sub_breakdown, "theme_breakdown": theme_breakdown,
        "assigned_quizzes": assigned_quizzes,
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


OTP_MAX_PER_WINDOW = 3
OTP_WINDOW_MINUTES = 15


def normalize_phone(raw):
    """Numéro ivoirien au format unique 10 chiffres (« 0707070707 »), quelle
    que soit la saisie (+225, 00225, espaces, points, tirets). None si invalide."""
    raw = str(raw if raw is not None else "").strip()
    if re.fullmatch(r"\d+\.0+", raw):      # cellule Excel numérique lue « 707070707.0 »
        raw = raw.split(".")[0]
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("00225"):
        digits = digits[5:]
    elif digits.startswith("225") and len(digits) in (12, 13):
        digits = digits[3:]
    if len(digits) == 9:                       # Excel a mangé le 0 initial (0707… -> 707…)
        digits = "0" + digits
    return digits if len(digits) == 10 else None


def _otp_rate_limited(phone):
    since = timezone.now() - timedelta(minutes=OTP_WINDOW_MINUTES)
    return OTPCode.objects.filter(phone=phone, created_at__gte=since).count() >= OTP_MAX_PER_WINDOW


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
        phone = normalize_phone(request.POST.get("phone", ""))
        if space and space.access_code and request.POST.get("access_code", "").strip() != space.access_code:
            error = "Code d'accès incorrect."
        elif not phone:
            error = "Numéro invalide : 10 chiffres, ex. 07 07 07 07 07."
        elif _otp_rate_limited(phone):
            error = f"Trop de codes demandés — réessaie dans {OTP_WINDOW_MINUTES} minutes."
        else:
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
            _match_by_phone(Membership.objects.all(), phone, player)
            if not player.full_name:
                # Priorité à l'établissement via lequel la connexion a lieu — chaque
                # établissement garde sa propre fiche (Membership.full_name) ; on ne
                # pioche dans les autres qu'à défaut, juste pour préremplir le champ
                # (l'utilisateur reste libre de le modifier sur l'écran suivant).
                matched = None
                if space_slug:
                    matched = Membership.objects.filter(player=player, space__slug=space_slug).exclude(
                        full_name="").order_by("-created_at").first()
                if not matched:
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
    manquantes : le nom complet est sauté s'il est déjà connu (fourni par
    l'établissement via lequel la connexion a eu lieu, voir account_verify).
    Il reste modifiable ensuite à tout moment sur account_profile — inutile de
    redemander à l'inscription une info déjà donnée par l'établissement."""
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


def account_profile(request):
    """Profil du joueur, modifiable à tout moment (pas seulement à l'inscription) :
    pseudo/nom/ville sont globaux au joueur, jamais synchronisés avec la fiche
    qu'un établissement tient sur lui (Membership.full_name reste propre à chaque
    espace — voir dashboard_member_detail). Affiche aussi, pour info, la
    catégorie/sous-catégorie et la licence en cours dans chaque établissement."""
    player_id = request.session.get("verified_player_id")
    player = Player.objects.filter(id=player_id).first() if player_id else None
    if not player:
        return redirect("account_login")
    if not player.pseudo:
        return redirect("account_register")

    error = None
    saved = False
    if request.method == "POST":
        pseudo = request.POST.get("pseudo", "").strip()[:30]
        full_name = request.POST.get("full_name", "").strip()[:80]
        city = request.POST.get("city", "").strip()[:50]
        if not pseudo:
            error = "Le pseudo est obligatoire."
        else:
            player.pseudo = pseudo
            player.full_name = full_name
            player.city = city
            player.save(update_fields=["pseudo", "full_name", "city"])
            saved = True

    establishments, seen_spaces = [], set()
    for m in (Membership.objects.filter(player=player)
             .select_related("space", "category", "sub_category", "license")
             .order_by("space__name", "-created_at")):
        if m.space_id in seen_spaces:
            continue  # une ligne par établissement : son adhésion la plus récente
        seen_spaces.add(m.space_id)
        establishments.append(m)

    return render(request, "game/account_profile.html", {
        "player": player, "error": error, "saved": saved, "establishments": establishments,
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
        # Filtré par l'espace de la SESSION (pas Quiz.space) : un quiz partagé
        # (space=None) joué via cet espace doit quand même apparaître ici.
        for qz in Quiz.objects.filter(sessions__player=player, sessions__space=sp).distinct():
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
        sub_totals, shared_cache = {}, {}
        for a in space_answers.select_related("question__sub_category__category", "question__quiz"):
            sub = _answer_subject(a.question, sp, shared_cache)
            if not sub:
                continue
            row = sub_totals.setdefault(sub.id, {"sub": sub, "n": 0, "correct": 0})
            row["n"] += 1
            row["correct"] += 1 if a.is_correct else 0
        sub_breakdown = sorted((
            {"sub_category": r["sub"], "n": r["n"], "pct": round(100 * r["correct"] / r["n"])}
            for r in sub_totals.values()
        ), key=lambda r: r["pct"])

        # Même chose par thématique (quand les questions en portent une) — plus
        # fin que la matière, seulement affiché s'il y a des données à montrer.
        theme_totals = {}
        for a in space_answers.select_related("question__theme__sub_category", "question__quiz"):
            th = _answer_theme(a.question, sp, shared_cache)
            if not th:
                continue
            row = theme_totals.setdefault(th.key, {"theme": th, "n": 0, "correct": 0})
            row["n"] += 1
            row["correct"] += 1 if a.is_correct else 0
        theme_breakdown = sorted((
            {"theme": r["theme"], "n": r["n"], "pct": round(100 * r["correct"] / r["n"])}
            for r in theme_totals.values()
        ), key=lambda r: r["pct"])

        priority = None
        if len(sub_breakdown) > 1 and sub_breakdown[0]["pct"] < 70:
            weak_sub = sub_breakdown[0]["sub_category"]
            candidates = list(Quiz.objects.filter(space=sp, active=True, sub_category=weak_sub)) \
                + list(_global_quizzes_for(weak_sub.category, weak_sub))
            quiz = next((q for q in candidates if q.id not in played_quiz_ids), None) \
                or (candidates[0] if candidates else None)
            if quiz:
                priority = {"sub_category": weak_sub, "pct": sub_breakdown[0]["pct"], "quiz": quiz}

        # Quiz correspondant à l'établissement + catégorie/sous-catégorie de CHAQUE
        # adhésion du joueur (licence en cours ou passée) : un quiz d'une année
        # antérieure reste utile en révision, pas seulement l'année en cours.
        # Les quiz partagés (admin, sans espace) dont le niveau/matière
        # correspond sont mêlés automatiquement, comme les quiz propres à l'espace.
        assigned_quizzes = []
        seen_quiz_ids = set()
        for m in memberships:
            if not m.category_id or _license_expired(m.license):
                # Licence passée : les résultats déjà obtenus restent visibles
                # dans l'historique ci-dessous, mais on n'offre plus de jouer
                # de nouveaux quiz sur la seule base de cette adhésion.
                continue
            days_left = _license_days_left(m.license)
            for q in _quizzes_for_membership(sp, m):
                if q.id in played_quiz_ids or q.id in seen_quiz_ids:
                    continue
                seen_quiz_ids.add(q.id)
                assigned_quizzes.append({
                    "quiz": q,
                    "current": bool(membership and m.id == membership.id),
                    "period_label": m.license.period_label if m.license_id else "",
                    "days_left": days_left,
                })
        # Comme sur l'accueil : les quiz dont la licence expire bientôt remontent
        # en premier, pour que l'élève les voie avant qu'ils ne disparaissent.
        assigned_quizzes.sort(key=lambda a: a["days_left"] if a["days_left"] is not None else 9999)

        flat_count = GameSession.objects.filter(
            space=sp, quiz__isnull=True, player=player, flagged=False).exclude(status="playing").count()
        space_blocks.append({"space": sp, "membership": membership, "history": history,
                            "assigned_quizzes": assigned_quizzes, "space_pct": space_pct,
                            "quiz_rows": quiz_rows, "flat_count": flat_count,
                            "has_quizzes": sp.quizzes.filter(active=True).exists(),
                            "sub_breakdown": sub_breakdown, "theme_breakdown": theme_breakdown,
                            "priority": priority})

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
