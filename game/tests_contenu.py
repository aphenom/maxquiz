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

    def _contenu_complet(self, dossier):
        """Le contenu livré s'importe en entier, chaque quiz a son cours et sa fiche PDF."""
        base = os.path.join(ROOT, "contenu", dossier)
        call_command("import_questions", os.path.join(base, "quiz.xlsx"), "--shared", verbosity=0)
        call_command("import_cours", os.path.join(base, "cours.xlsx"),
                     "--fiches", os.path.join(base, "fiches"), verbosity=0)
        ws = openpyxl.load_workbook(os.path.join(base, "quiz.xlsx"), read_only=True).worksheets[0]
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        for niveau in {r[0] for r in rows}:
            mine = [r for r in rows if r[0] == niveau]
            chapitres = {(r[1], r[2]) for r in mine}
            quizzes = Quiz.objects.filter(space__isnull=True, shared_level_name=niveau)
            self.assertEqual(quizzes.count(), len(chapitres), niveau)
            self.assertEqual(Question.objects.filter(quiz__in=quizzes).count(), len(mine), niveau)
            for quiz in quizzes:
                lesson = Lesson.objects.get(space__isnull=True, shared_level_name=niveau,
                                            shared_subject_name=quiz.shared_subject_name, shared_theme_name=quiz.name)
                self.assertTrue(lesson.has_pdf, f"{niveau} {quiz.name}")
        return {r[0] for r in rows}

    def test_contenu_3eme_complet(self):
        self.assertEqual(self._contenu_complet("3eme"), {"3ème"})

    def _college(self, dossier, niveau, matieres):
        self.assertEqual(self._contenu_complet(dossier), {niveau})
        libres = Lesson.objects.filter(space__isnull=True, shared_level_name=niveau, free_preview=True)
        self.assertEqual(sorted(libres.values_list("shared_subject_name", flat=True)), matieres)

    def test_contenu_4eme_complet(self):
        self._college("4eme", "4ème", ["EDHC", "Mathématiques", "Physique-Chimie"])

    def test_contenu_6eme_complet(self):
        self._college("6eme", "6ème", ["EDHC", "Physique-Chimie"])

    def test_contenu_5eme_complet(self):
        self._college("5eme", "5ème", ["EDHC", "Mathématiques", "Physique-Chimie"])

    def test_contenu_terminale_complet(self):
        self.assertEqual(self._contenu_complet("terminale"), {"Tle A", "Tle C", "Tle D"})
        # Un premier chapitre gratuit par matière et par classe
        for niveau in ("Tle A", "Tle C", "Tle D"):
            libres = Lesson.objects.filter(space__isnull=True, shared_level_name=niveau, free_preview=True)
            self.assertEqual(libres.values("shared_subject_name").distinct().count(), libres.count(), niveau)
            self.assertGreaterEqual(libres.count(), 2, niveau)

    def test_filtre_fiche_echappe(self):
        html = fiche("■ Titre\n• a < b\n1. étape\n<script>x</script>")
        self.assertIn('<h3 class="fiche-h">Titre</h3>', html)
        self.assertIn("a &lt; b", html)
        self.assertNotIn("<script>", html)


class RechercheTests(TestCase):
    def test_cherchable_normalise(self):
        from game.templatetags.fiche import cherchable
        self.assertEqual(cherchable("■ Théorème  de\nPythagore • Égalité"), "theoreme de pythagore egalite")

    def test_reviser_accordeons_et_recherche(self):
        from game.models import Category, Membership, Player
        from game.student import save_profile
        space = catalog_space()
        Lesson.objects.create(space=None, shared_level_name="3ème", shared_subject_name="SVT",
                              shared_theme_name="Le sol", title="Le sol", summary="■ Composition\n• L'humus")
        player = Player.objects.create(phone="0701010101", pseudo="")
        save_profile(player, "Awa", Category.objects.get(space=space, name="3ème"))
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = player.id
        s.save()
        html = self.client.get(f"/e/{space.slug}/cours/").content.decode()
        self.assertIn('id="mqSearch"', html)
        self.assertIn('class="dash-accordion subj"', html)
        self.assertIn("l'humus", html.replace("&#x27;", "'"))
