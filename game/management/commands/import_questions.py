"""Import en masse d'une banque de questions depuis un .xlsx, ou un .csv (UTF-8 ou
Windows-1252, séparateur « ; » ou « , »).

Colonnes : niveau;matiere;thematique;difficulte;question;a;b;c;d;bonne;explication
  - bonne : A, B, C ou D ; difficulte : 1 à 4
Deux cibles :
  --space <slug>   questions propres à un établissement, rattachées à sa
                   sous-catégorie (niveau/matière) et à son Theme (thématique).
  --shared         contenu MQ vendu à toutes les écoles : un quiz partagé par
                   (niveau, matière, thématique) est créé ou réutilisé, avec
                   shared_level_name / shared_subject_name renseignés — c'est ce
                   qui alimente les points faibles par matière et par chapitre.
Usage :
  python manage.py import_questions banque.xlsx --shared --dry-run
  python manage.py import_questions banque.csv --shared --questions-par-partie 10
  python manage.py import_questions banque.csv --space college-la-reussite
"""
import csv
import io

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from game.models import Question, Quiz, Space, SubCategory, Theme

LETTERS = {"A": 0, "B": 1, "C": 2, "D": 3}


def _read_rows(path):
    """Lignes en dictionnaires, depuis un .xlsx (1re feuille, 1re ligne = en-têtes)
    ou un .csv en UTF-8 OU en Windows-1252 (« CSV (séparateur : point-virgule) »
    d'Excel en français), séparateur « ; » ou « , » détecté sur l'en-tête."""
    if path.lower().endswith(".xlsx"):
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True)
        head = [str(h or "").strip() for h in next(it, [])]
        return [{h: ("" if v is None else str(v)) for h, v in zip(head, row)}
                for row in it if row and any(v is not None for v in row)]
    data = open(path, "rb").read()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = data.decode("cp1252")
    first = text.split("\n", 1)[0]
    delim = ";" if first.count(";") >= first.count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


class Command(BaseCommand):
    help = "Importe des questions depuis un CSV, dans un espace ou en quiz partagés (contenu MQ)."

    def add_arguments(self, parser):
        parser.add_argument("csv_path")
        target = parser.add_mutually_exclusive_group(required=True)
        target.add_argument("--space", help="slug de l'espace")
        target.add_argument("--shared", action="store_true",
                            help="contenu MQ : un quiz partagé par niveau/matière/thématique")
        parser.add_argument("--questions-par-partie", type=int, default=10)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, csv_path, space=None, shared=False, dry_run=False, **opts):
        sp = Space.objects.filter(slug=space).first() if space else None
        if space and not sp:
            raise CommandError(f"Espace introuvable : {space}")
        rows = _read_rows(csv_path)

        errors, plan = [], []          # plan : (clé quiz partagé ou None, Question)
        quizzes = {}                   # (niveau, matière, thématique) -> Quiz existant ou None
        seen = set()
        for n, r in enumerate(rows, start=2):
            r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
            text, good = r.get("question", ""), r.get("bonne", "").upper()
            niveau, matiere, chap = r.get("niveau", ""), r.get("matiere", ""), r.get("thematique", "")
            if not text or good not in LETTERS or not all(r.get(x) for x in "abcd"):
                errors.append(f"ligne {n} : question, a/b/c/d et bonne (A-D) obligatoires")
                continue
            diff = int(r["difficulte"]) if r.get("difficulte", "").isdigit() else 1
            q = Question(kind="quiz", category="ec", difficulty=min(max(diff, 1), 4), text=text,
                         option_a=r["a"][:200], option_b=r["b"][:200], option_c=r["c"][:200],
                         option_d=r["d"][:200], correct=LETTERS[good], explanation=r.get("explication", ""))
            key = None
            if shared:
                if not (niveau and matiere and chap):
                    errors.append(f"ligne {n} : niveau, matière et thématique obligatoires en --shared")
                    continue
                key = (niveau, matiere, chap)
                if key not in quizzes:
                    quizzes[key] = Quiz.objects.filter(
                        space__isnull=True, shared_level_name__iexact=niveau,
                        shared_subject_name__iexact=matiere, name__iexact=chap).first()
                qz = quizzes[key]
                if qz and Question.objects.filter(quiz=qz, text=text).exists():
                    continue           # doublon : ré-import sans risque
            else:
                sub = SubCategory.objects.filter(category__space=sp, category__name__iexact=niveau,
                                                 name__iexact=matiere).first()
                if not sub:
                    errors.append(f"ligne {n} : niveau/matière « {niveau} / {matiere} » inconnus")
                    continue
                theme = Theme.objects.filter(sub_category=sub, name__iexact=chap).first() if chap else None
                if chap and not theme:
                    errors.append(f"ligne {n} : thématique « {chap} » inconnue dans {niveau} / {matiere}")
                    continue
                if Question.objects.filter(space=sp, text=text).exists():
                    continue
                q.space, q.sub_category, q.theme = sp, sub, theme
            if (key, text) in seen:
                continue
            seen.add((key, text))
            plan.append((key, q))

        for e in errors:
            self.stderr.write(e)
        new_quizzes = sorted({k for k, _ in plan if k and not quizzes.get(k)})
        if dry_run:
            self.stdout.write(f"[dry-run] {len(plan)} question(s) à créer, {len(new_quizzes)} quiz "
                              f"partagé(s) à créer, {len(errors)} erreur(s).")
            return
        with transaction.atomic():
            for k in new_quizzes:
                niveau, matiere, chap = k
                base = slugify(f"{niveau}-{matiere}-{chap}")[:55]
                slug, i = base, 2
                while Quiz.objects.filter(space__isnull=True, slug=slug).exists():
                    slug, i = f"{base}-{i}", i + 1
                quizzes[k] = Quiz.objects.create(
                    space=None, shared_level_name=niveau, shared_subject_name=matiere, name=chap[:100],
                    slug=slug,
                    question_count=opts["questions_par_partie"], survey_every=0,
                    replay_policy="unlimited", show_corrections=True)
            for k, q in plan:
                if k:
                    q.quiz = quizzes[k]
            Question.objects.bulk_create([q for _, q in plan])
        self.stdout.write(self.style.SUCCESS(
            f"{len(plan)} question(s) importée(s), {len(new_quizzes)} quiz partagé(s) créé(s), "
            f"{len(errors)} erreur(s)."))
        if shared:
            # Quelles écoles voient ce contenu ? Une école absente de la liste a des
            # libellés de niveau/matière qui ne se rapprochent pas (voir label_key).
            from game.views import shared_match
            spaces = list(Space.objects.filter(active=True))
            for k in sorted({k for k, _ in plan if k} | set(quizzes) - {None}):
                qz = quizzes.get(k)
                if not qz:
                    continue
                seen_by = [sp_.name for sp_ in spaces if shared_match(sp_, qz)]
                self.stdout.write(f"  {' / '.join(k)} : visible dans {len(seen_by)} espace(s)"
                                  + (f" ({', '.join(seen_by)})" if seen_by else " -- AUCUNE école ne le voit"))
