"""Cours (PDF / vidéo YouTube lue dans la plateforme) et séances en direct
payantes (YouTube Live ou Jitsi intégrés, ou lien externe) avec différé."""
from datetime import datetime

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import learning
from .models import Lesson, LiveSession, Quiz, SessionBooking, Theme, youtube_id
from .subscriptions import access_status, current_membership
from .views import _dashboard_gate, _log_action, _player, _space
from .views_school import _staff, _teacher_subjects


# --- Élève : cours ---------------------------------------------------------------
def lessons_list(request, slug):
    space = _space(slug)
    player = _player(request)
    membership = current_membership(space, player)
    if space.members_only and not membership:
        return redirect("student_login", slug=slug)
    return render(request, "game/lessons_list.html", {
        "space": space, "player": player, "tab": "lessons",
        "subjects": learning.lessons_by_subject(space, membership),
        "access": access_status(space, player) if player else None,
    })


def lesson_detail(request, slug, lesson_id):
    space = _space(slug)
    player = _player(request)
    lesson = get_object_or_404(Lesson.objects.defer("pdf_data"), id=lesson_id)
    ok, reason = learning.can_open_lesson(space, player, lesson)
    if reason == "missing":
        raise Http404()
    if not ok:
        if reason == "login":
            return redirect("student_login", slug=slug)
        return redirect("space_subscribe", slug=slug)
    # Quiz pour s'entraîner sur ce chapitre juste après le cours
    if lesson.space_id:
        quizzes = list(Quiz.objects.filter(space=space, active=True, theme_id=lesson.theme_id)[:3]) if lesson.theme_id else []
    else:
        quizzes = list(Quiz.objects.filter(space__isnull=True, active=True,
                                           shared_level_name__iexact=lesson.shared_level_name,
                                           shared_subject_name__iexact=lesson.shared_subject_name,
                                           name__iexact=lesson.shared_theme_name)[:3])
    return render(request, "game/lesson_detail.html", {
        "space": space, "player": player, "lesson": lesson, "quizzes": quizzes,
        "page": request.GET.get("page", ""), "tab": "lessons",
    })


