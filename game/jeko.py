"""Paiement en ligne des abonnements MaxQuiz École avec Jèko (Wave, Orange Money,
MTN, Moov, Djamo). Documentation : https://developer.jeko.africa

Parcours :
1. l'élève choisit sa formule et son opérateur ; on crée l'abonnement « initiated »
   et une demande de paiement Jèko (montant fixé par le serveur) ;
2. l'élève paie dans son application mobile money, puis revient sur /paiement/jeko/retour/ ;
3. Jèko confirme par webhook (TRANSACTION_COMPLETED, signé HMAC-SHA256) : c'est la
   source de vérité. Le retour du navigateur et la commande `jeko_verifier` interrogent
   aussi le statut, car un paiement échoué n'envoie pas de webhook.
Un paiement confirmé active l'abonnement tout de suite (validate) et prévient l'élève.
"""
import hashlib
import hmac
import json
import logging
import secrets
import urllib.error
import urllib.request

from django.conf import settings
from django.db import transaction
from django.urls import reverse

log = logging.getLogger(__name__)

METHODS = [("wave", "Wave"), ("orange", "Orange Money"), ("mtn", "MTN MoMo"),
           ("moov", "Moov Money"), ("djamo", "Djamo")]


class JekoError(Exception):
    pass


def enabled():
    return all(getattr(settings, k, "") for k in ("JEKO_API_KEY", "JEKO_API_KEY_ID", "JEKO_STORE_ID"))


def available_for(space):
    """Le compte Jèko est celui de MQ Technologies : seulement pour l'espace MaxQuiz École."""
    return enabled() and space is not None and space.kind == "catalog"


def _call(method, path, payload=None):
    url = settings.JEKO_API_URL.rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "X-API-KEY": settings.JEKO_API_KEY, "X-API-KEY-ID": settings.JEKO_API_KEY_ID,
        "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as exc:
        body = exc.read()[:500].decode(errors="replace")
        log.warning("Jèko %s %s : %s %s", method, path, exc.code, body)
        raise JekoError(f"HTTP {exc.code}") from exc
    except Exception as exc:                    # réseau, délai, réponse illisible
        log.warning("Jèko %s %s : %s", method, path, exc)
        raise JekoError(str(exc)) from exc


def _base_url(request=None):
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    if base:
        return base
    return request.build_absolute_uri("/").rstrip("/") if request else ""


def start_payment(request, membership, plan, method, promo=None):
    """Crée l'abonnement en attente et la demande de paiement Jèko.
    Renvoie (abonnement, url de paiement)."""
    from .models import Subscription
    if method not in dict(METHODS):
        raise JekoError("Opérateur inconnu")
    ref = f"MQ-{membership.id}-{secrets.token_hex(5).upper()}"
    with transaction.atomic():
        sub = Subscription.objects.create(membership=membership, plan=plan["code"], amount=plan["price"],
                                          list_price=plan.get("list_price", plan["price"]), promo=promo,
                                          payment_ref=ref, provider="jeko", payment_method=method,
                                          status="initiated", payer_phone=membership.phone or "")
    back = _base_url(request) + reverse("jeko_return")
    try:
        res = _call("POST", "/partner_api/payment_requests", {
            "storeId": settings.JEKO_STORE_ID,
            "amountCents": int(plan["price"]) * 100,
            "currency": "XOF",
            "reference": ref,
            "paymentDetails": {"type": "redirect", "data": {
                "paymentMethod": method,
                "successUrl": f"{back}?ref={ref}",
                "errorUrl": f"{back}?ref={ref}&echec=1"}},
        })
    except JekoError:
        sub.status = "failed"
        sub.note = "Demande de paiement refusée par Jèko"
        sub.save(update_fields=["status", "note"])
        raise
    sub.provider_id = str(res.get("id", ""))[:80]
    sub.save(update_fields=["provider_id"])
    url = res.get("redirectUrl")
    if not url:
        sub.status = "failed"
        sub.note = f"Pas de lien de paiement ({res.get('errorReason') or 'inconnu'})"[:200]
        sub.save(update_fields=["status", "note"])
        raise JekoError("Pas de lien de paiement")
    return sub, url


