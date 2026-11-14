"""Envoie un SMS de test, pour vérifier la configuration et la réception par opérateur.

  maxquiz tester_sms 0707070707 0505050505 0101010101
Attends quelques minutes, puis regarde Admin > SMS envoyés (statut de l'accusé de réception).
"""
from django.core.management.base import BaseCommand

from game import sms
from game.views import normalize_phone


class Command(BaseCommand):
    help = "Envoie un SMS de test à un ou plusieurs numéros."

    def add_arguments(self, parser):
        parser.add_argument("numeros", nargs="+")
        parser.add_argument("--texte", default="MaxQuiz : SMS de test. Si tu le recois, l'envoi fonctionne.")

    def handle(self, numeros, texte, **opts):
        self.stdout.write(f"Prestataire : {sms.provider()}")
        for raw in numeros:
            phone = normalize_phone(raw)
            if not phone:
                self.stderr.write(f"{raw} : numéro invalide")
                continue
            try:
                row = sms.envoyer(phone, texte, kind="test")
                self.stdout.write(self.style.SUCCESS(
                    f"{phone} ({sms.operateur(phone)}) : envoyé, nom d'expéditeur « {row.sender_name or 'par défaut'} », "
                    f"id {row.resource_id or '-'}"))
            except sms.SmsError as exc:
                self.stderr.write(f"{phone} ({sms.operateur(phone)}) : échec : {exc}")
