"""Import du contenu commun MaxQuiz (cours + quiz) et matière EDHC."""
import os
import tempfile

import openpyxl
from django.core.management import call_command
from django.test import TestCase

from game.models import Lesson, Question, Quiz, SubCategory
from game.student import catalog_space
from game.templatetags.fiche import fiche

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENU = os.path.join(ROOT, "contenu", "3eme")


def _xlsx(rows):
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    wb = openpyxl.Workbook()
    for r in rows:
        wb.active.append(r)
    wb.save(path)
    return path


class ContenuTests(TestCase):
    def test_edhc_au_college(self):
        space = catalog_space()
        names = set(SubCategory.objects.filter(category__space=space, category__name="3ème")
                    .values_list("name", flat=True))
        self.assertIn("EDHC", names)

    def test_import_cours_cree_puis_met_a_jour(self):
        head = ["niveau", "matiere", "chapitre", "titre", "resume", "youtube", "fiche_pdf", "ordre", "gratuit"]
        path = _xlsx([head, ["3ème", "Mathématiques", "Vecteurs", "Vecteurs", "■ Essentiel\n• A", "", "", "3", "oui"]])
        call_command("import_cours", path, verbosity=0)
        lesson = Lesson.objects.get(space__isnull=True, shared_theme_name="Vecteurs")
        self.assertTrue(lesson.free_preview)
        self.assertEqual(lesson.order, 3)
        path2 = _xlsx([head, ["3ème", "Mathématiques", "Vecteurs", "Vecteurs", "nouveau", "", "", "3", "non"]])
        call_command("import_cours", path2, verbosity=0)
        self.assertEqual(Lesson.objects.filter(space__isnull=True).count(), 1)
        lesson.refresh_from_db()
        self.assertEqual(lesson.summary, "nouveau")
        self.assertFalse(lesson.free_preview)

    def test_import_cours_dry_run_et_pdf_manquant(self):
        head = ["niveau", "matiere", "chapitre", "titre", "resume", "youtube", "fiche_pdf", "ordre", "gratuit"]
        path = _xlsx([head, ["3ème", "Mathématiques", "Vecteurs", "Vecteurs", "", "", "absent.pdf", "1", ""],
                      ["3ème", "Mathématiques", "Thalès", "Thalès", "", "", "", "2", ""]])
        call_command("import_cours", path, "--dry-run", verbosity=0)
        self.assertEqual(Lesson.objects.count(), 0)
        call_command("import_cours", path, verbosity=0)
        self.assertEqual(list(Lesson.objects.values_list("title", flat=True)), ["Thalès"])

    def test_contenu_3eme_complet(self):
        """Le contenu livré s'importe en entier, chaque quiz a son cours et sa fiche PDF."""
        call_command("import_questions", os.path.join(CONTENU, "quiz.xlsx"), "--shared", verbosity=0)
        call_command("import_cours", os.path.join(CONTENU, "cours.xlsx"),
                     "--fiches", os.path.join(CONTENU, "fiches"), verbosity=0)
        self.assertEqual(Quiz.objects.filter(space__isnull=True, shared_level_name="3ème").count(), 25)
        self.assertGreaterEqual(Question.objects.filter(quiz__shared_level_name="3ème").count(), 300)
        for quiz in Quiz.objects.filter(space__isnull=True, shared_level_name="3ème"):
            lesson = Lesson.objects.get(space__isnull=True, shared_level_name="3ème",
                                        shared_subject_name=quiz.shared_subject_name, shared_theme_name=quiz.name)
            self.assertTrue(lesson.has_pdf, quiz.name)

    def test_filtre_fiche_echappe(self):
        html = fiche("■ Titre\n• a < b\n1. étape\n<script>x</script>")
        self.assertIn('<h3 class="fiche-h">Titre</h3>', html)
        self.assertIn("a &lt; b", html)
        self.assertNotIn("<script>", html)
