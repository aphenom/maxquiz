"""Rappels de séances, d'échéances d'abonnement et mission du jour (à lancer toutes les 10 min)."""
from django.core.management.base import BaseCommand

from game.reminders import run_reminders


class Command(BaseCommand):
    help = "Envoie les rappels de séances (30 min avant) et de fin d'abonnement (3 jours avant)."

    def handle(self, *args, **opts):
        from game.engagement import envoyer_rappels_missions
        res = run_reminders()
        missions = envoyer_rappels_missions()
        self.stdout.write(self.style.SUCCESS(f"{res['sessions']} séance(s), {res['subscriptions']} abonnement(s), "
                                             f"{missions} mission(s) du jour rappelé(s)."))
