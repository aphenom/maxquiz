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


import io
import re as _re

import openpyxl
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import AuditLog, GameSession, Resource, Teacher, Theme
from . import school


class SchoolTests(TestCase):
    """Connexion par PIN, fratries, équipe, ressources des professeurs, bilans."""

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.space = Space.objects.create(name="Collège Test", slug="college-test", dashboard_code="secret123",
                                          members_only=True, consent_required=False, one_per_day=False)
        self.license = License.objects.create(space=self.space, period_label="2026-2027", seat_count=100,
                                              start_date=self.today - timedelta(days=30),
                                              end_date=self.today + timedelta(days=200))
        self.cat = Category.objects.create(space=self.space, name="3ème", slug="3eme")
        self.maths = SubCategory.objects.create(category=self.cat, name="Mathématiques", slug="maths")
        self.fr = SubCategory.objects.create(category=self.cat, name="Français", slug="francais")
        self.theme = Theme.objects.create(sub_category=self.maths, name="Équations", slug="equations",
                                          taught_on=self.today - timedelta(days=10))
        self.m1 = Membership.objects.create(space=self.space, license=self.license, full_name="Kouassi Aya",
                                            phone="0707070707", external_ref="M001", category=self.cat,
                                            parent_phone="0505050505")

    def _dash(self):
        s = self.client.session
        s[f"dash_{self.space.id}"] = self.space.dashboard_code
        s.save()

    # --- PIN -------------------------------------------------------------------
    def test_pin_generation_login_and_hash(self):
        self._dash()
        r = self.client.post(reverse("dashboard_pins", args=[self.space.slug]), {"action": "generate", "scope": "missing"})
        pin = _re.search(r'class="pin">(\d{6})<', r.content.decode()).group(1)
        self.m1.refresh_from_db()
        self.assertNotIn(pin, self.m1.pin_hash)               # stocké haché
        self.client.logout()
        r = self.client.post(reverse("student_login", args=[self.space.slug]), {"matricule": "m001", "pin": pin})
        self.assertRedirects(r, reverse("space_home", args=[self.space.slug]), fetch_redirect_response=False)
        self.m1.refresh_from_db()
        self.assertIsNotNone(self.m1.player_id)
        self.assertIsNone(self.m1.player.phone)               # compte propre à l'élève

    def test_pin_lock_is_temporary(self):
        school.set_pin(self.m1)
        url = reverse("student_login", args=[self.space.slug])
        for _ in range(5):
            self.client.post(url, {"matricule": "M001", "pin": "000000"})
        self.m1.refresh_from_db()
        self.assertIsNotNone(self.m1.pin_locked_until)
        self.assertLessEqual(self.m1.pin_locked_until, timezone.now() + timedelta(minutes=16))
        r = self.client.post(url, {"matricule": "M001", "pin": "000000"})
        self.assertContains(r, "Réessaie dans")

    def test_device_limit(self):
        url = reverse("student_login", args=[self.space.slug])
        for _ in range(school.DEVICE_MAX_FAILS_PER_HOUR):
            self.client.post(url, {"matricule": "INCONNU", "pin": "000000"})
        r = self.client.post(url, {"matricule": "INCONNU", "pin": "000000"})
        self.assertContains(r, "depuis cet appareil")

    # --- Fratrie -----------------------------------------------------------------
    def test_import_siblings_same_phone_with_matricule(self):
        self._dash()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Nom complet*", "Téléphone (élève)", "Matricule", "Niveau", "Matière", "Téléphone du parent"])
        ws.append(["Yao Koffi", "0101010101", "M010", "3ème", "", "0101010101"])
        ws.append(["Yao Ama", "0101010101", "M011", "3ème", "", "0101010101"])
        ws.append(["Sans Rien", "", "", "3ème", "", ""])
        buf = io.BytesIO(); wb.save(buf)
        f = SimpleUploadedFile("eleves.xlsx", buf.getvalue())
        r = self.client.post(reverse("dashboard_members", args=[self.space.slug]),
                             {"action": "import_csv", "csv_file": f}, follow=True)
        self.assertEqual(Membership.objects.filter(phone="0101010101").count(), 2)
        self.assertContains(r, "ni téléphone ni matricule")
        # un compte joueur avec ce numéro ne s'approprie pas les deux fiches
        p = Player.objects.create(pseudo="Parent", phone="0101010101")
        from .views import _match_by_phone
        _match_by_phone(Membership.objects.filter(space=self.space), "0101010101", p)
        self.assertFalse(Membership.objects.filter(player=p).exists())

    # --- Équipe et ressources ----------------------------------------------------
    def _teacher(self, role="teacher"):
        t = Teacher(space=self.space, full_name="M. Kouadio", username="kouadio.test", role=role)
        t.set_password("motdepasse1")
        t.save()
        t.sub_categories.set([self.maths])
        return t

    def test_team_creation_shows_password_once(self):
        self._dash()
        r = self.client.post(reverse("dashboard_team", args=[self.space.slug]),
                             {"action": "add", "full_name": "Mme Traoré", "role": "teacher",
                              "subjects": [self.fr.id]}, follow=True)
        t = Teacher.objects.get(full_name="Mme Traoré")
        pwd = _re.search(r"mot de passe : (\w+)", r.content.decode()).group(1)
        self.assertTrue(t.check_password(pwd))
        self.assertEqual(list(t.sub_categories.all()), [self.fr])

    def test_teacher_login_cannot_open_direction_pages(self):
        self._teacher()
        r = self.client.post(reverse("dashboard_login_common"), {"identifiant": "kouadio.test", "password": "motdepasse1"})
        self.assertRedirects(r, reverse("school_resources", args=[self.space.slug]), fetch_redirect_response=False)
        r = self.client.get(reverse("dashboard_pins", args=[self.space.slug]))
        self.assertEqual(r.status_code, 302)

    def test_resource_flow_upload_convert_validate(self):
        t = self._teacher()
        self.client.post(reverse("dashboard_login_common"), {"identifiant": "kouadio.test", "password": "motdepasse1"})
        url = reverse("school_resources", args=[self.space.slug])
        # rythme : chapitre en retard tant que rien n'est déposé
        self.assertContains(self.client.get(url), "en retard")
        # le prof ne peut pas déposer dans une matière qui n'est pas la sienne
        self.client.post(url, {"action": "upload", "sub_category_id": self.fr.id, "title": "X",
                               "file": SimpleUploadedFile("x.pdf", b"%PDF")})
        self.assertFalse(Resource.objects.exists())
        self.client.post(url, {"action": "upload", "sub_category_id": self.maths.id, "theme_id": self.theme.id,
                               "title": "Série 1", "file": SimpleUploadedFile("serie1.pdf", b"%PDF-1.4 test",
                                                                            content_type="application/pdf")})
        res = Resource.objects.get()
        self.assertEqual((res.teacher, res.status), (t, "deposited"))
        r = self.client.get(reverse("resource_file", args=[self.space.slug, res.id]))
        self.assertEqual(r.content, b"%PDF-1.4 test")
        # MQ / direction transforme en quiz
        self._dash()
        csv_bytes = ("question;a;b;c;d;bonne;difficulte;explication\n"
                     "2x = 6, x = ?;3;2;6;12;A;1;On divise par 2\n"
                     "x + 5 = 9, x = ?;4;14;5;9;A;1;\n").encode("utf-8")
        self.client.post(url, {"action": "convert", "resource_id": res.id,
                               "questions_file": SimpleUploadedFile("q.csv", csv_bytes)})
        res.refresh_from_db()
        self.assertEqual(res.status, "converted")
        self.assertEqual(res.questions.filter(active=False).count(), 2)
        # le professeur valide
        self.client.post(url, {"action": "validate", "resource_id": res.id})
        res.refresh_from_db()
        self.assertEqual(res.status, "validated")
        self.assertEqual(res.questions.filter(active=True, theme=self.theme).count(), 2)
        self.assertTrue(AuditLog.objects.filter(model_name="Resource").exists())

    # --- Bilan mensuel --------------------------------------------------------------
    def test_monthly_report_message_and_whatsapp(self):
        p = Player.objects.create(pseudo="Aya", phone="0707070707")
        self.m1.player = p
        self.m1.save()
        q = [Question.objects.create(space=self.space, sub_category=self.maths, kind="quiz", category="ec",
                                     difficulty=1, text=f"Q{i}", option_a="a", option_b="b", option_c="c",
                                     option_d="d", correct=0) for i in range(4)]
        sess = GameSession.objects.create(player=p, space=self.space, mode="space", status="finished",
                                          question_ids=[x.id for x in q])
        from .models import Answer
        for i, x in enumerate(q):
            Answer.objects.create(session=sess, question=x, choice=0 if i else 1, time_ms=3000, is_correct=bool(i))
        rows = school.monthly_report(self.space, self.today.year, self.today.month)
        r = rows[0]
        self.assertEqual((r["quizzes"], r["pct"], r["weak"]), (1, 75, "Mathématiques"))
        self.assertIn("1 quiz fait, 75 %", r["message"])
        self.assertTrue(r["whatsapp"].startswith("https://wa.me/2250505050505?text="))
        self._dash()
        resp = self.client.get(reverse("dashboard_reports", args=[self.space.slug]) +
                               f"?mois={self.today:%Y-%m}&export=csv")
        self.assertIn("Kouassi Aya", resp.content.decode("utf-8"))


