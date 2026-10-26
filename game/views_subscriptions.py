"""Abonnements des élèves : page famille (choisir une formule, déclarer un
paiement mobile money), et pages du tableau de bord (valider les paiements,
suivre les échéances, relevé de la part de l'établissement)."""
from datetime import timedelta

import openpyxl
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from openpyxl.styles import Font

from django.urls import reverse

from .push import direction_of, notify
from .models import Subscription
from .subscriptions import (access_status, current_membership, plan_prices,
                            share_report, validate)
from .views import _dashboard_gate, _log_action, _player, _space, normalize_phone


def space_subscribe(request, slug):
    """Page « Mon abonnement » d'un élève dans un espace."""
    space = _space(slug)
    player = _player(request)
    if not player:
        return redirect(f"/compte/connexion/?space={space.slug}")
    access = access_status(space, player)
    membership = access["membership"] or current_membership(space, player)
    plans = plan_prices(space)

    if request.method == "POST" and membership:
        plan = request.POST.get("plan", "")
        ref = request.POST.get("payment_ref", "").strip()[:60]
        chosen = next((p for p in plans if p["code"] == plan), None)
        if not chosen or len(ref) < 4:
            messages.error(request, "Choisis une formule et saisis la référence de la transaction "
                                    "(au moins 4 caractères).")
        else:
            try:
                with transaction.atomic():  # point de sauvegarde : un doublon ne casse pas la requête
                    Subscription.objects.create(
                        membership=membership, plan=plan, amount=chosen["price"], payment_ref=ref,
                        payer_phone=normalize_phone(request.POST.get("payer_phone", "")) or "")
                notify(teachers=direction_of(space), kind="payment_pending",
                       title="Paiement d'abonnement à vérifier",
                       body=f"{membership.full_name} · {chosen['price']} F · réf. {ref}",
                       url=reverse("dashboard_subscriptions", args=[space.slug]))
                messages.success(request, "Paiement déclaré. Ton accès s'ouvrira dès sa vérification "
                                          "par l'établissement.")
            except IntegrityError:
                messages.error(request, "Cette référence de transaction a déjà été déclarée.")
        return redirect("space_subscribe", slug=slug)

    if space.kind == "catalog" and membership and not (access.get("subscription")):
        from . import meta
        meta.track(request, "InitiateCheckout", getattr(player, "attribution", None))
    history = list(membership.subscriptions.all()[:10]) if membership else []
    return render(request, "game/space_subscribe.html", {
        "space": space, "player": player, "access": access, "membership": membership,
        "plans": plans, "history": history, "tab": "home",
    })


