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
