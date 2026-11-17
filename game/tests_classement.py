"""Côté École : temps de réponse adapté à la réflexion, et classement par meilleur score."""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from game.models import Answer, GameConfig, GameSession, Player, Question, Quiz
from game.student import catalog_space
from game.views import _best_ranked, question_timer


def _question(quiz, difficulty=4, **kw):
    return Question.objects.create(quiz=quiz, category="ec", difficulty=difficulty, text=kw.pop("text", "?"),
                                   option_a="a", option_b="b", option_c="c", option_d="d", correct=0, **kw)


class ChronoEcoleTests(TestCase):
    def setUp(self):
        self.cfg = GameConfig.get()
        self.catalog = catalog_space()
        self.maths = Quiz.objects.create(space=None, shared_level_name="Tle C", shared_subject_name="Mathématiques",
                                         name="Intégrales", slug="integrales")
        self.svt = Quiz.objects.create(space=None, shared_level_name="Tle C", shared_subject_name="SVT",
                                       name="Glycémie", slug="glycemie")

    def test_plus_de_temps_quand_c_est_difficile(self):
        facile, expert = _question(self.svt, 1, text="f"), _question(self.svt, 4, text="e")
        self.assertEqual(question_timer(self.cfg, facile, self.catalog, self.svt), 30)
        self.assertEqual(question_timer(self.cfg, expert, self.catalog, self.svt), 120)

    def test_calculs_en_maths_et_physique(self):
        q = _question(self.maths, 4)
        self.assertEqual(question_timer(self.cfg, q, self.catalog, self.maths), 180)

    def test_temps_propre_a_une_question(self):
        q = _question(self.maths, 4, time_limit=240)
        self.assertEqual(question_timer(self.cfg, q, self.catalog, self.maths), 240)

    def test_defi_public_inchange(self):
        q = _question(self.svt, 4)
        self.assertEqual(question_timer(self.cfg, q, None, None), 6)

    def test_reglable_dans_l_administration(self):
        self.cfg.school_timer_by_difficulty = {"1": 20, "2": 40, "3": 60, "4": 90}
        self.cfg.school_timer_factors = {"Mathématiques": 2}
        self.cfg.save()
        q = _question(self.maths, 4)
        self.assertEqual(question_timer(GameConfig.get(), q, self.catalog, self.maths), 180)


class MeilleurScoreTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.quiz = Quiz.objects.create(space=None, shared_level_name="Tle D", shared_subject_name="SVT",
                                        name="Neurone", slug="neurone", elimination=False)
        self.qs = [_question(self.quiz, 2, text=f"q{i}") for i in range(4)]
        self.t0 = timezone.now() - timedelta(days=1)

    def _partie(self, player, bonnes, minutes, temps_ms=60000):
        s = GameSession.objects.create(player=player, mode="space", space=self.space, quiz=self.quiz,
                                       status="finished", reached=4, total_time_ms=temps_ms,
                                       question_ids=[q.id for q in self.qs])
        GameSession.objects.filter(id=s.id).update(started_at=self.t0 + timedelta(minutes=minutes))
        for i, q in enumerate(self.qs):
            Answer.objects.create(session=s, question=q, choice=0 if i < bonnes else 1,
                                  time_ms=5000, is_correct=i < bonnes)
        return GameSession.objects.get(id=s.id)

    def test_une_ligne_par_eleve_avec_son_meilleur_score(self):
        awa = Player.objects.create(pseudo="Awa", phone="0707000002")
        kofi = Player.objects.create(pseudo="Kofi", phone="0707000003")
        self._partie(awa, 2, 1)
        meilleur = self._partie(awa, 4, 2)
        self._partie(awa, 3, 3)
        self._partie(kofi, 3, 4)
        rows = _best_ranked(GameSession.objects.filter(quiz=self.quiz))
        self.assertEqual([r.player.pseudo for r in rows], ["Awa", "Kofi"])
        self.assertEqual(rows[0].id, meilleur.id)
        self.assertEqual((rows[0].attempts, rows[0].tries), (3, 2))

    def test_a_score_egal_le_moins_d_essais_passe_devant(self):
        awa = Player.objects.create(pseudo="Awa", phone="0707000002")
        kofi = Player.objects.create(pseudo="Kofi", phone="0707000003")
        self._partie(awa, 1, 1, temps_ms=10000)
        self._partie(awa, 4, 2, temps_ms=10000)         # 100 % au 2e essai, très rapide
        self._partie(kofi, 4, 3, temps_ms=90000)        # 100 % du premier coup, plus lent
        rows = _best_ranked(GameSession.objects.filter(quiz=self.quiz))
        self.assertEqual([r.player.pseudo for r in rows], ["Kofi", "Awa"])

    def test_page_classement_du_quiz(self):
        awa = Player.objects.create(pseudo="Awa", phone="0707000002")
        self._partie(awa, 2, 1)
        self._partie(awa, 4, 2)
        r = self.client.get(f"/e/{self.space.slug}/q/{self.quiz.slug}/classement/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content.decode().count("Awa"), 1)
        self.assertContains(r, "meilleur de 2 essais")