def dashboard_subscriptions(request, slug):
    """Validation des paiements déclarés et suivi des abonnements."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    if request.method == "POST":
        sub = get_object_or_404(Subscription, id=request.POST.get("sub_id"), membership__space=space)
        action = request.POST.get("action")
        if action == "validate" and sub.status == "pending":
            validate(sub)
            _log_action(space, "update", sub,
                        f"Paiement validé ({sub.amount} F, réf. {sub.payment_ref}) : "
                        f"du {sub.start_date:%d/%m/%Y} au {sub.end_date:%d/%m/%Y}")
            notify(players=[sub.membership.player], kind="sub_ok", title="Abonnement activé",
                   body=f"Accès complet jusqu'au {sub.end_date:%d/%m/%Y}. Bonnes révisions !",
                   url=reverse("space_home", args=[space.slug]))
            messages.success(request, f"Abonnement de {sub.membership.full_name} validé jusqu'au "
                                      f"{sub.end_date:%d/%m/%Y}.")
        elif action == "reject" and sub.status == "pending":
            sub.status = "rejected"
            sub.note = request.POST.get("note", "").strip()[:200]
            sub.save(update_fields=["status", "note"])
            _log_action(space, "update", sub, f"Paiement refusé (réf. {sub.payment_ref}) {sub.note}")
            notify(players=[sub.membership.player], kind="sub_refused", title="Paiement non validé",
                   body="Vérifie la référence de la transaction ou contacte l'école.",
                   url=reverse("space_subscribe", args=[space.slug]))
            messages.success(request, f"Paiement de {sub.membership.full_name} refusé.")
        return redirect("dashboard_subscriptions", slug=slug)

    today = timezone.localdate()
    base = Subscription.objects.filter(membership__space=space).select_related("membership")
    active = list(base.filter(status="active", start_date__lte=today, end_date__gte=today)
                  .order_by("end_date"))
    return render(request, "game/dashboard_subscriptions.html", {
        "space": space,
        "pending": list(base.filter(status="pending").order_by("created_at")),
        "expiring": [s for s in active if s.end_date <= today + timedelta(days=7)],
        "active": active,
        "members_total": space.members.count(),
        "trial_active": bool(space.free_until and today <= space.free_until),
        "today": today,
    })


def dashboard_shares(request, slug):
    """Relevé mensuel de la part de l'établissement, avec export Excel."""
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    rows = share_report(space)
    if request.GET.get("export") == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reversements"
        ws.append([f"{space.name} : part de l'établissement "
                   f"({space.school_share_per_month} F par élève abonné et par mois)"])
        ws.append(["Mois", "Élèves abonnés", "Part due (F CFA)", "Encaissé par MQ ce mois (F CFA)"])
        for c in ws[2]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append([r["label"], r["students"], r["share"], r["collected"]])
        ws.append(["Total", "", sum(r["share"] for r in rows), sum(r["collected"] for r in rows)])
        for col, width in zip("ABCD", (12, 16, 18, 30)):
            ws.column_dimensions[col].width = width
        resp = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        resp["Content-Disposition"] = f'attachment; filename="reversements-{space.slug}.xlsx"'
        wb.save(resp)
        return resp
    return render(request, "game/dashboard_shares.html", {
        "space": space, "rows": rows,
        "total_share": sum(r["share"] for r in rows),
        "total_collected": sum(r["collected"] for r in rows),
    })


def ads_report(space, since=None):
    """Résultats par campagne et par pub : inscrits, payants, chiffre d'affaires.
    Calculé sur nos propres données (inscriptions et paiements validés), pas sur Meta."""
    from .models import AdAttribution, Membership
    members = Membership.objects.filter(space=space).select_related("player")
    if since:
        members = members.filter(created_at__gte=since)
    members = list(members)
    attrib = {a.player_id: a for a in AdAttribution.objects.filter(player_id__in=[m.player_id for m in members if m.player_id])}
    paid = {}
    for s in Subscription.objects.filter(membership__in=members, status="active"):
        paid[s.membership_id] = paid.get(s.membership_id, 0) + s.amount
    rows = {}
    for m in members:
        a = attrib.get(m.player_id)
        campaign = (a.campaign_label() if a else "") or "Sans pub (direct, bouche-à-oreille, école)"
        ad = (a.utm_content if a else "") or "—"
        r = rows.setdefault((campaign, ad), {"campaign": campaign, "ad": ad, "signups": 0, "paying": 0, "revenue": 0})
        r["signups"] += 1
        if m.id in paid:
            r["paying"] += 1
            r["revenue"] += paid[m.id]
    out = sorted(rows.values(), key=lambda r: (-r["revenue"], -r["signups"]))
    for r in out:
        r["rate"] = round(100 * r["paying"] / r["signups"]) if r["signups"] else 0
    return out


def dashboard_ads(request, slug):
    """Tableau « Résultats des pubs » de l'espace MaxQuiz École."""
    from django.conf import settings as dj_settings
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    period = request.GET.get("p", "30")
    days = {"7": 7, "30": 30, "90": 90}.get(period)
    since = timezone.now() - timedelta(days=days) if days else None
    rows = ads_report(space, since)
    return render(request, "game/dashboard_ads.html", {
        "space": space, "rows": rows, "period": period if days else "all",
        "totals": {k: sum(r[k] for r in rows) for k in ("signups", "paying", "revenue")},
        "pixel_on": bool(dj_settings.META_PIXEL_ID), "capi_on": bool(dj_settings.META_CAPI_TOKEN),
    })
