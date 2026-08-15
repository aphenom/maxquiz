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

**Tableau de bord client** sur `/e/slug/tableau-de-bord/` (protégé par identifiant +
mot de passe) : participants uniques et participations (avec la moyenne par
participant, pour distinguer portée et engagement), taux de complétion, contacts
consentants **rapportés au total de participants** (le consentement conditionne
l'export avec numéro — sans ce contexte, le chiffre brut ne veut rien dire), export
CSV, taux de bonne réponse par question trié des produits **les moins maîtrisés** aux
mieux connus (l'outil d'étude de marché), et répartition des réponses aux sondages.
Les résultats par catégorie (niveau, gamme de produits...) sont **repliés dans des
accordions**, un par catégorie — utile dès qu'il y a plusieurs niveaux/matières à
parcourir.

Le classement « Meilleurs participants » s'adapte à la structure de l'espace : dès
qu'il y a des **quiz distincts** (longueurs différentes), comparer la question
atteinte n'a pas de sens d'un quiz à l'autre — le tableau de bord bascule alors sur un
classement par **assiduité** (nombre de participations, comparable quel que soit le
quiz), le score par quiz restant sur sa page de détail (`dashboard_quiz_detail`, avec
le même repère en % qu'ailleurs sur le site plutôt qu'un numéro de question brut). Un
espace à pool unique (sans quiz structuré, ex. Banque Horizon) garde le classement par
score, puisque tout le monde y affronte le même jeu.

**Connexion** : une page unique, `/tableau-de-bord/connexion/`, sert **tous** les
établissements — pas besoin de distribuer une URL différente par client. L'identifiant
(`Space.dashboard_username`) est **généré automatiquement à la création de l'espace**,
volontairement distinct du slug d'URL (public, visible dans les liens `/e/slug/...` —
un identifiant de connexion ne doit pas être devinable à partir d'une URL publique) ;
le mot de passe (`Space.dashboard_code`) est créé par MQ Technologies dans l'admin
Django. Les deux sont communiqués à l'établissement, qui peut ensuite changer son mot
de passe lui-même depuis son tableau de bord (« 🔒 Mot de passe » dans le menu, ancien
mot de passe requis pour confirmer), sans repasser par l'admin. Toute visite directe
d'une page de tableau de bord sans session valide redirige vers cette connexion
commune (avec retour automatique sur la page demandée une fois connecté), sans jamais
révéler ni pré-remplir l'identifiant. Le menu propose aussi « 🚪 Déconnexion »
(`dashboard_logout`), qui ne retire que la session de **ce** tableau de bord — sans
affecter une éventuelle session élève active en parallèle dans le même navigateur.

Une session élève et une session établissement peuvent être actives **en même temps
dans le même navigateur** : elles vivent dans des clés de session distinctes
(`player_id`/`verified_player_id` côté élève, `dash_<id espace>` côté établissement),
sans interférence — se déconnecter de l'une n'affecte pas l'autre.

**Démo commerciale incluse** : `python manage.py seed_demo_space` crée l'espace
« Banque Horizon » (`/e/banque-horizon/`, identifiant tableau de bord `HORIZON-ADMIN`,
mot de passe `HORIZON2026`) avec 10 questions produits bancaires, 2 sondages et 40 participations
simulées pour un tableau de bord immédiatement parlant en rendez-vous.

### Performance et confort du tableau de bord à grande échelle

Les pages Questions, Quiz, Catégories et Membres sont **paginées côté serveur** avec
une **recherche fluide** (auto-soumission après une courte pause de frappe, focus
restauré après chaque rechargement) — nécessaire dès qu'un espace accumule des
centaines de questions, de quiz ou de membres, une liste à plat ne tiendrait pas la
charge.

Les pages Questions et Membres proposent aussi une **sélection multiple** : une case
à cocher par carte (rattachée à un formulaire dédié via l'attribut HTML `form=`,
sans imbriquer de formulaire dans un autre puisque chaque carte a déjà les siens),
une barre d'actions groupées qui apparaît dès qu'au moins une carte est cochée
(nombre sélectionné, tout désélectionner), et des actions par lot — activer/
désactiver/supprimer plusieurs questions à la fois, supprimer plusieurs membres à la
fois — chacune confirmée avant exécution vu leur caractère impactant (la suppression,
elle, reste réversible — voir ci-dessous).

### Suppression douce et journal d'activité

Aucune action de suppression du tableau de bord établissement (catégorie,
sous-catégorie, thématique, quiz, question, membre — individuelle ou en lot)
**n'efface réellement une ligne en base**. `SoftDeleteManager` (le manager par défaut
de ces six modèles) renseigne simplement `deleted_at` et filtre ces lignes de tout
accès normal — y compris les relations inverses (`categorie.subcategories.all()`,
`space.quizzes.all()`...), puisque Django utilise le manager par défaut du modèle
pour celles-ci : aucun appel existant n'a eu besoin d'être modifié pour respecter ce
filtre. Deux raisons à ce choix plutôt qu'un vrai `DELETE` :
- **Robustesse** : la cascade réelle de Django (`on_delete=CASCADE`) sur ces modèles
  aurait sinon effacé des données historiques (ex. supprimer une question détruit
  ses réponses (`Answer`), supprimer une catégorie détruit ses sous-catégories et
  thématiques) sans possibilité de retour en arrière ni de trace.
