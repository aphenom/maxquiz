"""Normalise une fois les téléphones déjà en base (« +225 07 07… » -> « 0707070707 »).
Tourne tout seul au déploiement (build.sh lance migrate) : pas besoin de shell."""
import re

from django.db import migrations


def _norm(raw):
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("00225"):
        digits = digits[5:]
    elif digits.startswith("225") and len(digits) in (12, 13):
        digits = digits[3:]
    if len(digits) == 9:
        digits = "0" + digits
    return digits if len(digits) == 10 else None


def forwards(apps, schema_editor):
    Player = apps.get_model("game", "Player")
    Membership = apps.get_model("game", "Membership")
    taken = set(Player.objects.values_list("phone", flat=True))
    for p in Player.objects.all():
        n = _norm(p.phone)
        if n and n != p.phone and n not in taken:   # doublon éventuel : laissé tel quel, à fusionner à la main
            taken.discard(p.phone); taken.add(n)
            p.phone = n
            p.save(update_fields=["phone"])
    for m in Membership.objects.all():
        n = _norm(m.phone)
        if n and n != m.phone and not Membership.objects.filter(
                space_id=m.space_id, license_id=m.license_id, phone=n).exists():
            m.phone = n
            m.save(update_fields=["phone"])


class Migration(migrations.Migration):
    dependencies = [("game", "0018_auditlog_remove_quiz_unique_global_quiz_slug_and_more")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
