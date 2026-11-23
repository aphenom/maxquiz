"""Incidents : erreurs du serveur et des pages, lenteurs, santé du site, alertes et suivi."""
import json
from datetime import timedelta
from unittest import mock

from django.core.management import call_command
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import include, path
from django.utils import timezone

from game import incidents
from game.models import Incident, IncidentEvent, Notification, Player, Pouls


def boom(request):
    raise ValueError("division impossible")


def lent(request):
    return HttpResponse("ok")


from django.contrib import admin  # noqa: E402

urlpatterns = [path("boom/", boom), path("lent/", lent), path("admin/", admin.site.urls),
               path("", include("game.urls"))]
handler500 = "game.views_incidents.erreur_500"


@override_settings(ROOT_URLCONF="game.tests_incidents", INCIDENTS_ALERT_PHONES="0707999999", PUSH_SYNC=True,
                   INCIDENTS_EMAIL="")
class IncidentsTests(TestCase):
    def setUp(self):
        incidents._alertes.update(heure=None, n=0)
        self.admin_phone = Player.objects.create(pseudo="Amos", phone="0707999999")
        self.eleve = Player.objects.create(pseudo="Awa", phone="0707000001")
        self.client.raise_request_exception = False

    def connecte(self, player):
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = player.id
        s.save()

    def test_erreur_serveur_page_amicale_incident_et_alerte(self):
        self.connecte(self.eleve)
        with mock.patch("game.push.notify") as notify:
            r = self.client.get("/boom/?code=123456")
        self.assertEqual(r.status_code, 500)
        self.assertContains(r, "L'équipe MaxQuiz a été prévenue", status_code=500)
        inc = Incident.objects.get(kind="serveur")
        self.assertIn("ValueError", inc.title)
        self.assertIn("division impossible", inc.detail)
        ev = inc.events.get()
        self.assertEqual(ev.player, self.eleve)
        self.assertNotIn("123456", ev.path)                     # pas de code de connexion enregistré
        notify.assert_called_once()
        self.assertEqual(notify.call_args.kwargs["players"], [self.admin_phone])

    def test_meme_erreur_regroupee_sans_nouvelle_alerte(self):
        with mock.patch("game.push.notify") as notify:
            self.client.get("/boom/")
            self.client.get("/boom/")
        inc = Incident.objects.get(kind="serveur")
        self.assertEqual((inc.count, Incident.objects.count()), (2, 1))
        self.assertEqual(notify.call_count, 1)

    def test_relance_quand_beaucoup_d_eleves_touches(self):
        with mock.patch("game.push.notify") as notify:
            for i in range(10):
                p = Player.objects.create(pseudo=f"E{i}", phone=f"07070001{i:02d}")
                self.connecte(p)
                self.client.get("/boom/")
        inc = Incident.objects.get()
        self.assertEqual(inc.users, 10)
        self.assertEqual(notify.call_count, 2)                    # nouveau, puis « 10 utilisateurs touchés »
        self.assertIn("10 utilisateurs", notify.call_args.kwargs["title"])

    def test_incident_resolu_qui_revient(self):
        self.client.get("/boom/")
        Incident.objects.update(status="resolu", resolved_at=timezone.now())
        with mock.patch("game.push.notify") as notify:
            self.client.get("/boom/")
        inc = Incident.objects.get()
        self.assertEqual(inc.status, "nouveau")
        self.assertIn("revenu", notify.call_args.kwargs["title"])

    def test_page_lente_cote_serveur(self):
        with mock.patch("game.incidents.LENTEUR_SERVEUR_MS", 0):
            self.client.get("/lent/")
        self.assertEqual(Incident.objects.get().kind, "lenteur")

    def envoie(self, data, **kw):
        return self.client.post("/api/incident/", json.dumps(data), content_type="application/json", **kw)

    def test_erreur_dans_la_page(self):
        r = self.envoie({"kind": "erreur", "message": "TypeError: x is undefined", "source": "/static/game/push.js?v=2",
                         "line": 40, "path": "/e/maxquiz/"})
        self.assertEqual(r.status_code, 204)
        inc = Incident.objects.get(kind="page")
        self.assertIn("x is undefined", inc.title)
        self.assertIn("push.js", inc.detail)

    def test_bruit_et_petites_lenteurs_ignores(self):
        self.envoie({"kind": "erreur", "message": "Script error.", "path": "/"})
        self.envoie({"kind": "lenteur", "ms": 3000, "path": "/"})
        self.assertFalse(Incident.objects.exists())
        self.envoie({"kind": "lenteur", "ms": 12000, "path": "/e/maxquiz/cours/"})
        self.assertEqual(Incident.objects.get().kind, "lenteur")

    def test_panne_reseau_alerte_a_partir_de_cinq_personnes(self):
        with mock.patch("game.push.notify") as notify:
            for i in range(5):
                self.envoie({"kind": "reseau", "message": "HTTP 502", "path": "/e/maxquiz/q/x/jouer/"},
                            REMOTE_ADDR=f"10.0.0.{i}")
                if i < 4:
                    notify.assert_not_called()
        self.assertEqual(notify.call_count, 1)
        self.assertEqual(Incident.objects.get().users, 5)

    def test_resolu_et_prevenir_les_eleves(self):
        self.connecte(self.eleve)
        self.client.get("/boom/")
        inc = Incident.objects.get()
        n = incidents.prevenir_utilisateurs(inc)
        self.assertEqual(n, 1)
        self.assertTrue(Notification.objects.filter(player=self.eleve, kind="incident_resolu").exists())

    def test_admin(self):
        from django.contrib.auth.models import User
        self.client.get("/boom/")
        self.client.force_login(User.objects.create_superuser("a", "a@a.a", "x"))
        self.assertContains(self.client.get("/admin/"), "Incidents")
        inc = Incident.objects.get()
        self.assertContains(self.client.get(f"/admin/game/incident/{inc.pk}/change/"), "division impossible")
        r = self.client.post("/admin/game/incident/", {"action": "resolu_et_prevenir", "_selected_action": [inc.pk]})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Incident.objects.get().status, "resolu")

    def test_sante(self):
        self.assertEqual(self.client.get("/sante/").json(), {"ok": True})

    def test_verifier_sante_rappels_arretes(self):
        Pouls.objects.create(nom="rappels", dernier=timezone.now() - timedelta(hours=2))
        with mock.patch("game.push.notify") as notify:
            call_command("verifier_sante", stdout=mock.MagicMock())
            call_command("verifier_sante", stdout=mock.MagicMock())        # pas de relance 10 min après
        inc = Incident.objects.get(kind="sante")
        self.assertIn("rappels", inc.title)
        self.assertEqual(notify.call_count, 1)
        self.assertTrue(Pouls.objects.filter(nom="sante").exists())

    def test_rappels_laissent_un_battement(self):
        with mock.patch("game.engagement.envoyer_rappels_missions", return_value=0):
            call_command("envoyer_rappels", stdout=mock.MagicMock())
        self.assertTrue(Pouls.objects.filter(nom="rappels").exists())

    def test_bilan_du_matin(self):
        self.client.get("/boom/")
        sept_heures = timezone.make_aware(timezone.datetime.combine(timezone.localdate(), timezone.datetime.min.time())
                                          .replace(hour=7, minute=5))
        with mock.patch("game.push.notify") as notify, mock.patch("django.utils.timezone.now", return_value=sept_heures):
            call_command("verifier_sante", stdout=mock.MagicMock())
        titres = [c.kwargs["title"] for c in notify.call_args_list]
        self.assertTrue(any("Bilan" in t for t in titres))
        self.assertEqual(IncidentEvent.objects.count(), 1)
