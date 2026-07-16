# MaxQuiz — MVP Django
**MQ Technologies** · Jeu de quiz « survie » à cagnotte journalière — Côte d'Ivoire

Chaque jour, un défi de 50 questions à difficulté croissante et chrono qui raccourcit.
Une erreur = éliminé pour la journée… sauf joker (payant ou publicité vidéo).
Ceux qui tiennent jusqu'au bout se partagent la cagnotte du jour, retirable par mobile money.
Participation gratuite, financée par la publicité des partenaires.

## Démarrage rapide

```bash
pip install django
python manage.py migrate
python manage.py seed              # config + 44 questions (4 difficultés) + campagnes de démo
python manage.py createsuperuser
python manage.py runserver
```

- Jeu : http://127.0.0.1:8000/
- Back-office : http://127.0.0.1:8000/admin/

## Tout est paramétrable dans l'admin (Configuration du jeu)

Nombre de questions du défi (50 par défaut), répartition des difficultés en %
(40/30/20/10), chrono par niveau (15/12/9/6 s), fréquence des pubs, cagnotte du jour
et son sponsor, et le système de joker : activer/désactiver le joker payant et le joker
publicitaire indépendamment, prix par niveau de difficulté (100/200/500/1000 F),
nombre maximum par partie (3).

## Boucle de jeu

Questions aléatoires PAR JOUEUR ET PAR SESSION (tirage indépendant, ordre des options
mélangé) : impossible de partager les réponses. La difficulté suit la courbe configurée,
le chrono raccourcit avec le niveau. Mauvaise réponse ou temps écoulé → écran
d'élimination avec offre de joker : payer (débité du solde du portefeuille) ou regarder
une pub vidéo de 15 s d'un partenaire. Sans joker : éliminé jusqu'à demain, mais classé
au tableau du jour selon la question atteinte (départage au temps total).

Les finalistes se partagent la cagnotte : action admin « Répartir la cagnotte » sur les
parties du jour → crédit des portefeuilles. Les joueurs demandent le retrait par mobile
money depuis la page Portefeuille ; l'équipe traite les demandes dans l'admin.

## Monétisation intégrée

Interstitiels entre les questions (impressions comptées), pubs vidéo « joker » (le
format le plus valorisable : attention totale), sponsor de cagnotte affiché sur
l'accueil, jokers payants. Le back-office suit impressions et clics par campagne.

## Anti-triche

Bonnes réponses jamais envoyées au client (validation par question via `/api/answer/`),
signalement automatique des réponses correctes < 800 ms et des incohérences entre temps
déclarés et durée réelle serveur, verrou « une tentative par jour » en contrainte de
base, sessions signalées exclues du classement et de la cagnotte, révision humaine dans
l'admin avant tout paiement.


## Espaces entreprises (multi-tenant, offre B2B)

Chaque client dispose d'un espace cloisonné avec son branding (logo, couleurs, message),
sa banque de questions **quiz** et **sondages** (intercalés toutes les N questions), son
mode de jeu (engagement sans élimination, ou survie), son accès (lien public `/e/slug/`
ou code d'accès), et sa récompense annoncée — les lots sont décidés et offerts par
l'entreprise, la participation reste gratuite.

À l'inscription dans un espace, le participant laisse pseudo + téléphone et coche (ou
non) une case de **consentement marketing** explicite : l'entreprise est responsable de
traitement de ses données first-party, MaxQuiz est le sous-traitant technique.

**Tableau de bord client** sur `/e/slug/tableau-de-bord/` (protégé par code) :
participations, taux de complétion, contacts consentants avec export CSV, taux de bonne
réponse par question trié des produits **les moins maîtrisés** aux mieux connus (l'outil
d'étude de marché), et répartition des réponses aux sondages.

**Démo commerciale incluse** : `python manage.py seed_demo_space` crée l'espace
« Banque Horizon » (`/e/banque-horizon/`, tableau de bord avec le code `HORIZON2026`)
avec 10 questions produits bancaires, 2 sondages et 40 participations simulées pour un
tableau de bord immédiatement parlant en rendez-vous.

Le jeu public MaxQuiz (défi du jour, cagnotte, jokers) reste inchangé et coexiste.

## ⚠️ Avertissement important

Le **joker payant** peut faire qualifier le jeu de jeu d'argent (paiement + gain en
argent), secteur régulé en Côte d'Ivoire. Il est désactivable d'un clic dans l'admin.
**Ne pas lancer en production avec le joker payant activé sans validation par un juriste
ivoirien.** Le joker publicitaire, lui, maintient la gratuité totale de la participation.

## Prochaines étapes (hors MVP)

Authentification téléphone + OTP SMS, intégration paiement mobile money (encaissement
jokers + retraits automatisés via agrégateur), répartition automatique de la cagnotte à
minuit (cron/Celery), banque de questions industrialisée (plusieurs milliers, avec
processus de validation), PostgreSQL + Redis, PWA (manifest + service worker),
déploiement gunicorn + whitenoise.
