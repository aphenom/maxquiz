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

### Catégories, sous-catégories & quiz (B2C comme B2B, multi-vertical)

Au-delà du pool de questions à plat (toujours disponible via le lien générique
`/e/slug/`), une entreprise peut structurer ses questions en **catégories** →
**sous-catégories** → **quiz**, avec un **lien direct par quiz**
(`/e/slug/q/quiz-slug/`) à distribuer au bon public — par exemple un niveau scolaire
et une matière pour une école, une famille de produits et une gamme pour une banque.
Les libellés « Catégorie »/« Sous-catégorie » sont personnalisables par espace
(`category_label`/`subcategory_label`, ex. « Niveau »/« Matière » pour une école).

Ce système est **entièrement optionnel par espace** : un espace sans quiz créé (ex.
Banque Horizon aujourd'hui) continue de fonctionner exactement comme avant, avec le
lien unique et le pool de questions à plat.

**Tableau de bord client étendu**, accessible via les onglets Vue d'ensemble /
Catégories / Quiz :
- `/e/slug/tableau-de-bord/categories/` : créer/renommer/supprimer catégories et
  sous-catégories.
- `/e/slug/tableau-de-bord/quiz/` : créer un quiz (nom, catégorie, sous-catégorie,
  nombre de questions, fréquence des sondages, mode survie, **rejouabilité** —
  une fois par jour / une seule fois jamais rejouable / illimité, réglable par
  quiz : adapté à un quiz d'évaluation type école (« une seule fois », pour que
  le taux de maîtrise affiché reste un signal fiable) comme à un quiz
  d'engagement type banque (« illimité » ou « une fois par jour »)), récupérer
  son lien partageable, l'activer/désactiver ou le supprimer.
- Vue d'ensemble : arbre catégorie → sous-catégorie → quiz avec participations et
  taux de complétion, jusqu'au détail par quiz (taux de bonne réponse par question,
  sondages, meilleurs participants) sur `/e/slug/tableau-de-bord/quiz/quiz-slug/`.

**Démo commerciale école incluse** : `python manage.py seed_demo_school_space` crée
l'espace « Collège La Réussite » (`/e/college-la-reussite/`, tableau de bord avec le
code `REUSSITE2026`) avec 4 niveaux (6ème à 3ème) × 2 matières (Mathématiques,
Français) = 8 quiz avec lien direct (ex. `/e/college-la-reussite/q/5eme-mathematiques/`),
40 questions et des dizaines de participations simulées avec un taux de maîtrise
différent par quiz, pour un tableau de bord immédiatement parlant en rendez-vous.

### Comptes utilisateurs (téléphone + OTP comme parcours standard) & branding enrichi

Le téléphone + code à usage unique est désormais le **seul** point d'entrée pour
jouer, jeu public comme espaces — plus de pseudo libre non vérifié. Sur `/`, un
espace (`/e/slug/`) ou un quiz direct (`/e/slug/q/quiz-slug/`), un visiteur pas
encore identifié sur cet appareil voit un formulaire téléphone qui poste vers
`/compte/connexion/` (avec `next` = la page d'origine et `space` = le slug le cas
échéant, pour y revenir après coup et rester dans le bon branding) ; en environnement
de dev, aucun SMS n'est réellement envoyé, le code est affiché à l'écran et loggué
console (`_send_otp()` dans `game/views.py` est le point unique à brancher sur un
vrai fournisseur SMS plus tard). **Première connexion d'un numéro** = inscription :
après validation du code, un court formulaire (`/compte/inscription/`) demande
pseudo, nom complet et ville avant de renvoyer vers la page d'origine — le nom
complet sert notamment à l'appariement avec la base d'un établissement (voir
ci-dessous). Une fois `player_id` posé en session (vérifié au moins une fois sur cet
appareil), l'accueil et les pages d'espace détectent le joueur connu et affichent
directement un bouton de démarrage rapide, sans repasser par l'OTP.

Une fois connecté, `/compte/` (« Mes quiz ») liste l'historique du joueur — jeu
public et chaque espace joué, avec score et rang — et une connexion initiée depuis
le lien d'un établissement atterrit sur une page de confirmation brandée
(`/e/slug/connecte/`) plutôt que l'accueil générique.

Pour un élève, la valeur n'est pas juste le score : `/compte/` calcule, par
établissement, un **taux de maîtrise par catégorie/sous-catégorie** (matière) —
pas seulement une moyenne globale qui masque les écarts — trié du point le plus
faible au plus fort, avec un encart « 🎯 Priorité » pointant vers la sous-catégorie
la plus en retard (< 70 %) et un lien direct pour s'entraîner dessus. C'est la
promesse vendue aux établissements : des métriques claires sur les points
forts/faibles de chaque élève, avec une orientation concrète pour combler les
lacunes — pas juste un historique de scores.

