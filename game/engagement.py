"""Faire revenir l'élève chaque jour : mission du jour, série de jours, rappel push.

- mission_du_jour() : UNE action, la plus utile, choisie dans cet ordre :
  quiz commencé pas terminé → révision espacée d'un chapitre raté (J+1, J+3, J+7) →
  point faible → chapitre suivant du programme → nouveau cours → entraînement.
  Elle est fixée pour la journée (table Mission).
- serie() : jours d'activité d'affilée (un quiz commencé ou un cours ouvert), avec un
  joker : un jour manqué par semaine ne casse pas la série.
- envoyer_rappels_missions() : au plus un push par jour, entre 7 h et 21 h, à l'heure
  choisie par l'élève, sinon à l'heure où il révise d'habitude, sinon 18 h 30
  (14 h 30 le mercredi). Après 3 rappels sans visite : un jour sur deux.
"""
from datetime import time, timedelta
from statistics import median

from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone

from .models import (GameSession, Lesson, LessonView, Membership, Mission, PushDevice, Quiz,
                     Rappels)

SEUIL_REUSSITE = 60            # % : en dessous, le chapitre revient en révision
JOURS_REVISION = (1, 3, 7)
HEURE_DEFAUT = time(18, 30)
HEURE_MERCREDI = time(14, 30)
PREMIERE_HEURE, DERNIERE_HEURE = time(7, 0), time(21, 0)


# --- Activité et série ---------------------------------------------------------------
def _perimetre(space):
    """Activité prise en compte : tout MaxQuiz, ou seulement ce qui se passe dans une école
    (ses quiz, ses cours) quand on calcule pour le tableau de bord de cette école."""
    if space is None or space.kind == "catalog":
        return Q(), Q()
    return Q(space=space), Q(lesson__space=space)


def jours_actifs(player, depuis, space=None):
    qs, ql = _perimetre(space)
    quiz_days = (GameSession.objects.filter(qs, player=player, day__gte=depuis)
                 .annotate(n=Count("answers")).filter(n__gt=0).values_list("day", flat=True))
    lesson_days = LessonView.objects.filter(ql, player=player, day__gte=depuis).values_list("day", flat=True)
    return set(quiz_days) | set(lesson_days)


def actif_aujourdhui(player, today=None):
    today = today or timezone.localdate()
    return today in jours_actifs(player, today)


def serie(player, today=None, space=None):
    """Nombre de jours d'activité de la série en cours. Un jour sans activité par semaine
    est toléré (joker), à condition que la veille de ce jour soit active."""
    today = today or timezone.localdate()
    days = jours_actifs(player, today - timedelta(days=90), space)
    d = today if today in days else today - timedelta(days=1)
    n, jokers = 0, set()
    while d >= today - timedelta(days=90):
        if d in days:
            n += 1
        else:
            week = d.isocalendar()[:2]
            if n and week not in jokers and (d - timedelta(days=1)) in days:
                jokers.add(week)
            else:
                break
        d -= timedelta(days=1)
    return n


# --- Ce que l'élève peut travailler ----------------------------------------------------
def _quizzes_par_matiere(space, membership):
    """[(matière, [quiz dans l'ordre du programme])] pour la classe de l'élève."""
    from .learning import member_subjects
    from .views import _global_quizzes_for, label_key
    out = []
    lessons = list(Lesson.objects.filter(space__isnull=True, active=True).defer("pdf_data")
                   .values_list("shared_level_name", "shared_subject_name", "shared_theme_name", "order"))
    for sub in member_subjects(space, membership):
        quizzes = list(Quiz.objects.filter(space=space, active=True, sub_category=sub)) \
            + list(_global_quizzes_for(sub.category, sub))
        rank = {label_key(t): o for lvl, s, t, o in lessons
                if label_key(lvl) == label_key(sub.category.name) and label_key(s) == label_key(sub.name)}
        quizzes.sort(key=lambda q: (rank.get(label_key(q.name), 999), q.name))
        if quizzes:
            out.append((sub, quizzes))
    return out


def _scores(player, space, since):
    """{session_id: (session, réponses, bonnes)} des quiz terminés ou abandonnés."""
    rows = (GameSession.objects.filter(player=player, space=space, quiz__isnull=False, started_at__gte=since)
            .annotate(n=Count("answers", filter=Q(answers__question__kind="quiz")),
                      ok=Count("answers", filter=Q(answers__is_correct=True, answers__question__kind="quiz")))
            .select_related("quiz").order_by("started_at"))
    return [(s, s.n, s.ok) for s in rows]


