from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (Category, License, Membership, Player, Question, Quiz, Space,
                     SubCategory, Subscription)
from .subscriptions import access_status, add_months, share_report, validate


class SubscriptionTests(TestCase):
    """Accès, abonnement individuel et part de l'établissement."""

    def setUp(self):
        self.today = timezone.localdate()
        self.space = Space.objects.create(
            name="Collège Test", slug="college-test", dashboard_code="secret123",
            members_only=True, subscription_required=True, consent_required=False,
            payment_number="0700000000", one_per_day=False)
        self.license = License.objects.create(
            space=self.space, period_label="2026-2027", seat_count=100,
            start_date=self.today - timedelta(days=30), end_date=self.today + timedelta(days=200))
        self.cat = Category.objects.create(space=self.space, name="3ème", slug="3eme")
        self.sub = SubCategory.objects.create(category=self.cat, name="Mathématiques", slug="maths")
        self.quiz = Quiz.objects.create(space=self.space, name="Équations", slug="equations",
                                        category=self.cat, sub_category=self.sub, question_count=3,
                                        survey_every=0)
        for i in range(3):
            Question.objects.create(space=self.space, sub_category=self.sub, kind="quiz", category="ec",
                                    difficulty=1, text=f"Q{i}", option_a="a", option_b="b",
                                    option_c="c", option_d="d", correct=0)
        self.player = Player.objects.create(pseudo="Aya", phone="0707070707")
        self.member = Membership.objects.create(
            space=self.space, license=self.license, full_name="Aya Kouassi", phone="0707070707",
            external_ref="M001", player=self.player, category=self.cat, sub_category=self.sub)
        self.outsider = Player.objects.create(pseudo="Inconnu", phone="0101010101")

    def _login(self, player):
        session = self.client.session
        session["player_id"] = player.id
        session["verified_player_id"] = player.id
        session.save()

    def _dash_login(self):
        session = self.client.session
        session[f"dash_{self.space.id}"] = self.space.dashboard_code
        session.save()

    # --- règles d'accès ---------------------------------------------------
    def test_outsider_is_refused(self):
        self.assertEqual(access_status(self.space, self.outsider)["reason"], "not_member")

    def test_member_without_subscription_is_refused(self):
        res = access_status(self.space, self.player)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "no_subscription")

    def test_trial_gives_access(self):
        self.space.free_until = self.today + timedelta(days=10)
        self.space.save()
        res = access_status(self.space, self.player)
        self.assertTrue(res["ok"])
        self.assertTrue(res["trial"])

    def test_trial_over_refuses(self):
        self.space.free_until = self.today - timedelta(days=1)
        self.space.save()
        self.assertFalse(access_status(self.space, self.player)["ok"])

    def test_pending_payment_does_not_give_access(self):
        Subscription.objects.create(membership=self.member, plan="monthly", amount=2000, payment_ref="REF1")
        res = access_status(self.space, self.player)
        self.assertFalse(res["ok"])
        self.assertEqual(res["reason"], "pending")

    def test_open_space_unchanged(self):
        self.space.members_only = self.space.subscription_required = False
        self.space.save()
        self.assertTrue(access_status(self.space, self.outsider)["ok"])

    # --- calcul des périodes ------------------------------------------------
    def test_add_months_end_of_month(self):
        self.assertEqual(add_months(date(2027, 1, 31), 1), date(2027, 2, 28))

    def test_monthly_period(self):
        s = validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                                 amount=2000, payment_ref="REF1"))
        self.assertEqual(s.start_date, self.today)
        self.assertEqual(s.end_date, add_months(self.today, 1) - timedelta(days=1))
        self.assertTrue(access_status(self.space, self.player)["ok"])

    def test_yearly_ends_with_school_year(self):
        s = validate(Subscription.objects.create(membership=self.member, plan="yearly",
                                                 amount=15000, payment_ref="REF2"))
        self.assertEqual(s.end_date, self.license.end_date)

    def test_early_renewal_keeps_remaining_days(self):
        first = validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                                     amount=2000, payment_ref="REF1"))
        second = validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                                      amount=2000, payment_ref="REF2"))
        self.assertEqual(second.start_date, first.end_date + timedelta(days=1))

    # --- part de l'établissement -------------------------------------------
    def test_share_counts_each_student_once_per_month(self):
        validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                             amount=2000, payment_ref="REF1"))
        validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                             amount=2000, payment_ref="REF2"))
        rows = share_report(self.space, up_to=self.today)
        self.assertEqual(rows[0]["students"], 1)
        self.assertEqual(rows[0]["share"], 500)

    # --- parcours web ---------------------------------------------------------
    def test_quiz_start_redirects_to_subscription(self):
        self._login(self.player)
        r = self.client.post(reverse("quiz_start", args=[self.space.slug, self.quiz.slug]))
        self.assertRedirects(r, reverse("space_subscribe", args=[self.space.slug]),
                             fetch_redirect_response=False)

    def test_full_flow_declare_validate_play(self):
        self._login(self.player)
        url = reverse("space_subscribe", args=[self.space.slug])
        self.assertContains(self.client.get(url), "0700000000")
        self.client.post(url, {"plan": "monthly", "payment_ref": "CI2610.ABCD", "payer_phone": "+225 05 05 05 05 05"})
        sub = Subscription.objects.get()
        self.assertEqual((sub.status, sub.amount, sub.payer_phone), ("pending", 2000, "0505050505"))
        # même référence deux fois : refusée
        self.client.post(url, {"plan": "monthly", "payment_ref": "CI2610.ABCD"})
        self.assertEqual(Subscription.objects.count(), 1)
        # validation dans le tableau de bord
        self._dash_login()
        dash = reverse("dashboard_subscriptions", args=[self.space.slug])
        self.assertContains(self.client.get(dash), "CI2610.ABCD")
        self.client.post(dash, {"sub_id": sub.id, "action": "validate"})
        sub.refresh_from_db()
        self.assertEqual(sub.status, "active")
        # l'élève peut maintenant lancer le quiz
        r = self.client.post(reverse("quiz_start", args=[self.space.slug, self.quiz.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "game-data")

    def test_dashboard_pages_need_login(self):
        r = self.client.get(reverse("dashboard_subscriptions", args=[self.space.slug]))
        self.assertEqual(r.status_code, 302)
        self.assertIn("connexion", r["Location"])

    def test_shares_export_xlsx(self):
        validate(Subscription.objects.create(membership=self.member, plan="monthly",
                                             amount=2000, payment_ref="REF1"))
        self._dash_login()
        r = self.client.get(reverse("dashboard_shares", args=[self.space.slug]) + "?export=xlsx")
        self.assertEqual(r.status_code, 200)
        self.assertIn("spreadsheetml", r["Content-Type"])

    def test_outsider_cannot_declare_level(self):
        self._login(self.outsider)
        self.client.post(reverse("space_declare_level", args=[self.space.slug]), {"category": self.cat.id})
        self.assertFalse(Membership.objects.filter(phone="0101010101").exists())
