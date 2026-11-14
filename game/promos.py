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


# --- Parrainage (influenceurs, partenaires) ------------------------------------------
SESSION_REF = "promo_parrain"


def code_parrain_valide(code):
    """Code de parrainage utilisable aujourd'hui (actif, dans sa période), ou None."""
    promo = CodePromo.objects.filter(code=clean(code), active=True).first()
    today = timezone.localdate()
    if not promo or (promo.starts_on and today < promo.starts_on) or (promo.ends_on and today > promo.ends_on):
        return None
    return promo


def rattacher(request, player):
    """Rattache l'élève au code par lequel il est arrivé (lien /p/CODE), une seule fois,
    et seulement s'il n'est pas déjà abonné."""
    code = request.session.get(SESSION_REF) if hasattr(request, "session") else None
    if not (code and player) or player.promo_parrain_id:
        return None
    promo = code_parrain_valide(code)
    if not promo or Subscription.objects.filter(membership__player=player, status="active").exists():
        return None
    from .models import Player
    Player.objects.filter(pk=player.pk, promo_parrain__isnull=True).update(
        promo_parrain=promo, promo_parrain_at=timezone.now())
    player.promo_parrain, player.promo_parrain_at = promo, timezone.now()
    return promo


def source_lien(promo):
    return f"promo-{promo.code.lower()}"


def rapport_partenaires(debut=None, fin=None):
    """Une ligne par code de parrainage : visites, inscrits, payants, encaissé, commission."""
    from decimal import Decimal

    from django.db.models import Sum

    from .models import Player, Visite
    rows = []
    for promo in CodePromo.objects.exclude(partenaire="").order_by("partenaire", "code"):
        visites = Visite.objects.filter(source=source_lien(promo))
        inscrits = Player.objects.filter(promo_parrain=promo)
        payes = promo.subscriptions.filter(status="active")
        if debut:
            visites, inscrits = visites.filter(day__gte=debut), inscrits.filter(promo_parrain_at__date__gte=debut)
            payes = payes.filter(validated_at__date__gte=debut)
        if fin:
            visites, inscrits = visites.filter(day__lte=fin), inscrits.filter(promo_parrain_at__date__lte=fin)
            payes = payes.filter(validated_at__date__lte=fin)
        encaisse = payes.aggregate(t=Sum("amount"))["t"] or 0
        commission = (Decimal(encaisse) * promo.commission / 100).quantize(Decimal("1"))
        nb_visiteurs = visites.values("day", "visiteur").distinct().count()
        nb_inscrits = inscrits.count()
        rows.append(dict(promo=promo, visiteurs=nb_visiteurs, inscrits=nb_inscrits, payants=payes.count(),
                         encaisse=encaisse, commission=int(commission),
                         conversion=round(100 * payes.count() / nb_inscrits) if nb_inscrits else 0))
    totals = {k: sum(r[k] for r in rows) for k in ("visiteurs", "inscrits", "payants", "encaisse", "commission")}
    return rows, totals