def lesson_pdf(request, slug, lesson_id):
    space = _space(slug)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    ok, _ = learning.can_open_lesson(space, _player(request), lesson)
    is_direction, teacher = _staff(request, space)
    if not (ok or ((is_direction or teacher) and lesson.space_id == space.id)) or not lesson.has_pdf:
        raise Http404()
    resp = HttpResponse(bytes(lesson.pdf_data), content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="{lesson.pdf_name}"'
    return resp


# --- Élève : séances en direct ------------------------------------------------------
def sessions_list(request, slug):
    space = _space(slug)
    player = _player(request)
    membership = current_membership(space, player)
    if not membership:
        return redirect("student_login", slug=slug)
    sessions = list(learning.upcoming_sessions(space, membership))
    rows = [{"s": s, "rights": learning.session_rights(s, membership), "left": learning.seats_left(s)}
            for s in sessions]
    return render(request, "game/sessions_list.html", {
        "space": space, "player": player, "rows": rows, "tab": "sessions",
    })


def session_detail(request, slug, session_id):
    space = _space(slug)
    player = _player(request)
    membership = current_membership(space, player)
    if not membership:
        return redirect("student_login", slug=slug)
    session = get_object_or_404(LiveSession.objects.select_related("teacher", "sub_category", "theme"),
                                id=session_id, space=space, cancelled=False)
    if request.method == "POST":
        kind = request.POST.get("kind")
        price = session.price_live if kind == "live" else session.price_replay if kind == "replay" else None
        ref = request.POST.get("payment_ref", "").strip()[:60]
        if price is None:
            messages.error(request, "Choisis le direct ou le différé.")
        elif kind == "live" and learning.seats_left(session) == 0:
            messages.error(request, "Plus de place pour le direct : le différé reste disponible.")
        elif price and len(ref) < 4:
            messages.error(request, "Saisis la référence de la transaction mobile money.")
        else:
            try:
                with transaction.atomic():
                    b = SessionBooking.objects.create(session=session, membership=membership, kind=kind,
                                                      amount=price, payment_ref=ref)
                if price == 0:
                    learning.validate_booking(b)
                    messages.success(request, "Inscription confirmée.")
                else:
                    messages.success(request, "Paiement déclaré : ton accès s'ouvre dès sa vérification.")
            except IntegrityError:
                messages.error(request, "Tu es déjà inscrit à cette formule.")
        return redirect("session_detail", slug=slug, session_id=session.id)

    rights = learning.session_rights(session, membership)
    return render(request, "game/session_detail.html", {
        "space": space, "player": player, "s": session, "rights": rights,
        "left": learning.seats_left(session), "jitsi_domain": learning.jitsi_domain(),
        "display_name": membership.full_name, "tab": "sessions",
        "chat_domain": request.get_host().split(":")[0],
    })


# --- Professeur / direction : cours et séances -------------------------------------
def _staff_or_login(request, space):
    is_direction, teacher = _staff(request, space)
    if not (is_direction or teacher):
        return None, None, redirect(f"/tableau-de-bord/connexion/?next={request.path}")
    return is_direction, teacher, None


def _parse_dt(value):
    try:
        return timezone.make_aware(datetime.strptime(value, "%Y-%m-%dT%H:%M"))
    except (TypeError, ValueError):
        return None


def staff_lessons(request, slug):
    space = _space(slug)
    is_direction, teacher, gate = _staff_or_login(request, space)
    if gate:
        return gate
    subjects = _teacher_subjects(space, is_direction, teacher)
    subject_ids = {s.id for s in subjects}
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            sub = subjects.filter(id=request.POST.get("sub_category_id") or 0).first()
            theme = Theme.objects.filter(id=request.POST.get("theme_id") or 0, sub_category=sub).first() if sub else None
            title = request.POST.get("title", "").strip()[:150]
            yt = request.POST.get("youtube_url", "").strip()
            pdf = request.FILES.get("pdf")
            if not (sub and title):
                messages.error(request, "Matière et titre sont obligatoires.")
            elif yt and not youtube_id(yt):
                messages.error(request, "Lien YouTube non reconnu (ex. : https://youtu.be/XXXXXXXXXXX).")
            elif not yt and not pdf:
                messages.error(request, "Ajoute une vidéo YouTube, une fiche PDF, ou les deux.")
            elif pdf and (pdf.size > Lesson.MAX_PDF_BYTES or not pdf.name.lower().endswith(".pdf")):
                messages.error(request, "La fiche doit être un PDF de 5 Mo maximum.")
            else:
                lesson = Lesson.objects.create(
                    space=space, sub_category=sub, theme=theme, teacher=teacher, title=title,
                    summary=request.POST.get("summary", "").strip(), youtube_url=yt,
                    pdf_name=pdf.name[:200] if pdf else "", pdf_data=pdf.read() if pdf else None,
                    free_preview=request.POST.get("free_preview") == "on")
                _log_action(space, "create", lesson, "Cours publié")
                messages.success(request, f"Cours « {lesson.title} » publié.")
        elif action in ("toggle", "preview"):
            lesson = get_object_or_404(Lesson, id=request.POST.get("lesson_id"), space=space,
                                       sub_category_id__in=subject_ids)
            if action == "toggle":
                lesson.active = not lesson.active
            else:
                lesson.free_preview = not lesson.free_preview
            lesson.save(update_fields=["active", "free_preview"])
            _log_action(space, "toggle", lesson)
        return redirect("staff_lessons", slug=slug)
    return render(request, "game/staff_lessons.html", {
        "space": space, "is_direction": is_direction, "teacher": teacher, "subjects": subjects,
        "themes": Theme.objects.filter(sub_category_id__in=subject_ids).select_related("sub_category"),
        "lessons": Lesson.objects.filter(space=space, sub_category_id__in=subject_ids)
                         .select_related("sub_category", "theme", "teacher").defer("pdf_data"),
    })


def staff_sessions(request, slug):
    space = _space(slug)
    is_direction, teacher, gate = _staff_or_login(request, space)
    if gate:
        return gate
    subjects = _teacher_subjects(space, is_direction, teacher)
    subject_ids = {s.id for s in subjects}
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            sub = subjects.filter(id=request.POST.get("sub_category_id") or 0).first()
            starts = _parse_dt(request.POST.get("starts_at"))
            provider = request.POST.get("provider", "youtube")
            stream = request.POST.get("stream_url", "").strip()
            title = request.POST.get("title", "").strip()[:150]
            if not (sub and starts and title):
                messages.error(request, "Matière, titre, date et heure sont obligatoires.")
            elif provider == "youtube" and stream and not youtube_id(stream):
                messages.error(request, "Lien YouTube Live non reconnu.")
            elif provider == "external" and not stream:
                messages.error(request, "Indique le lien Meet ou Zoom.")
            else:
                def _int(name, default):
                    v = request.POST.get(name, "")
                    return int(v) if v.isdigit() else default
                s = LiveSession.objects.create(
                    space=space, teacher=teacher, sub_category=sub, title=title,
                    theme=Theme.objects.filter(id=request.POST.get("theme_id") or 0, sub_category=sub).first(),
                    description=request.POST.get("description", "").strip(), starts_at=starts,
                    duration_min=_int("duration_min", 60), price_live=_int("price_live", 500),
                    price_replay=_int("price_replay", 300), seats=_int("seats", 0),
                    provider=provider if provider in ("youtube", "jitsi", "external") else "youtube",
                    stream_url=stream)
                _log_action(space, "create", s, "Séance programmée")
                messages.success(request, f"Séance « {s.title} » programmée le {timezone.localtime(s.starts_at):%d/%m à %H:%M}.")
        else:
            s = get_object_or_404(LiveSession, id=request.POST.get("session_id"), space=space,
                                  sub_category_id__in=subject_ids)
            if action == "links":
                stream = request.POST.get("stream_url", "").strip()
                replay = request.POST.get("replay_url", "").strip()
                if replay and not youtube_id(replay):
                    messages.error(request, "Lien du différé non reconnu (vidéo YouTube).")
                else:
                    s.stream_url, s.replay_url = stream or s.stream_url, replay or s.replay_url
                    s.save(update_fields=["stream_url", "replay_url"])
                    _log_action(space, "update", s, "Liens mis à jour")
            elif action == "cancel":
                s.cancelled = True
                s.save(update_fields=["cancelled"])
                _log_action(space, "update", s, "Séance annulée")
                messages.success(request, "Séance annulée : pense à prévenir les inscrits et à rembourser les paiements validés.")
        return redirect("staff_sessions", slug=slug)
    sessions = (LiveSession.objects.filter(space=space, sub_category_id__in=subject_ids)
                .select_related("sub_category__category", "teacher").order_by("-starts_at"))
    return render(request, "game/staff_sessions.html", {
        "space": space, "is_direction": is_direction, "teacher": teacher, "subjects": subjects,
        "themes": Theme.objects.filter(sub_category_id__in=subject_ids).select_related("sub_category"),
        "rows": [{"s": s, "booked": s.bookings.filter(status="active").count(),
                  "pending": s.bookings.filter(status="pending").count()} for s in sessions],
        "now": timezone.now(),
    })


# --- Direction : paiements des séances et revenus ----------------------------------
def dashboard_sessions(request, slug):
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    if request.method == "POST":
        b = get_object_or_404(SessionBooking, id=request.POST.get("booking_id"), session__space=space)
        if b.status == "pending":
            if request.POST.get("action") == "validate":
                learning.validate_booking(b)
                _log_action(space, "update", b, f"Paiement de séance validé ({b.amount} F, réf. {b.payment_ref})")
                messages.success(request, f"Inscription de {b.membership.full_name} validée.")
            else:
                b.status = "rejected"
                b.save(update_fields=["status"])
                _log_action(space, "update", b, f"Paiement de séance refusé (réf. {b.payment_ref})")
        return redirect("dashboard_sessions", slug=slug)
    report = learning.earnings_report(space)
    return render(request, "game/dashboard_sessions.html", {
        "space": space,
        "pending": SessionBooking.objects.filter(session__space=space, status="pending")
                   .select_related("membership", "session").order_by("created_at"),
        "report": report,
        "totals": {k: sum(r[k] for r in report) for k in ("total", "teacher_share", "school_share", "mq_share")},
    })
