"""Vérifie auprès de Jèko les paiements en ligne restés « en cours » (un paiement échoué
n'envoie pas de webhook, et un webhook peut se perdre). À lancer toutes les 10 minutes :
  */10 * * * *  maxquiz jeko_verifier
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from game import jeko
from game.models import Subscription


class Command(BaseCommand):
    help = "Met à jour les paiements Jèko en cours (activés, échoués ou abandonnés)."

    def handle(self, **opts):
        if not jeko.enabled():
            self.stdout.write("Jèko n'est pas configuré.")
            return
        now = timezone.now()
        pending = Subscription.objects.filter(provider="jeko", status="initiated",
                                              created_at__lte=now - timedelta(minutes=2))
        done = {"success": 0, "failed": 0, "pending": 0, "abandoned": 0, "errors": 0}
        for sub in pending.select_related("membership__space", "membership__player"):
            try:
                status = jeko.refresh(sub)
            except jeko.JekoError:
                done["errors"] += 1
                continue
            if status == "success":
                done["success"] += 1
            elif status in ("error", "failed", "expired", "cancelled", "canceled"):
                done["failed"] += 1
            elif sub.created_at < now - timedelta(hours=24):
                jeko.mark_failed(sub, "Abandonné (pas de paiement en 24 h)")
                done["abandoned"] += 1
            else:
                done["pending"] += 1
        self.stdout.write(", ".join(f"{k} : {v}" for k, v in done.items()))
