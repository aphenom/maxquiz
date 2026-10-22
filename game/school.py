"""Règles métier de l'offre école : codes PIN des élèves, rythme des
ressources des professeurs, transformation en quiz et bilan mensuel des
parents. Aucune vue ici : seulement de la logique testable."""
import calendar
import secrets
import urllib.parse
from datetime import date, timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone

from .models import Answer, GameSession, Membership, Player, Question, Resource, Theme

# --- Codes PIN des élèves -----------------------------------------------------
PIN_LENGTH = 6
LOCK_AFTER = 5                      # échecs consécutifs avant verrou
FIRST_LOCK = timedelta(minutes=15)  # 1er verrou
NEXT_LOCK = timedelta(hours=1)      # verrous suivants (jamais définitif)
ALERT_AFTER = 10                    # échecs sur 24 h : fiche signalée à l'école
IP_MAX_FAILS_PER_HOUR = 100         # large : beaucoup d'élèves derrière la même IP
DEVICE_MAX_FAILS_PER_HOUR = 20


def new_pin():
    return f"{secrets.randbelow(10 ** PIN_LENGTH):0{PIN_LENGTH}d}"


def set_pin(membership):
    """Génère un PIN, le stocke haché et remet les compteurs à zéro.
    Renvoie le PIN en clair : c'est le seul moment où il est connu (coupon)."""
    pin = new_pin()
    membership.pin_hash = make_password(pin)
    membership.pin_failed = 0
    membership.pin_failures_24h = 0
    membership.pin_locked_until = None
    membership.save(update_fields=["pin_hash", "pin_failed", "pin_failures_24h", "pin_locked_until"])
    return pin


def _client_keys(request):
    ip = (request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
          or request.META.get("REMOTE_ADDR", ""))
    device = request.session.session_key or ""
    return f"pinfail:ip:{ip}", f"pinfail:dev:{device}"


def _bump(key):
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, 3600)


def client_blocked(request):
    ip_key, dev_key = _client_keys(request)
    return (cache.get(ip_key, 0) >= IP_MAX_FAILS_PER_HOUR
            or cache.get(dev_key, 0) >= DEVICE_MAX_FAILS_PER_HOUR)


def pin_alert(membership):
    """Fiche à signaler en rouge à l'école : beaucoup d'échecs sur 24 h."""
    return (membership.pin_failures_24h >= ALERT_AFTER and membership.pin_last_failed_at
            and membership.pin_last_failed_at > timezone.now() - timedelta(hours=24))


def authenticate_pin(request, space, matricule, pin):
    """Vérifie matricule + PIN. Renvoie (membership, erreur).

    Protections : verrou temporaire par fiche (jamais définitif, pour qu'un
    camarade ne puisse pas bloquer un élève jusqu'à une intervention), limite
    par appareil et par adresse IP, compteur d'alerte sur 24 h."""
    if client_blocked(request):
        return None, "Trop d'essais depuis cet appareil. Réessaie dans une heure."
    now = timezone.now()
    m = (Membership.objects.filter(space=space, external_ref__iexact=matricule.strip())
         .exclude(pin_hash="").select_related("license").order_by("-created_at").first())
    if m and m.pin_locked_until and m.pin_locked_until > now:
        minutes = int((m.pin_locked_until - now).total_seconds() // 60) + 1
        return None, f"Trop d'essais sur ce matricule. Réessaie dans {minutes} min."
    if m and check_password(pin.strip(), m.pin_hash):
        m.pin_failed = 0
        m.pin_locked_until = None
        m.save(update_fields=["pin_failed", "pin_locked_until"])
        return m, None
    ip_key, dev_key = _client_keys(request)
    _bump(ip_key)
    _bump(dev_key)
    if m:
        if not m.pin_last_failed_at or m.pin_last_failed_at < now - timedelta(hours=24):
            m.pin_failures_24h = 0
        m.pin_failed += 1
        m.pin_failures_24h += 1
        m.pin_last_failed_at = now
        if m.pin_failed % LOCK_AFTER == 0:
            m.pin_locked_until = now + (FIRST_LOCK if m.pin_failed == LOCK_AFTER else NEXT_LOCK)
        m.save(update_fields=["pin_failed", "pin_failures_24h", "pin_last_failed_at", "pin_locked_until"])
    return None, "Matricule ou code PIN incorrect."


def player_for(membership):
    """Compte joueur propre à l'élève (créé à la première connexion par PIN)."""
    if membership.player_id:
        return membership.player
    first = (membership.full_name.split() or ["Élève"])[-1][:30]
    player = Player.objects.create(pseudo=first, full_name=membership.full_name[:80])
    membership.player = player
    membership.matched_at = timezone.now()
    membership.save(update_fields=["player", "matched_at"])
    return player


# --- Ressources des professeurs -------------------------------------------------
RESOURCE_DELAY = timedelta(days=7)


def chapter_rhythm(space, sub_categories, today=None):
    """Pour chaque chapitre des matières données : date du cours, ressources
    déposées et état (à jour, en retard, à venir, date non renseignée)."""
    today = today or timezone.localdate()
    rows = []
    themes = (Theme.objects.filter(sub_category__in=sub_categories)
              .select_related("sub_category__category")
              .annotate(n_res=Count("resources"))
              .order_by("sub_category__category__order", "sub_category__order", "taught_on", "order"))
    for th in themes:
        if th.n_res:
            state = "ok"
        elif not th.taught_on:
            state = "undated"
        elif th.taught_on + RESOURCE_DELAY < today:
            state = "late"
        else:
            state = "upcoming"
        due = th.taught_on + RESOURCE_DELAY if th.taught_on else None
        rows.append({"theme": th, "count": th.n_res, "state": state, "due": due})
    return rows


LETTERS = {"A": 0, "B": 1, "C": 2, "D": 3}


def import_resource_questions(resource, rows):
    """Crée, à partir des lignes d'un fichier (.xlsx ou .csv), les questions
    d'une ressource. Elles restent INACTIVES tant que le professeur ne les a
    pas validées. Colonnes : question;a;b;c;d;bonne;difficulte;explication
    (la 1re ligne doit être l'en-tête). Renvoie (créées, erreurs)."""
    rows = list(rows)
    if not rows:
        return 0, ["Fichier vide."]
    head = [str(h or "").strip().lower() for h in rows[0]]
    created, errors = [], []
    for n, values in enumerate(rows[1:], start=2):
        r = {h: str(v or "").strip() for h, v in zip(head, values)}
        good = r.get("bonne", "").upper()
        if not r.get("question") or good not in LETTERS or not all(r.get(x) for x in "abcd"):
            if any(r.values()):
                errors.append(f"ligne {n} : question, a/b/c/d et bonne (A à D) obligatoires")
            continue
        diff = int(r["difficulte"]) if r.get("difficulte", "").isdigit() else 1
        created.append(Question(
            space=resource.space, sub_category=resource.sub_category, theme=resource.theme,
            resource=resource, kind="quiz", category="ec", difficulty=min(max(diff, 1), 4),
            text=r["question"], option_a=r["a"][:200], option_b=r["b"][:200], option_c=r["c"][:200],
            option_d=r["d"][:200], correct=LETTERS[good], explanation=r.get("explication", ""),
            active=False))
    Question.objects.bulk_create(created)
    if created:
        resource.status = "converted"
        resource.converted_at = timezone.now()
        resource.save(update_fields=["status", "converted_at"])
    return len(created), errors


def validate_resource(resource):
    """Le professeur valide : les questions de la ressource deviennent visibles."""
    n = resource.questions.update(active=True)
    resource.status = "validated"
    resource.validated_at = timezone.now()
    resource.save(update_fields=["status", "validated_at"])
    return n


# --- Bilan mensuel des parents ----------------------------------------------------
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
             "septembre", "octobre", "novembre", "décembre"]


