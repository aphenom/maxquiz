"""Incidents : savoir tout de suite quand un élève rencontre un problème.

Sources :
- erreurs du serveur (erreur 500), captées par le signal got_request_exception ;
- pages lentes côté serveur (plus de LENTEUR_SERVEUR_MS), par IncidentsMiddleware ;
- erreurs dans la page, chargements trop longs et pannes de connexion pendant un quiz,
  envoyés par le téléphone ou l'ordinateur sur /api/incident/ ;
- contrôles de santé (commande verifier_sante, toutes les 10 minutes).

Les occurrences d'une même cause sont regroupées (signature). L'équipe est prévenue par push
(numéros de INCIDENTS_ALERT_PHONES) et par e-mail (INCIDENTS_EMAIL, sinon SIGNALEMENTS_EMAIL) :
- erreur du serveur ou de page : dès la première occurrence ;
- lenteur : à partir de 5 occurrences en une heure ;
- connexion impossible : à partir de 5 utilisateurs différents en 15 minutes ;
- relance quand le nombre d'utilisateurs touchés passe 10, 50, 200, 1000 ;
- un incident résolu qui revient repasse en « nouveau » et prévient de nouveau.
Jamais de code de connexion, de mot de passe ni de données de paiement dans les incidents.
"""
import hashlib
import logging
import re
import threading
import traceback
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone

log = logging.getLogger("maxquiz.incidents")

LENTEUR_SERVEUR_MS = 3000
LENTEUR_PAGE_MS = 8000
PALIERS = (10, 50, 200, 1000)
MAX_ALERTES_PAR_HEURE = 20
SECRETS = re.compile(r"(code|otp|password|mot_de_passe|token|secret|signature|key)=([^&\s]+)", re.I)
_alertes = {"heure": None, "n": 0}


def _clean(text, n=2000):
    return SECRETS.sub(r"\1=***", str(text or ""))[:n]


def signature(*parts):
    raw = "|".join(re.sub(r"\d+", "N", str(p or "")) for p in parts)
    return hashlib.sha1(raw.encode()).hexdigest()


def _infos_requete(request):
    from .stats import appareil, visiteur
    if request is None:
        return {}
    ua = request.META.get("HTTP_USER_AGENT", "")[:250]
    pid = None
    try:
        pid = request.session.get("verified_player_id") or request.session.get("player_id")
    except Exception:                                  # session illisible : on n'insiste pas
        pass
    return dict(player_id=pid, visiteur=visiteur(request), device=appareil(ua), user_agent=ua,
                path=_clean(request.get_full_path(), 300))


def enregistrer(kind, title, *, page="", detail="", request=None, sig=None, duration_ms=None, extra="",
                infos=None):
    """Ajoute une occurrence (et crée l'incident au besoin), puis décide s'il faut prévenir.
    Ne lève jamais d'exception : un incident ne doit pas en provoquer un autre."""
    from .models import Incident, IncidentEvent
    try:
        info = infos if infos is not None else _infos_requete(request)
        sig = sig or signature(kind, title, page)
        now = timezone.now()
        with transaction.atomic():
            inc, created = Incident.objects.get_or_create(signature=sig, defaults=dict(
                kind=kind, title=_clean(title, 200), page=_clean(page, 200), detail=_clean(detail, 8000),
                last_seen=now))
            reouvert = inc.status == "resolu"
            qui = dict(player_id=info.get("player_id")) if info.get("player_id") else \
                dict(visiteur=info.get("visiteur", ""))
            deja = bool(qui.get("player_id") or qui.get("visiteur")) and \
                IncidentEvent.objects.filter(incident=inc, **qui).exists()
            IncidentEvent.objects.create(incident=inc, duration_ms=duration_ms, extra=_clean(extra, 2000), **info)
            changes = dict(count=F("count") + 1, last_seen=now)
            if not deja:
                changes["users"] = F("users") + 1
            if reouvert:
                changes.update(status="nouveau", resolved_at=None, users_notified_at=None, alert_level=0)
            if detail and not inc.detail:
                changes["detail"] = _clean(detail, 8000)
            Incident.objects.filter(pk=inc.pk).update(**changes)
        inc.refresh_from_db()
        _peut_etre_alerter(inc, created, reouvert)
        return inc
    except Exception:
        log.exception("Impossible d'enregistrer l'incident « %s »", title)
        return None


