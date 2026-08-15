"""Crée l'espace de démonstration « Banque Horizon » avec des questions produits,
des sondages, et ~40 participations simulées pour un tableau de bord parlant.
Usage : python manage.py seed_demo_space
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from game.models import Space, Question, Player, GameSession, Answer, License

QUIZ = [
    (1, "Quel document est indispensable pour ouvrir un compte chez Banque Horizon ?",
     ["Une pièce d'identité valide", "Un acte de naissance uniquement", "Rien du tout", "Un passeport étranger"], 0),
    (1, "L'application mobile Horizon Pay permet de…",
     ["Consulter son solde et faire des virements", "Uniquement voir la météo", "Jouer à des jeux", "Rien de tout ça"], 0),
    (2, "Quel est le plafond journalier de retrait au GAB avec la carte Horizon Classic ?",
     ["200 000 F", "500 000 F", "1 000 000 F", "Sans limite"], 1),
    (2, "Le compte épargne Horizon Avenir est rémunéré à…",
     ["1 % par an", "3,5 % par an", "10 % par an", "Il n'est pas rémunéré"], 1),
    (2, "Combien coûte l'ouverture d'un compte Horizon Étudiant ?",
     ["25 000 F", "10 000 F", "C'est gratuit", "50 000 F"], 2),
    (3, "Le crédit immobilier Horizon Logis finance jusqu'à…",
     ["50 % du bien", "70 % du bien", "90 % du bien", "100 % du bien"], 2),
    (3, "Horizon Pay permet d'envoyer de l'argent vers les portefeuilles mobile money…",
     ["Non, jamais", "Oui, vers tous les opérateurs", "Uniquement vers un seul opérateur", "Seulement à l'étranger"], 1),
    (3, "Quel service Horizon protège vos achats en ligne ?",
     ["La e-carte virtuelle", "Le carnet de chèques", "Le coffre-fort", "Aucun"], 0),
    (4, "Le programme Horizon Diaspora s'adresse aux…",
     ["Étudiants d'Abidjan", "Ivoiriens vivant à l'étranger", "Grandes entreprises", "Fonctionnaires uniquement"], 1),
    (4, "Quelle assurance est incluse avec la carte Horizon Gold ?",
     ["Assurance voyage et achats", "Assurance auto", "Assurance habitation", "Aucune assurance"], 0),
]
SURVEYS = [
    ("Comment préférez-vous contacter votre banque ?",
     ["WhatsApp", "Appel téléphonique", "En agence", "E-mail"]),
    ("Quel nouveau service aimeriez-vous voir chez Banque Horizon ?",
     ["Épargne automatique", "Crédit express en ligne", "Cashback sur la carte", "Conseiller dédié WhatsApp"]),
]
PSEUDOS = ["Aya K.","Koffi D.","Aminata T.","Jean-Marc B.","Fatou C.","Yao S.","Adjoua N.",
           "Ibrahim F.","Mariam O.","Serge G.","Awa B.","Moussa K.","Clarisse Y.","Didier T.",
           "Nadia S.","Franck A.","Salimata D.","Eric N.","Bintou C.","Olivier K."]


class Command(BaseCommand):
    help = "Espace démo Banque Horizon + données simulées pour le tableau de bord"

    def handle(self, *args, **options):
        space, created = Space.objects.get_or_create(slug="banque-horizon", defaults=dict(
            name="Banque Horizon", emoji="🏦",
            color_primary="#0A3D7A", color_accent="#E9A820",
            welcome="Testez vos connaissances sur nos produits et services, "
                    "donnez votre avis, et tentez de gagner des lots !",
            reward_text="10 000 F de crédit téléphonique pour les 3 meilleurs de la semaine",
            dashboard_username="HORIZON-ADMIN", dashboard_code="HORIZON2026",
            question_count=10, survey_every=4,
            elimination=False))

        License.objects.get_or_create(space=space, period_label="2026", defaults=dict(
            billing_mode="forfait", price="Forfait annuel — tarif à convenir",
            start_date=date(2026, 1, 1), end_date=date(2026, 12, 31), active=True))

        if created:
            for diff, text, opts, correct in QUIZ:
                Question.objects.create(space=space, kind="quiz", category="cg",
                                        difficulty=diff, text=text, option_a=opts[0],
                                        option_b=opts[1], option_c=opts[2], option_d=opts[3],
                                        correct=correct)
            for text, opts in SURVEYS:
                Question.objects.create(space=space, kind="survey", category="cg",
                                        difficulty=1, text=text, option_a=opts[0],
                                        option_b=opts[1], option_c=opts[2], option_d=opts[3],
                                        correct=0)
        # Participations simulées (certains produits volontairement mal connus)
        if not GameSession.objects.filter(space=space).exists():
            questions = list(space.questions.all())
            hard_ids = {q.id for q in questions if q.kind == "quiz" and q.difficulty >= 3}
            for i, pseudo in enumerate(PSEUDOS * 2):
                p, _ = Player.objects.get_or_create(
                    phone=f"07{random.randint(10000000, 99999999)}",
                    defaults=dict(pseudo=pseudo))
                sess = GameSession.objects.create(
                    player=p, mode="space", space=space,
                    consent=random.random() < 0.7,
                    question_ids=[q.id for q in questions],
                    day=timezone.localdate() - timedelta(days=random.randint(0, 5)))
                total_ms = 0
                for q in questions:
                    if q.kind == "survey":
                        choice = random.choices([0, 1, 2, 3], weights=[35, 15, 20, 30])[0]
                        ok = True
                    else:
                        # les produits « difficiles » sont mal maîtrisés : ~35 % de réussite
                        p_ok = 0.35 if q.id in hard_ids else 0.8
                        ok = random.random() < p_ok
                        choice = q.correct if ok else (q.correct + random.randint(1, 3)) % 4
                    ms = random.randint(2500, 9000)
                    total_ms += ms
                    Answer.objects.create(session=sess, question=q, choice=choice,
                                          time_ms=ms, is_correct=ok)
                sess.reached = len(questions)
                sess.total_time_ms = total_ms
                sess.status = "finished"
                sess.finished_at = timezone.now()
                sess.save()
        self.stdout.write(self.style.SUCCESS(
            f"Espace « {space.name} » prêt : /e/{space.slug}/ · "
            f"tableau de bord : /tableau-de-bord/connexion/ (identifiant {space.dashboard_username}, "
            f"mot de passe {space.dashboard_code}) · "
            f"{GameSession.objects.filter(space=space).count()} participations simulées."))
