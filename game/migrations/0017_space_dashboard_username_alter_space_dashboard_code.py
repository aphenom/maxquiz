# Ajout d'un identifiant de tableau de bord distinct du slug : en 3 étapes
# (colonne non-unique -> backfill Python -> contrainte unique) car un default
# callable ne peut pas être évalué en une seule passe SQL pour des lignes
# existantes (voir https://docs.djangoproject.com/en/6.0/howto/writing-migrations/#migrations-that-add-unique-fields).

import random

import game.models
from django.db import migrations, models

# Copie autonome de game.models._generate_dashboard_username, sans dépendre du
# modèle "vivant" (qui pourrait évoluer indépendamment de cette migration figée).
_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _backfill_dashboard_username(apps, schema_editor):
    Space = apps.get_model("game", "Space")
    used = set(Space.objects.exclude(dashboard_username="").values_list("dashboard_username", flat=True))
    for space in Space.objects.all():
        value = "".join(random.choices(_ALPHABET, k=8))
        while value in used:
            value = "".join(random.choices(_ALPHABET, k=8))
        used.add(value)
        space.dashboard_username = value
        space.save(update_fields=["dashboard_username"])


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_alter_space_dashboard_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='dashboard_username',
            field=models.CharField(
                default="", blank=True, max_length=30,
                verbose_name='Identifiant du tableau de bord'),
        ),
        migrations.RunPython(_backfill_dashboard_username, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='space',
            name='dashboard_username',
            field=models.CharField(
                default=game.models._generate_dashboard_username, max_length=30, unique=True,
                help_text="Généré automatiquement à la création, distinct du slug d'URL — modifiable si "
                          "besoin. Avec le mot de passe ci-dessous, sert à se connecter sur la page de "
                          "connexion commune à tous les établissements.",
                verbose_name='Identifiant du tableau de bord'),
        ),
        migrations.AlterField(
            model_name='space',
            name='dashboard_code',
            field=models.CharField(
                max_length=20,
                help_text="Avec l'identifiant du tableau de bord ci-dessus, sert à se connecter sur la "
                          "page de connexion commune à tous les établissements. Modifiable ensuite par "
                          "l'établissement lui-même depuis son tableau de bord (l'ancien mot de passe lui "
                          "sera demandé).",
                verbose_name='Mot de passe du tableau de bord'),
        ),
    ]
