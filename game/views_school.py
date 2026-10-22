"""Vues de l'offre école : connexion élève par matricule + PIN, codes PIN et
coupons, équipe pédagogique, ressources des professeurs, bilans parents."""
import csv
import secrets
from datetime import timedelta

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from django.urls import reverse

from .push import direction_of, notify, students_of
from . import school
from .models import Membership, Resource, SubCategory, Teacher, Theme
from .views import _dashboard_gate, _log_action, _rows_from_upload, _space


# --- Accès du personnel ---------------------------------------------------------
def _staff(request, space):
    """(is_direction, teacher) : direction = identifiant de l'établissement ou
    compte enseignant de rôle direction. (False, None) = personne."""
    teacher = None
    tid = request.session.get("teacher_id")
    if tid:
        teacher = Teacher.objects.filter(id=tid, space=space, active=True).first()
    is_direction = (request.session.get(f"dash_{space.id}") == space.dashboard_code
                    or bool(teacher and teacher.role == "direction"))
    return is_direction, teacher


def _teacher_subjects(space, is_direction, teacher):
    if is_direction or not teacher:
        return SubCategory.objects.filter(category__space=space).select_related("category")
    return teacher.sub_categories.filter(category__space=space).select_related("category")


# --- Connexion élève : matricule + PIN -------------------------------------------
def student_login(request, slug):
    space = _space(slug)
    error = None
    if request.method == "POST":
        if not request.session.session_key:
            request.session.save()
        member, error = school.authenticate_pin(
            request, space, request.POST.get("matricule", ""), request.POST.get("pin", ""))
        if member:
            player = school.player_for(member)
            request.session["player_id"] = player.id
            request.session["verified_player_id"] = player.id
            return redirect("space_home", slug=slug)
    return render(request, "game/student_login.html", {"space": space, "error": error, "tab": "account"})


# --- Codes PIN et coupons (direction) -----------------------------------------------
def dashboard_pins(request, slug):
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    members = list(space.members.select_related("category").order_by("category__order", "full_name"))
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "generate":
            scope = request.POST.get("scope", "missing")
            cat_id = request.POST.get("category_id") or ""
            targets = [m for m in members if m.external_ref
                       and (scope == "all" or not m.pin_hash)
                       and (not cat_id or str(m.category_id) == cat_id)]
            if not targets:
                messages.error(request, "Aucun élève concerné (un matricule est nécessaire pour un code PIN).")
                return redirect("dashboard_pins", slug=slug)
            coupons = [{"member": m, "pin": school.set_pin(m)} for m in targets]
            for c in coupons:
                _log_action(space, "update", c["member"], "Code PIN généré")
            return render(request, "game/pin_coupons.html", {
                "space": space, "coupons": coupons,
                "login_url": request.build_absolute_uri(f"/e/{space.slug}/connexion-eleve/")})
        if action == "reset":
            m = get_object_or_404(Membership, id=request.POST.get("member_id"), space=space)
            pin = school.set_pin(m)
            _log_action(space, "update", m, "Code PIN régénéré")
            return render(request, "game/pin_coupons.html", {
                "space": space, "coupons": [{"member": m, "pin": pin}],
                "login_url": request.build_absolute_uri(f"/e/{space.slug}/connexion-eleve/")})
    now = timezone.now()
    rows = [{"m": m, "has_pin": bool(m.pin_hash), "alert": school.pin_alert(m),
             "locked": bool(m.pin_locked_until and m.pin_locked_until > now)} for m in members]
    return render(request, "game/dashboard_pins.html", {
        "space": space, "rows": rows,
        "without_ref": sum(1 for m in members if not m.external_ref),
        "without_pin": sum(1 for m in members if m.external_ref and not m.pin_hash),
        "alerts": [r for r in rows if r["alert"]],
        "categories": space.categories.all(),
    })


# --- Équipe pédagogique (direction) ------------------------------------------------
def _new_password():
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    return "".join(secrets.choice(alphabet) for _ in range(10))


