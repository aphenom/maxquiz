"""Notifications planifiées : rappel avant une séance, fin d'abonnement proche.
Lancé toutes les 10 minutes (commande envoyer_rappels ou /cron/rappels/)."""
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from .models import LiveSession, Subscription
from .push import notify

REMIND_BEFORE = timedelta(minutes=30)
EXPIRY_NOTICE = timedelta(days=3)


def run_reminders(now=None):
    now = now or timezone.now()
    sessions_done, subs_done = 0, 0
    soon = LiveSession.objects.filter(cancelled=False, reminder_sent_at__isnull=True,
                                      starts_at__gt=now, starts_at__lte=now + REMIND_BEFORE)
    for s in soon.select_related("space"):
        players = [b.membership.player for b in s.bookings.filter(status="active", kind="live")
                   .select_related("membership__player") if b.membership.player_id]
        if s.price_live == 0:   # séance gratuite : tous les élèves concernés
            from .push import students_of
            players = students_of(s.space, s.sub_category)
        minutes = max(1, int((s.starts_at - now).total_seconds() // 60))
        notify(players=players, kind="session_soon", title=f"Ta séance commence dans {minutes} min",
               body=s.title, url=reverse("session_detail", args=[s.space.slug, s.id]))
        LiveSession.objects.filter(id=s.id).update(reminder_sent_at=now)
        sessions_done += 1
    today = timezone.localdate()
    ending = Subscription.objects.filter(status="active", expiry_notified_at__isnull=True,
                                         end_date__gte=today, end_date__lte=today + EXPIRY_NOTICE)
    for sub in ending.select_related("membership__player", "membership__space"):
        if sub.membership.player_id:
            notify(players=[sub.membership.player], kind="sub_ending",
                   title="Ton abonnement se termine bientôt",
                   body=f"Il prend fin le {sub.end_date:%d/%m}. Renouvelle-le pour garder l'accès aux cours et aux quiz.",
                   url=reverse("space_subscribe", args=[sub.membership.space.slug]))
        Subscription.objects.filter(id=sub.id).update(expiry_notified_at=now)
        subs_done += 1
    return {"sessions": sessions_done, "subscriptions": subs_done}
