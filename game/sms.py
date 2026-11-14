"""Envoi des SMS (code de connexion) avec l'API SMS d'Orange Côte d'Ivoire.

Réglages (fichier d'environnement) :
  SMS_PROVIDER=orange              (sans réglage : « console », le code est seulement écrit dans les journaux)
  ORANGE_CLIENT_ID / ORANGE_CLIENT_SECRET   : Orange Developer > My apps
  ORANGE_SMS_SENDER_NUMBER=2250000          : adresse d'envoi de la Côte d'Ivoire (par défaut)
  ORANGE_SMS_SENDER_NAME=MaxQuiz            : nom d'expéditeur validé par Orange
  SMS_NOM_OPERATEURS=orange                 : opérateurs chez qui le nom est autorisé (orange,mtn,moov) ;
                                              ailleurs, le SMS part sans nom personnalisé
Accusés de réception : POST /sms/orange/accuse/ (voir views_sms.py).
Documentation : https://developer.orange.com/apis/sms/getting-started
"""
import base64
import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

log = logging.getLogger(__name__)
API = "https://api.orange.com"
_token = {"value": "", "expires": 0.0}

MESSAGE_CODE = "MaxQuiz : ton code de connexion est {code}. Il expire dans 10 minutes. Ne le communique a personne."


class SmsError(Exception):
    pass


def operateur(phone):
    """Opérateur d'un numéro ivoirien à 10 chiffres (plan de numérotation de 2021)."""
    p = "".join(c for c in str(phone or "") if c.isdigit())
    if p.startswith("225") and len(p) == 13:
        p = p[3:]
    return {"07": "orange", "05": "mtn", "01": "moov"}.get(p[:2], "autre")


def international(phone):
    p = "".join(c for c in str(phone or "") if c.isdigit())
    return p if p.startswith("225") and len(p) == 13 else "225" + p


def provider():
    return (getattr(settings, "SMS_PROVIDER", "") or "console").lower()


def _http(method, url, headers, data=None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as exc:
        body = exc.read()[:400].decode(errors="replace")
        raise SmsError(f"HTTP {exc.code} {body}") from exc
    except Exception as exc:
        raise SmsError(str(exc)) from exc


def _orange_token():
    if _token["value"] and _token["expires"] > time.time() + 60:
        return _token["value"]
    creds = f"{settings.ORANGE_CLIENT_ID}:{settings.ORANGE_CLIENT_SECRET}".encode()
    _, res = _http("POST", f"{API}/oauth/v3/token", {
        "Authorization": "Basic " + base64.b64encode(creds).decode(),
        "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        b"grant_type=client_credentials")
    _token["value"] = res.get("access_token", "")
    _token["expires"] = time.time() + int(res.get("expires_in") or 3600)
    if not _token["value"]:
        raise SmsError("Pas de jeton Orange")
    return _token["value"]


def _orange_send(phone, text, sender_name):
    sender = settings.ORANGE_SMS_SENDER_NUMBER
    req = {"address": f"tel:+{international(phone)}", "senderAddress": f"tel:+{sender}",
           "outboundSMSTextMessage": {"message": text}}
    if sender_name:
        req["senderName"] = sender_name
    url = f"{API}/smsmessaging/v1/outbound/{urllib.parse.quote(f'tel:+{sender}', safe='')}/requests"
    for attempt in (1, 2):
        headers = {"Authorization": f"Bearer {_orange_token()}", "Content-Type": "application/json",
                   "Accept": "application/json"}
        try:
            _, res = _http("POST", url, headers, json.dumps({"outboundSMSMessageRequest": req}).encode())
            break
        except SmsError as exc:
            if attempt == 1 and "HTTP 401" in str(exc):
                _token["value"] = ""               # jeton expiré : on en redemande un
                continue
            raise
    resource = ((res.get("outboundSMSMessageRequest") or {}).get("resourceURL") or "")
    return resource.rstrip("/").rsplit("/", 1)[-1]


def envoyer(phone, text, kind="otp"):
    """Envoie un SMS ; renvoie la ligne SmsEnvoi. Lève SmsError si l'envoi échoue."""
    from .models import SmsEnvoi
    op = operateur(phone)
    if provider() == "console":
        log.warning("[SMS console] %s : %s", phone, text)
        print(f"[SMS] {phone} -> {text}")
        return SmsEnvoi.objects.create(phone=phone, operateur=op, kind=kind, provider="console", status="console")
    if provider() != "orange":
        raise SmsError(f"Prestataire SMS inconnu : {provider()}")
    allowed = {o.strip() for o in getattr(settings, "SMS_NOM_OPERATEURS", "orange").split(",") if o.strip()}
    name = settings.ORANGE_SMS_SENDER_NAME if (op in allowed and settings.ORANGE_SMS_SENDER_NAME) else ""
    row = SmsEnvoi(phone=phone, operateur=op, kind=kind, provider="orange", sender_name=name[:11])
    try:
        row.resource_id = _orange_send(phone, text, name)[:120]
        row.status = "sent"
    except SmsError as exc:
        row.status, row.error = "failed", str(exc)[:200]
        row.save()
        log.warning("SMS Orange vers %s impossible : %s", phone, exc)
        raise
    row.save()
    return row


def envoyer_code(phone, code):
    return envoyer(phone, MESSAGE_CODE.format(code=code), kind="otp")
