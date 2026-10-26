"""Mesure des pubs Meta (Facebook, Instagram) pour MaxQuiz École.

- Provenance : les paramètres utm_* et fbclid de l'adresse d'arrivée sont gardés
  en session (premier contact), puis rattachés à l'élève à son inscription.
- Pixel (navigateur) + API Conversions (serveur) : chaque événement part des deux
  côtés avec le même event_id, et Meta n'en compte qu'un. L'achat (paiement validé
  à la main, plus tard) ne part que du serveur.
- Uniquement avec le consentement (cookie mq_consent=1) et si META_PIXEL_ID et
  META_CAPI_TOKEN sont réglés. Aucune donnée personnelle de l'élève n'est envoyée :
  ni numéro, ni nom, ni classe ; seulement l'événement, le montant et les
  identifiants techniques de clic (fbc, fbp), l'adresse IP et le navigateur.
"""
import json
import logging
import threading
import time
import urllib.request
import uuid

from django.conf import settings

log = logging.getLogger(__name__)

UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign", "utm_content")
CONSENT_COOKIE = "mq_consent"


def enabled():
    return bool(settings.META_PIXEL_ID)


def has_consent(request):
    return request.COOKIES.get(CONSENT_COOKIE) == "1"


def capture(request):
    """Premier contact : garde en session la provenance de la visite (une seule fois)."""
    if request.method != "GET" or "ad_src" in request.session:
        return
    params = {k: request.GET.get(k, "")[:150] for k in UTM_KEYS if request.GET.get(k)}
    fbclid = request.GET.get("fbclid", "")[:255]
    if not (params or fbclid):
        return
    if fbclid:
        params["fbclid"] = fbclid
        params["fbc"] = f"fb.1.{int(time.time() * 1000)}.{fbclid}"
    params["landing_path"] = request.path[:200]
    request.session["ad_src"] = params


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or None


def attach(request, player):
    """À l'inscription : enregistre la provenance de l'élève (premier contact)."""
    from .models import AdAttribution
    if hasattr(player, "attribution"):
        return player.attribution
    src = request.session.get("ad_src") or {}
    a = AdAttribution(player=player, **{k: src.get(k, "") for k in UTM_KEYS + ("fbclid", "landing_path")})
    if has_consent(request):
        set_consent(a, request, save=False)
    a.save()
    return a


def set_consent(attribution, request, save=True):
    """Consentement donné : on garde les identifiants techniques utiles à Meta
    (sans consentement, seule la campagne d'origine est conservée, pour nos chiffres)."""
    src = request.session.get("ad_src") or {}
    attribution.consent = True
    attribution.fbc = (src.get("fbc") or request.COOKIES.get("_fbc", ""))[:300]
    attribution.fbp = request.COOKIES.get("_fbp", "")[:100]
    attribution.user_agent = request.META.get("HTTP_USER_AGENT", "")[:300]
    attribution.ip = _client_ip(request)
    if save:
        attribution.save(update_fields=["consent", "fbc", "fbp", "user_agent", "ip"])


def queue_browser(request, name, event_id, params=None):
    """Événement à déclencher par le pixel à l'affichage de la prochaine page."""
    events = request.session.get("pixel_events", [])
    events.append({"name": name, "id": event_id, "params": params or {}})
    request.session["pixel_events"] = events[-5:]


def _post(payload):
    url = (f"https://graph.facebook.com/{settings.META_API_VERSION}/{settings.META_PIXEL_ID}/events"
           f"?access_token={settings.META_CAPI_TOKEN}")
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status
    except Exception as exc:                       # la mesure ne doit jamais bloquer l'élève
        log.warning("API Conversions Meta : %s", exc)
        return None


def build_event(name, event_id, attribution=None, request=None, value=None, source_url=""):
    user_data = {}
    if attribution:
        user_data = {k: v for k, v in (("fbc", attribution.fbc), ("fbp", attribution.fbp),
                                        ("client_user_agent", attribution.user_agent),
                                        ("client_ip_address", attribution.ip)) if v}
    if request:
        user_data.setdefault("client_user_agent", request.META.get("HTTP_USER_AGENT", "")[:300])
        user_data.setdefault("client_ip_address", _client_ip(request))
        fbp = request.COOKIES.get("_fbp")
        if fbp:
            user_data.setdefault("fbp", fbp)
        source_url = source_url or request.build_absolute_uri()
    event = {"event_name": name, "event_time": int(time.time()), "event_id": event_id,
             "action_source": "website", "user_data": {k: v for k, v in user_data.items() if v}}
    if source_url:
        event["event_source_url"] = source_url
    if value is not None:
        event["custom_data"] = {"value": value, "currency": "XOF"}
    return event


def send_server(name, event_id, attribution=None, request=None, value=None, source_url=""):
    """API Conversions : envoie l'événement depuis le serveur (en arrière-plan)."""
    if not (enabled() and settings.META_CAPI_TOKEN):
        return None
    if attribution is not None and not attribution.consent:
        return None
    if attribution is None and request is not None and not has_consent(request):
        return None
    payload = {"data": [build_event(name, event_id, attribution, request, value, source_url)]}
    if settings.META_TEST_EVENT_CODE:
        payload["test_event_code"] = settings.META_TEST_EVENT_CODE
    if getattr(settings, "META_SYNC", False):
        return _post(payload)
    threading.Thread(target=_post, args=(payload,), daemon=True).start()
    return payload


def track(request, name, attribution=None, value=None):
    """Même événement côté navigateur (pixel) et côté serveur, dédoublonné par event_id."""
    if not enabled():
        return None
    event_id = f"{name.lower()}-{uuid.uuid4().hex[:16]}"
    params = {"value": value, "currency": "XOF"} if value is not None else {}
    if has_consent(request):
        queue_browser(request, name, event_id, params)
    send_server(name, event_id, attribution=attribution, request=request if attribution is None else None,
                value=value, source_url=request.build_absolute_uri())
    return event_id


def track_purchase(subscription):
    """Paiement d'abonnement validé (MaxQuiz École) : achat envoyé à Meta par le serveur."""
    m = subscription.membership
    if not (enabled() and m.space.kind == "catalog" and m.player_id):
        return None
    attribution = getattr(m.player, "attribution", None)
    if not attribution:
        return None
    base = settings.SITE_URL.rstrip("/")
    return send_server("Purchase", f"sub-{subscription.id}", attribution=attribution,
                       value=subscription.amount,
                       source_url=f"{base}/e/{m.space.slug}/abonnement/" if base else "")