def month_bounds(year, month):
    return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])


def monthly_report(space, year, month):
    """Une ligne par élève inscrit : activité du mois, réussite, matière la
    plus solide et la plus fragile, et un message prêt à envoyer au parent."""
    start, end = month_bounds(year, month)
    label = f"{MONTHS_FR[month - 1]} {year}"
    rows = []
    members = (space.members.select_related("player", "category")
               .order_by("category__order", "full_name"))
    for m in members:
        answers = Answer.objects.none()
        quizzes = 0
        if m.player_id:
            sessions = GameSession.objects.filter(space=space, player_id=m.player_id, flagged=False,
                                                  day__gte=start, day__lte=end).exclude(status="playing")
            quizzes = sessions.count()
            answers = Answer.objects.filter(session__in=sessions, question__kind="quiz")
        n = answers.count()
        pct = round(100 * answers.filter(is_correct=True).count() / n) if n else None
        subjects = list(answers.exclude(question__sub_category__isnull=True)
                        .values("question__sub_category__name")
                        .annotate(n=Count("id"), ok=Count("id", filter=Q(is_correct=True)))
                        .filter(n__gte=3))
        for s in subjects:
            s["pct"] = round(100 * s["ok"] / s["n"])
        subjects.sort(key=lambda s: s["pct"])
        weak = subjects[0]["question__sub_category__name"] if subjects else ""
        strong = subjects[-1]["question__sub_category__name"] if len(subjects) > 1 else ""
        first_name = (m.full_name.split() or [""])[-1]
        if quizzes:
            msg = (f"Bonjour, voici le bilan MaxQuiz de {first_name} ({space.name}) pour {label} : "
                   f"{quizzes} quiz fait{'s' if quizzes > 1 else ''}, {pct} % de bonnes réponses.")
            if strong:
                msg += f" Point fort : {strong}."
            if weak:
                msg += f" À revoir : {weak}."
            msg += " Merci de l'encourager à continuer !"
        else:
            msg = (f"Bonjour, {first_name} n'a fait aucun quiz MaxQuiz en {label} avec {space.name}. "
                   f"Quelques minutes par semaine suffisent pour réviser ce qui est vu en classe.")
        to = m.parent_phone or ""
        wa = ""
        if to:
            wa = "https://wa.me/225" + to + "?text=" + urllib.parse.quote(msg)
        rows.append({"member": m, "quizzes": quizzes, "pct": pct, "strong": strong, "weak": weak,
                     "message": msg, "parent_phone": to, "whatsapp": wa})
    return rows
