"""Envoi des codes par SMS (API Orange simulée) et accusés de réception."""
import base64
import json
from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings

from game import sms
from game.models import OTPCode, SmsEnvoi

ORANGE = dict(SMS_PROVIDER="orange", ORANGE_CLIENT_ID="cid", ORANGE_CLIENT_SECRET="sec",
              ORANGE_SMS_SENDER_NUMBER="2250000", ORANGE_SMS_SENDER_NAME="MaxQuiz", SMS_NOM_OPERATEURS="orange",
              OTP_AFFICHER_CODE=False, DEBUG=False)


def fake_http(calls):
    def _http(method, url, headers, data=None):
        calls.append((method, url, headers, data))
        if url.endswith("/oauth/v3/token"):
            return 200, {"access_token": "tok", "expires_in": "3600"}
        return 201, {"outboundSMSMessageRequest": {
            "resourceURL": "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2250000/requests/abc123"}}
    return _http


@override_settings(**ORANGE)
class SmsTests(TestCase):
    def setUp(self):
        sms._token.update(value="", expires=0)

    def test_operateurs(self):
        self.assertEqual([sms.operateur(p) for p in ("0707070707", "0505050505", "0101010101", "2250707070707")],
                         ["orange", "mtn", "moov", "orange"])

    def test_code_envoye_par_orange(self):
        calls = []
        with mock.patch("game.sms._http", side_effect=fake_http(calls)):
            r = self.client.post("/connexion/", {"phone": "07 07 07 07 07"})
        self.assertRedirects(r, "/connexion/code/", fetch_redirect_response=False)   # code jamais dans l'adresse
        token, send = calls
        self.assertTrue(token[2]["Authorization"].startswith("Basic "))
        self.assertIn("/smsmessaging/v1/outbound/tel%3A%2B2250000/requests", send[1])
        body = json.loads(send[3])["outboundSMSMessageRequest"]
        self.assertEqual(body["address"], "tel:+2250707070707")
        self.assertEqual(body["senderName"], "MaxQuiz")
        self.assertIn(OTPCode.objects.get().code, body["outboundSMSTextMessage"]["message"])
        row = SmsEnvoi.objects.get()
        self.assertEqual((row.operateur, row.resource_id, row.status), ("orange", "abc123", "sent"))

    def test_pas_de_nom_chez_mtn_tant_que_non_valide(self):
        calls = []
        with mock.patch("game.sms._http", side_effect=fake_http(calls)):
            self.client.post("/connexion/", {"phone": "0505050505"})
        body = json.loads(calls[-1][3])["outboundSMSMessageRequest"]
        self.assertNotIn("senderName", body)

    def test_echec_affiche_un_message(self):
        with mock.patch("game.sms._http", side_effect=sms.SmsError("HTTP 400")):
            r = self.client.post("/connexion/", {"phone": "0707070707"})
        self.assertContains(r, "Le SMS n&#x27;a pas pu partir")
        self.assertEqual(SmsEnvoi.objects.get().status, "failed")

    @override_settings(ORANGE_DLR_USER="orange-dlr", ORANGE_DLR_PASSWORD="motdepasse")
    def test_accuse_de_reception(self):
        SmsEnvoi.objects.create(phone="0707070707", operateur="orange", resource_id="abc123")
        body = json.dumps({"deliveryInfoNotification": {"callbackData": "abc123", "deliveryInfo": {
            "address": "tel:+2250707070707", "deliveryStatus": "DeliveredToTerminal"}}})
        self.assertEqual(self.client.post("/sms/orange/accuse/", body, content_type="application/json").status_code, 401)
        auth = "Basic " + base64.b64encode(b"orange-dlr:motdepasse").decode()
        r = self.client.post("/sms/orange/accuse/", body, content_type="application/json", HTTP_AUTHORIZATION=auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(SmsEnvoi.objects.get().status, "DeliveredToTerminal")

    def test_commande_de_test(self):
        calls = []
        with mock.patch("game.sms._http", side_effect=fake_http(calls)):
            call_command("tester_sms", "0707070707", "0101010101", verbosity=0)
        self.assertEqual(SmsEnvoi.objects.filter(kind="test").count(), 2)


class ConsoleTests(TestCase):
    def test_sans_prestataire_rien_ne_part(self):
        with mock.patch("game.sms._http") as http:
            self.client.post("/connexion/", {"phone": "0707070707"})
        http.assert_not_called()
        self.assertEqual(SmsEnvoi.objects.get().provider, "console")
