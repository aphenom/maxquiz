"""Contenu de démonstration MaxQuiz École : l'espace des élèves inscrits seuls,
un cours commun et un quiz commun de 3ème (Mathématiques, théorème de Pythagore).

    python manage.py seed_demo_catalog
"""
from django.core.management.base import BaseCommand

from game.models import Lesson, Question, Quiz
from game.student import catalog_space

QUESTIONS = [
    ("ABC est rectangle en A avec AB = 6 cm et AC = 8 cm. Combien mesure BC ?",
     ["14 cm", "10 cm", "48 cm", "√14 cm"], 1, "BC² = AB² + AC² = 36 + 64 = 100, donc BC = 10 cm."),
    ("Dans un triangle rectangle, l'hypoténuse est…",
     ["le plus petit côté", "le côté opposé à l'angle droit", "un côté de l'angle droit", "la hauteur"], 1,
     "L'hypoténuse est le côté opposé à l'angle droit, et c'est le plus long."),
    ("Un triangle a pour côtés 5, 12 et 13. Est-il rectangle ?",
     ["Oui", "Non", "On ne peut pas savoir", "Seulement s'il est isocèle"], 0,
     "13² = 169 et 5² + 12² = 25 + 144 = 169 : d'après la réciproque, il est rectangle."),
    ("ABC est rectangle en A, BC = 13 cm et AB = 5 cm. Combien mesure AC ?",
     ["8 cm", "18 cm", "12 cm", "√194 cm"], 2, "AC² = BC² − AB² = 169 − 25 = 144, donc AC = 12 cm."),
    ("Une échelle de 5 m est posée à 3 m du pied d'un mur. À quelle hauteur touche-t-elle le mur ?",
     ["2 m", "4 m", "8 m", "√34 m"], 1, "h² = 5² − 3² = 25 − 9 = 16, donc h = 4 m."),
]


class Command(BaseCommand):
    help = "Crée l'espace MaxQuiz École et un exemple de cours et de quiz communs (3ème, Mathématiques)."

    def handle(self, *args, **options):
        space = catalog_space()
        quiz, made = Quiz.objects.get_or_create(
            space=None, slug="3eme-maths-pythagore", defaults=dict(
                name="Le théorème de Pythagore", shared_level_name="3ème",
                shared_subject_name="Mathématiques", question_count=5, survey_every=0,
                replay_policy="unlimited", show_corrections=True))
        if made:
            for i, (text, opts, correct, expl) in enumerate(QUESTIONS):
                Question.objects.create(quiz=quiz, kind="quiz", category="ec", difficulty=1 + i % 3,
                                        text=text, option_a=opts[0], option_b=opts[1], option_c=opts[2],
                                        option_d=opts[3], correct=correct, explanation=expl)
        Lesson.objects.get_or_create(
            space=None, title="Le théorème de Pythagore", defaults=dict(
                shared_level_name="3ème", shared_subject_name="Mathématiques",
                shared_theme_name="Le théorème de Pythagore", free_preview=True,
                summary="Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés "
                        "des deux autres côtés : BC² = AB² + AC².\nRéciproque : si BC² = AB² + AC², "
                        "le triangle est rectangle en A.\n(Ajoutez le lien YouTube et la fiche PDF dans "
                        "l'administration, rubrique Cours.)"))
        self.stdout.write(self.style.SUCCESS(
            f"MaxQuiz École prêt : accueil /, espace /e/{space.slug}/ · tableau de bord : identifiant "
            f"{space.dashboard_username}, mot de passe {space.dashboard_code} · essai gratuit "
            f"{'de ' + str(space.trial_days) + ' jours' if space.trial_enabled else 'désactivé'} "
            "(réglable dans l'administration, rubrique Espaces)."))
