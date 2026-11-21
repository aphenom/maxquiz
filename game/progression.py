"""Où en est l'élève dans chaque matière, par rapport au programme de l'année.

- chapitres() : les chapitres de la classe de l'élève, matière par matière, dans l'ordre du
  programme, avec le mois où chacun est normalement étudié (Lesson.mois).
- etat_matieres() : pour chaque matière, chapitres travaillés, réussis, attendus à cette date,
  en retard, jours depuis la dernière activité, et le prochain chapitre à travailler.
- programme_du_jour() : trois activités courtes dans trois matières différentes (la suite la plus
  utile, un chapitre du programme, une matière délaissée).
- semaine() : matières travaillées cette semaine, et semaines complètes (toutes les matières).
Un chapitre est « travaillé » dès qu'un quiz y est commencé ou son cours ouvert ; « réussi » à
partir de 60 % de bonnes réponses à son quiz.
"""
from datetime import timedelta

from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone

from .models import GameSession, Lesson, LessonView

SEUIL_REUSSITE = 60
MOIS = {9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre", 1: "janvier", 2: "février",
        3: "mars", 4: "avril", 5: "mai", 6: "juin", 7: "juillet", 8: "août"}
ORDRE_SCOLAIRE = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]


def rang_scolaire(mois):
    """Position du mois dans l'année scolaire (septembre = 0 … août = 11)."""
    return ORDRE_SCOLAIRE.index(mois) if mois in ORDRE_SCOLAIRE else None


def attendu(mois, today):
    """Le chapitre devrait-il déjà avoir été vu à cette date ? (Les vacances comptent comme
    la fin de l'année : tout est attendu.)"""
    if not mois:
        return False
    return rang_scolaire(mois) <= rang_scolaire(today.month)


# --- Le programme de la classe ----------------------------------------------------------
def _lecons_communes():
    from .views import label_key
    out = {}
    for l in Lesson.objects.filter(space__isnull=True, active=True).defer("pdf_data", "summary"):
        out[(label_key(l.shared_level_name), label_key(l.shared_subject_name), label_key(l.shared_theme_name))] = l
    return out


def chapitres(space, membership):
    """[(matière, [{quiz, lesson, mois, ordre, nom}])] dans l'ordre du programme."""
    from .engagement import _quizzes_par_matiere
    from .views import label_key
    communes = _lecons_communes()
    out = []
    for sub, quizzes in _quizzes_par_matiere(space, membership):
        rows = []
        for i, q in enumerate(quizzes):
            if q.space_id:
                lesson = (Lesson.objects.filter(space=space, active=True, theme_id=q.theme_id).defer("pdf_data").first()
                          if q.theme_id else None)
            else:
                lesson = communes.get((label_key(q.shared_level_name), label_key(q.shared_subject_name),
                                       label_key(q.name)))
            rows.append(dict(quiz=q, lesson=lesson, nom=q.name, ordre=i,
                             mois=lesson.mois if lesson else None))
        out.append((sub, rows))
    return out


# --- Ce que l'élève a fait ----------------------------------------------------------------
def activite(player, space):
    """({quiz_id: (meilleur %, dernier jour)}, {lesson_id: dernier jour}) sur l'année."""
    since = timezone.localdate() - timedelta(days=330)
    quiz = {}
    rows = (GameSession.objects.filter(player=player, space=space, quiz__isnull=False, day__gte=since)
            .annotate(n=Count("answers", filter=Q(answers__question__kind="quiz")),
                      ok=Count("answers", filter=Q(answers__is_correct=True, answers__question__kind="quiz")))
            .filter(n__gt=0).values_list("quiz_id", "n", "ok", "day"))
    for qid, n, ok, day in rows:
        pct = round(100 * ok / n)
        best, last = quiz.get(qid, (0, day))
        quiz[qid] = (max(best, pct), max(last, day))
    lessons = {}
    for lid, day in LessonView.objects.filter(player=player, day__gte=since).values_list("lesson_id", "day"):
        lessons[lid] = max(lessons.get(lid, day), day)
    return quiz, lessons


def _url(space, ch):
    return reverse("quiz_home", args=[space.slug, ch["quiz"].slug])


