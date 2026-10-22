"""Génère les clés VAPID des notifications Web Push (une seule fois, à garder)."""
from django.core.management.base import BaseCommand

from game.push import generate_vapid_keys


class Command(BaseCommand):
    help = "Affiche une paire de clés VAPID à mettre dans les variables d'environnement."

    def handle(self, *args, **opts):
        priv, pub = generate_vapid_keys()
        self.stdout.write("À ajouter dans les variables d'environnement de l'hébergement :\n")
        self.stdout.write(f"VAPID_PRIVATE_KEY={priv}")
        self.stdout.write(f"VAPID_PUBLIC_KEY={pub}")
        self.stdout.write("VAPID_SUBJECT=mailto:contact@votre-domaine.ci")
        self.stdout.write(self.style.WARNING(
            "Gardez ces clés : en changer obligera chaque appareil à se réabonner."))