- **Traçabilité** : chaque création/modification/activation/suppression est
  journalisée (`AuditLog`, un enregistrement par objet même pour une action groupée)
  et consultable sur `/e/slug/tableau-de-bord/journal/` — qui, quoi, quand, avec un
  bouton « ♻️ Restaurer » en un clic sur toute entrée de suppression (l'objet étant
  toujours en base, la restauration ne fait que vider `deleted_at`).

Les contraintes d'unicité concernées (slug de catégorie/sous-catégorie/thématique/
quiz, couple téléphone+licence d'un membre) sont **conditionnelles**
(`UniqueConstraint(..., condition=Q(deleted_at__isnull=True))`) plutôt que globales :
sans ça, recréer un élément avec le même nom après une suppression douce heurterait
la ligne masquée mais toujours présente en base et ferait échouer l'enregistrement —
exactement le genre de blocage que la suppression douce doit éviter. Vérifié en
direct : supprimer puis recréer une catégorie ou un membre avec les mêmes
identifiants fonctionne sans erreur.

Limite connue, assumée par simplicité : la suppression cascade proprement (supprimer
une catégorie masque aussi ses sous-catégories et thématiques, supprimer un quiz
masque sa banque de questions dédiée), mais la **restauration ne cascade pas** —
restaurer une catégorie ne restaure pas automatiquement ses sous-catégories, il faut
les restaurer individuellement depuis le journal si besoin.

Les calculs qui alimentent la vue d'ensemble et le détail d'un quiz (taux de bonne
réponse par question, répartition des sondages, participations par quiz dans l'arbre
catégorie/sous-catégorie) sont construits sur des **requêtes groupées** plutôt
qu'une requête par question ou par quiz (évite le classique problème N+1) — un
espace avec une grosse banque de questions ou beaucoup de quiz ne ralentit pas le
chargement du tableau de bord.

Chaque lien de quiz partageable (`/e/slug/tableau-de-bord/quiz/`) a un bouton
« 📋 Copier » (presse-papiers du navigateur, repli sur la sélection de texte si
indisponible) — plus besoin de sélectionner puis Ctrl+C à la main.

Le jeu public MaxQuiz (défi du jour, cagnotte, jokers) reste inchangé et coexiste.

### Catégories, sous-catégories, thématiques & quiz (B2C comme B2B, multi-vertical)

Au-delà du pool de questions à plat (toujours disponible via le lien générique
`/e/slug/`), une entreprise peut structurer ses questions en **catégories** →
**sous-catégories** → **quiz**, avec un **lien direct par quiz**
(`/e/slug/q/quiz-slug/`) à distribuer au bon public — par exemple un niveau scolaire
et une matière pour une école, une famille de produits et une gamme pour une banque.
Les libellés « Catégorie »/« Sous-catégorie »/« Thématique » sont personnalisables
par espace (`category_label`/`subcategory_label`/`theme_label`, ex. « Niveau »/
« Matière »/« Thématique » pour une école, ou tout autre triplet pertinent hors
scolaire).