def confirm(sub, source, transaction_id=""):
    """Paiement confirmé : active l'abonnement une seule fois et prévient l'élève."""
    from .models import Subscription
    from .push import notify
    from .subscriptions import validate
    with transaction.atomic():
        sub = Subscription.objects.select_for_update().get(pk=sub.pk)
        if sub.status == "active":
            return sub, False
        if transaction_id:
            sub.note = f"Jèko {transaction_id} ({source})"[:200]
            sub.save(update_fields=["note"])
        validate(sub)
    m = sub.membership
    if m.player_id:
        notify(players=[m.player], kind="sub_ok", title="Abonnement activé",
               body=f"Paiement reçu. Accès complet jusqu'au {sub.end_date:%d/%m/%Y}. Bonnes révisions !",
               url=reverse("space_home", args=[m.space.slug]))
    return sub, True


def amount_ok(sub, amount):
    """Jèko donne les montants en centimes (plus petite unité) : 2 000 F = 200000."""
    try:
        return int(amount) == sub.amount * 100
    except (TypeError, ValueError):
        return False


def hold(sub, amount, source):
    """Montant reçu inattendu ou absent : validation manuelle dans le tableau de bord.
    Un abonnement déjà actif n'est jamais rétrogradé."""
    from .models import Subscription
    log.warning("Jèko (%s) : montant inattendu pour %s (%s au lieu de %s centimes)",
                source, sub.payment_ref, amount, sub.amount * 100)
    return bool(Subscription.objects.filter(pk=sub.pk).exclude(status="active").update(
        status="pending", note=f"Montant reçu {amount} centimes au lieu de {sub.amount * 100} : à vérifier"[:200]))


def mark_failed(sub, reason=""):
    from .models import Subscription
    updated = Subscription.objects.filter(pk=sub.pk, status="initiated").update(
        status="failed", note=(reason or "Paiement non abouti")[:200])
    return bool(updated)


def refresh(sub):
    """Interroge Jèko sur une demande en cours ; met l'abonnement à jour. Renvoie le statut Jèko."""
    if sub.provider != "jeko" or not sub.provider_id or sub.status != "initiated":
        return None
    res = _call("GET", f"/partner_api/payment_requests/{sub.provider_id}")
    status = str(res.get("status", "")).lower()
    if status == "success":
        txn = res.get("transaction") or {}
        amount = (txn.get("amount") or {}).get("amount")
        if amount_ok(sub, amount):
            confirm(sub, "statut", txn.get("id", ""))
        else:
            hold(sub, amount, "statut")
    elif status in ("error", "failed", "expired", "cancelled", "canceled"):
        mark_failed(sub, res.get("errorReason") or "Paiement non abouti")
    return status


def valid_signature(raw_body, signature):
    secret = getattr(settings, "JEKO_WEBHOOK_SECRET", "")
    if not (secret and signature):
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature.strip().lower())


def handle_webhook(event, body):
    """TRANSACTION_COMPLETED : on retrouve l'abonnement par notre référence et on vérifie
    le montant avant d'activer. Renvoie un court compte rendu (pour les journaux)."""
    from .models import Subscription
    if event != "TRANSACTION_COMPLETED":
        return f"ignoré : {event}"
    details = body.get("transactionDetails") or {}
    ref = details.get("reference") or ""
    if body.get("transactionType", "payment") != "payment" or not ref:
        return "ignoré : pas un paiement MaxQuiz"
    sub = Subscription.objects.filter(provider="jeko", payment_ref=ref).select_related("membership").first()
    if not sub:
        return f"référence inconnue : {ref}"
    status = str(body.get("status", "")).lower()
    if status != "success":
        if status == "error":
            mark_failed(sub, "Paiement refusé")
        return f"{ref} : {status}"
    amount = (body.get("amount") or {}).get("amount")
    if not amount_ok(sub, amount):
        hold(sub, amount, "webhook")
        return f"{ref} : montant à vérifier"
    confirm(sub, "webhook", body.get("id", ""))
    return f"{ref} : activé"