from .models import Lesson, LiveSession, SessionBooking, youtube_id
from . import learning


class LearningTests(TestCase):
    """Cours PDF/vidéo, lien depuis les corrections, séances en direct payantes."""

    def setUp(self):
        cache.clear()
        self.today = timezone.localdate()
        self.space = Space.objects.create(name="Collège Test", slug="college-test", dashboard_code="secret123",
                                          members_only=True, subscription_required=True,
                                          free_until=self.today - timedelta(days=1), consent_required=False,
                                          one_per_day=False, payment_number="0700000000")
        self.license = License.objects.create(space=self.space, period_label="2026-2027", seat_count=100,
                                              start_date=self.today - timedelta(days=30),
                                              end_date=self.today + timedelta(days=200))
        self.cat = Category.objects.create(space=self.space, name="3e", slug="3e")
        self.maths = SubCategory.objects.create(category=self.cat, name="Maths", slug="maths")
        self.theme = Theme.objects.create(sub_category=self.maths, name="Pythagore", slug="pythagore")
        self.player = Player.objects.create(pseudo="Aya", phone="0707070707")
        self.member = Membership.objects.create(space=self.space, license=self.license, full_name="Kouassi Aya",
                                                phone="0707070707", external_ref="M001", category=self.cat,
                                                player=self.player)
        self.teacher = Teacher(space=self.space, full_name="M. Kouadio", username="kouadio.t", role="teacher")
        self.teacher.set_password("motdepasse1")
        self.teacher.save()
        self.teacher.sub_categories.set([self.maths])
        self.lesson = Lesson.objects.create(space=self.space, sub_category=self.maths, theme=self.theme,
                                            title="Pythagore en 10 min", youtube_url="https://youtu.be/dQw4w9WgXcQ",
                                            pdf_name="fiche.pdf", pdf_data=b"%PDF-1.4 fiche")

    def _login(self):
        s = self.client.session
        s["player_id"] = self.player.id
        s["verified_player_id"] = self.player.id
        s.save()

    def _subscribe(self):
        validate(Subscription.objects.create(membership=self.member, plan="monthly", amount=2000, payment_ref="R1"))

    def test_youtube_id_forms(self):
        for url in ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=3", "https://youtu.be/dQw4w9WgXcQ",
                    "https://www.youtube.com/live/dQw4w9WgXcQ?si=x", "https://youtube.com/shorts/dQw4w9WgXcQ"):
            self.assertEqual(youtube_id(url), "dQw4w9WgXcQ")
        self.assertEqual(youtube_id("https://vimeo.com/123"), "")

    def test_lesson_requires_subscription_then_plays_inline(self):
        self._login()
        url = reverse("lesson_detail", args=[self.space.slug, self.lesson.id])
        self.assertRedirects(self.client.get(url), reverse("space_subscribe", args=[self.space.slug]),
                             fetch_redirect_response=False)
        self._subscribe()
        r = self.client.get(url)
        self.assertContains(r, "youtube-nocookie.com/embed/dQw4w9WgXcQ")
        pdf = self.client.get(reverse("lesson_pdf", args=[self.space.slug, self.lesson.id]))
        self.assertEqual(pdf["Content-Disposition"].split(";")[0], "inline")

    def test_free_preview_without_subscription(self):
        self.lesson.free_preview = True
        self.lesson.save()
        self._login()
        r = self.client.get(reverse("lesson_detail", args=[self.space.slug, self.lesson.id]))
        self.assertEqual(r.status_code, 200)

    def test_global_lesson_matches_school_labels(self):
        g = Lesson.objects.create(space=None, shared_level_name="3ème", shared_subject_name="Mathématiques",
                                  shared_theme_name="Équations", title="Équations (MQ)",
                                  youtube_url="https://youtu.be/aaaaaaaaaaa")
        titles = [l.title for grp in learning.lessons_by_subject(self.space, self.member)
                  for c in grp["chapters"] for l in c["lessons"]]
        self.assertIn(g.title, titles)
        self.assertIn(self.lesson.title, titles)

    def test_wrong_answer_links_to_lesson(self):
        self._subscribe()
        self._login()
        quiz = Quiz.objects.create(space=self.space, name="Pythagore", slug="pyth", category=self.cat,
                                   sub_category=self.maths, theme=self.theme, question_count=2, survey_every=0)
        for i in range(2):
            Question.objects.create(space=self.space, sub_category=self.maths, theme=self.theme, kind="quiz",
                                    category="ec", difficulty=1, text=f"Q{i}", option_a="a", option_b="b",
                                    option_c="c", option_d="d", correct=0, explanation="Parce que.")
        r = self.client.post(reverse("quiz_start", args=[self.space.slug, quiz.slug]))
        import json as _json
        data = _json.loads(_re.search(r'<script id="game-data" type="application/json">(.*?)</script>',
                                      r.content.decode(), _re.S).group(1))
        q0 = data["questions"][0]["id"]
        resp = self.client.post(reverse("space_answer"), data=_json.dumps(
            {"session_id": data["session_id"], "question_id": q0, "choice": 1, "time_ms": 3000}),
            content_type="application/json").json()
        self.assertEqual(resp["lesson"]["url"], reverse("lesson_detail", args=[self.space.slug, self.lesson.id]))

    def test_teacher_publishes_lesson_in_own_subject_only(self):
        self.client.post(reverse("dashboard_login_common"), {"identifiant": "kouadio.t", "password": "motdepasse1"})
        url = reverse("staff_lessons", args=[self.space.slug])
        self.client.post(url, {"action": "create", "sub_category_id": self.maths.id, "title": "Mauvais lien",
                               "youtube_url": "https://vimeo.com/1"})
        self.assertFalse(Lesson.objects.filter(title="Mauvais lien").exists())
        other = SubCategory.objects.create(category=self.cat, name="Français", slug="fr")
        self.client.post(url, {"action": "create", "sub_category_id": other.id, "title": "Hors matière",
                               "youtube_url": "https://youtu.be/bbbbbbbbbbb"})
        self.assertFalse(Lesson.objects.filter(title="Hors matière").exists())
        self.client.post(url, {"action": "create", "sub_category_id": self.maths.id, "theme_id": self.theme.id,
                               "title": "Réciproque", "youtube_url": "https://youtu.be/ccccccccccc"})
        self.assertEqual(Lesson.objects.get(title="Réciproque").teacher, self.teacher)

    # --- séances ---------------------------------------------------------------
    def _session(self, **kw):
        defaults = dict(space=self.space, teacher=self.teacher, sub_category=self.maths, title="Révision",
                        starts_at=timezone.now() + timedelta(minutes=10), duration_min=60,
                        provider="youtube", stream_url="https://www.youtube.com/live/ddddddddddd")
        defaults.update(kw)
        return LiveSession.objects.create(**defaults)

    def test_paid_live_flow_and_earnings(self):
        s = self._session()
        self._login()
        url = reverse("session_detail", args=[self.space.slug, s.id])
        self.client.post(url, {"kind": "live", "payment_ref": "OM123456"})
        b = SessionBooking.objects.get()
        self.assertEqual((b.status, b.amount), ("pending", 500))
        self.assertFalse(learning.session_rights(s, self.member)["live_open"])
        self.assertNotContains(self.client.get(url), "youtube-nocookie.com/embed/ddddddddddd")
        s2 = self.client.session
        s2[f"dash_{self.space.id}"] = self.space.dashboard_code
        s2.save()
        self.client.post(reverse("dashboard_sessions", args=[self.space.slug]), {"booking_id": b.id, "action": "validate"})
        self.assertContains(self.client.get(url), "youtube-nocookie.com/embed/ddddddddddd")   # fenêtre ouverte (10 min avant)
        rows = learning.earnings_report(self.space)
        self.assertEqual((rows[0]["teacher_share"], rows[0]["school_share"], rows[0]["mq_share"]), (300, 50, 150))

    def test_replay_after_end_and_seats(self):
        s = self._session(starts_at=timezone.now() - timedelta(hours=3), seats=1,
                          replay_url="https://youtu.be/eeeeeeeeeee")
        b = SessionBooking.objects.create(session=s, membership=self.member, kind="replay", amount=300, payment_ref="X1")
        learning.validate_booking(b)
        r = learning.session_rights(s, self.member)
        self.assertTrue(r["replay_open"])
        self.assertFalse(r["live_open"])
        other = Membership.objects.create(space=self.space, license=self.license, full_name="Yao Koffi",
                                          external_ref="M002", category=self.cat)
        SessionBooking.objects.create(session=s, membership=other, kind="live", amount=500, payment_ref="X2")
        self.assertEqual(learning.seats_left(s), 0)

    def test_free_jitsi_session_embeds_visio(self):
        s = self._session(provider="jitsi", stream_url="", price_live=0, price_replay=0)
        self.assertTrue(s.jitsi_room.startswith("maxquiz-college-test-"))
        self._login()
        r = self.client.get(reverse("session_detail", args=[self.space.slug, s.id]))
        self.assertContains(r, f"https://meet.jit.si/{s.jitsi_room}")
        self.assertContains(r, "Kouassi%20Aya")


