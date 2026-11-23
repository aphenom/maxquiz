"""Contrôle de santé de MaxQuiz, à lancer toutes les 10 minutes (cron) :

  - la base de données répond (sinon la commande échoue et cron le note) ;
  - place libre sur le disque ;
  - la tâche des rappels (envoyer_rappels) est passée il y a moins de 30 minutes ;
  - les SMS de la dernière heure ne sont pas majoritairement en échec ;
  - pas de paiements Jèko bloqués « en cours » depuis plus de 2 heures ;
  - chaque matin vers 7 h : bilan des dernières 24 heures envoyé à l'équipe.
Un problème crée (ou relance) un incident « Santé du site » et prévient l'équipe.
"""
import shutil
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count, Sum
from django.utils import timezone

from game import incidents
from game.models import Incident, IncidentEvent, Pouls, SmsEnvoi, Subscription


def _alerte(titre, detail, cle):
    """Un incident de santé par problème et par jour : on ne relance pas toutes les 10 minutes."""
    return incidents.enregistrer("sante", titre, detail=detail, infos={},
                                 sig=incidents.signature("sante", cle, timezone.localdate().isoformat()))


class Command(BaseCommand):
    help = "Vérifie la santé du site et prévient l'équipe en cas de problème."

    def handle(self, *args, **opts):
        settings.PUSH_SYNC = True                 # la commande s'arrête juste après : envoyer avant
        now = timezone.now()
        problemes = []

        usage = shutil.disk_usage(settings.BASE_DIR)
        libre_go = usage.free / 1024 ** 3
        if libre_go < 1 or usage.free / usage.total < 0.08:
            problemes.append(_alerte("Disque presque plein",
                                     f"Il reste {libre_go:.1f} Go libres sur {usage.total / 1024 ** 3:.0f} Go.", "disque"))

        rappels = Pouls.objects.filter(nom="rappels").first()
        if rappels and rappels.dernier < now - timedelta(minutes=30):
            problemes.append(_alerte("La tâche des rappels ne tourne plus",
                                     f"Dernier passage : {timezone.localtime(rappels.dernier):%d/%m %H:%M}. "
                                     "Vérifier /etc/cron.d/maxquiz.", "rappels"))

        sms = SmsEnvoi.objects.filter(created_at__gte=now - timedelta(hours=1)).exclude(provider="console")
        n, echecs = sms.count(), sms.filter(status__in=("failed", "DeliveryImpossible")).count()
        if n >= 3 and echecs / n > 0.5:
            derniere = sms.filter(status="failed").exclude(error="").values_list("error", flat=True).first() or ""
            problemes.append(_alerte("Les SMS de connexion échouent",
                                     f"{echecs} échecs sur {n} SMS dans la dernière heure. {derniere}", "sms"))

        bloques = Subscription.objects.filter(provider="jeko", status="initiated",
                                              created_at__lte=now - timedelta(hours=2),
                                              created_at__gte=now - timedelta(days=1)).count()
        if bloques >= 3:
            problemes.append(_alerte("Paiements Jèko sans confirmation",
                                     f"{bloques} paiements en cours depuis plus de 2 heures : vérifier le webhook "
                                     "Jèko (ou lancer maxquiz jeko_verifier).", "jeko"))

        # Ménage : occurrences de plus de 60 jours
        IncidentEvent.objects.filter(created_at__lt=now - timedelta(days=60)).delete()

        local = timezone.localtime(now)
        bilan = Pouls.objects.filter(nom="bilan").first()
        if local.hour == 7 and (not bilan or timezone.localtime(bilan.dernier).date() != local.date()):
            self.bilan_du_matin(now)
            incidents.battement("bilan")
        incidents.battement("sante")
        self.stdout.write(f"Santé : {len([p for p in problemes if p])} problème(s).")

    def bilan_du_matin(self, now):
        depuis = now - timedelta(hours=24)
        recents = Incident.objects.filter(last_seen__gte=depuis)
        par_type = {r["kind"]: r for r in recents.values("kind").annotate(n=Count("id"), u=Sum("users"))}
        ouverts = Incident.objects.exclude(status="resolu").filter(kind__in=("serveur", "page", "sante")).count()
        lent = (IncidentEvent.objects.filter(created_at__gte=depuis, incident__kind="lenteur")
                .values("incident__page").annotate(n=Count("id")).order_by("-n").first())
        sms = SmsEnvoi.objects.filter(created_at__gte=depuis).exclude(provider="console")
        recus = sms.filter(status="DeliveredToTerminal").count()
        lignes = [f"{dict(Incident.KINDS)[k]} : {v['n']} ({v['u'] or 0} utilisateurs)" for k, v in par_type.items()]
        texte = (" · ".join(lignes) if lignes else "Aucun incident ces dernières 24 heures 👍")
        texte += f". Incidents non résolus : {ouverts}."
        if lent:
            texte += f" Page la plus lente : {lent['incident__page']} ({lent['n']} fois)."
        if sms.count():
            texte += f" SMS reçus : {round(100 * recus / sms.count())} % de {sms.count()}."
        incidents.prevenir_equipe("☀️ Bilan MaxQuiz des dernières 24 h", texte, "/admin/game/incident/")
