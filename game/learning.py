"""Règles des cours (PDF / vidéo) et des séances en direct payantes."""
from datetime import timedelta

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from .models import Lesson, LiveSession, SessionBooking, SubCategory
from .subscriptions import access_status

JOIN_EARLY = timedelta(minutes=15)


def jitsi_domain():
    return getattr(settings, "JITSI_DOMAIN", "meet.jit.si")


# --- Périmètre d'un élève -----------------------------------------------------
def member_subjects(space, membership):
    """Matières que l'élève peut voir : sa matière précise, sinon toutes celles
    de son niveau ; sans fiche (espace ouvert), toutes celles de l'espace."""
    qs = SubCategory.objects.filter(category__space=space).select_related("category")
    if membership and membership.sub_category_id:
        return qs.filter(id=membership.sub_category_id)
    if membership and membership.category_id:
        return qs.filter(category_id=membership.category_id)
    return qs


def _global_matches(space, subjects):
    """Cours communs MQ dont le niveau/matière se rapproche d'une matière de l'élève."""
    from .views import label_key
    keys = {(label_key(s.category.name), label_key(s.name)): s for s in subjects}
    out = []
    for lesson in Lesson.objects.filter(space__isnull=True, active=True).defer("pdf_data"):
        sub = keys.get((label_key(lesson.shared_level_name), label_key(lesson.shared_subject_name)))
        if sub:
            out.append((sub, lesson))
    return out


def lessons_by_subject(space, membership):
    """[{sub, chapters: [{name, lessons}]}] : cours de l'école + cours communs."""
    subjects = list(member_subjects(space, membership))
    grouped = {s.id: {"sub": s, "chapters": {}} for s in subjects}
    own = (Lesson.objects.filter(space=space, active=True, sub_category__in=subjects)
           .select_related("theme").defer("pdf_data"))
    for lesson in own:
        chap = lesson.theme.name if lesson.theme else "Général"
        grouped[lesson.sub_category_id]["chapters"].setdefault(chap, []).append(lesson)
    for sub, lesson in _global_matches(space, subjects):
        chap = lesson.shared_theme_name or "Général"
        grouped[sub.id]["chapters"].setdefault(chap, []).append(lesson)
    return [{"sub": g["sub"], "chapters": [{"name": n, "lessons": ls} for n, ls in g["chapters"].items()]}
            for g in grouped.values() if g["chapters"]]


def lesson_visible_in(space, lesson):
    if lesson.space_id:
        return lesson.space_id == space.id
    subjects = SubCategory.objects.filter(category__space=space).select_related("category")
    return any(l.id == lesson.id for _, l in _global_matches(space, subjects))


def can_open_lesson(space, player, lesson):
    """(autorisé, raison) — cours inclus dans l'abonnement, sauf aperçu gratuit."""
    if not lesson.active or not lesson_visible_in(space, lesson):
        return False, "missing"
    if lesson.free_preview:
        return True, "free"
    if not player:
        return False, "login"
    acc = access_status(space, player)
    return acc["ok"], acc["reason"]


def lesson_for_question(question, space):
    """Cours à revoir après une erreur : celui fixé sur la question, sinon le
    cours du même chapitre (école), sinon le cours commun du chapitre du quiz
    partagé (même nom de niveau, de matière et de chapitre)."""
    if question.lesson_id and question.lesson.active:
        return question.lesson
    if question.theme_id:
        found = (Lesson.objects.filter(space=space, active=True, theme_id=question.theme_id)
                 .defer("pdf_data").first())
        if found:
            return found
    quiz = question.quiz
    if quiz and quiz.space_id is None:
        from .views import label_key
        wanted = (label_key(quiz.shared_level_name), label_key(quiz.shared_subject_name), label_key(quiz.name))
        for lesson in Lesson.objects.filter(space__isnull=True, active=True).defer("pdf_data"):
            if (label_key(lesson.shared_level_name), label_key(lesson.shared_subject_name),
                    label_key(lesson.shared_theme_name)) == wanted:
                return lesson
    return None


# --- Séances en direct -----------------------------------------------------------
def upcoming_sessions(space, membership, now=None):
    now = now or timezone.now()
    subjects = member_subjects(space, membership)
    return (LiveSession.objects.filter(space=space, cancelled=False, sub_category__in=subjects)
            .filter(Q(starts_at__gte=now - timedelta(hours=6)) | Q(bookings__membership=membership))
            .select_related("sub_category__category", "teacher", "theme").distinct().order_by("starts_at"))


def seats_left(session):
    if not session.seats:
        return None
    taken = session.bookings.filter(kind="live").exclude(status="rejected").count()
    return max(0, session.seats - taken)


def session_rights(session, membership, now=None):
    """Ce que l'élève peut voir maintenant : direct (fenêtre ouverte 15 min
    avant le début jusqu'à la fin), différé (après la fin, si disponible)."""
    now = now or timezone.now()
    rights = {"live_booked": False, "replay_booked": False, "pending": False,
              "live_open": False, "replay_open": False, "ended": now > session.ends_at,
              "window": session.starts_at - JOIN_EARLY <= now <= session.ends_at}
    if not membership:
        return rights
    bookings = list(session.bookings.filter(membership=membership))
    active = {b.kind for b in bookings if b.status == "active"}
    rights["pending"] = any(b.status == "pending" for b in bookings)
    if session.price_live == 0:
        active.add("live")
    if session.price_replay == 0:
        active.add("replay")
    rights["live_booked"] = "live" in active
    rights["replay_booked"] = bool(active)          # le direct inclut le différé
    rights["live_open"] = rights["live_booked"] and rights["window"]
    rights["replay_open"] = (rights["replay_booked"] and rights["ended"]
                             and bool(session.replay_video_id))
    return rights


def validate_booking(booking):
    booking.status = "active"
    booking.validated_at = timezone.now()
    booking.save(update_fields=["status", "validated_at"])
    return booking


def earnings_report(space, up_to=None):
    """Revenus des séances par mois et par professeur, répartis selon les
    pourcentages de l'espace (le reste revient à MQ)."""
    up_to = up_to or timezone.localdate()
    bookings = list(SessionBooking.objects.filter(session__space=space, status="active",
                                                  validated_at__isnull=False)
                    .select_related("session__teacher"))
    rows = {}
    for b in bookings:
        d = timezone.localtime(b.validated_at).date()
        if d > up_to:
            continue
        teacher = b.session.teacher.full_name if b.session.teacher else "Sans professeur"
        key = (d.year, d.month, teacher)
        r = rows.setdefault(key, {"label": f"{d.month:02d}/{d.year}", "teacher": teacher,
                                  "count": 0, "total": 0})
        r["count"] += 1
        r["total"] += b.amount
    out = []
    for key in sorted(rows):
        r = rows[key]
        r["teacher_share"] = r["total"] * space.live_teacher_share_pct // 100
        r["school_share"] = r["total"] * space.live_school_share_pct // 100
        r["mq_share"] = r["total"] - r["teacher_share"] - r["school_share"]
        out.append(r)
    return out