def _unique_username(space, full_name):
    base = (slugify(full_name).replace("-", ".")[:24] or "prof") + "." + space.slug[:10]
    username, i = base, 2
    while Teacher.objects.filter(username=username).exists():
        username, i = f"{base}{i}", i + 1
    return username


def dashboard_team(request, slug):
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    subjects = SubCategory.objects.filter(category__space=space).select_related("category")
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = request.POST.get("full_name", "").strip()[:120]
            if not name:
                messages.error(request, "Le nom est obligatoire.")
            else:
                t = Teacher(space=space, full_name=name, username=_unique_username(space, name),
                            role="direction" if request.POST.get("role") == "direction" else "teacher")
                pwd = _new_password()
                t.set_password(pwd)
                t.save()
                t.sub_categories.set(subjects.filter(id__in=request.POST.getlist("subjects")))
                _log_action(space, "create", t)
                messages.success(request, f"Compte créé pour {t.full_name}. Identifiant : {t.username} · "
                                          f"mot de passe : {pwd} (à noter maintenant, il ne sera plus affiché).")
        else:
            t = get_object_or_404(Teacher, id=request.POST.get("teacher_id"), space=space)
            if action == "reset":
                pwd = _new_password()
                t.set_password(pwd)
                t.save(update_fields=["password_hash"])
                _log_action(space, "update", t, "Mot de passe réinitialisé")
                messages.success(request, f"Nouveau mot de passe de {t.full_name} : {pwd}")
            elif action == "toggle":
                t.active = not t.active
                t.save(update_fields=["active"])
                _log_action(space, "toggle", t)
            elif action == "subjects":
                t.sub_categories.set(subjects.filter(id__in=request.POST.getlist("subjects")))
                _log_action(space, "update", t, "Matières modifiées")
        return redirect("dashboard_team", slug=slug)
    return render(request, "game/dashboard_team.html", {
        "space": space, "subjects": subjects,
        "teachers": space.teachers.prefetch_related("sub_categories").order_by("-active", "full_name"),
    })


# --- Ressources des professeurs ---------------------------------------------------
def school_resources(request, slug):
    space = _space(slug)
    is_direction, teacher = _staff(request, space)
    if not (is_direction or teacher):
        return redirect(f"/tableau-de-bord/connexion/?next={request.path}")
    subjects = _teacher_subjects(space, is_direction, teacher)
    subject_ids = {s.id for s in subjects}

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "upload":
            f = request.FILES.get("file")
            sub = subjects.filter(id=request.POST.get("sub_category_id") or 0).first()
            theme = Theme.objects.filter(id=request.POST.get("theme_id") or 0, sub_category=sub).first() if sub else None
            title = request.POST.get("title", "").strip()[:150]
            if not (f and sub and title):
                messages.error(request, "Matière, titre et fichier sont obligatoires.")
            elif f.size > Resource.MAX_BYTES:
                messages.error(request, "Fichier trop lourd (5 Mo maximum). Photographie les pages en qualité moyenne.")
            else:
                r = Resource.objects.create(
                    space=space, teacher=teacher, sub_category=sub, theme=theme, title=title,
                    note=request.POST.get("note", "").strip(), file_name=f.name[:200],
                    content_type=f.content_type or "application/octet-stream", data=f.read())
                _log_action(space, "create", r, "Ressource déposée")
                notify(teachers=direction_of(space), kind="resource_new", title="Nouveaux exercices déposés",
                       body=f"{r.title} · {sub.name}", url=reverse("school_resources", args=[space.slug]))
                messages.success(request, f"« {r.title} » déposée. MQ la transforme en quiz, "
                                          f"tu pourras ensuite les vérifier et les valider.")
        elif action == "taught_on":
            th = get_object_or_404(Theme, id=request.POST.get("theme_id"), sub_category_id__in=subject_ids)
            th.taught_on = request.POST.get("taught_on") or None
            th.save(update_fields=["taught_on"])
        elif action in ("convert", "validate"):
            r = get_object_or_404(Resource, id=request.POST.get("resource_id"), space=space,
                                  sub_category_id__in=subject_ids)
            if action == "convert":
                if not is_direction:
                    raise Http404()
                f = request.FILES.get("questions_file")
                if not f:
                    messages.error(request, "Choisis le fichier de questions (.xlsx ou .csv).")
                else:
                    n, errors = school.import_resource_questions(r, _rows_from_upload(f))
                    if n:
                        _log_action(space, "update", r, f"{n} question(s) créée(s), en attente de validation")
                        notify(teachers=[r.teacher], kind="resource_review", title="Questions à vérifier",
                               body=f"{n} question(s) prête(s) pour « {r.title} »",
                               url=reverse("school_resources", args=[space.slug]))
                        messages.success(request, f"{n} question(s) créée(s) pour « {r.title} ». "
                                                  f"Elles seront visibles des élèves après validation du professeur.")
                    for e in errors[:10]:
                        messages.error(request, e)
            else:
                n = school.validate_resource(r)
                _log_action(space, "update", r, f"Validée : {n} question(s) visibles des élèves")
                notify(players=students_of(space, r.sub_category), kind="quiz_new",
                       title=f"Nouveaux quiz : {r.theme.name if r.theme else r.sub_category.name}",
                       body=f"{n} question(s) pour réviser ce que tu as vu en classe",
                       url=reverse("space_home", args=[space.slug]))
                messages.success(request, f"{n} question(s) de « {r.title} » sont maintenant visibles des élèves.")
        return redirect("school_resources", slug=slug)

    resources = (Resource.objects.filter(space=space, sub_category_id__in=subject_ids)
                 .select_related("sub_category", "theme", "teacher").defer("data")
                 .prefetch_related("questions"))
    return render(request, "game/school_resources.html", {
        "space": space, "teacher": teacher, "is_direction": is_direction,
        "subjects": subjects,
        "themes": Theme.objects.filter(sub_category_id__in=subject_ids).select_related("sub_category"),
        "resources": resources,
        "rhythm": school.chapter_rhythm(space, subjects),
        "late": sum(1 for r in school.chapter_rhythm(space, subjects) if r["state"] == "late"),
    })


