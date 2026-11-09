"""Aide et contact, signalement d'erreurs dans le contenu.

- /aide/ : WhatsApp, e-mail, questions fréquentes et formulaire d'assistance.
- /signaler/ : signaler une erreur sur une question (depuis le quiz, en JSON) ou
  sur un cours (formulaire de la page du cours).
Tout arrive dans l'administration (Signalements et assistance)."""
import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Lesson, Player, Question, Signalement
from .views import normalize_phone

MAX_PAR_JOUR = 20
MOTIFS_CONTENU = ("reponse", "enonce", "explication", "cours", "faute", "autre")
MOTIFS_ASSISTANCE = ("technique", "paiement", "compte", "autre")


def _player(request):
    pid = request.session.get("verified_player_id") or request.session.get("player_id")
    return Player.objects.filter(id=pid).first() if pid else None


def _too_many(request, player):
    since = timezone.now() - timedelta(days=1)
    if player:
        return Signalement.objects.filter(player=player, created_at__gte=since).count() >= MAX_PAR_JOUR
    sent = [t for t in request.session.get("signalements", []) if t > since.timestamp()]
    request.session["signalements"] = sent
    return len(sent) >= 5


def _remember(request):
    request.session["signalements"] = request.session.get("signalements", []) + [timezone.now().timestamp()]


def _alert_team(s):
    """Prévient l'équipe par e-mail si SIGNALEMENTS_EMAIL est réglé (sinon : administration seulement)."""
    to = getattr(settings, "SIGNALEMENTS_EMAIL", "")
    if not to:
        return
    from django.core.mail import send_mail
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    send_mail(f"[MaxQuiz] {s.get_kind_display()} : {s.get_motif_display()}",
              f"{s.target_label}\n\n{s.message}\n\nContact : {s.contact or '-'}\n"
              f"{base}/admin/game/signalement/{s.id}/change/",
              None, [to], fail_silently=True)


def _safe_next(request, default):
    nxt = request.POST.get("next") or request.GET.get("next") or ""
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()},
                                               require_https=request.is_secure()):
        return nxt
    return default


def aide(request):
    player = _player(request)
    error = None
    form = {"motif": "technique", "message": "", "contact": (player.phone if player else "") or ""}
    if request.method == "POST":
        form = {k: request.POST.get(k, "").strip() for k in ("motif", "message", "contact")}
        contact = normalize_phone(form["contact"]) if form["contact"] else ""
        if form["motif"] not in MOTIFS_ASSISTANCE:
            error = "Choisis le sujet de ta demande."
        elif len(form["message"]) < 5:
            error = "Explique ta demande en quelques mots."
        elif form["contact"] and not contact:
            error = "Numéro invalide : 10 chiffres, par exemple 07 07 07 07 07."
        elif not player and not contact:
            error = "Indique ton numéro pour qu'on puisse te répondre."
        elif _too_many(request, player):
            error = "Tu as déjà envoyé beaucoup de messages aujourd'hui. Écris-nous sur WhatsApp."
        else:
            s = Signalement.objects.create(
                kind="assistance", motif=form["motif"], message=form["message"][:1000], player=player,
                contact=contact or (player.phone if player else ""), page=_safe_next(request, "")[:300])
            _remember(request)
            _alert_team(s)
            messages.success(request, "Message envoyé. Nous te répondons au plus vite, en général sous 24 h.")
            return redirect("aide")
    wa = "".join(c for c in settings.CONTACT_WHATSAPP if c.isdigit())
    return render(request, "game/eleve/aide.html", {
        "form": form, "error": error, "contact_whatsapp": wa, "tab": "me" if player else None,
        "motifs": [(k, v) for k, v in Signalement.MOTIFS if k in MOTIFS_ASSISTANCE],
        "next": _safe_next(request, ""),
    })


@require_POST
def signaler(request):
    """Signalement d'une erreur de contenu. JSON depuis le quiz, formulaire depuis un cours."""
    is_json = request.content_type == "application/json"
    data = json.loads(request.body or "{}") if is_json else request.POST
    player = _player(request)
    motif = data.get("motif", "")
    message = str(data.get("message", "")).strip()[:1000]
    question = lesson = None
    if data.get("question_id"):
        question = Question.objects.filter(id=data.get("question_id")).select_related("quiz").first()
    if data.get("lesson_id"):
        lesson = Lesson.objects.filter(id=data.get("lesson_id")).first()

    def reply(ok, text):
        if is_json:
            return JsonResponse({"ok": ok, "message": text}, status=200 if ok else 400)
        (messages.success if ok else messages.error)(request, text)
        return redirect(_safe_next(request, "/"))

    if not (question or lesson):
        return reply(False, "Contenu introuvable.")
    if motif not in MOTIFS_CONTENU:
        return reply(False, "Choisis ce qui ne va pas.")
    if motif == "autre" and len(message) < 3:
        return reply(False, "Précise l'erreur en quelques mots.")
    if _too_many(request, player):
        return reply(False, "Tu as déjà envoyé beaucoup de signalements aujourd'hui. Merci !")
    s = Signalement.objects.create(
        kind="contenu", motif=motif, message=message, player=player, contact=(player.phone if player else "") or "",
        question=question, lesson=lesson,
        space=(question.space if question and question.space_id else lesson.space if lesson else None),
        page=str(data.get("page", ""))[:300])
    _remember(request)
    _alert_team(s)
    return reply(True, "Merci ! Notre équipe va vérifier et corriger si besoin.")
