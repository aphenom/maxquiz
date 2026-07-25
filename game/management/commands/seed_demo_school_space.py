"""Crée l'espace de démonstration « Collège La Réussite » : catégories (niveaux),
sous-catégories (matières) et un quiz par niveau/matière, chacun avec son lien
direct partageable, plus des participations simulées pour un tableau de bord parlant.
Usage : python manage.py seed_demo_school_space
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from game.models import Space, Category, SubCategory, Quiz, Question, Player, GameSession, Answer

LEVELS = ["6ème", "5ème", "4ème", "3ème"]
SUBJECTS = ["Mathématiques", "Français"]

QUESTIONS = {
    ("6ème", "Mathématiques"): [
        (1, "Combien font 7 x 8 ?", ["54", "56", "58", "64"], 1),
        (1, "Quel est le périmètre d'un carré de côté 5 cm ?", ["10 cm", "20 cm", "25 cm", "15 cm"], 1),
        (2, "Quelle fraction représente la moitié ?", ["1/3", "1/2", "2/3", "1/4"], 1),
        (2, "Combien de centimètres dans 1 mètre ?", ["10", "100", "1000", "50"], 1),
        (3, "Dans 24 ÷ 4 + 2, quel est le résultat en respectant les priorités ?", ["8", "6", "14", "4"], 0),
    ],
    ("6ème", "Français"): [
        (1, "Quel est le pluriel de « cheval » ?", ["chevals", "chevaux", "chevales", "chevaus"], 1),
        (1, "Quel mot est un verbe dans « Le chat dort sur le lit » ?", ["chat", "dort", "lit", "le"], 1),
        (2, "Quel est le synonyme de « rapide » ?", ["lent", "vif", "calme", "triste"], 1),
        (2, "Combien y a-t-il de syllabes dans « ordinateur » ?", ["3", "4", "5", "2"], 1),
        (3, "Quel est l'antonyme de « joyeux » ?", ["content", "triste", "gai", "heureux"], 1),
    ],
    ("5ème", "Mathématiques"): [
        (1, "Combien font -3 + 5 ?", ["-8", "2", "8", "-2"], 1),
        (2, "Quelle est la fraction irréductible de 4/8 ?", ["1/4", "1/2", "2/4", "1/8"], 1),
        (2, "Un article coûte 20 F et augmente de 10 %. Nouveau prix ?", ["20 F", "22 F", "21 F", "25 F"], 1),
        (3, "Combien font (-4) x (-3) ?", ["-12", "12", "-7", "7"], 1),
        (3, "Quelle est la valeur de x dans 2x = 10 ?", ["2", "5", "10", "20"], 1),
    ],
    ("5ème", "Français"): [
        (1, "Quel est le féminin de « acteur » ?", ["actrisse", "actrice", "acteure", "actriste"], 1),
        (2, "Dans « Elle mange une pomme », quel est le COD ?", ["Elle", "mange", "une pomme", "aucun"], 2),
        (2, "Quel temps exprime « je mangerai » ?", ["présent", "futur simple", "imparfait", "passé composé"], 1),
        (3, "Quelle est la nature du mot « rapidement » ?", ["adjectif", "nom", "adverbe", "verbe"], 2),
        (3, "Quel est le contraire de « commencer » ?", ["débuter", "terminer", "continuer", "ouvrir"], 1),
    ],
    ("4ème", "Mathématiques"): [
        (2, "Combien font 2³ ?", ["6", "8", "9", "4"], 1),
        (2, "Dans un triangle rectangle, comment s'appelle le côté opposé à l'angle droit ?",
         ["cathète", "hypoténuse", "médiane", "bissectrice"], 1),
        (3, "Un triangle a des côtés 3, 4 et 5 cm. Est-il rectangle ?",
         ["Oui", "Non", "Impossible à dire", "Seulement si équilatéral"], 0),
        (3, "Résous : 3x - 2 = 7. x = ?", ["2", "3", "5", "9"], 1),
        (4, "Quelle est la racine carrée de 81 ?", ["8", "9", "7", "11"], 1),
    ],
    ("4ème", "Français"): [
        (2, "Quel est le mode du verbe dans « Viens ici ! » ?", ["indicatif", "impératif", "subjonctif", "conditionnel"], 1),
        (2, "Quelle figure de style est « Il pleut des cordes » ?", ["comparaison", "métaphore", "hyperbole", "litote"], 1),
        (3, "Quel est le complément circonstanciel dans « Il travaille le soir » ?", ["Il", "travaille", "le soir", "aucun"], 2),
        (3, "Quel auteur a écrit « Les Misérables » ?", ["Molière", "Victor Hugo", "Balzac", "Voltaire"], 1),
        (4, "Quelle est la classe grammaticale de « que » dans « Je sais que tu viens » ?",
         ["pronom relatif", "conjonction de subordination", "adverbe", "préposition"], 1),
    ],
    ("3ème", "Mathématiques"): [
        (2, "Que mesure la médiane d'une série de données ?", ["la moyenne", "la valeur centrale", "l'écart-type", "le mode"], 1),
        (3, "Dans le théorème de Thalès, les triangles doivent être…", ["semblables", "identiques", "rectangles", "isocèles"], 0),
        (3, "Quelle est l'image de 3 par la fonction f(x) = 2x + 1 ?", ["5", "6", "7", "4"], 2),
        (4, "Quel est le développement de (x+2)² ?", ["x²+4", "x²+4x+4", "x²+2x+4", "2x²+4"], 1),
        (4, "Quelle est la solution de l'inéquation 2x > 8 ?", ["x > 4", "x < 4", "x > 2", "x < 2"], 0),
    ],
    ("3ème", "Français"): [
        (2, "Quel est le registre du texte « Ô rage ! ô désespoir ! » ?", ["comique", "tragique", "ironique", "didactique"], 1),
        (3, "Quel est le sujet dans « Depuis hier, pleure la petite fille » ?",
         ["Depuis hier", "pleure", "la petite fille", "aucun"], 2),
        (3, "Quel mouvement littéraire est associé à Victor Hugo ?", ["le classicisme", "le romantisme", "le réalisme", "le surréalisme"], 1),
        (4, "Quelle est la fonction de la proposition subordonnée dans « Je pense que tu as raison » ?",
         ["sujet", "COD", "complément du nom", "apposition"], 1),
        (4, "Quel est le sens du mot « lucide » ?", ["confus", "clairvoyant", "triste", "rapide"], 1),
    ],
}
SURVEYS = [
    ("Quel est ton format de révision préféré ?",
     ["Fiches de révision", "Vidéos explicatives", "Exercices en ligne", "Cours particuliers"]),
    ("Comment préfères-tu être informé de tes résultats ?",
     ["Par SMS", "Par e-mail", "Sur l'appli", "En classe"]),
]
PSEUDOS = ["Aya K.", "Koffi D.", "Aminata T.", "Jean-Marc B.", "Fatou C.", "Yao S.", "Adjoua N.",
           "Ibrahim F.", "Mariam O.", "Serge G.", "Awa B.", "Moussa K.", "Clarisse Y.", "Didier T.",
           "Nadia S.", "Franck A.", "Salimata D.", "Eric N.", "Bintou C.", "Olivier K."]


class Command(BaseCommand):
    help = "Espace démo Collège La Réussite (niveaux/matières/quiz) + données simulées pour le tableau de bord"

    def handle(self, *args, **options):
        space, created = Space.objects.get_or_create(slug="college-la-reussite", defaults=dict(
            name="Collège La Réussite", emoji="🎓",
            color_primary="#0B9A5C", color_accent="#F2790F",
            welcome="Teste tes connaissances par niveau et par matière, et défie tes camarades !",
            reward_text="Un diplôme numérique et des bons points pour les meilleurs de chaque quiz",
            dashboard_code="REUSSITE2026", question_count=5, survey_every=5,
            elimination=False, category_label="Niveau", category_label_plural="Niveaux",
            subcategory_label="Matière", subcategory_label_plural="Matières"))

        if created:
            for i, level in enumerate(LEVELS):
                cat = Category.objects.create(space=space, name=level, slug=slugify(level), order=i)
                for j, subject in enumerate(SUBJECTS):
                    sub = SubCategory.objects.create(category=cat, name=subject, slug=slugify(subject), order=j)
                    Quiz.objects.create(
                        space=space, category=cat, sub_category=sub,
                        name=f"{level} · {subject}", slug=slugify(f"{level}-{subject}"),
                        question_count=5, survey_every=5, elimination=False)
                    for diff, text, opts, correct in QUESTIONS[(level, subject)]:
                        Question.objects.create(space=space, kind="quiz", category="ec", sub_category=sub,
                                                difficulty=diff, text=text, option_a=opts[0],
                                                option_b=opts[1], option_c=opts[2], option_d=opts[3],
                                                correct=correct)
            for text, opts in SURVEYS:
                Question.objects.create(space=space, kind="survey", category="ec",
                                        difficulty=1, text=text, option_a=opts[0],
                                        option_b=opts[1], option_c=opts[2], option_d=opts[3], correct=0)

        # Participations simulées : chaque quiz a son propre taux de maîtrise
        if not GameSession.objects.filter(space=space).exists():
            surveys = list(space.questions.filter(kind="survey"))
            for quiz in Quiz.objects.filter(space=space).select_related("sub_category"):
                questions = list(quiz.sub_category.questions.filter(kind="quiz", active=True))
                base_success = random.uniform(0.4, 0.9)
                for _ in range(random.randint(6, 14)):
                    p = Player.objects.create(phone=f"07{random.randint(10000000, 99999999)}",
                                              pseudo=random.choice(PSEUDOS))
                    deck = list(questions)
                    if surveys:
                        deck.append(random.choice(surveys))
                    sess = GameSession.objects.create(
                        player=p, mode="space", space=space, quiz=quiz,
                        consent=random.random() < 0.6,
                        question_ids=[q.id for q in deck],
                        day=timezone.localdate() - timedelta(days=random.randint(0, 6)))
                    total_ms = 0
                    for q in deck:
                        if q.kind == "survey":
                            choice, ok = random.randint(0, 3), True
                        else:
                            ok = random.random() < base_success
                            choice = q.correct if ok else (q.correct + random.randint(1, 3)) % 4
                        ms = random.randint(2000, 9000)
                        total_ms += ms
                        Answer.objects.create(session=sess, question=q, choice=choice,
                                              time_ms=ms, is_correct=ok)
                    sess.reached = len(deck)
                    sess.total_time_ms = total_ms
                    sess.status = "finished"
                    sess.finished_at = timezone.now()
                    sess.save()

        self.stdout.write(self.style.SUCCESS(
            f"Espace « {space.name} » prêt : /e/{space.slug}/ · "
            f"tableau de bord : /e/{space.slug}/tableau-de-bord/ (code {space.dashboard_code}) · "
            f"{Quiz.objects.filter(space=space).count()} quiz · "
            f"{GameSession.objects.filter(space=space).count()} participations simulées."))
