"""Ajoute l'EDHC (Éducation aux droits de l'homme et à la citoyenneté) aux classes
du collège de l'espace MaxQuiz École déjà créé (les nouveaux espaces l'ont d'office)."""
from django.conf import settings
from django.db import migrations

COLLEGE = ["6ème", "5ème", "4ème", "3ème"]


def add_edhc(apps, schema_editor):
    Space = apps.get_model("game", "Space")
    Category = apps.get_model("game", "Category")
    SubCategory = apps.get_model("game", "SubCategory")
    space = Space.objects.filter(slug=getattr(settings, "CATALOG_SPACE_SLUG", "maxquiz")).first()
    if not space:
        return
    for cat in Category.objects.filter(space=space, name__in=COLLEGE):
        if SubCategory.objects.filter(category=cat, name__iexact="EDHC").exists():
            continue
        last = SubCategory.objects.filter(category=cat).order_by("-order").first()
        SubCategory.objects.create(category=cat, name="EDHC", slug="edhc",
                                   order=(last.order + 1) if last else 0)


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0026_paiement_appli_play"),
    ]

    operations = [
        migrations.RunPython(add_edhc, migrations.RunPython.noop),
    ]