def etat_matieres(player, space, membership, today=None, programme=None, faits=None):
    """Une ligne par matière, dans l'ordre des matières de la classe."""
    today = today or timezone.localdate()
    programme = programme if programme is not None else chapitres(space, membership)
    quiz_done, lesson_done = faits if faits is not None else activite(player, space)
    out = []
    for sub, rows in programme:
        travailles = reussis = 0
        retard, a_faire, derniere = [], [], None
        for ch in rows:
            q = quiz_done.get(ch["quiz"].id)
            l_day = lesson_done.get(ch["lesson"].id) if ch["lesson"] else None
            ch["best"] = q[0] if q else None
            ch["fait"] = bool(q or l_day)
            days = [d for d in ((q[1] if q else None), l_day) if d]
            if days:
                derniere = max([derniere] + days) if derniere else max(days)
            if ch["fait"]:
                travailles += 1
                if q and q[0] >= SEUIL_REUSSITE:
                    reussis += 1
            else:
                a_faire.append(ch)
                if attendu(ch["mois"], today):
                    retard.append(ch)
        attendus = sum(1 for ch in rows if attendu(ch["mois"], today))
        # Prochain chapitre : le plus ancien en retard, sinon le suivant du programme,
        # sinon le moins réussi.
        prochain = (retard or a_faire or [None])[0]
        if prochain is None and rows:
            prochain = min(rows, key=lambda c: (c["best"] if c["best"] is not None else 101))
        out.append(dict(
            sub=sub, nom=sub.name, total=len(rows), travailles=travailles, reussis=reussis,
            attendus=attendus, retard=retard, nb_retard=len(retard), a_jour=not retard,
            derniere=derniere, jours_sans=(today - derniere).days if derniere else None,
            prochain=prochain, pct=round(100 * travailles / len(rows)) if rows else 0,
            pct_reussis=round(100 * reussis / len(rows)) if rows else 0))
    return out


# --- Programme du jour ------------------------------------------------------------------------
def _activite(space, ch, kind, matiere, text, today, jours_sans=None):
    titre = f"{matiere} : « {ch['nom']} »"
    if ch["lesson"] and not ch["fait"]:
        url, cta, cible = reverse("lesson_detail", args=[space.slug, ch["lesson"].id]), "Lire le cours", \
            f"lesson:{ch['lesson'].id}"
    else:
        url, cta, cible = _url(space, ch), "Faire le quiz", f"quiz:{ch['quiz'].id}"
    return dict(kind=kind, matiere=matiere, title=titre, text=text, url=url, cta=cta, cible=cible,
                quiz_id=ch["quiz"].id, lesson_id=ch["lesson"].id if ch["lesson"] else None,
                chapitre=ch["nom"], jours_sans=jours_sans)


def _js(etat):
    """Jours sans activité dans la matière (-1 : jamais commencée)."""
    return etat["jours_sans"] if etat["jours_sans"] is not None else -1


def programme_du_jour(player, space, membership, today=None, premiere=None):
    """Jusqu'à trois activités dans des matières différentes. `premiere` est la mission
    choisie par engagement.choisir_mission (la suite la plus utile)."""
    today = today or timezone.localdate()
    programme = chapitres(space, membership)
    etats = etat_matieres(player, space, membership, today, programme)
    items, prises = [], set()
    if premiere:
        e = next((e for e in etats if e["nom"] == premiere.get("matiere")), None)
        premiere = dict(premiere, jours_sans=_js(e) if e else None)
        items.append(premiere)
        prises.add(premiere.get("matiere"))

    # 2. Le programme : la matière la plus en retard, sinon le chapitre suivant
    candidats = sorted((e for e in etats if e["prochain"] and e["nom"] not in prises),
                       key=lambda e: (-e["nb_retard"], e["pct"]))
    if candidats:
        e = candidats[0]
        ch = e["prochain"]
        quand = f"Au programme depuis {MOIS[ch['mois']]}" if ch["mois"] and attendu(ch["mois"], today) else (
            f"Prévu en {MOIS[ch['mois']]}" if ch["mois"] else "Chapitre suivant")
        text = f"{quand}. " + (f"{e['nb_retard']} chapitre{'s' if e['nb_retard'] > 1 else ''} à rattraper en {e['nom']}."
                               if e["nb_retard"] > 1 else "Environ 5 minutes.")
        items.append(_activite(space, ch, "programme", e["nom"], text, today, _js(e)))
        prises.add(e["nom"])

    # 3. La matière délaissée : jamais travaillée, ou pas depuis le plus longtemps
    restes = [e for e in etats if e["prochain"] and e["nom"] not in prises]
    if restes:
        e = max(restes, key=lambda e: (e["jours_sans"] is None, e["jours_sans"] or 0, e["nb_retard"]))
        if e["jours_sans"] is None:
            text = f"Tu n'as pas encore commencé {e['nom']}. On s'y met 5 minutes ?"
        elif e["jours_sans"] >= 2:
            text = f"Pas de {e['nom']} depuis {e['jours_sans']} jours. Un petit tour ?"
        else:
            text = "Pour garder toutes tes matières en route."
        items.append(_activite(space, e["prochain"], "delaissee", e["nom"], text, today, _js(e)))
        prises.add(e["nom"])

    # Compléter si l'élève a peu de matières
    for e in etats:
        if len(items) >= 3:
            break
        if e["prochain"] and e["nom"] not in prises:
            items.append(_activite(space, e["prochain"], "programme", e["nom"], "Environ 5 minutes.", today, _js(e)))
            prises.add(e["nom"])
    return items[:3]


