"""Codes d'influenceurs : lien, rattachement, application automatique, commissions."""
from decimal import Decimal
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from game.models import Category, CodePromo, Player, Subscription, Visite
from game.promos import rapport_partenaires
from game.student import catalog_space, save_profile

JEKO = dict(JEKO_API_KEY="k", JEKO_API_KEY_ID="kid", JEKO_STORE_ID="store-1", JEKO_WEBHOOK_SECRET="s",
            SITE_URL="https://maxquiz.net", OTP_NUMEROS_TEST={"0706060606": "123456"})
ANDROID = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130.0 Mobile Safari/537.36"


@override_settings(**JEKO)
class ParrainageTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.space.price_monthly, self.space.price_yearly = 2000, 15000
        self.space.save()
        self.promo = CodePromo.objects.create(code="AMINA", percent=20, first_only=True, max_uses=0,
                                              partenaire="Amina (TikTok)", commission=Decimal("15"))

    def inscription(self):
        """Parcours réel : lien de l'influenceur, puis connexion par code."""
        r = self.client.get("/p/amina/", HTTP_USER_AGENT=ANDROID)
        self.assertIn("utm_source=promo-amina", r["Location"])
        self.client.get(r["Location"], HTTP_USER_AGENT=ANDROID)
        self.client.post("/connexion/", {"phone": "0706060606"})
        self.client.post("/connexion/code/", {"code": "123456"})
        player = Player.objects.get(phone="0706060606")
        save_profile(player, "Awa", Category.objects.get(space=self.space, name="3ème"))
        return player

    def test_lien_rattache_et_applique_le_code(self):
        player = self.inscription()
        self.assertEqual(player.promo_parrain_id, self.promo.id)
        self.assertEqual(Visite.objects.filter(source="promo-amina").count(), 1)
        self.assertContains(self.client.get(f"/e/{self.space.slug}/"), "Code AMINA : -20 %")
        page = self.client.get(f"/e/{self.space.slug}/abonnement/")
        self.assertContains(page, 'data-price="1600"')                 # appliqué sans rien taper

    def test_commission_sur_le_paiement(self):
        self.inscription()
        self.client.get(f"/e/{self.space.slug}/abonnement/")
        with mock.patch("game.jeko._call", return_value={"id": "pr", "redirectUrl": "https://pay.jeko.africa/x"}):
            self.client.post(f"/e/{self.space.slug}/abonnement/", {"action": "jeko", "plan": "yearly", "method": "wave"})
        sub = Subscription.objects.get()
        self.assertEqual((sub.amount, sub.promo_id), (12000, self.promo.id))
        from game.jeko import confirm
        confirm(sub, "test")
        rows, totals = rapport_partenaires()
        self.assertEqual((rows[0]["inscrits"], rows[0]["payants"], rows[0]["encaisse"], rows[0]["commission"]),
                         (1, 1, 12000, 1800))

    def test_lien_invalide(self):
        r = self.client.get("/p/INCONNU/")
        self.assertEqual(r["Location"], "/")

    def test_tableau_et_export(self):
        staff = User.objects.create_user("chef", password="pw-tres-long-123", is_staff=True)
        self.client.force_login(staff)
        page = self.client.get(f"/e/{self.space.slug}/tableau-de-bord/partenaires/?mois=tout")
        self.assertContains(page, "Amina (TikTok)")
        self.assertContains(page, "https://maxquiz.net/p/AMINA/")
        csv = self.client.get(f"/e/{self.space.slug}/tableau-de-bord/partenaires/?mois=tout&csv=1")
        self.assertIn("Amina (TikTok);AMINA", csv.content.decode("utf-8-sig"))
