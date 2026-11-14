"""Génère des codes promo uniques (une utilisation chacun), par exemple pour une école,
un concours ou des ambassadeurs, et les écrit dans un CSV à distribuer.

  maxquiz generer_codes_promo --nombre 50 --taux 50 --prefixe BEPC --fin 2026-12-31 \\
          --formules monthly,yearly --note "Collège X" --csv codes-bepc.csv
"""
import csv
import secrets
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from game.models import CodePromo

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"            # sans 0/O ni 1/I, faciles à recopier


class Command(BaseCommand):
    help = "Génère des codes promo à usage unique et les exporte en CSV."

    def add_arguments(self, parser):
        parser.add_argument("--nombre", type=int, required=True)
        parser.add_argument("--taux", type=int, required=True, help="réduction en %% (1 à 100)")
        parser.add_argument("--prefixe", default="MQ")
        parser.add_argument("--formules", default="monthly,quarterly,yearly")
        parser.add_argument("--debut", default="", help="AAAA-MM-JJ")
        parser.add_argument("--fin", default="", help="AAAA-MM-JJ (inclus)")
        parser.add_argument("--premier", action="store_true", help="réservé à un premier abonnement")
        parser.add_argument("--note", default="")
        parser.add_argument("--csv", dest="fichier", default="codes-promo.csv")

    def handle(self, nombre, taux, prefixe, formules, debut, fin, premier, note, fichier, **opts):
        if not (1 <= taux <= 100) or not (1 <= nombre <= 5000):
            raise CommandError("Taux de 1 à 100 et nombre de 1 à 5000.")
        plans = {p.strip() for p in formules.split(",")}
        if not plans <= {"monthly", "quarterly", "yearly"}:
            raise CommandError("Formules possibles : monthly, quarterly, yearly.")
        parse = lambda s: date.fromisoformat(s) if s else None
        created = []
        while len(created) < nombre:
            code = (prefixe.upper()[:12] + "-" + "".join(secrets.choice(ALPHABET) for _ in range(6)))
            code = code.replace("-", "")
            if CodePromo.objects.filter(code=code).exists():
                continue
            created.append(CodePromo.objects.create(
                code=code, percent=taux, monthly="monthly" in plans, quarterly="quarterly" in plans,
                yearly="yearly" in plans, max_uses=1, max_per_player=1, first_only=premier,
                starts_on=parse(debut), ends_on=parse(fin), note=note[:120]))
        with open(fichier, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["code", "reduction", "valable_jusqu_au", "note"])
            for c in created:
                w.writerow([c.code, f"{c.percent} %", c.ends_on.strftime("%d/%m/%Y") if c.ends_on else "", c.note])
        self.stdout.write(self.style.SUCCESS(f"{len(created)} code(s) créé(s), liste dans {fichier}"))
