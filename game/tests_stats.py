"""Statistiques : visites, téléchargements, tableau de bord."""
import os
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from game.models import Telechargement, Visite
from game.stats import page_cle
from game.student import catalog_space

ANDROID = "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 Chrome/130.0 Mobile Safari/537.36"


class StatsTests(TestCase):
    def setUp(self):
        self.space = catalog_space()

    def test_visite_comptee_avec_provenance(self):
        self.client.get("/?utm_source=facebook&utm_campaign=bepc", HTTP_USER_AGENT=ANDROID)
        self.client.get("/confidentialite/", HTTP_USER_AGENT=ANDROID, HTTP_REFERER="https://l.facebook.com/")
        v = list(Visite.objects.order_by("id"))
        self.assertEqual(len(v), 2)
        self.assertEqual((v[0].source, v[0].device), ("facebook", "android"))
        self.assertEqual(v[0].visiteur, v[1].visiteur)          # même visiteur dans la journée

    def test_robots_admin_et_api_ignores(self):
        self.client.get("/", HTTP_USER_AGENT="facebookexternalhit/1.1")
        self.client.get("/admin/login/", HTTP_USER_AGENT=ANDROID)
        self.client.get("/manifest.webmanifest", HTTP_USER_AGENT=ANDROID)
        self.assertEqual(Visite.objects.count(), 0)

    def test_page_cle(self):
        self.assertEqual(page_cle("/e/maxquiz/cours/12/"), "/e/…/cours/…/")
        self.assertEqual(page_cle("/e/maxquiz/q/3eme-svt-le-sol/"), "/e/…/q/…/")

    def test_apk_compte_une_fois_par_jour(self):
        fd, path = tempfile.mkstemp(suffix=".apk")
        os.write(fd, b"PK fake apk")
        os.close(fd)
        with override_settings(APK_FILE=path):
            r = self.client.get("/telecharger/maxquiz.apk", HTTP_USER_AGENT=ANDROID)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r["Content-Type"], "application/vnd.android.package-archive")
            self.assertEqual(b"".join(r.streaming_content), b"PK fake apk")
            self.client.get("/telecharger/maxquiz.apk", HTTP_USER_AGENT=ANDROID)
        self.assertEqual(Telechargement.objects.filter(kind="apk").count(), 1)
        os.remove(path)

    def test_apk_absent(self):
        self.assertEqual(self.client.get("/telecharger/maxquiz.apk").status_code, 404)

    def test_installation_navigateur(self):
        self.assertEqual(self.client.post("/stats/installation/", HTTP_USER_AGENT=ANDROID).status_code, 204)
        self.assertEqual(Telechargement.objects.filter(kind="pwa").count(), 1)

    def test_tableau_pour_l_administration(self):
        self.client.get("/", HTTP_USER_AGENT=ANDROID)
        staff = User.objects.create_user("chef", password="pw-tres-long-123", is_staff=True)
        self.client.force_login(staff)
        self.assertContains(self.client.get("/admin/"), "Statistiques")
        page = self.client.get(f"/e/{self.space.slug}/tableau-de-bord/statistiques/?p=7")
        self.assertContains(page, "visiteurs")
        self.assertContains(page, "APK téléchargés")

    def test_tableau_protege(self):
        r = self.client.get(f"/e/{self.space.slug}/tableau-de-bord/statistiques/")
        self.assertEqual(r.status_code, 302)


class CloisonnementEcoleTests(TestCase):
    """Une école ne voit jamais les données de MQ Technologies, ni l'activité de ses élèves
    en dehors de son espace."""
    def setUp(self):
        from game.models import Category, Membership, Player, Space
        self.catalog = catalog_space()
        self.school = Space.objects.create(name="Collège Test", slug="college-test", kind="school",
                                           members_only=True, dashboard_username="college-test",
                                           dashboard_code="code-ecole")
        cat = Category.objects.create(space=self.school, name="3ème", slug="3eme")
        self.player = Player.objects.create(phone="0703030303", pseudo="")
        Membership.objects.create(space=self.school, player=self.player, category=cat, full_name="Awa")
        s = self.client.session
        s[f"dash_{self.school.id}"] = "code-ecole"
        s.save()

    def test_pas_de_statistiques_ni_de_pubs(self):
        self.assertEqual(self.client.get("/e/college-test/tableau-de-bord/statistiques/").status_code, 404)
        self.assertEqual(self.client.get("/e/college-test/tableau-de-bord/pubs/").status_code, 404)
        page = self.client.get("/e/college-test/tableau-de-bord/assiduite/")
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "/tableau-de-bord/statistiques/")
        self.assertNotContains(page, "Résultats des pubs")

    def test_assiduite_limitee_a_l_ecole(self):
        from game.engagement import rapport
        from game.models import Answer, GameSession, Question, Quiz
        quiz = Quiz.objects.create(space=None, shared_level_name="3ème", shared_subject_name="SVT", name="Le sol",
                                   slug="sol")
        q = Question.objects.create(quiz=quiz, kind="quiz", category="ec", text="Q", option_a="a", option_b="b",
                                    option_c="c", option_d="d", correct=0)
        s = GameSession.objects.create(player=self.player, space=self.catalog, quiz=quiz, mode="space")
        Answer.objects.create(session=s, question=q, choice=0, time_ms=1, is_correct=True)
        self.assertEqual(rapport(self.school)["actifs_7"], 0)          # activité sur MaxQuiz École : invisible
        s2 = GameSession.objects.create(player=self.player, space=self.school, quiz=quiz, mode="space")
        Answer.objects.create(session=s2, question=q, choice=0, time_ms=1, is_correct=True)
        self.assertEqual(rapport(self.school)["actifs_7"], 1)
