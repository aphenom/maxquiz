"""Parcours élève MaxQuiz École (maxquiz.net) et accueil MaxQuiz Pro (pro.maxquiz.net).

Une seule porte d'entrée pour l'élève : numéro de téléphone, code reçu par SMS,
prénom et classe. Le même chemin sert à s'inscrire et à revenir.
"""
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Category, Player
from .student import (catalog_space, join_school, school_memberships, save_profile,
                      student_membership)
from .subscriptions import access_status
from .views import _check_otp, _match_by_phone, _otp_rate_limited, _send_otp, normalize_phone, OTP_WINDOW_MINUTES


def jeu_public(view):
    """Ancien jeu public (défi du jour, portefeuille, classement public) :
    hors service tant que JEU_PUBLIC_ACTIF n'est pas activé."""
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not settings.JEU_PUBLIC_ACTIF:
            return redirect("home")
        return view(request, *args, **kwargs)
    return wrapped


def _verified_player(request):
    pid = request.session.get("verified_player_id")
    return Player.objects.filter(id=pid).first() if pid else None


def _student_home_url():
    return reverse("space_home", args=[catalog_space().slug])


def home(request):
    if getattr(request, "product", "ecole") == "pro":
        return render(request, "game/pro_home.html", {
            "contact_whatsapp": "".join(c for c in settings.CONTACT_WHATSAPP if c.isdigit())})
    player = _verified_player(request)
    if player:
        if student_membership(player):
            return redirect(_student_home_url())
        return redirect("student_profile")
    space = catalog_space()
    return render(request, "game/eleve/bienvenue.html", {
        "catalog_trial_days": space.trial_days if space.trial_enabled else 0})


def student_phone(request):
    error, phone_raw = None, ""
    if request.method == "POST":
        phone_raw = request.POST.get("phone", "")
        phone = normalize_phone(phone_raw)
        if not phone:
            error = "Numéro invalide : 10 chiffres, par exemple 07 07 07 07 07."
        elif _otp_rate_limited(phone):
            error = f"Trop de codes demandés. Réessaie dans {OTP_WINDOW_MINUTES} minutes."
        else:
            code = _send_otp(phone)
            request.session["otp_phone"] = phone
            url = reverse("student_code")
            if settings.DEBUG or settings.OTP_AFFICHER_CODE:
                url += f"?dev_code={code}"
            return redirect(url)
    return render(request, "game/eleve/numero.html", {"error": error, "phone": phone_raw})


def student_code(request):
    phone = request.session.get("otp_phone")
    if not phone:
        return redirect("student_phone")
    error = None
    if request.method == "POST":
        error = _check_otp(phone, request.POST.get("code", ""))
        if not error:
            player, _ = Player.objects.get_or_create(phone=phone, defaults={"pseudo": ""})
            request.session["player_id"] = player.id
            request.session["verified_player_id"] = player.id
            request.session.pop("otp_phone", None)
            from .models import Membership
            _match_by_phone(Membership.objects.all(), phone, player)
            if student_membership(player):
                return redirect(_student_home_url())
            return redirect("student_profile")
    return render(request, "game/eleve/code.html", {
        "phone": phone, "error": error,
        "dev_code": request.GET.get("dev_code") if (settings.DEBUG or settings.OTP_AFFICHER_CODE) else None,
    })


def student_profile(request):
    """Prénom et classe : à l'inscription, puis pour changer de classe."""
    player = _verified_player(request)
    if not player:
        return redirect("student_phone")
    space = catalog_space()
    mine = student_membership(player)
    classes = list(Category.objects.filter(space=space))
    error = None
    first_name = (mine.full_name if mine else "") or player.pseudo or player.full_name
    picked = mine.category_id if mine else None
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()[:60]
        cat_id = request.POST.get("category", "")
        cat = next((c for c in classes if str(c.id) == cat_id), None)
        picked = cat.id if cat else None
        if not first_name or not cat:
            error = "Indique ton prénom et ta classe."
        else:
            save_profile(player, first_name, cat)
            if not mine:
                messages.success(request, f"Bienvenue {first_name} ! Ton essai gratuit commence aujourd'hui."
                                 if space.trial_enabled else f"Bienvenue {first_name} !")
            return redirect(_student_home_url())
    return render(request, "game/eleve/profil.html", {
        "classes": classes, "first_name": first_name, "picked": picked,
        "error": error, "editing": bool(mine),
    })


def student_me(request):
    player = _verified_player(request)
    if not player:
        return redirect("student_phone")
    mine = student_membership(player)
    if not mine:
        return redirect("student_profile")
    space = mine.space
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "parent":
            raw = request.POST.get("parent_phone", "").strip()
            parent = normalize_phone(raw) if raw else ""
            if raw and not parent:
                messages.error(request, "Numéro du parent invalide : 10 chiffres.")
            else:
                mine.parent_phone = parent
                mine.save(update_fields=["parent_phone"])
                messages.success(request, "Numéro du parent enregistré : il recevra ton bilan sur WhatsApp."
                                 if parent else "Numéro du parent retiré.")
        elif action == "school":
            school, error = join_school(player, request.POST.get("join_code", ""))
            if error:
                messages.error(request, error)
            else:
                messages.success(request, f"Tu as rejoint {school.name}.")
        return redirect("student_me")
    return render(request, "game/eleve/moi.html", {
        "player": player, "mine": mine, "space": space,
        "access": access_status(space, player),
        "schools": school_memberships(player), "tab": "me",
    })


@require_POST
def student_logout(request):
    request.session.flush()
    return redirect("home")
