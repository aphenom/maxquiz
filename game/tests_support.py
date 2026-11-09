"""Aide et contact, signalement d'erreurs."""
import json

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from game.models import Lesson, Notification, Player, Question, Quiz, Signalement


class SupportTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(phone="0701020304", pseudo="Awa")
        quiz = Quiz.objects.create(space=None, shared_level_name="3ème", shared_subject_name="SVT",
                                   name="Le sol", slug="3eme-svt-le-sol")
        self.q = Question.objects.create(quiz=quiz, kind="quiz", category="ec", text="Q ?", option_a="a",
                                         option_b="b", option_c="c", option_d="d", correct=0)
        self.lesson = Lesson.objects.create(space=None, shared_level_name="3ème", shared_subject_name="SVT",
                                            shared_theme_name="Le sol", title="Le sol")

    def login(self):
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = self.player.id
        s.save()

    def test_signaler_question_json(self):
        self.login()
        r = self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "reponse"}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["ok"])
        s = Signalement.objects.get()
        self.assertEqual((s.kind, s.question_id, s.player_id, s.status), ("contenu", self.q.id, self.player.id, "nouveau"))

    def test_signaler_autre_sans_message_refuse(self):
        r = self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "autre"}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertFalse(Signalement.objects.exists())

    def test_signaler_cours_formulaire_et_retour(self):
        r = self.client.post(reverse("signaler"), {"lesson_id": self.lesson.id, "motif": "cours",
                                                   "message": "faute ligne 2", "next": "/e/maxquiz/cours/1/"})
        self.assertRedirects(r, "/e/maxquiz/cours/1/", fetch_redirect_response=False)
        self.assertEqual(Signalement.objects.get().lesson_id, self.lesson.id)

    def test_next_externe_ignore(self):
        r = self.client.post(reverse("signaler"), {"lesson_id": self.lesson.id, "motif": "cours",
                                                   "next": "https://exemple.com/"})
        self.assertEqual(r["Location"], "/")

    def test_limite_anonyme(self):
        for _ in range(5):
            self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "faute"}),
                             content_type="application/json")
        r = self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "faute"}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Signalement.objects.count(), 5)

    def test_page_aide_et_demande(self):
        self.assertEqual(self.client.get(reverse("aide")).status_code, 200)
        r = self.client.post(reverse("aide"), {"motif": "technique", "message": "Je ne reçois pas le code",
                                               "contact": "07 07 07 07 07"})
        self.assertRedirects(r, reverse("aide"), fetch_redirect_response=False)
        s = Signalement.objects.get()
        self.assertEqual((s.kind, s.contact), ("assistance", "0707070707"))

    def test_aide_anonyme_sans_numero_refuse(self):
        r = self.client.post(reverse("aide"), {"motif": "technique", "message": "Bonjour à vous"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Signalement.objects.exists())

    def test_admin_traite_previent_eleve_une_fois(self):
        s = Signalement.objects.create(kind="contenu", motif="reponse", question=self.q, player=self.player)
        admin_user = User.objects.create_superuser("chef", "c@x.ci", "pw-tres-long-123")
        self.client.force_login(admin_user)
        self.assertEqual(self.client.get(reverse("admin:game_signalement_changelist")).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:game_signalement_change", args=[s.id])).status_code, 200)
        data = {"action": "marquer_traite", "_selected_action": [s.id]}
        self.client.post(reverse("admin:game_signalement_changelist"), data)
        self.client.post(reverse("admin:game_signalement_changelist"), data)
        s.refresh_from_db()
        self.assertEqual(s.status, "traite")
        self.assertIsNotNone(s.handled_at)
        self.assertEqual(Notification.objects.filter(player=self.player).count(), 1)

    @override_settings(SIGNALEMENTS_EMAIL="equipe@maxquiz.net")
    def test_copie_par_email_si_reglee(self):
        self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "reponse"}),
                         content_type="application/json")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("La bonne réponse est fausse", mail.outbox[0].subject)

    def test_pas_d_email_par_defaut(self):
        self.client.post(reverse("signaler"), json.dumps({"question_id": self.q.id, "motif": "reponse"}),
                         content_type="application/json")
        self.assertEqual(len(mail.outbox), 0)
