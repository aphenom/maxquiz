"""Programme du jour en plusieurs matières, progression dans le programme, objectif de la semaine."""
import os
from datetime import date, datetime, time, timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from game import engagement, progression
from game.models import (Answer, Category, GameSession, Lesson, LessonView, Mission, Player, Question, Quiz)
from game.student import catalog_space, save_profile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (matière, chapitre, mois)
PROGRAMME = [
    ("Mathématiques", "Calcul littéral", 10), ("Mathématiques", "Propriété de Thalès", 10),
    ("Mathématiques", "Vecteurs", 12), ("Mathématiques", "Statistiques", 4),
    ("SVT", "Les micro-organismes", 10), ("SVT", "Le sol", 3),
    ("Anglais", "Simple past", 10), ("Anglais", "La voix passive", 3),
]


class ProgressionTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.player = Player.objects.create(phone="0703030303", pseudo="Awa")
        self.m = save_profile(self.player, "Awa", Category.objects.get(space=self.space, name="3ème"))
        self.quiz = {}
        for i, (mat, nom, mois) in enumerate(PROGRAMME):
            q = Quiz.objects.create(space=None, shared_level_name="3ème", shared_subject_name=mat, name=nom,
                                    slug=f"p{i}", question_count=4, survey_every=0)
            Lesson.objects.create(space=None, shared_level_name="3ème", shared_subject_name=mat,
                                  shared_theme_name=nom, title=nom, order=i, mois=mois)
            for k in range(4):
                Question.objects.create(quiz=q, kind="quiz", category="ec", text=f"{nom} {k}", option_a="a",
                                        option_b="b", option_c="c", option_d="d", correct=0)
            self.quiz[nom] = q
        self.dec = date(2026, 12, 2)                     # mercredi 2 décembre

    def joue(self, nom, day, ok=4):
        q = self.quiz[nom]
        s = GameSession.objects.create(player=self.player, space=self.space, quiz=q, mode="space",
                                       status="finished", day=day)
        GameSession.objects.filter(pk=s.pk).update(started_at=timezone.make_aware(datetime.combine(day, time(17))))
        for i, question in enumerate(Question.objects.filter(quiz=q)):
            Answer.objects.create(session=s, question=question, choice=0, time_ms=4000, is_correct=i < ok)

    def test_chapitres_dans_l_ordre_du_programme(self):
        maths = dict((s.name, rows) for s, rows in progression.chapitres(self.space, self.m))["Mathématiques"]
        self.assertEqual([c["nom"] for c in maths], ["Calcul littéral", "Propriété de Thalès", "Vecteurs", "Statistiques"])

    def test_retard_et_a_jour(self):
        self.joue("Calcul littéral", self.dec - timedelta(days=20))
        etats = {e["nom"]: e for e in progression.etat_matieres(self.player, self.space, self.m, self.dec)}
        maths = etats["Mathématiques"]
        self.assertEqual((maths["travailles"], maths["reussis"], maths["attendus"]), (1, 1, 3))
        self.assertEqual([c["nom"] for c in maths["retard"]], ["Propriété de Thalès", "Vecteurs"])
        self.assertEqual(maths["prochain"]["nom"], "Propriété de Thalès")
        self.assertEqual(maths["jours_sans"], 20)
        self.assertIsNone(etats["SVT"]["jours_sans"])           # jamais commencé

    def test_programme_du_jour_trois_matieres_differentes(self):
        self.joue("Calcul littéral", self.dec - timedelta(days=1))
        self.joue("Simple past", self.dec - timedelta(days=9))
        m = engagement.choisir_mission(self.player, self.space, self.m, self.dec)
        items = progression.programme_du_jour(self.player, self.space, self.m, self.dec, m)
        self.assertEqual(len(items), 3)
        self.assertEqual(len({it["matiere"] for it in items}), 3)
        delaissee = next(it for it in items if it["kind"] == "delaissee")
        self.assertIn(delaissee["matiere"], ("SVT", "Anglais"))

    def test_activite_faite_et_enchainement(self):
        mission = engagement.mission_du_jour(self.player, self.space, self.m)
        self.assertEqual(len(mission.items), 3)
        first = mission.items[0]
        self.joue(Quiz.objects.get(id=first["quiz_id"]).name, timezone.localdate())
        faits = progression.faits_aujourdhui(self.player, mission.items)
        self.assertTrue(faits[0]["fait"])
        self.assertFalse(faits[1]["fait"])
        suite = progression.suivante(self.player, mission, sauf_quiz=first["quiz_id"])
        self.assertEqual(suite["title"], mission.items[1]["title"])

    def test_cours_ouvert_compte_comme_fait(self):
        mission = engagement.mission_du_jour(self.player, self.space, self.m)
        it = next(i for i in mission.items if i.get("lesson_id"))
        LessonView.objects.create(player=self.player, lesson_id=it["lesson_id"], day=timezone.localdate())
        faits = {x["title"]: x["fait"] for x in progression.faits_aujourdhui(self.player, mission.items)}
        self.assertTrue(faits[it["title"]])

    def test_objectif_de_la_semaine(self):
        lundi = self.dec - timedelta(days=self.dec.weekday())
        self.joue("Calcul littéral", lundi)
        self.joue("Le sol", lundi + timedelta(days=1))
        sem = progression.semaine(self.player, self.space, self.m, self.dec)
        self.assertEqual((sem["faites"], sem["total"], sem["manquantes"]), (2, 3, ["Anglais"]))
        self.assertFalse(sem["complete"])
        self.joue("Simple past", self.dec)
        sem = progression.semaine(self.player, self.space, self.m, self.dec)
        self.assertTrue(sem["complete"])
        self.assertEqual(sem["semaines_completes"], 1)

    def test_rappel_sur_la_matiere_delaissee(self):
        self.joue("Calcul littéral", self.dec - timedelta(days=1))
        self.joue("Simple past", self.dec - timedelta(days=1))
        self.joue("Les micro-organismes", self.dec - timedelta(days=12))
        m = engagement.choisir_mission(self.player, self.space, self.m, self.dec)
        items = progression.programme_du_jour(self.player, self.space, self.m, self.dec, m)
        mission = Mission.objects.create(player=self.player, space=self.space, day=self.dec, kind="suite",
                                         title="x", url="/", items=items)
        title, body, url, marque = engagement.message_du_rappel(self.player, mission, self.dec)
        self.assertEqual(title, "Ça fait 12 jours sans SVT")
        self.assertIn("Le sol", body)
        self.assertEqual(sum(1 for it in marque if it.get("rappel")), 1)

    def test_accueil_programme_et_progression(self):
        session = self.client.session
        session["player_id"] = session["verified_player_id"] = self.player.id
        session.save()
        r = self.client.get(f"/e/{self.space.slug}/")
        self.assertContains(r, "Ton programme du jour")
        self.assertContains(r, "Ma progression dans le programme")
        self.assertContains(r, "Cette semaine : 0/3 matières")


class ContenuProgrammeTests(TestCase):
    def test_import_des_mois_et_de_l_ordre(self):
        base = os.path.join(ROOT, "contenu", "3eme")
        call_command("import_cours", os.path.join(base, "cours.xlsx"), "--fiches", os.path.join(base, "fiches"),
                     verbosity=0)
        maths = list(Lesson.objects.filter(shared_level_name="3ème", shared_subject_name="Mathématiques")
                     .order_by("order").values_list("shared_theme_name", "mois"))
        self.assertEqual(maths[0], ("Calcul littéral", 10))
        self.assertEqual(maths[1], ("Propriété de Thalès", 10))
        self.assertEqual(maths[-1], ("Révision BEPC", 5))
        self.assertFalse(Lesson.objects.filter(mois__isnull=True).exists())