def _pct(n, ok):
    return round(100 * ok / n) if n else 0


def lecon_du_quiz(quiz, space):
    from .views import label_key
    if quiz.space_id:
        return (Lesson.objects.filter(space=space, active=True, theme_id=quiz.theme_id).defer("pdf_data").first()
                if quiz.theme_id else None)
    want = (label_key(quiz.shared_level_name), label_key(quiz.shared_subject_name), label_key(quiz.name))
    for lesson in Lesson.objects.filter(space__isnull=True, active=True).defer("pdf_data"):
        if (label_key(lesson.shared_level_name), label_key(lesson.shared_subject_name),
                label_key(lesson.shared_theme_name)) == want:
            return lesson
    return None


JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def _quand(day, today):
    delta = (today - day).days
    return "hier" if delta == 1 else (JOURS[day.weekday()] if delta < 7 else f"il y a {delta} jours")


def choisir_mission(player, space, membership, today=None):
    """La mission la plus utile aujourd'hui, ou None s'il n'y a rien à proposer."""
    today = today or timezone.localdate()
    now = timezone.now()
    matieres = _quizzes_par_matiere(space, membership)
    allowed = {q.id: (sub, q) for sub, qs in matieres for q in qs}
    if not allowed:
        return None
    url_quiz = lambda q: reverse("quiz_home", args=[space.slug, q.slug])
    sessions = [x for x in _scores(player, space, now - timedelta(days=60)) if x[0].quiz_id in allowed]
    best = {}                                       # quiz_id -> meilleur % obtenu
    last = {}                                       # quiz_id -> dernière partie
    for s, n, ok in sessions:
        if n:
            best[s.quiz_id] = max(best.get(s.quiz_id, 0), _pct(n, ok))
        last[s.quiz_id] = (s, n, ok)

    # 1. Quiz commencé dans les 48 h et laissé en route
    for s, n, ok in reversed(sessions):
        q = s.quiz
        if (s.status == "playing" and n and n < q.question_count and s.started_at >= now - timedelta(hours=48)
                and last[q.id][0].id == s.id):
            return dict(kind="reprendre", title=f"Termine ton quiz « {q.name} »",
                        text=f"Tu t'étais arrêté à la question {n + 1} sur {q.question_count}. Reprends-le en 5 minutes.",
                        url=url_quiz(q), cta="Reprendre le quiz")

    # 2. Révision espacée : chapitre raté il y a 1, 3 ou 7 jours, pas encore rattrapé
    for s, n, ok in reversed(sessions):
        q = s.quiz
        if n >= 5 and _pct(n, ok) < SEUIL_REUSSITE and (today - s.day).days in JOURS_REVISION:
            later_ok = any(x[0].quiz_id == q.id and x[0].started_at > s.started_at and _pct(x[1], x[2]) >= SEUIL_REUSSITE
                           for x in sessions)
            if later_ok:
                continue
            lesson = lecon_du_quiz(q, space)
            text = f"Tu avais eu {ok}/{n} {_quand(s.day, today)}. "
            if lesson:
                return dict(kind="revision", title=f"Revois « {q.name} »",
                            text=text + "Relis la fiche (3 minutes), puis refais le quiz.",
                            url=reverse("lesson_detail", args=[space.slug, lesson.id]), cta="Revoir le cours")
            return dict(kind="revision", title=f"Refais le quiz « {q.name} »", text=text + "C'est le bon moment pour retenter.",
                        url=url_quiz(q), cta="Refaire le quiz")

    # 3. Point faible : la matière la plus basse (au moins 2 quiz faits, moyenne < 60 %)
    by_sub = {}
    for qid, pct in best.items():
        by_sub.setdefault(allowed[qid][0].id, []).append(pct)
    weak = [(sum(v) / len(v), sid) for sid, v in by_sub.items() if len(v) >= 2 and sum(v) / len(v) < SEUIL_REUSSITE]
    if weak:
        _, sid = min(weak)
        sub, qs = next((sub, qs) for sub, qs in matieres if sub.id == sid)
        q = min((x for x in qs if x.id not in best), key=lambda x: 0, default=None) \
            or min((x for x in qs if x.id in best), key=lambda x: best[x.id])
        return dict(kind="point_faible", title=f"{sub.name} : « {q.name} »",
                    text=f"C'est ta matière la plus fragile en ce moment. On s'y met 5 minutes ?",
                    url=url_quiz(q), cta="Lancer le quiz")

    # 4. Chapitre suivant (une matière différente chaque jour)
    order = matieres[today.toordinal() % len(matieres):] + matieres[:today.toordinal() % len(matieres)]
    for sub, qs in order:
        q = next((x for x in qs if x.id not in last), None)
        if q:
            return dict(kind="suite", title=f"{sub.name} : « {q.name} »",
                        text=f"Nouveau chapitre pour toi · {q.question_count} questions, environ 5 minutes.",
                        url=url_quiz(q), cta="Lancer le quiz")

    # 5. Nouveau cours publié ces 3 derniers jours et pas encore ouvert
    from .learning import lessons_by_subject
    seen = set(LessonView.objects.filter(player=player).values_list("lesson_id", flat=True))
    fresh = [l for g in lessons_by_subject(space, membership) for ch in g["chapters"] for l in ch["lessons"]
             if l.created_at >= now - timedelta(days=3) and l.id not in seen]
    if fresh:
        l = max(fresh, key=lambda x: x.created_at)
        return dict(kind="cours", title=f"Nouveau cours : « {l.title} »", text="Il vient d'arriver dans ta classe.",
                    url=reverse("lesson_detail", args=[space.slug, l.id]), cta="Voir le cours")

    # 6. Tout est fait : on retravaille le chapitre le moins réussi
    if best:
        qid = min(best, key=best.get)
        q = allowed[qid][1]
        return dict(kind="entrainement", title=f"Bats ton score sur « {q.name} »",
                    text=f"Ton meilleur score : {best[qid]} %. Tu peux faire mieux !", url=url_quiz(q), cta="Relever le défi")
    return None