class SmokeTests(TestCase):
    """Les pages principales s'affichent, avec ou sans école, connecté ou non."""

    def setUp(self):
        self.today = timezone.localdate()
        self.school = Space.objects.create(name="Collège", slug="college", dashboard_code="secret123",
                                           members_only=True, subscription_required=True, consent_required=False)
        self.biz = Space.objects.create(name="Banque", slug="banque", dashboard_code="secret456")
        lic = License.objects.create(space=self.school, period_label="2026-2027", seat_count=10,
                                     start_date=self.today, end_date=self.today + timedelta(days=200))
        cat = Category.objects.create(space=self.school, name="3ème", slug="3eme")
        self.player = Player.objects.create(pseudo="Aya", phone="0707070707")
        Membership.objects.create(space=self.school, license=lic, full_name="Kouassi Aya", phone="0707070707",
                                  external_ref="M1", category=cat, player=self.player)

    def test_public_and_student_pages(self):
        for url in ("/", "/e/college/", "/e/college/connexion-eleve/", "/e/banque/"):
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertRedirects(self.client.get("/classement/"), "/", fetch_redirect_response=False)
        with self.settings(JEU_PUBLIC_ACTIF=True):
            self.assertEqual(self.client.get("/classement/").status_code, 200)
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = self.player.id
        s.save()
        for url in ("/compte/", "/e/college/", "/e/college/cours/", "/e/college/seances/", "/e/college/abonnement/"):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)
        self.assertContains(self.client.get("/compte/"), "Navigation élève")   # barre élève aussi sur le compte

    def test_dashboard_menu_fits_the_client(self):
        for space, school in ((self.school, True), (self.biz, False)):
            s = self.client.session
            s[f"dash_{space.id}"] = space.dashboard_code
            s.save()
            r = self.client.get(f"/e/{space.slug}/tableau-de-bord/")
            self.assertEqual(r.status_code, 200)
            self.assertEqual("Codes PIN" in r.content.decode(), school)
            self.assertEqual("À traiter" in r.content.decode(), school)


