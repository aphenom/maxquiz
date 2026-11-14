"""Accusés de réception des SMS envoyés par l'API d'Orange (« DLR »).

Orange envoie, pour chaque SMS, un POST JSON :
  {"deliveryInfoNotification": {"callbackData": "<id du SMS>",
      "deliveryInfo": {"address": "tel:+225…", "deliveryStatus": "DeliveredToTerminal"}}}
Protection : identifiant et mot de passe (ORANGE_DLR_USER / ORANGE_DLR_PASSWORD) si Orange
les envoie, et/ou adresses IP d'Orange (ORANGE_DLR_IPS, séparées par des virgules).
"""
import base64
import hmac
import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import SmsEnvoi

log = logging.getLogger(__name__)
STATUTS = {"DeliveredToTerminal", "DeliveredToNetwork", "DeliveryUncertain", "DeliveryImpossible", "MessageWaiting"}


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or ""


def _authorized(request):
    user, pwd = getattr(settings, "ORANGE_DLR_USER", ""), getattr(settings, "ORANGE_DLR_PASSWORD", "")
    ips = {i.strip() for i in getattr(settings, "ORANGE_DLR_IPS", "").split(",") if i.strip()}
    if user and pwd:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return False
        try:
            got = base64.b64decode(auth[6:]).decode()
        except (ValueError, UnicodeDecodeError):
            return False
        if not hmac.compare_digest(got, f"{user}:{pwd}"):
            return False
    if ips and _client_ip(request) not in ips:
        return False
    return True


@csrf_exempt
@require_POST
def orange_dlr(request):
    if not _authorized(request):
        return HttpResponse(status=401)
    try:
        info = json.loads(request.body or b"{}").get("deliveryInfoNotification") or {}
    except ValueError:
        return HttpResponse(status=400)
    rid = str(info.get("callbackData", ""))[:120]
    status = str((info.get("deliveryInfo") or {}).get("deliveryStatus", ""))
    if rid and status in STATUTS:
        SmsEnvoi.objects.filter(resource_id=rid).update(status=status, status_at=timezone.now())
    else:
        log.info("Accusé Orange ignoré : %s", info)
    return HttpResponse("ok")