Un établissement peut aussi faire correspondre les participants à sa propre base
(élèves, employés…) : import CSV (`nom,telephone[,reference]`) depuis l'onglet
« Membres » du tableau de bord, avec appariement automatique par téléphone — à
l'import si le numéro a déjà joué, ou dès sa première participation sinon.

Chaque espace peut aussi définir un logo et une image de couverture (`logo_url`/
`cover_url` dans l'admin) affichés en bannière façon page Facebook sur ses pages ;
sans ces champs, repli sur l'emoji et un dégradé des couleurs de l'espace.

### Licences (par siège / au forfait) et cycles annuels

Un espace peut avoir une ou plusieurs `License` (gérées dans l'admin, tarif
convenu par établissement) portant une **période** (ex. « 2026-2027 ») — ce
concept vaut pour tout type d'établissement, pas seulement les écoles :
- **Par siège** (`billing_mode="per_seat"`) : un nombre de sièges maximum
  (`seat_count`). Ajouter un membre au-delà de la limite (ajout manuel ou import
  CSV) est **bloqué** avec un message clair tant que la licence n'est pas étendue.
- **Au forfait** (`billing_mode="forfait"`) : participation illimitée, adapté à un
  établissement non scolaire où limiter les participants n'a pas de sens
  (ex. une banque en campagne d'engagement).

Une licence est **optionnelle par espace** : sans licence active, un espace
continue de fonctionner exactement comme avant, sans aucune limite.

Chaque adhésion (`Membership`) est rattachée à la licence active au moment de sa
création — un même téléphone peut ainsi avoir **une ligne par période**, ce qui
conserve l'historique d'une année sur l'autre (ex. 5ème en 2026-2027 puis 4ème en
2027-2028) au lieu de l'écraser. Ce parcours est visible sur la fiche membre du
tableau de bord et sur la page « Mes quiz » (`/compte/`) du joueur, qui affiche
aussi les **quiz assignés non encore joués** d'après la catégorie/sous-catégorie de
**chacune** des adhésions du joueur dans cet établissement — licence en cours comme
licences passées (ex. un quiz de 6ème non terminé reste proposé même une fois passé
en 5ème, étiqueté avec sa période) — pas seulement l'historique des parties déjà
jouées. Un lien « Parcourir tous les quiz » renvoie en plus vers l'arbre de
l'établissement (`/e/slug/`), qui applique le même filtre : un membre au profil
connu n'y voit que les quiz de sa/ses catégorie(s)/sous-catégorie(s), avec un lien
explicite « voir tout le catalogue » (`?all=1`) pour sortir du filtre s'il le
souhaite. Un visiteur pas encore identifié (ou sans catégorie/sous-catégorie
renseignée) voit le catalogue complet par défaut, faute de profil à filtrer.

### Récompenses et jokers : optionnels, plus le cœur du système

Sur une nouvelle installation, le jeu public démarre **sans cagnotte ni jokers**
(`GameConfig.rewards_enabled = False` par défaut) : le défi du jour garde
l'élimination et le classement, sans mise en avant financière — activable d'un
clic dans l'admin pour retrouver le comportement complet (cagnotte, jokers,
onglet Portefeuille, qui ne s'affiche que si pertinent).

Côté espace établissement, la **récompense** est optionnelle et se résout en
cascade `Quiz` → `Space` → `License` (le premier niveau qui en définit une
l'emporte), typée monétaire / en nature / autre. Le **joker « pub vidéo »**
(seconde chance, pas d'achat) reste distinct du joker payant du jeu public : il
doit être autorisé par la licence de l'espace (`License.jokers_allowed`) puis
activé au cas par cas sur chaque quiz (`Quiz.joker_enabled`) — utile par exemple
pour une banque qui organise un quiz à récompense réelle, sans l'imposer par
défaut à tous les établissements.

L'accueil (`/`) s'adapte au profil connecté : un membre d'établissement atterrit
directement sur son espace personnel (`/compte/`), le défi public restant
accessible via l'onglet « Jouer » (`/defi-du-jour/`) ou pour tout visiteur non
connecté.

Quand une récompense est configurée pour un quiz (résolue via la même cascade), les
participants **ayant terminé** ce quiz (donc éligibles) sont mis en évidence — un
badge « 🎁 Éligible à la récompense » sur leur historique personnel (`/compte/`) et
sur la liste des meilleurs participants du tableau de bord établissement, pour que
l'entreprise sache concrètement qui récompenser.

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
