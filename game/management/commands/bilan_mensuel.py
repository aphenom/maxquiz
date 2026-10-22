"""Bilan mensuel des parents : un message par élève, exporté en CSV (à envoyer
par WhatsApp ou par un fournisseur de SMS).

Usage : python manage.py bilan_mensuel college-la-reussite --mois 2026-11 [--sortie bilans.csv]
"""
import csv
import sys
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from game.models import Space
from game.school import monthly_report


class Command(BaseCommand):
    help = "Génère le bilan mensuel des parents d'un espace (CSV)."

    def add_arguments(self, parser):
        parser.add_argument("space")
        parser.add_argument("--mois", help="AAAA-MM (défaut : mois précédent)")
        parser.add_argument("--sortie", help="fichier CSV (défaut : écran)")

    def handle(self, space, mois=None, sortie=None, **opts):
        sp = Space.objects.filter(slug=space).first()
        if not sp:
            raise CommandError(f"Espace introuvable : {space}")
        if mois:
            year, month = (int(x) for x in mois.split("-"))
        else:
            prev = timezone.localdate().replace(day=1) - timedelta(days=1)
            year, month = prev.year, prev.month
        rows = monthly_report(sp, year, month)
        out = open(sortie, "w", newline="", encoding="utf-8-sig") if sortie else sys.stdout
        w = csv.writer(out, delimiter=";")
        w.writerow(["eleve", "matricule", "telephone_parent", "quiz", "reussite", "message"])
        for r in rows:
            w.writerow([r["member"].full_name, r["member"].external_ref, r["parent_phone"],
                        r["quizzes"], "" if r["pct"] is None else r["pct"], r["message"]])
        if sortie:
            out.close()
            self.stderr.write(self.style.SUCCESS(
                f"{len(rows)} bilan(s), dont {sum(1 for r in rows if r['parent_phone'])} avec téléphone parent."))