def espace_eleve(player):
    """(espace, fiche) où l'élève travaille : MaxQuiz École d'abord, sinon son école."""
    ms = list(Membership.objects.filter(player=player, space__members_only=True, space__active=True)
              .select_related("space", "category").order_by("-created_at"))
    m = next((x for x in ms if x.space.kind == "catalog"), ms[0] if ms else None)
    return (m.space, m) if m else (None, None)


def mission_du_jour(player, space=None, membership=None, today=None):
    """Mission fixée pour la journée (créée au premier besoin)."""
    today = today or timezone.localdate()
    if space is None:
        space, membership = espace_eleve(player)
    if not space:
        return None
    existing = Mission.objects.filter(player=player, day=today).first()
    if existing:
        return existing
    m = choisir_mission(player, space, membership, today)
    if not m:
        return None
    obj, _ = Mission.objects.get_or_create(player=player, day=today, defaults=dict(space=space, **m))
    return obj


# --- Rappels push --------------------------------------------------------------------
def reglages(player):
    obj, _ = Rappels.objects.get_or_create(player=player)
    return obj


def heure_habituelle(player, today=None):
    """Heure à laquelle l'élève révise d'habitude (médiane sur 3 semaines), ou None."""
    today = today or timezone.localdate()
    since = timezone.now() - timedelta(days=21)
    stamps = list(GameSession.objects.filter(player=player, started_at__gte=since).values_list("started_at", flat=True))
    stamps += list(LessonView.objects.filter(player=player, created_at__gte=since).values_list("created_at", flat=True))
    if len(stamps) < 4:
        return None
    minutes = median(timezone.localtime(s).hour * 60 + timezone.localtime(s).minute for s in stamps)
    minutes = int(minutes) - 30                      # un peu avant l'heure habituelle
    lo, hi = PREMIERE_HEURE.hour * 60, DERNIERE_HEURE.hour * 60 - 30
    minutes = max(lo, min(hi, minutes))
    return time(minutes // 60, minutes % 60)


def heure_du_rappel(player, prefs, today):
    if prefs.heure:
        return prefs.heure
    return heure_habituelle(player, today) or (HEURE_MERCREDI if today.weekday() == 2 else HEURE_DEFAUT)


def noter_visite(player):
    """L'élève a ouvert MaxQuiz : on remet à zéro les rappels ignorés et on note
    l'ouverture de la mission du jour si un rappel avait été envoyé."""
    prefs = Rappels.objects.filter(player=player).first()
    now = timezone.now()
    if prefs:
        changed = {"derniere_visite": now}
        if prefs.dernier_envoi and (not prefs.derniere_visite or prefs.derniere_visite < prefs.dernier_envoi):
            changed["ignores"] = 0
        Rappels.objects.filter(pk=prefs.pk).update(**changed)
    Mission.objects.filter(player=player, day=timezone.localdate(), pushed_at__isnull=False,
                           opened_at__isnull=True).update(opened_at=now)


def envoyer_rappels_missions(now=None):
    """À lancer toutes les 10 minutes. Renvoie le nombre de rappels envoyés."""
    from .push import notify
    from .subscriptions import access_status
    now = now or timezone.now()
    local = timezone.localtime(now)
    today = local.date()
    if not (PREMIERE_HEURE <= local.time() < DERNIERE_HEURE):
        return 0
    players = (PushDevice.objects.filter(active=True, player__isnull=False)
               .values_list("player_id", flat=True).distinct())
    sent = 0
    for pid in players:
        from .models import Player
        player = Player.objects.filter(id=pid).first()
        if not player:
            continue
        prefs = reglages(player)
        if not prefs.actifs or (prefs.pause_jusquau and prefs.pause_jusquau >= today):
            continue
        if prefs.dernier_envoi and timezone.localtime(prefs.dernier_envoi).date() == today:
            continue
        if prefs.ignores >= 3 and prefs.dernier_envoi and \
                timezone.localtime(prefs.dernier_envoi).date() == today - timedelta(days=1):
            continue                                  # un jour sur deux tant qu'il ne revient pas
        if local.time() < heure_du_rappel(player, prefs, today):
            continue
        if actif_aujourdhui(player, today):
            continue                                  # il a déjà travaillé aujourd'hui
        space, membership = espace_eleve(player)
        if not space or not access_status(space, player)["ok"]:
            continue
        mission = mission_du_jour(player, space, membership, today)
        if not mission:
            continue
        n = serie(player, today)
        if n >= 2:
            title, body = f"🔥 Ta série de {n} jours s'arrête ce soir", f"Garde-la : {mission.title}"
        else:
            title, body = mission.title, mission.text
        notify(players=[player], kind="mission", title=title, body=body, url=mission.url)
        Mission.objects.filter(pk=mission.pk).update(pushed_at=now)
        Rappels.objects.filter(pk=prefs.pk).update(dernier_envoi=now, ignores=prefs.ignores + 1)
        sent += 1
    return sent


# --- Mesure --------------------------------------------------------------------------
def rapport(space, jours=14, today=None):
    today = today or timezone.localdate()
    since = today - timedelta(days=jours - 1)
    members = Membership.objects.filter(space=space, player__isnull=False).values_list("player_id", flat=True)
    qs, ql = _perimetre(space)
    rows = []
    for i in range(jours):
        d = since + timedelta(days=i)
        q_ids = set(GameSession.objects.filter(qs, player_id__in=members, day=d).annotate(n=Count("answers"))
                    .filter(n__gt=0).values_list("player_id", flat=True))
        l_ids = set(LessonView.objects.filter(ql, player_id__in=members, day=d).values_list("player_id", flat=True))
        actifs = q_ids | l_ids
        missions = Mission.objects.filter(space=space, day=d)
        pushed = missions.filter(pushed_at__isnull=False)
        rows.append(dict(day=d, actifs=len(actifs), envoyes=pushed.count(),
                         ouverts=pushed.filter(opened_at__isnull=False).count(),
                         faites=sum(1 for m in missions.values_list("player_id", flat=True) if m in actifs)))
    from .models import Player
    players = Player.objects.filter(id__in=members)
    series = [serie(p, today, space) for p in players]
    actifs_7 = len(jours_actifs_groupes(members, today - timedelta(days=6), space))
    return dict(rows=rows, max_actifs=max([r["actifs"] for r in rows] + [1]),
                inscrits=len(series), actifs_7=actifs_7,
                serie_moyenne=round(sum(s for s in series if s) / max(1, sum(1 for s in series if s)), 1),
                en_serie=sum(1 for s in series if s >= 2),
                notifs=PushDevice.objects.filter(active=True, player_id__in=members).values("player_id").distinct().count(),
                envoyes=sum(r["envoyes"] for r in rows), ouverts=sum(r["ouverts"] for r in rows))


def jours_actifs_groupes(player_ids, since, space=None):
    qs, ql = _perimetre(space)
    a = set(GameSession.objects.filter(qs, player_id__in=player_ids, day__gte=since).annotate(n=Count("answers"))
            .filter(n__gt=0).values_list("player_id", flat=True))
    return a | set(LessonView.objects.filter(ql, player_id__in=player_ids, day__gte=since)
                   .values_list("player_id", flat=True))
