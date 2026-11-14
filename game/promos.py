"""Codes promo sur les abonnements : vérification et calcul du prix remisé.

Un code « consomme » une utilisation dès qu'un abonnement est créé avec lui
(en attente de validation, paiement en ligne en cours ou validé). Un paiement en
ligne échoué ou un paiement refusé rend l'utilisation.
"""
import re
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from .models import CodePromo, Subscription

STATUTS_QUI_COMPTENT = ("pending", "active")


def clean(raw):
    return re.sub(r"[^A-Za-z0-9]", "", str(raw or "")).upper()[:30]


def _uses(qs):
    """Utilisations qui comptent : validées, en attente, ou paiement en ligne commencé il y a moins de 2 h."""
    recent = timezone.now() - timedelta(hours=2)
    return qs.filter(Q(status__in=STATUTS_QUI_COMPTENT) | Q(status="initiated", created_at__gte=recent))


def check(raw_code, space, membership, plan_code=None):
    """Renvoie (code promo, None) si le code s'applique, sinon (None, message pour l'élève)."""
    code = clean(raw_code)
    if not code:
        return None, None
    promo = CodePromo.objects.filter(code=code).first()
    if not promo or not promo.active:
        return None, "Ce code promo n'existe pas ou n'est plus actif."
    if promo.space_id and promo.space_id != space.id:
        return None, "Ce code promo n'est pas valable ici."
    if not promo.space_id and space.kind != "catalog":
        return None, "Ce code promo n'est valable que sur MaxQuiz École."
    today = timezone.localdate()
    if promo.starts_on and today < promo.starts_on:
        return None, f"Ce code promo sera valable à partir du {promo.starts_on:%d/%m/%Y}."
    if promo.ends_on and today > promo.ends_on:
        return None, "Ce code promo a expiré."
    if promo.max_uses and _uses(promo.subscriptions.all()).count() >= promo.max_uses:
        return None, "Ce code promo a déjà été utilisé." if promo.max_uses == 1 else "Ce code promo est épuisé."
    if membership is not None:
        mine = _uses(promo.subscriptions.filter(membership__player_id=membership.player_id))
        if promo.max_per_player and mine.count() >= promo.max_per_player:
            return None, "Tu as déjà utilisé ce code promo."
        if promo.first_only and Subscription.objects.filter(
                membership__player_id=membership.player_id, membership__space=space, status="active").exists():
            return None, "Ce code promo est réservé à un premier abonnement."
    if plan_code and plan_code not in promo.plans():
        return None, "Ce code promo ne s'applique pas à cette formule."
    return promo, None


def discounted(price, promo):
    if not promo:
        return price
    return max(0, round(price * (100 - promo.percent) / 100))


def apply_to_plans(plans, promo):
    """Ajoute à chaque formule le prix d'origine et le prix remisé (si le code s'y applique)."""
    out = []
    for p in plans:
        q = dict(p, list_price=p["price"], promo=False)
        if promo and p["code"] in promo.plans():
            q["price"], q["promo"] = discounted(p["price"], promo), True
        out.append(q)
    return out
