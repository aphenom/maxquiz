"""Application installable (PWA), abonnement aux notifications push et centre
de notifications. Le contrat avec l'APK est volontairement minimal et stable :

- APK de type TWA (recommandé) : rien à coder dans l'APK. Le site fait tout
  (service worker + Web Push) ; /.well-known/assetlinks.json prouve à Android
  que l'APK et le site vont ensemble.
- APK WebView ou natif : l'APK obtient un jeton Firebase et appelle
  window.maxquizSetFcmToken(jeton) dans la page (ou POST /api/push/fcm/ avec
  les cookies de la WebView). Les notifications portent un champ data.url que
  l'APK ouvre dans la WebView au toucher.
"""
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST

from . import push
from .models import Notification, PushDevice, Teacher
from .views import _player


def _recipient(request):
    """(player, teacher) connecté : un élève/joueur, ou un enseignant."""
    player = _player(request)
    tid = request.session.get("teacher_id")
    teacher = Teacher.objects.filter(id=tid, active=True).first() if tid else None
    return player, teacher


# --- Application installable ---------------------------------------------------
@cache_control(max_age=0, no_cache=True)
def service_worker(request):
    resp = render(request, "game/sw.js", {"version": getattr(settings, "APP_VERSION", "1")},
                  content_type="application/javascript")
    resp["Service-Worker-Allowed"] = "/"
    return resp


@cache_control(max_age=3600)
def manifest(request):
    data = {
        "name": "MaxQuiz", "short_name": "MaxQuiz", "lang": "fr",
        "description": "Cours, quiz et séances en direct de ton école.",
        "start_url": "/?source=app", "scope": "/", "display": "standalone",
        "background_color": "#FDF6EC", "theme_color": "#0B9A5C",
        "icons": [
            {"src": static("game/icons/icon-192.png"), "sizes": "192x192", "type": "image/png"},
            {"src": static("game/icons/icon-512.png"), "sizes": "512x512", "type": "image/png"},
            {"src": static("game/icons/maskable-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": static("game/icons/maskable-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/manifest+json")


def assetlinks(request):
    """Association site ↔ APK (TWA) : nom du paquet Android et empreinte(s)
    SHA-256 du certificat de signature, fournis par variables d'environnement."""
    package = getattr(settings, "ANDROID_PACKAGE_NAME", "")
    prints = [p.strip() for p in getattr(settings, "ANDROID_SHA256_FINGERPRINTS", "").split(",") if p.strip()]
    data = [] if not (package and prints) else [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {"namespace": "android_app", "package_name": package, "sha256_cert_fingerprints": prints},
    }]
    return JsonResponse(data, safe=False)


# --- Abonnement aux notifications ---------------------------------------------------
def push_config(request):
    return JsonResponse({"webpush": push.webpush_configured(), "vapidPublicKey": push.vapid_public_key()})


def _attach(request, kind, endpoint, p256dh="", auth=""):
    player, teacher = _recipient(request)
    if not (player or teacher):
        return JsonResponse({"error": "connexion requise"}, status=401)
    if not endpoint or len(endpoint) > 700:
        return HttpResponseBadRequest("abonnement invalide")
    PushDevice.objects.update_or_create(endpoint=endpoint, defaults=dict(
        kind=kind, player=player, teacher=teacher, p256dh=p256dh[:200], auth=auth[:100], active=True,
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:200]))
    return JsonResponse({"ok": True})


@require_POST
def push_subscribe(request):
    try:
        sub = json.loads(request.body)
        keys = sub.get("keys") or {}
        return _attach(request, "webpush", sub.get("endpoint", ""), keys.get("p256dh", ""), keys.get("auth", ""))
    except (ValueError, AttributeError):
        return HttpResponseBadRequest("JSON invalide")


@require_POST
def push_fcm(request):
    try:
        token = (json.loads(request.body).get("token") or "").strip()
    except ValueError:
        token = request.POST.get("token", "").strip()
    return _attach(request, "fcm", token)


@require_POST
def push_unsubscribe(request):
    try:
        endpoint = json.loads(request.body).get("endpoint", "")
    except ValueError:
        endpoint = ""
    PushDevice.objects.filter(endpoint=endpoint).update(active=False)
    return JsonResponse({"ok": True})


# --- Centre de notifications -----------------------------------------------------------
def notifications_page(request):
    player, teacher = _recipient(request)
    if not (player or teacher):
        return redirect("account_login")
    qs = Notification.objects.filter(player=player) if player else Notification.objects.filter(teacher=teacher)
    items = list(qs[:50])
    now = timezone.now()
    for n in items:
        minutes = int((now - n.created_at).total_seconds() // 60)
        n.ago = ("à l'instant" if minutes < 1 else f"il y a {minutes} min" if minutes < 60
                 else f"il y a {minutes // 60} h" if minutes < 1440 else timezone.localtime(n.created_at).strftime("%d/%m"))
    unread_ids = [n.id for n in items if not n.read_at]
    response = render(request, "game/notifications.html", {
        "items": items, "unread_ids": set(unread_ids), "tab": "account",
        "webpush": push.webpush_configured(),
    })
    if unread_ids:
        Notification.objects.filter(id__in=unread_ids).update(read_at=timezone.now())
    return response


def notification_open(request, notif_id):
    """Ouvrir une notification : la marque lue puis mène à son lien."""
    player, teacher = _recipient(request)
    n = Notification.objects.filter(id=notif_id).filter(
        **({"player": player} if player else {"teacher": teacher})).first()
    if not n:
        return redirect("notifications")
    if not n.read_at:
        n.read_at = timezone.now()
        n.save(update_fields=["read_at"])
    return redirect(n.url or "notifications")


# --- Tâche planifiée (rappels) -------------------------------------------------------------
def cron_reminders(request):
    """Rappels de séances et d'échéances, appelable par un service de tâches
    planifiées gratuit (ex. cron-job.org) toutes les 10 minutes :
    /cron/rappels/?token=<CRON_TOKEN>. Équivaut à `manage.py envoyer_rappels`."""
    token = getattr(settings, "CRON_TOKEN", "")
    if not token or request.GET.get("token") != token:
        return HttpResponse(status=404)
    from .reminders import run_reminders
    return JsonResponse(run_reminders())
