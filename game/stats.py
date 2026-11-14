"""Statistiques de fréquentation de MaxQuiz École, mesurées par le site lui-même.

- Pages vues et visiteurs uniques du jour (identifiant anonyme : empreinte IP + navigateur
  salée avec la date, impossible à relier d'un jour à l'autre ; aucun cookie).
- Téléchargements de l'APK (lien /telecharger/maxquiz.apk) et installations depuis le navigateur.
- Inscrits, abonnés, actifs : calculés à partir des données de l'application.
"""
import hashlib
import re
from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

BOTS = re.compile(r"bot|crawl|spider|slurp|facebookexternalhit|preview|monitor|curl|wget|python|headless", re.I)
IGNORE = ("/admin/", "/api/", "/sms/", "/static/", "/media/", "/sw.js", "/manifest.webmanifest", "/hors-ligne/",
          "/.well-known/", "/favicon", "/robots.txt", "/paiement/jeko/webhook/", "/stats/", "/telecharger/")


def _ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or ""


def visiteur(request, day=None):
    day = day or timezone.localdate()
    raw = f"{settings.SECRET_KEY}|{day.isoformat()}|{_ip(request)}|{request.META.get('HTTP_USER_AGENT', '')}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def appareil(ua):
    if re.search(r"Android", ua):
        return "android"
    if re.search(r"iPhone|iPad|iPod", ua):
        return "ios"
    if re.search(r"Windows|Macintosh|Linux|CrOS", ua):
        return "ordinateur"
    return "autre"


def provenance(request):
    """utm_source, sinon le site d'où vient le visiteur (facebook, google, whatsapp…), sinon « direct »."""
    utm = request.GET.get("utm_source", "").strip().lower()
    if utm:
        return utm[:60]
    if request.GET.get("fbclid"):
        return "facebook (pub)"
    ref = request.META.get("HTTP_REFERER", "")
    if ref.startswith("android-app://"):
        return "application"
    host = (urlparse(ref).hostname or "").lower()
    if not host or host.endswith(request.get_host().split(":")[0]):
        return ""
    for name in ("facebook", "instagram", "whatsapp", "google", "tiktok", "youtube", "bing", "twitter", "linkedin"):
        if name in host or (name == "facebook" and host in ("fb.com", "l.facebook.com", "lm.facebook.com")):
            return name
    return host.removeprefix("www.")[:60]


def page_cle(path):
    """Regroupe les adresses par type de page (/e/maxquiz/cours/12/ → /e/…/cours/…)."""
    p = re.sub(r"/\d+(?=/|$)", "/…", path)
    p = re.sub(r"^/e/[^/]+/q/[^/]+/", "/e/…/q/…/", p)
    p = re.sub(r"^/e/[^/]+/", "/e/…/", p)
    return p[:120]


def noter(request, response):
    """Enregistre une page vue (pages HTML publiques et élèves, hors robots et administration)."""
    from .models import Visite
    if request.method != "GET" or response.status_code != 200 or getattr(request, "product", "ecole") != "ecole":
        return
    if not response.get("Content-Type", "").startswith("text/html"):
        return
    path = request.path
    if path.startswith(IGNORE) or "/tableau-de-bord" in path or "/ressources/" in path:
        return
    ua = request.META.get("HTTP_USER_AGENT", "")
    if not ua or BOTS.search(ua):
        return
    pid = request.session.get("verified_player_id") if hasattr(request, "session") else None
    Visite.objects.create(visiteur=visiteur(request), player_id=pid, page=page_cle(path), source=provenance(request),
                          device=appareil(ua), in_app=bool(getattr(request, "in_app", False)))


def noter_telechargement(request, kind):
    from .models import Telechargement
    pid = request.session.get("verified_player_id") if hasattr(request, "session") else None
    v = visiteur(request)
    today = timezone.localdate()
    if Telechargement.objects.filter(kind=kind, day=today, visiteur=v).exists():
        return False                                    # un même téléphone ne compte qu'une fois par jour
    src = provenance(request) or (request.GET.get("depuis", "") or "")[:60]
    Telechargement.objects.create(kind=kind, visiteur=v, player_id=pid, source=src)
    return True


