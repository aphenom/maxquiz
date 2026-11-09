"""Paiement en ligne Jèko (API simulée)."""
import hashlib
import hmac
import json
from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings

from game.models import Category, Notification, Player, Subscription
from game.student import catalog_space, save_profile

JEKO = dict(JEKO_API_KEY="k", JEKO_API_KEY_ID="kid", JEKO_STORE_ID="store-1", JEKO_WEBHOOK_SECRET="s3cret",
            SITE_URL="https://maxquiz.net")


def signed(body):
    raw = json.dumps(body).encode()
    return raw, hmac.new(b"s3cret", raw, hashlib.sha256).hexdigest()


@override_settings(**JEKO)
class JekoTests(TestCase):
    def setUp(self):
        self.space = catalog_space()
        self.space.price_monthly, self.space.price_yearly = 2000, 15000
        self.space.save()
        self.player = Player.objects.create(phone="0701010101", pseudo="")
        self.m = save_profile(self.player, "Awa", Category.objects.get(space=self.space, name="3ème"))
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = self.player.id
        s.save()
        self.url = f"/e/{self.space.slug}/abonnement/"

    def pay(self, method="wave", plan="monthly"):
        with mock.patch("game.jeko._call", return_value={"id": "pr_1", "status": "pending",
                                                        "redirectUrl": "https://pay.jeko.africa/x"}) as call:
            r = self.client.post(self.url, {"action": "jeko", "plan": plan, "method": method})
        return r, call

    def test_demarrer_paiement(self):
        page = self.client.get(self.url)
        self.assertContains(page, 'name="method" value="wave"')
        r, call = self.pay()
        self.assertRedirects(r, "https://pay.jeko.africa/x", fetch_redirect_response=False)
        sub = Subscription.objects.get()
        self.assertEqual((sub.status, sub.provider, sub.provider_id, sub.amount), ("initiated", "jeko", "pr_1", 2000))
        method, path, payload = call.call_args[0]
        self.assertEqual((method, path), ("POST", "/partner_api/payment_requests"))
        self.assertEqual(payload["amountCents"], 200000)
        self.assertEqual(payload["storeId"], "store-1")
        self.assertEqual(payload["reference"], sub.payment_ref)
        self.assertTrue(payload["paymentDetails"]["data"]["successUrl"].startswith("https://maxquiz.net/paiement/jeko/retour/"))

    def test_api_indisponible(self):
        from game.jeko import JekoError
        with mock.patch("game.jeko._call", side_effect=JekoError("HTTP 500")):
            r = self.client.post(self.url, {"action": "jeko", "plan": "monthly", "method": "orange"})
        self.assertRedirects(r, self.url, fetch_redirect_response=False)
        self.assertEqual(Subscription.objects.get().status, "failed")

    def webhook(self, sub, status="success", amount=200000, secret_ok=True):
        body = {"id": "txn_9", "status": status, "transactionType": "payment",
                "amount": {"amount": amount, "currency": "XOF"},
                "transactionDetails": {"reference": sub.payment_ref}}
        if amount is None:
            del body["amount"]
        raw, sig = signed(body)
        return self.client.post("/paiement/jeko/webhook/", raw, content_type="application/json",
                                HTTP_JEKO_SIGNATURE=sig if secret_ok else "0" * 64,
                                HTTP_JEKO_EVENT="TRANSACTION_COMPLETED")

    def test_webhook_active_une_seule_fois(self):
        self.pay()
        sub = Subscription.objects.get()
        self.assertEqual(self.webhook(sub).status_code, 200)
        self.assertEqual(self.webhook(sub).status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "active")
        self.assertIsNotNone(sub.end_date)
        self.assertEqual(Notification.objects.filter(player=self.player, kind="sub_ok").count(), 1)

    def test_webhook_signature_fausse(self):
        self.pay()
        sub = Subscription.objects.get()
        self.assertEqual(self.webhook(sub, secret_ok=False).status_code, 400)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "initiated")

    def test_webhook_montant_inattendu(self):
        self.pay()
        sub = Subscription.objects.get()
        self.webhook(sub, amount=100)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "pending")

    def test_webhook_montant_en_francs_refuse(self):
        # Jèko envoie des centimes : 2000 pour une formule à 2 000 F, c'est 20 F payés.
        self.pay()
        sub = Subscription.objects.get()
        self.webhook(sub, amount=2000)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "pending")

    def test_webhook_sans_montant(self):
        self.pay()
        sub = Subscription.objects.get()
        self.webhook(sub, amount=None)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "pending")

    def test_webhook_montant_faux_ne_retrograde_pas(self):
        self.pay()
        sub = Subscription.objects.get()
        self.webhook(sub)
        self.webhook(sub, amount=100)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "active")

    def test_retour_interroge_le_statut(self):
        self.pay()
        sub = Subscription.objects.get()
        with mock.patch("game.jeko._call", return_value={
                "id": "pr_1", "status": "success",
                "transaction": {"id": "txn_9", "amount": {"amount": 200000, "currency": "XOF"}}}):
            r = self.client.get(f"/paiement/jeko/retour/?ref={sub.payment_ref}")
        self.assertRedirects(r, f"/e/{self.space.slug}/", fetch_redirect_response=False)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "active")

    def test_retour_montant_inattendu(self):
        self.pay()
        sub = Subscription.objects.get()
        with mock.patch("game.jeko._call", return_value={
                "id": "pr_1", "status": "success",
                "transaction": {"id": "txn_9", "amount": {"amount": 100, "currency": "XOF"}}}):
            self.client.get(f"/paiement/jeko/retour/?ref={sub.payment_ref}")
        sub.refresh_from_db()
        self.assertEqual(sub.status, "pending")

    def test_retour_echec(self):
        self.pay()
        sub = Subscription.objects.get()
        with mock.patch("game.jeko._call", return_value={"id": "pr_1", "status": "pending"}):
            r = self.client.get(f"/paiement/jeko/retour/?ref={sub.payment_ref}&echec=1")
        self.assertRedirects(r, self.url, fetch_redirect_response=False)
        sub.refresh_from_db()
        self.assertEqual(sub.status, "failed")

    def test_verification_periodique(self):
        self.pay()
        Subscription.objects.update(created_at="2026-01-01T00:00:00Z")
        with mock.patch("game.jeko._call", return_value={"id": "pr_1", "status": "error"}):
            call_command("jeko_verifier", verbosity=0)
        self.assertEqual(Subscription.objects.get().status, "failed")

    @override_settings(JEKO_API_KEY="")
    def test_sans_configuration_paiement_declare(self):
        page = self.client.get(self.url)
        self.assertNotContains(page, 'name="method"')
        self.assertContains(page, 'name="payment_ref"')
