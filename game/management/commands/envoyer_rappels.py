"""Rappels de séances et d'échéances d'abonnement (à lancer toutes les 10 min)."""
from django.core.management.base import BaseCommand

from game.reminders import run_reminders


class Command(BaseCommand):
    help = "Envoie les rappels de séances (30 min avant) et de fin d'abonnement (3 jours avant)."

    def handle(self, *args, **opts):
        res = run_reminders()
        self.stdout.write(self.style.SUCCESS(f"{res['sessions']} séance(s), {res['subscriptions']} abonnement(s) rappelé(s)."))