def resource_file(request, slug, resource_id):
    space = _space(slug)
    is_direction, teacher = _staff(request, space)
    if not (is_direction or teacher):
        raise Http404()
    subject_ids = {s.id for s in _teacher_subjects(space, is_direction, teacher)}
    r = get_object_or_404(Resource, id=resource_id, space=space, sub_category_id__in=subject_ids)
    resp = HttpResponse(bytes(r.data), content_type=r.content_type)
    resp["Content-Disposition"] = f'attachment; filename="{r.file_name}"'
    return resp


# --- Bilans mensuels des parents (direction) ----------------------------------------
def dashboard_reports(request, slug):
    space = _space(slug)
    gate = _dashboard_gate(request, space)
    if gate:
        return gate
    today = timezone.localdate()
    default = (today.replace(day=1) - timedelta(days=1)) if today.day <= 10 else today
    try:
        year, month = (int(x) for x in request.GET.get("mois", f"{default:%Y-%m}").split("-"))
        school.month_bounds(year, month)
    except (ValueError, TypeError):
        year, month = default.year, default.month
    rows = school.monthly_report(space, year, month)
    if request.GET.get("export") == "csv":
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="bilans-{space.slug}-{year}-{month:02d}.csv"'
        resp.write("﻿")
        w = csv.writer(resp, delimiter=";")
        w.writerow(["Élève", "Matricule", "Téléphone parent", "Quiz", "Réussite %", "Point fort", "À revoir", "Message"])
        for r in rows:
            m = r["member"]
            w.writerow([m.full_name, m.external_ref, r["parent_phone"], r["quizzes"],
                        "" if r["pct"] is None else r["pct"], r["strong"], r["weak"], r["message"]])
        return resp
    return render(request, "game/dashboard_reports.html", {
        "space": space, "rows": rows, "mois": f"{year}-{month:02d}",
        "label": f"{school.MONTHS_FR[month - 1]} {year}",
        "active_count": sum(1 for r in rows if r["quizzes"]),
        "no_parent": sum(1 for r in rows if not r["parent_phone"]),
    })