from unittest import mock

from django.test import override_settings
from cryptography.hazmat.primitives import hashes as _h
from cryptography.hazmat.primitives.asymmetric import ec as _ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

from . import push
from .models import Notification, PushDevice
from .reminders import run_reminders

VAPID_PRIV, VAPID_PUB = push.generate_vapid_keys()


@override_settings(PUSH_SYNC=True)
class PushTests(TestCase):
    """Chiffrement Web Push (vecteur officiel RFC 8291), signature VAPID,
    abonnement des appareils, centre de notifications, déclencheurs, rappels."""

    def setUp(self):
        self.today = timezone.localdate()
        self.space = Space.objects.create(name="Collège Test", slug="college-test", dashboard_code="secret123",
                                          members_only=True, consent_required=False, payment_number="0700000000")
        lic = License.objects.create(space=self.space, period_label="2026-2027", seat_count=50,
                                     start_date=self.today - timedelta(days=30), end_date=self.today + timedelta(days=200))
        self.cat = Category.objects.create(space=self.space, name="3ème", slug="3eme")
        self.maths = SubCategory.objects.create(category=self.cat, name="Maths", slug="maths")
        self.player = Player.objects.create(pseudo="Aya", phone="0707070707")
        self.member = Membership.objects.create(space=self.space, license=lic, full_name="Kouassi Aya",
                                                phone="0707070707", external_ref="M1", category=self.cat,
                                                player=self.player)

    def _login(self):
        s = self.client.session
        s["player_id"] = s["verified_player_id"] = self.player.id
        s.save()

    def test_rfc8291_test_vector(self):
        as_priv = _ec.derive_private_key(int.from_bytes(push.b64u_dec("yfWPiYE-n46HLnH0KqZOF1fJJU3MYrct3AELtAQ-oRw"), "big"),
                                         _ec.SECP256R1())
        body = push.encrypt_payload(b"When I grow up, I want to be a watermelon",
                                    "BCVxsr7N_eNgVRqvHtD0zTZsEc6-VV-JvLexhqUzORcxaOzi6-AYWXvTBHm4bjyPjs7Vd8pZGH6SRpkNtoIAiw4",
                                    "BTBZMqHH6r4Tts7J_aSIgg", salt=push.b64u_dec("DGv6ra1nlYgDCS1FRnbzlw"), server_key=as_priv)
        self.assertEqual(push.b64u(body),
                         "DGv6ra1nlYgDCS1FRnbzlwAAEABBBP4z9KsN6nGRTbVYI_c7VJSPQTBtkgcy27mlmlMoZIIgDll6e3vCYLocInmYWAmS6TlzA"
                         "C8wEqKK6PBru3jl7A_yl95bQpu6cVPTpK4Mqgkf1CXztLVBSt2Ks3oZwbuwXPXLWyouBWLVWGNWQexSgSxsj_Qulcy4a-fN")

    @override_settings(VAPID_PRIVATE_KEY=VAPID_PRIV, VAPID_PUBLIC_KEY=VAPID_PUB)
    def test_vapid_signature_verifies(self):
        header = push.vapid_header("https://fcm.googleapis.com/fcm/send/abc")
        token = header.split("t=")[1].split(",")[0]
        head, body, sig = token.split(".")
        raw = push.b64u_dec(sig)
        der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
        pub = _ec.EllipticCurvePublicKey.from_encoded_point(_ec.SECP256R1(), push.b64u_dec(VAPID_PUB))
        pub.verify(der, f"{head}.{body}".encode(), _ec.ECDSA(_h.SHA256()))   # lève une erreur si faux
        import json as _json
        self.assertEqual(_json.loads(push.b64u_dec(body))["aud"], "https://fcm.googleapis.com")

    @override_settings(VAPID_PRIVATE_KEY=VAPID_PRIV, VAPID_PUBLIC_KEY=VAPID_PUB)
    def test_subscribe_notify_and_expired_device(self):
        self._login()
        ua = _ec.generate_private_key(_ec.SECP256R1())
        from cryptography.hazmat.primitives import serialization as _s
        p256dh = push.b64u(ua.public_key().public_bytes(_s.Encoding.X962, _s.PublicFormat.UncompressedPoint))
        import json as _json
        r = self.client.post("/api/push/subscribe/", data=_json.dumps(
            {"endpoint": "https://push.example/abc", "keys": {"p256dh": p256dh, "auth": push.b64u(b"0123456789abcdef")}}),
            content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PushDevice.objects.get().player, self.player)
        with mock.patch("game.push._post", return_value=(201, b"")) as post:
            push.notify(players=[self.player], title="Test", body="Corps", url="/x/")
        self.assertEqual(post.call_args[0][0], "https://push.example/abc")
        self.assertEqual(Notification.objects.get().pushed, 1)
        with mock.patch("game.push._post", return_value=(410, b"")):
            push.notify(players=[self.player], title="Encore")
        self.assertFalse(PushDevice.objects.get().active)          # appareil désinstallé : désactivé

    def test_notification_center_and_bell(self):
        push.notify(players=[self.player], title="Nouveau cours : Pythagore", url="/e/college-test/cours/")
        self._login()
        r = self.client.get("/e/college-test/")
        self.assertContains(r, 'class="badge">1<')
        self.assertContains(self.client.get("/notifications/"), "Nouveau cours : Pythagore")
        self.assertNotContains(self.client.get("/e/college-test/"), 'class="badge"')   # lue
        n = Notification.objects.get()
        self.assertRedirects(self.client.get(f"/notifications/{n.id}/"), "/e/college-test/cours/",
                             fetch_redirect_response=False)

    def test_lesson_publication_notifies_students(self):
        t = Teacher(space=self.space, full_name="M. Kouadio", username="k.t", role="teacher")
        t.set_password("motdepasse1")
        t.save()
        t.sub_categories.set([self.maths])
        self.client.post("/tableau-de-bord/connexion/", {"identifiant": "k.t", "password": "motdepasse1"})
        self.client.post(f"/e/college-test/ressources/cours/", {"action": "create", "sub_category_id": self.maths.id,
                                                              "title": "Pythagore", "youtube_url": "https://youtu.be/aaaaaaaaaaa"})
        self.assertTrue(Notification.objects.filter(player=self.player, kind="lesson_new").exists())

    def test_reminders_session_and_subscription(self):
        s = LiveSession.objects.create(space=self.space, sub_category=self.maths, title="Révision",
                                       starts_at=timezone.now() + timedelta(minutes=20), price_live=0)
        validate(Subscription.objects.create(membership=self.member, plan="monthly", amount=2000, payment_ref="R1"),
                 day=self.today - timedelta(days=28))
        res = run_reminders()
        self.assertEqual(res, {"sessions": 1, "subscriptions": 1})
        self.assertEqual(run_reminders(), {"sessions": 0, "subscriptions": 0})   # jamais deux fois
        kinds = set(Notification.objects.filter(player=self.player).values_list("kind", flat=True))
        self.assertEqual(kinds, {"session_soon", "sub_ending"})

    def test_pwa_files(self):
        self.assertEqual(self.client.get("/sw.js")["Service-Worker-Allowed"], "/")
        self.assertIn("standalone", self.client.get("/manifest.webmanifest").content.decode())
        with override_settings(ANDROID_PACKAGE_NAME="ci.mqtech.maxquiz", ANDROID_SHA256_FINGERPRINTS="AA:BB"):
            data = self.client.get("/.well-known/assetlinks.json").json()
        self.assertEqual(data[0]["target"]["package_name"], "ci.mqtech.maxquiz")
        self.assertEqual(self.client.get("/cron/rappels/").status_code, 404)        # sans jeton