Un quiz peut en plus être rattaché à une **thématique**, un point plus précis à
l'intérieur d'une sous-catégorie (ex. « Conjugaison » au sein de « Français ») —
optionnel : un quiz sans thématique reste simplement classé au niveau de la
sous-catégorie (« Général »). Les questions elles-mêmes peuvent être taguées à
une thématique ; le quiz correspondant pioche en priorité dedans, avec un **repli
automatique** sur le reste de la sous-catégorie si pas assez de questions taguées
— jamais de blocage. Sur la page de l'établissement (`/e/slug/`), les quiz d'une
sous-catégorie sont groupés par thématique, avec les quiz généraux à part.

Ce système est **entièrement optionnel par espace** : un espace sans quiz créé (ex.
Banque Horizon aujourd'hui) continue de fonctionner exactement comme avant, avec le
lien unique et le pool de questions à plat.

**Tableau de bord client étendu**, accessible via les onglets Vue d'ensemble /
Catégories / Quiz :
- `/e/slug/tableau-de-bord/categories/` : créer/renommer/supprimer catégories,
  sous-catégories et thématiques (imbriquées sous leur sous-catégorie).
- `/e/slug/tableau-de-bord/quiz/` : créer un quiz (nom, catégorie, sous-catégorie,
  thématique optionnelle, nombre de questions, fréquence des sondages, mode
  survie, **rejouabilité** — une fois par jour / une seule fois jamais rejouable /
  illimité, réglable par quiz : adapté à un quiz d'évaluation type école (« une
  seule fois », pour que le taux de maîtrise affiché reste un signal fiable)
  comme à un quiz d'engagement type banque (« illimité » ou « une fois par
  jour »)), récupérer son lien partageable, l'activer/désactiver ou le supprimer.
- Vue d'ensemble : arbre catégorie → sous-catégorie → quiz (thématique affichée à
  côté du nom) avec participations et taux de complétion, jusqu'au détail par quiz
  (taux de bonne réponse par question, sondages, meilleurs participants) sur
  `/e/slug/tableau-de-bord/quiz/quiz-slug/`.

**Démo commerciale école incluse** : `python manage.py seed_demo_school_space` crée
l'espace « Collège La Réussite » (`/e/college-la-reussite/`, identifiant tableau de
bord `REUSSITE-ADMIN`, mot de passe `REUSSITE2026`) avec 4 niveaux (6ème à 3ème) × 2 matières (Mathématiques,
Français) = 8 quiz avec lien direct (ex. `/e/college-la-reussite/q/5eme-mathematiques/`),
plus un exemple de thématique (« Conjugaison » sous 6ème · Français, avec son
propre quiz « Entraînement conjugaison » et ses questions dédiées), 40+ questions
et des dizaines de participations simulées avec un taux de maîtrise différent par
quiz, pour un tableau de bord immédiatement parlant en rendez-vous. Tous ces
quiz sont en rejouabilité « une seule fois » (évaluation scolaire), pas
« une fois par jour » — cohérent avec le fait qu'ici le score doit rester un
signal fiable, pas une invitation à retenter jusqu'à un meilleur résultat.

### Quiz partagés (admin, sans espace) — un même programme scolaire pour tous

Un quiz peut être créé depuis l'admin Django **sans le rattacher à un espace
précis** : il porte alors juste un niveau et, optionnellement, une matière en
texte libre (`Quiz.shared_level_name`/`shared_subject_name`, ex. « 6ème » /
« Français »), avec sa propre banque de questions dédiée (`Question.quiz`).
Ce quiz devient **automatiquement disponible** — sans aucune configuration de
leur part — dans tout espace dont une Catégorie/Sous-catégorie porte
**exactement ce nom** (insensible à la casse), et pour les membres de cet
espace dont l'adhésion y correspond : il apparaît dans l'arbre de
l'établissement (`/e/slug/`, sous « Général », un quiz partagé n'a pas de
thématique propre), dans « Quiz à faire » sur `/compte/`, et dans la vue
d'ensemble du tableau de bord établissement (marqué 🌐, en lecture seule —
l'établissement suit la participation de ses membres mais ne peut ni le
modifier ni le supprimer, ce n'est pas son quiz).

