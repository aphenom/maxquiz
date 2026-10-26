from django.db import migrations, models


def set_kinds(apps, schema_editor):
    Space = apps.get_model("game", "Space")
    for sp in Space.objects.all():
        sp.kind = "school" if (sp.members_only or sp.subscription_required) else "company"
        sp.save(update_fields=["kind"])


class Migration(migrations.Migration):
    dependencies = [("game", "0023_notifications_push")]

    operations = [
        migrations.AddField(model_name="space", name="kind", field=models.CharField(
            choices=[("catalog", "MaxQuiz École : élèves inscrits seuls (contenu commun)"),
                     ("school", "École partenaire"), ("company", "Entreprise (MaxQuiz Pro)")],
            default="company", max_length=10, verbose_name="Type d'espace",
            help_text="« MaxQuiz École » : l'espace unique des élèves inscrits depuis l'application. "
                      "« École partenaire » : un établissement que l'élève rejoint avec le code école. "
                      "« Entreprise » : un client MaxQuiz Pro.")),
        migrations.AddField(model_name="space", name="join_code", field=models.CharField(
            blank=True, default="", max_length=20, verbose_name="Code école",
            help_text="Code que l'élève saisit dans l'application (rubrique Moi > Mon école) pour "
                      "rejoindre cet établissement. Lettres et chiffres, sans espace. Vide = pas de rattachement.")),
        migrations.AddField(model_name="space", name="trial_enabled", field=models.BooleanField(
            default=False, verbose_name="Essai gratuit pour chaque nouvel élève",
            help_text="Chaque élève qui s'inscrit a accès à tout pendant la durée ci-dessous, sans payer.")),
        migrations.AddField(model_name="space", name="trial_days", field=models.PositiveSmallIntegerField(
            default=7, verbose_name="Durée de l'essai gratuit (jours)")),
        migrations.AlterField(model_name="space", name="name",
                              field=models.CharField(max_length=80, verbose_name="Nom")),
        migrations.AlterModelOptions(name="space", options={"verbose_name": "Espace"}),
        migrations.RunPython(set_kinds, migrations.RunPython.noop),
    ]
