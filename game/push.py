"""Notifications : centre de notifications dans l'application + envoi push.

Deux canaux, choisis par appareil :
- Web Push (RFC 8030/8291, clés VAPID RFC 8292) : navigateurs et APK de type
  TWA (Trusted Web Activity), où Chrome affiche la notification au nom de l'app.
- Firebase Cloud Messaging (API HTTP v1) : APK WebView/natif qui transmet son
  jeton FCM au serveur.

Aucune dépendance en plus de `cryptography` (déjà requise par Django pour le
hachage) : le chiffrement et les signatures sont faits ici, ce qui évite les
paquets difficiles à installer sur un petit hébergement.

Point d'entrée unique : notify(...). Tout nouveau type de notification se
déclare côté serveur, sans mise à jour de l'APK.
"""
import base64
import json
import logging
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlparse

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from django.conf import settings
from django.utils import timezone

log = logging.getLogger(__name__)


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64u_dec(text: str) -> bytes:
    text = text.strip()
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


# --- Clés VAPID ------------------------------------------------------------------
def generate_vapid_keys():
    """(clé privée, clé publique) au format base64url à mettre dans les
    variables d'environnement VAPID_PRIVATE_KEY / VAPID_PUBLIC_KEY."""
    priv = ec.generate_private_key(ec.SECP256R1())
    d = priv.private_numbers().private_value.to_bytes(32, "big")
    pub = priv.public_key().public_bytes(serialization.Encoding.X962,
                                         serialization.PublicFormat.UncompressedPoint)
    return b64u(d), b64u(pub)


def vapid_public_key():
    return getattr(settings, "VAPID_PUBLIC_KEY", "") or ""


def webpush_configured():
    return bool(vapid_public_key() and getattr(settings, "VAPID_PRIVATE_KEY", ""))


def _vapid_private():
    d = int.from_bytes(b64u_dec(settings.VAPID_PRIVATE_KEY), "big")
    return ec.derive_private_key(d, ec.SECP256R1())


def _es256_jwt(claims, private_key):
    head = b64u(json.dumps({"typ": "JWT", "alg": "ES256"}, separators=(",", ":")).encode())
    body = b64u(json.dumps(claims, separators=(",", ":")).encode())
    der = private_key.sign(f"{head}.{body}".encode(), ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(der)
    return f"{head}.{body}.{b64u(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"


def vapid_header(endpoint):
    u = urlparse(endpoint)
    claims = {"aud": f"{u.scheme}://{u.netloc}", "exp": int(time.time()) + 12 * 3600,
              "sub": getattr(settings, "VAPID_SUBJECT", "mailto:contact@mqtech.ci")}
    return f"vapid t={_es256_jwt(claims, _vapid_private())}, k={vapid_public_key()}"


# --- Chiffrement du message (RFC 8291, aes128gcm) ------------------------------
def encrypt_payload(payload: bytes, p256dh: str, auth: str, *, salt=None, server_key=None) -> bytes:
    ua_public = b64u_dec(p256dh)
    auth_secret = b64u_dec(auth)
    server_key = server_key or ec.generate_private_key(ec.SECP256R1())
    as_public = server_key.public_key().public_bytes(serialization.Encoding.X962,
                                                    serialization.PublicFormat.UncompressedPoint)
    ua_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), ua_public)
    ecdh = server_key.exchange(ec.ECDH(), ua_key)
    ikm = HKDF(algorithm=hashes.SHA256(), length=32, salt=auth_secret,
               info=b"WebPush: info\x00" + ua_public + as_public).derive(ecdh)
    salt = salt or os.urandom(16)
    cek = HKDF(algorithm=hashes.SHA256(), length=16, salt=salt,
               info=b"Content-Encoding: aes128gcm\x00").derive(ikm)
    nonce = HKDF(algorithm=hashes.SHA256(), length=12, salt=salt,
                 info=b"Content-Encoding: nonce\x00").derive(ikm)
    record = AESGCM(cek).encrypt(nonce, payload + b"\x02", None)
    header = salt + (4096).to_bytes(4, "big") + bytes([len(as_public)]) + as_public
    return header + record


def _post(url, data, headers, timeout=10):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def send_webpush(device, message):
    body = encrypt_payload(json.dumps(message).encode(), device.p256dh, device.auth)
    status, _ = _post(device.endpoint, body, {
        "Content-Encoding": "aes128gcm", "Content-Type": "application/octet-stream",
        "TTL": "86400", "Urgency": "normal", "Authorization": vapid_header(device.endpoint)})
    return status


# --- Firebase Cloud Messaging (HTTP v1) -------------------------------------------
_fcm_token = {"value": "", "exp": 0}


def _fcm_account():
    raw = getattr(settings, "FCM_SERVICE_ACCOUNT_JSON", "") or ""
    if not raw:
        return None
    if not raw.lstrip().startswith("{") and os.path.exists(raw):
        raw = open(raw).read()
    return json.loads(raw)