# --- Rapport ---------------------------------------------------------------------------
def rapport(space, jours=30, today=None):
    from .engagement import jours_actifs_groupes
    from .models import Membership, PushDevice, Subscription, Telechargement, Visite
    today = today or timezone.localdate()
    since = today - timedelta(days=jours - 1)
    v = Visite.objects.filter(day__gte=since)
    visiteurs = v.values("day", "visiteur").distinct().count()
    par_jour = {d["day"]: d for d in v.values("day").annotate(pages=Count("id"), visiteurs=Count("visiteur", distinct=True))}
    dl = Telechargement.objects.filter(day__gte=since)
    dl_jour = {(d["day"], d["kind"]): d["n"] for d in dl.values("day", "kind").annotate(n=Count("id"))}
    members = Membership.objects.filter(space=space, player__isnull=False)
    nouveaux = members.filter(created_at__date__gte=since)
    nouveaux_jour = {d["d"]: d["n"] for d in nouveaux.annotate(d=TruncDate("created_at")).values("d")
                     .annotate(n=Count("id"))}
    rows = []
    for i in range(jours):
        d = since + timedelta(days=i)
        r = par_jour.get(d, {})
        rows.append(dict(day=d, visiteurs=r.get("visiteurs", 0), pages=r.get("pages", 0),
                         inscrits=nouveaux_jour.get(d, 0),
                         apk=dl_jour.get((d, "apk"), 0), pwa=dl_jour.get((d, "pwa"), 0)))
    subs = Subscription.objects.filter(membership__space=space)
    actifs_abonnes = subs.filter(status="active", start_date__lte=today, end_date__gte=today) \
        .values("membership_id").distinct().count()
    revenus = subs.filter(status="active", validated_at__date__gte=since).aggregate(t=Sum("amount"))["t"] or 0
    player_ids = list(members.values_list("player_id", flat=True))

    def top(field, n=8):
        return [dict(label=x[field] or "direct", n=x["n"], pct=round(100 * x["n"] / max(1, visiteurs)))
                for x in v.values(field).annotate(n=Count("visiteur", distinct=True)).order_by("-n")[:n]]

    from .models import SmsEnvoi
    sms_rows = []
    for op, label in SmsEnvoi.OPERATEURS:
        q = SmsEnvoi.objects.filter(created_at__date__gte=since, operateur=op).exclude(provider="console")
        n = q.count()
        if not n:
            continue
        recus = q.filter(status="DeliveredToTerminal").count()
        echecs = q.filter(status__in=("failed", "DeliveryImpossible")).count()
        sms_rows.append(dict(label=label, envoyes=n, recus=recus, echecs=echecs,
                             taux=round(100 * recus / n), sans_nouvelles=n - recus - echecs))
    return dict(
        sms=sms_rows,
        jours=jours, rows=rows,
        max_visiteurs=max([r["visiteurs"] for r in rows] + [1]),
        visiteurs=visiteurs, pages=v.count(),
        apk=dl.filter(kind="apk").count(), pwa=dl.filter(kind="pwa").count(),
        apk_total=Telechargement.objects.filter(kind="apk").count(),
        inscrits_total=members.count(), inscrits=nouveaux.count(),
        abonnes=actifs_abonnes, revenus=revenus,
        actifs_7=len(jours_actifs_groupes(player_ids, today - timedelta(days=6))),
        actifs_30=len(jours_actifs_groupes(player_ids, today - timedelta(days=29))),
        notifs=PushDevice.objects.filter(active=True, player_id__in=player_ids).values("player_id").distinct().count(),
        conversion=round(100 * nouveaux.count() / visiteurs, 1) if visiteurs else 0,
        sources=top("source"),
        appareils=[dict(label=dict(Visite.DEVICES).get(x["device"], x["device"]), n=x["n"],
                        pct=round(100 * x["n"] / max(1, visiteurs)))
                   for x in v.values("device").annotate(n=Count("visiteur", distinct=True)).order_by("-n")],
        dans_appli=v.filter(in_app=True).values("day", "visiteur").distinct().count(),
        pages_top=list(v.values("page").annotate(n=Count("id")).order_by("-n")[:10]),
        classes=list(members.values("category__name").annotate(n=Count("id")).order_by("-n")),
    )
