"""Mission du jour, série et rappels."""
from datetime import datetime, time, timedelta
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from game import engagement
from game.models import (Answer, Category, GameSession, Lesson, LessonView, Mission, Player, PushDevice,
                         Question, Quiz, Rappels)
from game.student import catalog_space, save_profile


class EngagementTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.player = Player.objects.create(phone="0702020202", pseudo="")
        self.m = save_profile(self.player, "Awa", Category.objects.get(space=self.space, name="3ème"))
        self.quizzes = []
        for i, name in enumerate(["Calcul littéral", "Racines carrées"]):
            q = Quiz.objects.create(space=None, shared_level_name="3ème", shared_subject_name="Mathématiques",
                                    name=name, slug=f"q{i}", question_count=10)
            Lesson.objects.create(space=None, shared_level_name="3ème", shared_subject_name="Mathématiques",
                                  shared_theme_name=name, title=name, order=i)
            self.quizzes.append(q)
        self.questions = [Question.objects.create(quiz=self.quizzes[0], kind="quiz", category="ec", text=f"Q{i}",
                                                  option_a="a", option_b="b", option_c="c", option_d="d", correct=0)
                          for i in range(6)]
        self.today = timezone.localdate()

    def play(self, quiz, day, n, ok, status="finished"):
        s = GameSession.objects.create(player=self.player, space=self.space, quiz=quiz, mode="space",
                                       status=status, day=day)
        GameSession.objects.filter(pk=s.pk).update(
            started_at=timezone.make_aware(datetime.combine(day, time(17, 0))))
        for i in range(n):
            Answer.objects.create(session=s, question=self.questions[i], choice=0, time_ms=1000, is_correct=i < ok)
        return s

    def test_serie_avec_joker(self):
        for d in (0, 1, 3):
            LessonView.objects.create(player=self.player, lesson=Lesson.objects.first(),
                                      day=self.today - timedelta(days=d))
        self.assertEqual(engagement.serie(self.player), 3)

    def test_serie_cassee(self):
        LessonView.objects.create(player=self.player, lesson=Lesson.objects.first(), day=self.today - timedelta(days=3))
        self.assertEqual(engagement.serie(self.player), 0)

    def test_mission_chapitre_suivant(self):
        m = engagement.choisir_mission(self.player, self.space, self.m)
        self.assertEqual(m["kind"], "suite")
        self.assertIn("Calcul littéral", m["title"])

    def test_mission_reprendre(self):
        s = self.play(self.quizzes[0], self.today, 3, 2, status="playing")
        GameSession.objects.filter(pk=s.pk).update(started_at=timezone.now())
        self.assertEqual(engagement.choisir_mission(self.player, self.space, self.m)["kind"], "reprendre")

    def test_mission_revision_espacee(self):
        self.play(self.quizzes[0], self.today - timedelta(days=1), 6, 2)
        m = engagement.choisir_mission(self.player, self.space, self.m)
        self.assertEqual(m["kind"], "revision")
        self.assertIn("2/6", m["text"])
        self.assertIn("/cours/", m["url"])

    def test_mission_fixee_pour_la_journee(self):
        a = engagement.mission_du_jour(self.player)
        self.play(self.quizzes[0], self.today, 6, 6)
        self.assertEqual(engagement.mission_du_jour(self.player).pk, a.pk)

    def _device(self):
        PushDevice.objects.create(player=self.player, kind="web", endpoint="https://push.example/1")

    def at(self, h, m=0):
        return timezone.make_aware(datetime.combine(self.today, time(h, m)))

    @mock.patch("game.push.notify")
    def test_rappel_une_fois_par_jour_a_l_heure(self, notify):
        self._device()
        Rappels.objects.create(player=self.player, heure=time(18, 30))
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(18, 0)), 0)
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(18, 40)), 1)
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(19, 0)), 0)
        self.assertEqual(notify.call_count, 1)
        self.assertIsNotNone(Mission.objects.get(player=self.player).pushed_at)

    @mock.patch("game.push.notify")
    def test_pas_de_rappel_si_deja_actif_ou_la_nuit(self, notify):
        self._device()
        Rappels.objects.create(player=self.player, heure=time(18, 30))
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(21, 30)), 0)
        self.play(self.quizzes[0], self.today, 6, 6)
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(19, 0)), 0)
        notify.assert_not_called()

    @mock.patch("game.push.notify")
    def test_un_jour_sur_deux_apres_trois_rappels_ignores(self, notify):
        self._device()
        Rappels.objects.create(player=self.player, heure=time(18, 30), ignores=3,
                               dernier_envoi=self.at(18, 30) - timedelta(days=1))
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(19, 0)), 0)
        engagement.noter_visite(self.player)
        self.assertEqual(Rappels.objects.get(player=self.player).ignores, 0)
        self.assertEqual(engagement.envoyer_rappels_missions(self.at(19, 0)), 1)

    def login(self):
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = self.player.id
        s.save()

    def test_accueil_et_reglages(self):
        self.login()
        self.assertContains(self.client.get(f"/e/{self.space.slug}/"), "Mission du jour")
        self.client.post("/moi/", {"action": "rappels", "actifs": "on", "heure": "17:30"})
        self.assertEqual(Rappels.objects.get(player=self.player).heure, time(17, 30))
        self.client.post("/moi/", {"action": "rappels", "pause": "7"})
        self.assertIsNotNone(Rappels.objects.get(player=self.player).pause_jusquau)

    def test_cours_ouvert_compte_dans_la_serie(self):
        self.login()
        lesson = Lesson.objects.first()
        self.client.get(f"/e/{self.space.slug}/cours/{lesson.id}/")
        self.assertTrue(LessonView.objects.filter(player=self.player, lesson=lesson).exists())
        self.assertEqual(engagement.serie(self.player), 1)