from .models import OTPCode
from .student import catalog_space
from .subscriptions import access_status as _access


class StudentAppTests(TestCase):
    """MaxQuiz École : inscription par code SMS, classe, essai gratuit réglable,
    école facultative ; MaxQuiz Pro servi sur pro.<domaine>."""

    def setUp(self):
        self.catalog = catalog_space()
        self.third = self.catalog.categories.get(name="3ème")

    def _signup(self, phone="0707070701", name="Aya"):
        r = self.client.post("/connexion/", {"phone": phone})
        self.assertRedirects(r, reverse("student_code"), fetch_redirect_response=False)
        code = OTPCode.objects.filter(phone=phone).latest("created_at").code
        return self.client.post("/connexion/code/", {"code": code})

    def test_products_by_host(self):
        self.assertContains(self.client.get("/"), "Commencer")
        r = self.client.get("/", HTTP_HOST="pro.maxquiz.net")
        self.assertContains(r, "MaxQuiz Pro")
        self.assertContains(r, "bientôt")
        with self.settings(PRO_ACTIF=True):
            self.assertContains(self.client.get("/", HTTP_HOST="pro.maxquiz.net"), "Accéder à mon espace")
        self.assertRedirects(self.client.get("/defi-du-jour/"), "/", fetch_redirect_response=False)

    def test_signup_then_return_by_sms_code(self):
        r = self._signup()
        self.assertRedirects(r, reverse("student_profile"), fetch_redirect_response=False)
        r = self.client.post(reverse("student_profile"), {"first_name": "Aya", "category": self.third.id})
        self.assertRedirects(r, f"/e/{self.catalog.slug}/", fetch_redirect_response=False)
        m = Membership.objects.get(space=self.catalog, player__phone="0707070701")
        self.assertEqual((m.full_name, m.category), ("Aya", self.third))
        home = self.client.get(f"/e/{self.catalog.slug}/")
        self.assertContains(home, "Essai gratuit : encore 7 jours")
        self.assertContains(home, "Moi")
        self.assertContains(self.client.get("/moi/"), "Mon école")
        self.client.post(reverse("student_logout"))
        r = self._signup()                       # même chemin pour revenir : directement l'accueil
        self.assertRedirects(r, f"/e/{self.catalog.slug}/", fetch_redirect_response=False)
        self.assertEqual(Membership.objects.filter(space=self.catalog).count(), 1)

    def test_trial_is_set_in_admin(self):
        self._signup()
        self.client.post(reverse("student_profile"), {"first_name": "Aya", "category": self.third.id})
        player = Player.objects.get(phone="0707070701")
        self.assertTrue(_access(self.catalog, player)["ok"])
        m = Membership.objects.get(space=self.catalog, player=player)
        Membership.objects.filter(id=m.id).update(created_at=timezone.now() - timedelta(days=7))
        self.assertFalse(_access(self.catalog, player)["ok"])       # 7 jours écoulés
        self.catalog.trial_days = 30
        self.catalog.save()
        self.assertTrue(_access(self.catalog, player)["ok"])
        self.catalog.trial_enabled = False
        self.catalog.save()
        self.assertEqual(_access(self.catalog, player)["reason"], "no_subscription")

    def test_join_school_with_code_is_optional(self):
        school = Space.objects.create(name="Collège La Réussite", slug="reussite", dashboard_code="x1234567",
                                      kind="school", join_code="REUSSITE", members_only=True,
                                      subscription_required=True, consent_required=False)
        cat = Category.objects.create(space=school, name="3e", slug="3e")
        self._signup()
        self.client.post(reverse("student_profile"), {"first_name": "Aya", "category": self.third.id})
        player = Player.objects.get(phone="0707070701")
        self.assertFalse(_access(school, player)["ok"])
        self.client.post("/moi/", {"action": "school", "join_code": "faux"})
        self.assertFalse(Membership.objects.filter(space=school).exists())
        self.client.post("/moi/", {"action": "school", "join_code": " reussite "})
        m = Membership.objects.get(space=school, player=player)
        self.assertEqual(m.category, cat)                        # « 3ème » = « 3e »
        self.assertTrue(_access(school, player)["ok"])           # l'essai MaxQuiz École ouvre l'école
        self.client.post("/moi/", {"action": "parent", "parent_phone": "05 05 05 05 05"})
        self.assertEqual(Membership.objects.get(space=self.catalog, player=player).parent_phone, "0505050505")


