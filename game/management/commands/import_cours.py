"""Import des cours communs MaxQuiz (fiche de cours + PDF + vidéo) depuis un .xlsx
ou un .csv, avec le même lecteur que import_questions.

Colonnes : niveau;matiere;chapitre;titre;resume;youtube;fiche_pdf;ordre;gratuit
  - chapitre : même nom que le quiz du chapitre (import_questions, colonne
    « thematique ») : c'est ce qui relie une erreur au cours à revoir.
  - fiche_pdf : nom du fichier PDF, cherché dans le dossier --fiches.
  - gratuit : oui / non (cours ouvert sans abonnement, pour faire découvrir).
Un cours déjà présent (même niveau, matière et chapitre et même titre) est mis à
jour : on peut corriger le fichier et le réimporter sans créer de doublon.
Usage :
  python manage.py import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches --dry-run
  python manage.py import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches
"""
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from game.models import Lesson

from .import_questions import _read_rows

YES = {"oui", "o", "yes", "y", "1", "true", "vrai", "x"}


class Command(BaseCommand):
    help = "Importe les cours communs MaxQuiz (fiches, PDF, vidéos) depuis un .xlsx ou un .csv."

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--fiches", default="", help="dossier des fiches PDF")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, path, fiches="", dry_run=False, **opts):
        errors, plan = [], []
        for n, r in enumerate(_read_rows(path), start=2):
            r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
            niveau, matiere, chap = r.get("niveau", ""), r.get("matiere", ""), r.get("chapitre", "")
            title = (r.get("titre") or chap)[:150]
            if not (niveau and matiere and chap):
                errors.append(f"ligne {n} : niveau, matière et chapitre obligatoires")
                continue
            pdf_name, pdf_data = r.get("fiche_pdf", ""), None
            if pdf_name:
                full = os.path.join(fiches, pdf_name)
                if not os.path.isfile(full):
                    errors.append(f"ligne {n} : fiche PDF introuvable : {full}")
                    continue
                pdf_data = open(full, "rb").read()
                if len(pdf_data) > Lesson.MAX_PDF_BYTES:
                    errors.append(f"ligne {n} : {pdf_name} dépasse 5 Mo")
                    continue
            order = r.get("ordre", "")
            plan.append(dict(
                key=(niveau, matiere, chap, title),
                fields=dict(summary=r.get("resume", ""), youtube_url=r.get("youtube", ""),
                            order=int(order) if order.isdigit() else 0,
                            free_preview=r.get("gratuit", "").lower() in YES, active=True),
                pdf=(pdf_name, pdf_data)))

        for e in errors:
            self.stderr.write(e)
        created = updated = 0
        with transaction.atomic():
            for item in plan:
                niveau, matiere, chap, title = item["key"]
                lesson = Lesson.objects.filter(
                    space__isnull=True, shared_level_name__iexact=niveau,
                    shared_subject_name__iexact=matiere, shared_theme_name__iexact=chap,
                    title__iexact=title).first()
                if lesson:
                    updated += 1
                else:
                    created += 1
                    lesson = Lesson(space=None, shared_level_name=niveau, shared_subject_name=matiere,
                                    shared_theme_name=chap[:100], title=title)
                for k, v in item["fields"].items():
                    setattr(lesson, k, v)
                pdf_name, pdf_data = item["pdf"]
                if pdf_data:
                    lesson.pdf_name, lesson.pdf_data = pdf_name[:200], pdf_data
                if not dry_run:
                    lesson.save()
            if dry_run:
                transaction.set_rollback(True)
        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}{created} cours créé(s), {updated} mis à jour, {len(errors)} erreur(s)."))