# --- Erreurs et lenteurs du serveur ------------------------------------------------------
def erreur_serveur(sender=None, request=None, **kwargs):
    """Branché sur django.core.signals.got_request_exception."""
    import sys
    exc_type, exc, tb = sys.exc_info()
    if exc is None:
        return
    frames = traceback.extract_tb(tb)
    ours = [f for f in frames if "/game/" in f.filename or "/maxquiz/" in f.filename] or frames
    where = f"{ours[-1].filename.rsplit('/', 1)[-1]}:{ours[-1].lineno}" if ours else ""
    from .stats import page_cle
    page = page_cle(request.path) if request is not None else ""
    title = f"{exc_type.__name__} : {str(exc)[:140]}"
    log.error("Erreur 500 sur %s : %s", request.path if request is not None else "?", title, exc_info=True)
    enregistrer("serveur", title, page=page, request=request,
                detail="".join(traceback.format_exception(exc_type, exc, tb)),
                sig=signature("serveur", exc_type.__name__, where, page))


class IncidentsMiddleware:
    """Note les pages qui mettent trop de temps à répondre."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        t0 = time.monotonic()
        response = self.get_response(request)
        ms = int((time.monotonic() - t0) * 1000)
        if ms >= LENTEUR_SERVEUR_MS and not request.path.startswith(("/static/", "/admin/", "/telecharger/")):
            from .stats import page_cle
            page = page_cle(request.path)
            enregistrer("lenteur", f"Page lente côté serveur : {page}", page=page, request=request,
                        duration_ms=ms, sig=signature("lenteur-serveur", page))
        return response


# --- Ce que signalent les téléphones et ordinateurs ------------------------------------------
BRUIT = ("script error", "resizeobserver loop", "chrome-extension://", "moz-extension://", "safari-extension",
         "webkit-masked-url", "__gcrweb", "instantsearchsdkjsbridge")


def depuis_navigateur(request, data):
    """Événement envoyé par la page (game/static/game/incidents.js)."""
    from .stats import page_cle
    kind = str(data.get("kind", ""))[:12]
    message = str(data.get("message", ""))[:300]
    path = str(data.get("path", ""))[:300]
    page = page_cle(path.split("?")[0]) if path else ""
    if any(b in (message + " " + str(data.get("source", ""))).lower() for b in BRUIT):
        return None
    info = _infos_requete(request)
    info["path"] = _clean(path, 300)
    if kind == "erreur":
        source = re.sub(r"\?.*$", "", str(data.get("source", "")))[:200]
        where = f"{source.rsplit('/', 1)[-1]}:{data.get('line', '')}"
        return enregistrer("page", f"Erreur dans la page : {message}", page=page, infos=info,
                           detail=_clean(f"{message}\n{source}:{data.get('line', '')}:{data.get('col', '')}\n"
                                         f"{data.get('stack', '')}", 4000),
                           sig=signature("page", message, where))
    if kind == "lenteur":
        ms = int(float(data.get("ms") or 0))
        if ms < LENTEUR_PAGE_MS:
            return None
        return enregistrer("lenteur", f"Page longue à s'afficher : {page}", page=page, infos=info, duration_ms=ms,
                           extra=str(data.get("detail", ""))[:500], sig=signature("lenteur-page", page))
    if kind == "reseau":
        jour = timezone.localdate().isoformat()
        return enregistrer("reseau", f"Connexion impossible au serveur : {page}", page=page, infos=info,
                           extra=_clean(message, 300), sig=signature("reseau", page, jour))
    return None


# --- Alertes ---------------------------------------------------------------------------------
def _alerte_due(inc, created, reouvert):
    from .models import IncidentEvent
    now = timezone.now()
    if inc.status == "resolu":
        return None
    if reouvert:
        return "revient"
    if inc.kind in ("serveur", "page", "sante") and created:
        return "nouveau"
    if inc.kind == "lenteur" and not inc.alerted_at and \
            IncidentEvent.objects.filter(incident=inc, created_at__gte=now - timedelta(hours=1)).count() >= 5:
        return "nouveau"
    if inc.kind == "reseau" and not inc.alerted_at:
        recents = IncidentEvent.objects.filter(incident=inc, created_at__gte=now - timedelta(minutes=15))
        personnes = {(e.player_id, e.visiteur) for e in recents.only("player_id", "visiteur")}
        if len(personnes) >= 5:
            return "nouveau"
    palier = max([p for p in PALIERS if inc.users >= p], default=0)
    if palier > inc.alert_level and inc.alerted_at:
        return "aggrave"
    return None


def _peut_etre_alerter(inc, created, reouvert):
    from .models import Incident
    raison = _alerte_due(inc, created, reouvert)
    if not raison:
        return
    heure = timezone.now().replace(minute=0, second=0, microsecond=0)
    if _alertes["heure"] != heure:
        _alertes.update(heure=heure, n=0)
    if _alertes["n"] >= MAX_ALERTES_PAR_HEURE:
        return
    _alertes["n"] += 1
    palier = max([p for p in PALIERS if inc.users >= p], default=0)
    Incident.objects.filter(pk=inc.pk).update(alerted_at=timezone.now(), alert_level=palier)
    titre = {"nouveau": "⚠️ Nouveau problème", "revient": "⚠️ Problème revenu",
             "aggrave": f"⚠️ {inc.users} utilisateurs touchés"}[raison]
    prevenir_equipe(f"{titre} : {inc.get_kind_display()}", inc.title, url_admin(inc), inc)


def url_admin(inc):
    return f"/admin/game/incident/{inc.pk}/change/"


def numeros_equipe():
    raw = getattr(settings, "INCIDENTS_ALERT_PHONES", "") or ""
    return [p.strip() for p in raw.split(",") if p.strip()]


def prevenir_equipe(titre, texte, url, inc=None):
    """Push aux numéros de l'équipe et e-mail, en arrière-plan (la page de l'élève n'attend pas)."""
    from .models import Player
    from .push import notify
    try:
        joueurs = list(Player.objects.filter(phone__in=numeros_equipe()))
        if joueurs:
            notify(players=joueurs, kind="incident", title=titre[:120], body=texte[:300], url=url)
    except Exception:
        log.exception("Alerte push impossible")
    to = getattr(settings, "INCIDENTS_EMAIL", "") or getattr(settings, "SIGNALEMENTS_EMAIL", "")
    if not to:
        return
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    corps = f"{texte}\n\n{base}{url}\n"
    if inc is not None:
        corps += (f"\nPage : {inc.page or '-'}\nOccurrences : {inc.count} · utilisateurs touchés : {inc.users}\n"
                  f"\n{inc.detail[-3000:]}")

    def envoyer():
        from django.core.mail import send_mail
        send_mail(f"[MaxQuiz] {titre}"[:150], corps, None, [a.strip() for a in to.split(",")], fail_silently=True)
    if getattr(settings, "PUSH_SYNC", False):
        envoyer()
    else:
        threading.Thread(target=envoyer, daemon=True).start()


def prevenir_utilisateurs(inc):
    """Après correction : chaque élève touché reçoit un message (application et push)."""
    from .models import Incident, Player
    from .push import notify
    ids = set(inc.events.exclude(player__isnull=True).values_list("player_id", flat=True))
    joueurs = list(Player.objects.filter(id__in=ids))
    if joueurs:
        notify(players=joueurs, kind="incident_resolu", title="Problème corrigé ✅",
               body="Le souci que tu as rencontré sur MaxQuiz est corrigé. Merci de ta patience, tu peux reprendre !",
               url="/")
    Incident.objects.filter(pk=inc.pk).update(users_notified_at=timezone.now())
    return len(joueurs)


# --- Battements des tâches planifiées -----------------------------------------------------------
def battement(nom, valeur=""):
    from .models import Pouls
    try:
        Pouls.objects.update_or_create(nom=nom, defaults=dict(dernier=timezone.now(), valeur=str(valeur)[:60]))
    except Exception:
        log.exception("Battement « %s » impossible", nom)
