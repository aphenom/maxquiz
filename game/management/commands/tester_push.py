"""Diagnostic des notifications push d'un élève : appareils enregistrés et envoi de test.

    maxquiz tester_push 0707000001
"""
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Liste les appareils push d'un numéro et leur envoie une notification de test."

    def add_arguments(self, parser):
        parser.add_argument("phone")

    def handle(self, *args, **opts):
        from game import push
        from game.models import Player, PushDevice
        player = Player.objects.filter(phone=opts["phone"].strip()).first()
        if not player:
            raise CommandError("Aucun élève avec ce numéro.")
        if not push.webpush_configured():
            self.stdout.write(self.style.ERROR("Clés VAPID absentes : les notifications ne peuvent pas partir."))
        devices = list(PushDevice.objects.filter(player=player).order_by("-created_at"))
        if not devices:
            self.stdout.write("Aucun appareil : l'élève n'a jamais accepté les notifications.")
            return
        message = {"title": "Test MaxQuiz", "body": "Si tu lis ceci, les notifications marchent.",
                   "url": "/", "tag": "test"}
        for d in devices:
            where = d.user_agent[:60] or "?"
            if not d.active:
                self.stdout.write(f"- appareil {d.id} ({where}) : désactivé (abonnement expiré)")
                continue
            try:
                status = push.send_webpush(d, message) if d.kind == "webpush" else push.send_fcm(d, message)
            except Exception as exc:                       # noqa: BLE001
                self.stdout.write(self.style.ERROR(f"- appareil {d.id} ({where}) : erreur {exc}"))
                continue
            verdict = "envoyé" if 200 <= status < 300 else (
                "expiré : l'élève doit réactiver les notifications" if status in (404, 410) else "refusé")
            if status in (404, 410):
                PushDevice.objects.filter(id=d.id).update(active=False)
            self.stdout.write(f"- appareil {d.id} ({where}) : HTTP {status}, {verdict}")
