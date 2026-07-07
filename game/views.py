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
