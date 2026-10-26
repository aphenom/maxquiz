"""MaxQuiz École : l'élève inscrit seul depuis l'application (pub, APK).

L'élève a une fiche (Membership) dans l'espace « MaxQuiz École » (kind=catalog),
avec sa classe. Le contenu commun (quiz et cours partagés, sans espace) y
apparaît automatiquement par rapprochement des libellés de classe et de
matière (voir views.label_key). Rejoindre une école partenaire avec son code
ajoute une deuxième fiche, dans l'espace de l'école : rien n'en dépend.
"""
import re
import secrets

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import Category, Membership, Space, SubCategory

COLLEGE = ["Mathématiques", "Français", "Anglais", "Physique-Chimie", "SVT", "Histoire-Géographie"]
LYCEE_A = ["Français", "Anglais", "Histoire-Géographie", "Mathématiques"]
LYCEE_CD = ["Mathématiques", "Physique-Chimie", "SVT", "Français", "Anglais", "Histoire-Géographie"]
CLASSES = [
    ("6ème", COLLEGE), ("5ème", COLLEGE), ("4ème", COLLEGE), ("3ème", COLLEGE),
    ("2nde A", LYCEE_A), ("2nde C", LYCEE_CD),
    ("1ère A", LYCEE_A + ["Philosophie"]), ("1ère C", LYCEE_CD), ("1ère D", LYCEE_CD),
    ("Tle A", LYCEE_A + ["Philosophie"]), ("Tle C", LYCEE_CD + ["Philosophie"]),
    ("Tle D", LYCEE_CD + ["Philosophie"]),
]


def _slug(text):
    from django.utils.text import slugify
    return slugify(text)[:60] or "x"


def catalog_space():
    """L'espace MaxQuiz École, créé au premier besoin avec les classes et les
    matières du programme (modifiables ensuite dans l'administration)."""
    slug = settings.CATALOG_SPACE_SLUG
    space = Space.objects.filter(slug=slug).first()
    if space:
        return space
    with transaction.atomic():
        space = Space.objects.create(
            name="MaxQuiz École", slug=slug, kind="catalog", emoji="MQ",
            dashboard_username=f"mq-{slug}"[:30], dashboard_code=secrets.token_urlsafe(9)[:12],
            members_only=True, subscription_required=True, trial_enabled=True, trial_days=7,
            one_per_day=False, consent_required=False,
            category_label="Classe", category_label_plural="Classes",
            subcategory_label="Matière", subcategory_label_plural="Matières",
            theme_label="Chapitre", theme_label_plural="Chapitres",
            payment_instructions="Indique ton numéro MaxQuiz en motif du paiement, puis saisis "
                                 "ci-dessous la référence de la transaction reçue par SMS.")
        for i, (name, subjects) in enumerate(CLASSES):
            cat = Category.objects.create(space=space, name=name, slug=_slug(name), order=i)
            for j, subject in enumerate(subjects):
                SubCategory.objects.create(category=cat, name=subject, slug=_slug(subject), order=j)
    return space


def is_catalog(space):
    return bool(space) and space.kind == "catalog"


def student_membership(player):
    """Fiche MaxQuiz École de l'élève (la plus récente), ou None."""
    if not player:
        return None
    return (Membership.objects.filter(player=player, space__kind="catalog", space__active=True)
            .select_related("space", "category").order_by("-created_at").first())


def school_memberships(player):
    if not player:
        return []
    return list(Membership.objects.filter(player=player, space__kind="school", space__active=True)
                .select_related("space").order_by("space__name"))


def save_profile(player, first_name, category):
    """Crée ou met à jour la fiche MaxQuiz École (prénom + classe)."""
    space = catalog_space()
    m = student_membership(player)
    if m:
        m.full_name, m.category = first_name, category
        m.save(update_fields=["full_name", "category"])
    else:
        m = Membership.objects.create(space=space, player=player, full_name=first_name,
                                      phone=player.phone or "", category=category,
                                      matched_at=timezone.now())
    changed = []
    if not player.pseudo:
        player.pseudo = first_name[:30]
        changed.append("pseudo")
    if not player.full_name:
        player.full_name = first_name[:80]
        changed.append("full_name")
    if changed:
        player.save(update_fields=changed)
    return m


def clean_join_code(raw):
    return re.sub(r"[^A-Za-z0-9]", "", str(raw or "")).upper()[:20]


def join_school(player, raw_code):
    """Rattache l'élève à l'école partenaire de ce code. Renvoie (école, erreur)."""
    from .views import _current_license, label_key
    code = clean_join_code(raw_code)
    if not code:
        return None, "Saisis le code de ton école."
    school = Space.objects.filter(kind="school", active=True, join_code__iexact=code).first()
    if not school:
        return None, "Ce code ne correspond à aucune école. Vérifie-le auprès de ton école."
    if Membership.objects.filter(space=school, player=player).exists():
        return school, None
    mine = student_membership(player)
    cat = None
    if mine and mine.category_id:
        key = label_key(mine.category.name)
        cat = next((c for c in school.categories.all() if label_key(c.name) == key), None)
    Membership.objects.create(
        space=school, player=player, license=_current_license(school), category=cat,
        full_name=(mine.full_name if mine else "") or player.full_name or player.pseudo,
        phone=player.phone or "", parent_phone=mine.parent_phone if mine else "",
        matched_at=timezone.now())
    return school, None