Le matching étant strictement par nom, un espace qui a renommé sa catégorie
(ex. « 6eme RENOMME » au lieu de « 6ème ») ne bénéficie plus automatiquement
d'un quiz partagé tant que le nom ne correspond pas exactement — comportement
attendu, pas un bug. Le formulaire admin du quiz sépare clairement les deux
usages en deux sections : « Quiz propre à un espace » (`space`/`category`/
`sub_category`/`theme`, les selects habituels) vs « Quiz partagé » (niveau/
matière), pour ne pas donner l'impression qu'un quiz partagé serait quand
même rattaché à un espace précis. Les champs niveau/matière restent du texte
libre (un niveau pas encore créé par aucun espace doit pouvoir être saisi à
l'avance) mais proposent en suggestion (`<datalist>`) les noms de Catégorie/
Sous-catégorie déjà utilisés quelque part, pour limiter le risque de faute de
frappe qui casserait silencieusement le rattachement automatique. C'est le
mécanisme pensé pour construire, une fois, une bibliothèque de quiz alignée
sur un même programme scolaire et la
propager progressivement à tous les établissements qui l'utilisent, sans que
chacun ait à recréer son propre contenu.

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

À la 1ère connexion (`/compte/inscription/`), seules les infos **manquantes**
sont demandées — le nom n'est pas redemandé s'il est déjà connu (fourni par
l'établissement via lequel la connexion a eu lieu), pour ne pas faire perdre de
temps à l'utilisateur avec une info que l'établissement a déjà donnée. Cette
identité reste éditable à tout moment ensuite sur `/compte/profil/` (pseudo,
nom, ville), qui
liste aussi, pour chaque établissement où le joueur a une adhésion, sa
catégorie/sous-catégorie et sa licence en cours. Ce profil global (`Player`)
est indépendant de la fiche que chaque établissement tient sur lui
(`Membership.full_name`, propre à chaque espace) : si un même numéro est membre
de plusieurs établissements sous des identités différentes (ex. saisies via
deux imports CSV distincts), chacun garde la sienne — modifier son profil
public ne touche à aucune fiche établissement, et inversement. Le
préremplissage à l'inscription privilégie d'ailleurs l'établissement via
lequel la connexion a eu lieu, pas un autre choisi arbitrairement.

Pour un élève, la valeur n'est pas juste le score : `/compte/` calcule, par
établissement, un **taux de maîtrise par catégorie/sous-catégorie** (matière) —
pas seulement une moyenne globale qui masque les écarts — trié du point le plus
faible au plus fort, avec un encart « 🎯 Priorité » pointant vers la sous-catégorie
la plus en retard (< 70 %) et un lien direct pour s'entraîner dessus, et la même
chose **par thématique** quand les questions en portent une. C'est la
promesse vendue aux établissements : des métriques claires sur les points
forts/faibles de chaque élève, avec une orientation concrète pour combler les
lacunes — pas juste un historique de scores.

**Classement par quiz** : au-delà du classement du défi public, `/classement/`
liste pour un joueur connecté chacun des quiz d'établissement auxquels il a
déjà participé (« 🏫 Mes quiz d'établissement »), avec son rang et son
éligibilité à la récompense s'il y en a une — chaque quiz a son propre
classement complet sur `/e/slug/q/quiz-slug/classement/` (accessible aussi
depuis la page du quiz), qui affiche la récompense en tête si elle existe et
marque les participants ayant terminé comme éligibles.

**Corrections activables** (`Quiz.show_corrections`, décoché par défaut) :
un établissement peut choisir, quiz par quiz, de révéler la bonne réponse et
l'explication de chaque question dans l'historique du joueur sur `/compte/`
une fois la partie terminée — utile en pédagogie, mais pas automatique (ex.
un même quiz réutilisé sur plusieurs classes à des dates différentes). Pour
un quiz partagé (sans espace), c'est l'admin qui active ce réglage, pas de
tableau de bord établissement pour ce cas.

Un établissement peut aussi faire correspondre les participants à sa propre base
(élèves, employés…) : import en masse depuis l'onglet « Membres » du tableau de
bord, avec appariement automatique par téléphone — à l'import si le numéro a déjà
joué, ou dès sa première participation sinon.

**Modèle de fichier personnalisé** (`dashboard_members_template`, bouton
« ⬇️ Télécharger le modèle » au-dessus du formulaire d'import) : un `.xlsx` généré à
la volée avec les colonnes déjà aux libellés de l'espace (ex. « Niveau »/« Matière »
pour une école), et des **listes déroulantes de vérification** sur les colonnes
catégorie/sous-catégorie — une feuille « Catégories disponibles » liste toutes les
paires valides et sert de source à ces listes, pour qu'on ne puisse pas taper une
valeur qui ne matchera rien à l'import (faute de frappe, variante non reconnue).
L'import accepte aussi bien ce `.xlsx` rempli que l'ancien format CSV
(`nom,telephone,reference,categorie,sous_categorie` — seuls nom et téléphone sont
obligatoires, les colonnes suivantes optionnelles, résolues par nom insensible à la
casse). Le seul étage de complexité volontairement pas géré : la sous-catégorie
n'est pas filtrée dynamiquement selon la catégorie choisie (pas de liste en cascade)
— la feuille de référence reste la source de vérité à consulter en cas de doute.

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

Sur `/e/slug/tableau-de-bord/membres/`, le compteur de sièges ne porte que sur la
licence **en cours** — la liste des membres s'y limite donc **par défaut** pour que
ce chiffre reste traçable (« ce sont eux qui comptent dans les sièges ci-dessus »),
avec un sélecteur pour basculer sur une période précédente, « sans licence » ou
toutes les périodes ; la carte de chaque membre n'affiche sa période que quand la vue
n'est pas déjà filtrée dessus, pour ne rien répéter inutilement. La liste est
**paginée côté serveur** (30 par page) et une **recherche** (nom, téléphone,
référence) filtre par requête serveur avec auto-soumission après une courte pause de
frappe (debounce ~450 ms) plutôt qu'à chaque touche — nécessaire dès qu'il y a
beaucoup de membres, un simple filtre côté client ne tiendrait pas la charge.

Une licence est **optionnelle par espace** : sans licence active, un espace
continue de fonctionner exactement comme avant, sans aucune limite.

Chaque adhésion (`Membership`) est rattachée à la licence active au moment de sa
création — un même téléphone peut ainsi avoir **une ligne par période**, ce qui
conserve l'historique d'une année sur l'autre (ex. 5ème en 2026-2027 puis 4ème en
2027-2028) au lieu de l'écraser. Ce parcours est visible sur la fiche membre du
tableau de bord (`dashboard_member_detail`), qui reprend côté établissement les
mêmes insights que la page « Mes quiz » du joueur : taux de réussite global, points
forts/à travailler par matière puis par thématique (accordion, replié par défaut),
quiz encore à faire pour ce membre (avec avertissement d'expiration de licence), et
historique en accordion imbriqué — une ligne par quiz, avec % de réussite (ou
FINALISTE) plutôt qu'un numéro de question brut, éligibilité à la récompense, et un
lien direct vers la page de détail de ce quiz. Le tout construit sur les mêmes
requêtes que côté joueur, juste reciblées sur ce membre précis.

La page « Mes quiz » (`/compte/`) du joueur affiche
aussi les **quiz assignés non encore joués** d'après la catégorie/sous-catégorie de
**chacune** des adhésions du joueur dans cet établissement — licence en cours comme
licences passées (ex. un quiz de 6ème non terminé reste proposé même une fois passé
en 5ème, étiqueté avec sa période) — pas seulement l'historique des parties déjà
jouées. Un lien « Parcourir tous les quiz » renvoie en plus vers l'arbre de
l'établissement (`/e/slug/`), qui filtre lui aussi par profil — mais uniquement
sur l'**adhésion en cours** (licence active), pas l'historique : parcourir le
catalogue doit refléter le niveau actuel de l'élève, pas mélanger d'anciennes
années (celles-ci restent proposées, étiquetées, dans « Quiz à faire »
ci-dessus, pas dans l'arbre de découverte). Le filtre est strict, sans
échappatoire « voir tout le catalogue » : voir des niveaux qui ne le
concernent pas n'apporte rien à l'élève, ce qui lui est utile (son parcours,
son historique) est sur `/compte/`. Un visiteur pas encore identifié (ou sans
catégorie/sous-catégorie renseignée) voit le catalogue complet par défaut,
faute de profil à filtrer. Le cloisonnement dépend précisément de ce que
l'adhésion précise : une matière définie (sous-catégorie renseignée) limite à
cette seule matière ; un niveau seul (catégorie renseignée, pas de
sous-catégorie) ne cloisonne à rien — l'élève voit **toutes** les matières de
ce niveau, pas seulement les quiz sans matière du tout. Sur cette page
catalogue (`/e/slug/`), chaque matière (sous-catégorie) est **repliée dans
son propre accordion** dès qu'il y en a plus d'une à afficher côte à côte —
cas courant depuis ce même correctif, un profil niveau seul pouvant voir
plusieurs matières en même temps. Avec une seule matière (profil cloisonné à
une matière précise, ou catalogue à une seule matière), pas d'accordion :
inutile d'ajouter un clic quand il n'y a qu'une section à montrer.

Une fois la période d'une licence **passée** (désactivée dans l'admin, ou
date de fin dépassée), l'adhésion qu'elle couvre bascule en lecture seule :
ses quiz disparaissent de « Quiz à faire »/« Quiz en attente » et le
lancement direct d'un de ces quiz (`quiz_start`) est bloqué côté serveur avec
un message dédié — pas seulement caché de la liste, une tentative par URL
directe échoue aussi. Seuls les **résultats déjà obtenus** restent
consultables : l'historique, les stats détaillées et le classement par quiz
de cette période ne sont pas affectés. Si un même quiz reste par ailleurs
accessible via une autre adhésion du joueur (licence toujours active), il
continue d'être proposé normalement — seule l'adhésion expirée perd l'accès
au jeu, pas le quiz lui-même. Un quiz dont la licence expire dans **7 jours
ou moins** remonte en tête de « Quiz à faire »/« Quiz en attente » avec un
avertissement (« ⏳ Plus que N jours pour le faire ») : disparaître de la
liste sans prévenir aurait été frustrant pour l'élève.

Un élève qui découvre le lien d'un établissement sans que son numéro y ait
été chargé (oubli, faute de frappe, arrivée en cours d'année) peut **se
déclarer lui-même** un niveau (et une matière, facultative) directement
depuis `/e/slug/` — ça crée son adhésion pour la période en cours, avec le
catalogue filtré qui va avec. Cette auto-déclaration ne prend jamais le pas
sur une fiche déjà réglée par l'établissement (elle ne s'affiche que tant
qu'aucune catégorie n'est renseignée pour lui) et respecte la limite de
sièges de la licence le cas échéant ; l'établissement reste libre de la
corriger ensuite depuis son tableau de bord — ce n'est qu'un point de départ.

Sur l'accueil (`/`), un membre connecté voit ses **quiz en attente** (tous
établissements confondus) mis en avant, avant même le défi public du jour et
l'entraînement libre — l'accueil reste unique pour tout le monde, pas de
redirection séparée vers `/compte/` qui masquerait les options du jeu public.

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

### Navigation contextuelle et ambiance ludique/sobre

La barre d'onglets en bas de page (Jouer / Classement / Portefeuille / Mon
compte) s'adapte au contexte plutôt que de renvoyer systématiquement vers le
jeu public national : à l'intérieur d'un espace établissement (`/e/slug/...`),
« 🎮 Jouer » pointe vers le catalogue de cet établissement, et « 🏅 Classement »
vers le classement du quiz consulté quand il y en a un précis — pas vers le
classement du défi public. Ça évite de sortir un élève de son contexte
scolaire par réflexe de navigation ; en dehors de tout espace, la barre garde
son comportement public habituel.

Le ton très ludique du jeu (confettis, séries « 🔥 », vibrations) est pensé
pour le défi public, mais peut être coupé par espace via `Space.playful_fx`
(activé par défaut) — utile pour un quiz d'évaluation notée ou un quiz de
conformité bancaire, où l'ambiance festive serait déplacée. Minuteur, score et
retours texte restent identiques ; seuls les effets sont retirés.

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
