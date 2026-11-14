"""Codes promo sur les abonnements."""
import os
import tempfile
from datetime import timedelta
from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from game.models import Category, CodePromo, Player, Subscription
from game.student import catalog_space, save_profile

JEKO = dict(JEKO_API_KEY="k", JEKO_API_KEY_ID="kid", JEKO_STORE_ID="store-1", JEKO_WEBHOOK_SECRET="s",
            SITE_URL="https://maxquiz.net")


@override_settings(**JEKO)
class PromoTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.space.price_monthly, self.space.price_yearly, self.space.trial_enabled = 2000, 15000, False
        self.space.save()
        self.url = f"/e/{self.space.slug}/abonnement/"

    def student(self, phone="0705050505"):
        player = Player.objects.create(phone=phone, pseudo="")
        save_profile(player, "Awa", Category.objects.get(space=self.space, name="3ème"))
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = player.id
        s.save()
        return player

    def apply(self, code):
        return self.client.post(self.url, {"action": "promo", "code": code})

    def pay(self, plan="yearly"):
        with mock.patch("game.jeko._call", return_value={"id": "pr", "redirectUrl": "https://pay.jeko.africa/x"}) as call:
            r = self.client.post(self.url, {"action": "jeko", "plan": plan, "method": "wave"})
        return r, call

    def test_reduction_appliquee_au_paiement(self):
        CodePromo.objects.create(code="bepc-2027", percent=20)
        self.student()
        self.apply("bepc2027")
        page = self.client.get(self.url)
        self.assertContains(page, "-20 %")
        self.assertContains(page, 'data-price="12000"')
        self.assertContains(page, "<s class=\"small\" style=\"display:block\">15000 F</s>")
        r, call = self.pay("yearly")
        self.assertEqual(call.call_args[0][2]["amountCents"], 1200000)
        sub = Subscription.objects.get()
        self.assertEqual((sub.amount, sub.list_price, sub.promo.code), (12000, 15000, "BEPC2027"))

    def test_code_unique_utilise_une_seule_fois(self):
        from game.promos import check
        CodePromo.objects.create(code="UNIQUE1", percent=50, max_uses=1)
        self.student("0705050501")
        self.apply("UNIQUE1")
        self.pay("monthly")
        self.assertEqual(check("UNIQUE1", self.space, None), (None, "Ce code promo a déjà été utilisé."))
        self.client.cookies.clear()
        self.student("0705050502")
        self.apply("UNIQUE1")
        self.assertIsNone(self.client.session.get(f"promo_{self.space.id}"))

    def test_code_reutilisable_une_fois_par_compte(self):
        CodePromo.objects.create(code="RENTREE", percent=10, max_uses=0, max_per_player=1)
        self.student("0705050503")
        self.apply("RENTREE")
        self.pay("monthly")
        self.apply("RENTREE")
        self.assertEqual(self.client.session.get(f"promo_{self.space.id}"), None)
        self.client.cookies.clear()
        self.student("0705050504")
        self.apply("RENTREE")
        self.assertEqual(self.client.session.get(f"promo_{self.space.id}"), "RENTREE")

    def test_paiement_echoue_rend_le_code(self):
        CodePromo.objects.create(code="UNIQUE2", percent=50, max_uses=1)
        self.student("0705050505")
        self.apply("UNIQUE2")
        self.pay("monthly")
        Subscription.objects.update(status="failed")
        self.apply("UNIQUE2")
        self.assertEqual(self.client.session.get(f"promo_{self.space.id}"), "UNIQUE2")

    def test_formule_non_concernee_et_expiration(self):
        CodePromo.objects.create(code="MOIS", percent=50, yearly=False)
        CodePromo.objects.create(code="VIEUX", percent=50, ends_on=timezone.localdate() - timedelta(days=1))
        self.student()
        self.assertIn("Ce code promo a expiré.", [str(m) for m in self.apply("VIEUX").wsgi_request._messages])
        self.apply("MOIS")
        r, call = self.pay("yearly")
        self.assertEqual(call.call_args[0][2]["amountCents"], 1500000)        # pas de remise sur l'annuel
        self.assertIsNone(Subscription.objects.get().promo)

    def test_code_a_100_pourcent_active_sans_paiement(self):
        CodePromo.objects.create(code="OFFERT", percent=100)
        self.student()
        self.apply("OFFERT")
        with mock.patch("game.jeko._call") as call:
            r = self.client.post(self.url, {"action": "jeko", "plan": "monthly", "method": "wave"})
        call.assert_not_called()
        sub = Subscription.objects.get()
        self.assertEqual((sub.status, sub.amount, sub.list_price), ("active", 0, 2000))
        self.assertRedirects(r, f"/e/{self.space.slug}/", fetch_redirect_response=False)

    def test_generation_de_codes_uniques(self):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        call_command("generer_codes_promo", nombre=5, taux=30, prefixe="ECOLE", fin="2026-12-31",
                     formules="monthly", fichier=path, verbosity=0)
        codes = CodePromo.objects.filter(code__startswith="ECOLE")
        self.assertEqual(codes.count(), 5)
        self.assertTrue(all(c.max_uses == 1 and not c.yearly for c in codes))
        self.assertEqual(len(open(path, encoding="utf-8").read().strip().splitlines()), 6)
        os.remove(path)