def fcm_configured():
    return bool(getattr(settings, "FCM_SERVICE_ACCOUNT_JSON", ""))


def _fcm_access_token(account):
    if _fcm_token["value"] and _fcm_token["exp"] > time.time() + 60:
        return _fcm_token["value"]
    now = int(time.time())
    head = b64u(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    body = b64u(json.dumps({"iss": account["client_email"], "aud": account["token_uri"], "iat": now,
                            "exp": now + 3600,
                            "scope": "https://www.googleapis.com/auth/firebase.messaging"}).encode())
    key = serialization.load_pem_private_key(account["private_key"].encode(), password=None)
    sig = key.sign(f"{head}.{body}".encode(), padding.PKCS1v15(), hashes.SHA256())
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": f"{head}.{body}.{b64u(sig)}"}).encode()
    status, raw = _post(account["token_uri"], data, {"Content-Type": "application/x-www-form-urlencoded"})
    info = json.loads(raw or b"{}")
    _fcm_token.update(value=info.get("access_token", ""), exp=now + int(info.get("expires_in", 0)))
    return _fcm_token["value"]


def send_fcm(device, message):
    account = _fcm_account()
    token = _fcm_access_token(account)
    payload = {"message": {
        "token": device.endpoint,
        "notification": {"title": message["title"], "body": message["body"]},
        "data": {"url": message["url"], "tag": message["tag"]},
        "android": {"priority": "high", "notification": {"tag": message["tag"]}},
    }}
    status, raw = _post(f"https://fcm.googleapis.com/v1/projects/{account['project_id']}/messages:send",
                        json.dumps(payload).encode(),
                        {"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    if status == 400 and b"registration-token-not-registered" in (raw or b"").lower():
        return 404
    return status


# --- Envoi ----------------------------------------------------------------------
def _deliver(device_ids, message, notification_ids):
    from .models import Notification, PushDevice
    reached = 0
    for device in PushDevice.objects.filter(id__in=device_ids, active=True):
        try:
            if device.kind == "webpush" and webpush_configured():
                status = send_webpush(device, message)
            elif device.kind == "fcm" and fcm_configured():
                status = send_fcm(device, message)
            else:
                continue
        except Exception:  # un appareil en erreur ne bloque jamais les autres
            log.exception("Échec d'envoi push vers l'appareil %s", device.id)
            continue
        if status in (404, 410):           # abonnement expiré ou désinstallé
            PushDevice.objects.filter(id=device.id).update(active=False)
        elif 200 <= status < 300:
            reached += 1
            PushDevice.objects.filter(id=device.id).update(last_success_at=timezone.now())
    if reached:
        Notification.objects.filter(id__in=notification_ids).update(pushed=reached)


def notify(*, players=(), teachers=(), title, body="", url="", kind="info"):
    """Crée la notification dans l'application pour chaque destinataire et
    l'envoie en push à ses appareils, en arrière-plan (la requête de la
    personne qui a déclenché l'envoi n'attend pas)."""
    from .models import Notification, PushDevice
    players = {p.id: p for p in players if p}
    teachers = {t.id: t for t in teachers if t}
    if not (players or teachers):
        return 0
    rows = ([Notification(player_id=pid, kind=kind, title=title[:120], body=body[:300], url=url[:300])
             for pid in players]
            + [Notification(teacher_id=tid, kind=kind, title=title[:120], body=body[:300], url=url[:300])
               for tid in teachers])
    created = Notification.objects.bulk_create(rows)
    device_ids = list(PushDevice.objects.filter(active=True)
                      .filter(models_q(players=list(players), teachers=list(teachers)))
                      .values_list("id", flat=True))
    if device_ids:
        message = {"title": title, "body": body, "url": url or "/", "tag": kind}
        ids = [n.id for n in created if n.id]
        if getattr(settings, "PUSH_SYNC", False):
            _deliver(device_ids, message, ids)
        else:
            threading.Thread(target=_deliver, args=(device_ids, message, ids), daemon=True).start()
    return len(created)


def models_q(players, teachers):
    from django.db.models import Q
    return Q(player_id__in=players) | Q(teacher_id__in=teachers)


# --- Destinataires courants ---------------------------------------------------------
def students_of(space, sub_category=None):
    """Joueurs inscrits dans l'espace, limités à une matière si elle est donnée
    (un élève inscrit au niveau entier reçoit les nouveautés de toutes ses matières)."""
    from django.db.models import Q
    from .models import Player
    qs = space.members.filter(player__isnull=False)
    if sub_category is not None:
        qs = qs.filter(category_id=sub_category.category_id).filter(
            Q(sub_category__isnull=True) | Q(sub_category_id=sub_category.id))
    return list(Player.objects.filter(id__in=qs.values("player_id")))


def direction_of(space):
    return list(space.teachers.filter(active=True, role="direction"))