import json
from .meta import build_event
from .models import AdAttribution, Subscription
from .subscriptions import validate as _validate


@override_settings(META_PIXEL_ID="123456", META_CAPI_TOKEN="tok", META_SYNC=True, SITE_URL="https://maxquiz.net")
class AdsTrackingTests(TestCase):
    """Pixel Meta + API Conversions : provenance, consentement, achat au paiement validé,
    aucune donnée personnelle de l'élève envoyée."""

    def setUp(self):
        self.catalog = catalog_space()
        self.third = self.catalog.categories.get(name="3ème")

    def _signup(self, consent=True):
        if consent:
            self.client.cookies["mq_consent"] = "1"
        self.client.get("/?utm_source=facebook&utm_campaign=rentree&utm_content=video-aya&fbclid=ABC123")
        self.client.post("/connexion/", {"phone": "0707070701"})
        code = OTPCode.objects.filter(phone="0707070701").latest("created_at").code
        self.client.post("/connexion/code/", {"code": code})
        return self.client.post(reverse("student_profile"), {"first_name": "Aya", "category": self.third.id})

    def test_attribution_events_and_purchase(self):
        with mock.patch("game.meta._post", return_value=200) as post:
            self._signup()
            a = AdAttribution.objects.get(player__phone="0707070701")
            self.assertEqual((a.utm_campaign, a.utm_content, a.consent), ("rentree", "video-aya", True))
            self.assertTrue(a.fbc.endswith(".ABC123"))
            names = [c.args[0]["data"][0]["event_name"] for c in post.call_args_list]
            self.assertEqual(names, ["CompleteRegistration", "StartTrial"])
            sent = json.dumps([c.args[0] for c in post.call_args_list])
            for private in ("0707070701", "Aya", "3ème"):
                self.assertNotIn(private, sent)          # rien sur l'élève
            home = self.client.get(f"/e/{self.catalog.slug}/")
            self.assertContains(home, "fbevents.js")
            self.assertContains(home, "CompleteRegistration")    # rejoué par le pixel, même event_id
            m = Membership.objects.get(space=self.catalog, player__phone="0707070701")
            sub = Subscription.objects.create(membership=m, plan="yearly", amount=15000, payment_ref="OM123")
            post.reset_mock()
            _validate(sub)
            ev = post.call_args.args[0]["data"][0]
            self.assertEqual((ev["event_name"], ev["event_id"], ev["custom_data"]),
                             ("Purchase", f"sub-{sub.id}", {"value": 15000, "currency": "XOF"}))
        s = self.client.session
        s[f"dash_{self.catalog.id}"] = self.catalog.dashboard_code
        s.save()
        r = self.client.get(f"/e/{self.catalog.slug}/tableau-de-bord/pubs/")
        self.assertContains(r, "rentree")
        self.assertContains(r, "15000 F")

    def test_no_consent_no_sending(self):
        with mock.patch("game.meta._post", return_value=200) as post:
            self._signup(consent=False)
            self.assertFalse(post.called)
        home = self.client.get(f"/e/{self.catalog.slug}/")
        self.assertNotContains(home, "fbevents.js\");")
        self.assertContains(home, "On mesure l'efficacité de nos publicités")

    def test_event_payload_shape(self):
        a = AdAttribution(fbc="fb.1.1.X", fbp="fb.1.2.Y", user_agent="UA", ip="1.2.3.4", consent=True)
        ev = build_event("Purchase", "sub-1", a, value=2000, source_url="https://maxquiz.net/x")
        self.assertEqual(ev["user_data"], {"fbc": "fb.1.1.X", "fbp": "fb.1.2.Y",
                                           "client_user_agent": "UA", "client_ip_address": "1.2.3.4"})
        self.assertEqual(ev["action_source"], "website")
