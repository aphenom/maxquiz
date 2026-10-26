"""Règles d'accès et d'abonnement des élèves (accompagnement scolaire).

Tout ce qui décide « cet élève peut-il jouer ? », « quelles dates couvre ce
paiement ? » et « combien doit-on reverser à l'établissement ? » est ici, pour
que les vues n'aient qu'un appel à faire.
"""
import calendar
from datetime import date, timedelta

from django.utils import timezone

from .models import Membership, Subscription


def add_months(day, months):
    """Même jour, N mois plus tard (borné à la fin du mois : 31/01 + 1 = 28/02)."""
    month = day.month - 1 + months
    year = day.year + month // 12
    month = month % 12 + 1
    last = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last))


def plan_prices(space):
    """Formules proposées par l'espace, dans l'ordre d'affichage (prix 0 = non proposée)."""
    plans = [("monthly", "Mensuel", space.price_monthly, "1 mois"),
             ("quarterly", "Trimestriel", space.price_quarterly, "3 mois"),
             ("yearly", "Annuel", space.price_yearly, "jusqu'à la fin de l'année scolaire")]
    return [{"code": c, "label": l, "price": p, "duration": d} for c, l, p, d in plans if p]


def current_membership(space, player):
    """Fiche membre du joueur dans cet espace : celle de la licence active en
    priorité, sinon la plus récente."""
    if not player:
        return None
    memberships = list(Membership.objects.filter(space=space, player=player)
                       .select_related("license").order_by("-created_at"))
    if not memberships:
        return None
    active = [m for m in memberships if m.license and m.license.active]
    return (active or memberships)[0]


def current_subscription(membership, day=None):
    if not membership:
        return None
    day = day or timezone.localdate()
    return (membership.subscriptions.filter(status="active", start_date__lte=day, end_date__gte=day)
            .order_by("-end_date").first())


def trial_end(space, membership):
    """Dernier jour de l'essai gratuit individuel de cet élève (réglé dans
    l'administration : activé ou non, durée en jours), ou None."""
    if not (space.trial_enabled and space.trial_days and membership):
        return None
    start = timezone.localtime(membership.created_at).date()
    return start + timedelta(days=space.trial_days - 1)


def access_status(space, player, day=None):
    """Décide si le joueur peut lancer un quiz de l'espace.

    Renvoie un dict : ok (bool), reason (code), message (texte pour l'élève),
    membership, subscription, trial (bool : accès grâce à la période gratuite).
    Un espace qui n'active ni members_only ni subscription_required garde son
    comportement d'avant (tout le monde joue).
    """
    day = day or timezone.localdate()
    m = current_membership(space, player)
    res = {"ok": True, "reason": "open", "message": "", "membership": m,
           "subscription": None, "trial": False}
    if not (space.members_only or space.subscription_required):
        return res
    if not m and space.kind == "catalog":
        res.update(ok=False, reason="not_member", message="Choisis ta classe pour commencer.")
        return res
    if not m:
        res.update(ok=False, reason="not_member",
                   message="Ce quiz est réservé aux élèves inscrits par l'établissement. "
                           "Connecte-toi avec le numéro enregistré par ton école, "
                           "ou demande à ton professeur principal de t'ajouter.")
        return res
    if not space.subscription_required:
        res["reason"] = "member"
        return res
    sub = current_subscription(m, day)
    if sub:
        res.update(reason="subscribed", subscription=sub)
        return res
    if space.free_until and day <= space.free_until:
        res.update(reason="trial", trial=True, trial_end=space.free_until)
        return res
    end = trial_end(space, m)
    if end and day <= end:
        res.update(reason="trial", trial=True, trial_end=end, trial_days_left=(end - day).days + 1)
        return res
    if space.kind == "school":
        # Élève inscrit seul sur MaxQuiz École puis rattaché à son école :
        # son abonnement (ou son essai) MaxQuiz École lui ouvre aussi l'école.
        from .models import Space
        catalog = Space.objects.filter(kind="catalog", active=True).first()
        if catalog and catalog.id != space.id:
            via = access_status(catalog, player, day)
            if via["ok"]:
                via.update(membership=m, via_catalog=True)
                return via
    pending = m.subscriptions.filter(status="pending").exists()
    res.update(ok=False, reason="pending" if pending else "no_subscription",
               message=("Ton paiement est en cours de vérification. L'accès s'ouvre dès sa validation."
                        if pending else
                        "Ton abonnement n'est pas actif. Abonne-toi pour continuer à t'entraîner."))
    return res


def compute_period(subscription, day=None):
    """Dates couvertes par un paiement validé aujourd'hui.

    Début : aujourd'hui, ou le lendemain du dernier abonnement validé encore en
    cours (un réabonnement anticipé ne fait pas perdre de jours). Fin : début +
    durée de la formule, la veille du même jour ; l'annuel s'arrête à la fin de
    la licence de l'élève (l'année scolaire) quand elle existe.
    """
    day = day or timezone.localdate()
    m = subscription.membership
    last = (m.subscriptions.filter(status="active", end_date__gte=day)
            .exclude(id=subscription.id).order_by("-end_date").first())
    start = last.end_date + timedelta(days=1) if last else day
    if subscription.plan == "yearly" and m.license and m.license.end_date > start:
        end = m.license.end_date
    else:
        end = add_months(start, Subscription.PLAN_MONTHS[subscription.plan]) - timedelta(days=1)
    return start, end


def validate(subscription, day=None):
    start, end = compute_period(subscription, day)
    subscription.start_date, subscription.end_date = start, end
    subscription.status = "active"
    subscription.validated_at = timezone.now()
    subscription.save(update_fields=["start_date", "end_date", "status", "validated_at"])
    from .meta import track_purchase
    track_purchase(subscription)          # MaxQuiz École : achat annoncé à Meta (si la mesure est active)
    return subscription


def months_between(first, last):
    """Liste des (année, mois) de first à last inclus."""
    out, y, mth = [], first.year, first.month
    while (y, mth) <= (last.year, last.month):
        out.append((y, mth))
        mth += 1
        if mth == 13:
            y, mth = y + 1, 1
    return out


def share_report(space, up_to=None):
    """Part due à l'établissement, mois par mois : nombre d'élèves ayant un
    abonnement validé couvrant au moins un jour du mois × part mensuelle.
    Un élève ne compte qu'une fois par mois, même avec deux abonnements."""
    up_to = up_to or timezone.localdate()
    subs = list(Subscription.objects.filter(membership__space=space, status="active",
                                            start_date__isnull=False)
                .select_related("membership"))
    if not subs:
        return []
    first = min(s.start_date for s in subs)
    rows = []
    for y, mth in months_between(first, up_to):
        m_start = date(y, mth, 1)
        m_end = date(y, mth, calendar.monthrange(y, mth)[1])
        students = {s.membership_id for s in subs if s.start_date <= m_end and s.end_date >= m_start}
        cash = sum(s.amount for s in subs
                   if s.validated_at and m_start <= timezone.localtime(s.validated_at).date() <= m_end)
        rows.append({"year": y, "month": mth, "label": f"{mth:02d}/{y}",
                     "students": len(students),
                     "share": len(students) * space.school_share_per_month,
                     "collected": cash})
    return rows