def faits_aujourdhui(player, items, today=None):
    """Marque chaque activité du jour comme faite (quiz commencé ou cours ouvert aujourd'hui)."""
    today = today or timezone.localdate()
    quizzes = set(GameSession.objects.filter(player=player, day=today).annotate(n=Count("answers"))
                  .filter(n__gt=0).values_list("quiz_id", flat=True))
    lessons = set(LessonView.objects.filter(player=player, day=today).values_list("lesson_id", flat=True))
    out = []
    for it in items:
        it = dict(it)
        it["fait"] = bool((it.get("quiz_id") and it["quiz_id"] in quizzes)
                          or (it.get("lesson_id") and it["lesson_id"] in lessons))
        out.append(it)
    return out


def suivante(player, mission, sauf_quiz=None, sauf_lecon=None, today=None):
    """Activité suivante du programme du jour, pas encore faite (pour enchaîner)."""
    if not mission or not mission.items:
        return None
    for it in faits_aujourdhui(player, mission.items, today):
        if it["fait"] or (sauf_quiz and it.get("quiz_id") == sauf_quiz) or \
                (sauf_lecon and it.get("lesson_id") == sauf_lecon):
            continue
        return it
    return None


# --- Objectif de la semaine -------------------------------------------------------------------
def semaine(player, space, membership, today=None, programme=None):
    """Matières travaillées depuis lundi, et nombre de semaines complètes (toutes les matières)
    sur les 8 dernières semaines."""
    today = today or timezone.localdate()
    programme = programme if programme is not None else chapitres(space, membership)
    matieres = {}
    for sub, rows in programme:
        for ch in rows:
            matieres.setdefault(sub.name, set()).add(("q", ch["quiz"].id))
            if ch["lesson"]:
                matieres[sub.name].add(("l", ch["lesson"].id))
    lundi = today - timedelta(days=today.weekday())
    debut = lundi - timedelta(weeks=8)
    touches = {}                                          # lundi -> {matières}
    sessions = (GameSession.objects.filter(player=player, space=space, quiz__isnull=False, day__gte=debut)
                .annotate(n=Count("answers")).filter(n__gt=0).values_list("quiz_id", "day"))
    vues = LessonView.objects.filter(player=player, day__gte=debut).values_list("lesson_id", "day")
    for kind, rows in (("q", sessions), ("l", vues)):
        for oid, day in rows:
            for nom, ids in matieres.items():
                if (kind, oid) in ids:
                    touches.setdefault(day - timedelta(days=day.weekday()), set()).add(nom)
    noms = list(matieres)
    cette = touches.get(lundi, set())
    completes = sum(1 for k, v in touches.items() if k < lundi and noms and set(noms) <= v)
    return dict(total=len(noms), faites=len(cette), manquantes=[n for n in noms if n not in cette],
                complete=bool(noms) and set(noms) <= cette, semaines_completes=completes + (
                    1 if noms and set(noms) <= cette else 0))
