# Contenu commun MaxQuiz

Cours et quiz originaux MaxQuiz, visibles par tous les élèves de la classe concernée (MaxQuiz École et écoles partenaires).

## Ce qui est livré : 3ème

| Matière | Chapitres | Questions |
| --- | --- | --- |
| Mathématiques | 14 chapitres + Révision BEPC | 187 |
| Physique-Chimie | 9 chapitres + Révision BEPC | 123 |
| SVT | 7 chapitres + Révision BEPC | 99 |
| Anglais | 8 chapitres + Révision BEPC | 112 |
| Histoire-Géographie | 9 chapitres + Révision BEPC | 123 |
| Français | 7 chapitres + Révision BEPC | 80 |

Chaque chapitre comprend :
- une **fiche de cours** affichée dans l'application. Elle contient l'essentiel, la méthode, un exemple corrigé, les pièges à éviter et ce qui tombe au BEPC ;
- la même fiche en **PDF** (à garder ou à imprimer), avec 4 questions « Teste-toi » corrigées ;
- un **quiz** de 12 à 15 questions de difficulté 1 à 4, avec une explication pour chaque réponse.

Le premier chapitre de chaque matière est ouvert sans abonnement, pour faire découvrir.
Les questions marquées d'un schéma l'affichent pendant la partie (voir « Schémas et illustrations »).

## Ce qui est livré : Terminale (dossier `terminale/`)

| Matière | Classes | Chapitres | Questions |
| --- | --- | --- | --- |
| Mathématiques | Tle C et D | 10 communs + Arithmétique et Similitudes (Tle C) + Statistiques à deux variables (Tle D) + Révision BAC | 149 |
| Mathématiques | Tle A | 7 chapitres + Révision BAC | 87 |
| Physique-Chimie | Tle C et D | 7 de physique + 7 de chimie + Révision BAC | 159 |
| SVT | Tle C et D | 9 chapitres + Révision BAC | 110 |
| Histoire-Géographie | Tle A, C et D | 7 d'histoire + 7 de géographie + Révision BAC | 165 |
| Philosophie | Tle A, C et D | 16 leçons + commentaire de texte, citations, méthode et révision BAC | 207 |
| Anglais | Tle A, C et D | 8 unités + 3 « Getting ready » (préparation au BAC) + Révision BAC | 133 |
| Français | Tle A, C et D | Figures de style, registres et versification, argumentation, résumé et discussion, commentaire composé, dissertation, littérature africaine, Révision BAC | 97 |

## Ce qui est livré : 4ème (dossier `4eme/`)

| Matière | Chapitres | Questions |
| --- | --- | --- |
| Mathématiques | 10 chapitres + Révision de l'année | 116 |
| Physique-Chimie | 8 chapitres (électricité, lumière) + Révision de l'année | 97 |
| EDHC | 8 chapitres + Révision de l'année | 91 |
| Français | Texte explicatif, dialogue argumentatif, compte rendu, lettre officielle, résumé, pronoms, modes, subordonnées, orthographe + Révision | 110 |
| Anglais | 6 unités (School life … Communication and technology) + Révision | 70 |
| Histoire-Géographie | 8 leçons d'histoire (peuples de Côte d'Ivoire, contacts avec l'Europe, traite, Révolution française, révolution industrielle, pénétration française) + Révision | 91 |
| SVT | 9 chapitres (puberté, fécondation, roches, sols, maladies liées à l'eau, traitement de l'eau) + Révision | 102 |

## Ce qui est livré : 5ème (dossier `5eme/`)

| Matière | Chapitres | Questions |
| --- | --- | --- |
| Mathématiques | 11 chapitres + Révision de l'année | 124 |
| Physique-Chimie | 8 chapitres (matière, mélanges, air, combustions, masse volumique) + Révision | 94 |
| EDHC | 19 leçons (programme officiel complet + compléments) + Révision de l'année | 200 |
| Français | Portrait, poème en vers libres, compte rendu, GN, adjectif, pronoms, verbe et voix passive, orthographe + Révision | 100 |
| Anglais | 6 unités (At school … Food, drinks and health) + Révision | 70 |
| Histoire-Géographie | 5 leçons d'histoire + 5 de géographie + Révision | 113 |

## Ce qui est livré : 6ème (dossier `6eme/`)

| Matière | Chapitres | Questions |
| --- | --- | --- |
| Physique-Chimie | 7 chapitres (grandeurs, longueurs, aires, volumes, masse, temps, température) + Révision | 83 |
| EDHC | 7 chapitres + Révision de l'année | 81 |
| Français | Récit, description, phrase, groupe nominal, verbe, discours rapporté, adverbes, lettre, orthographe + Révision | 110 |
| Anglais | 7 unités (At school … Health and environment) + Révision | 80 |
| Histoire-Géographie | 7 leçons d'histoire + 9 de géographie (relief, climat, cartes, mouvements de la Terre, eau, impôt…) + 2 révisions | 184 |
| SVT | 9 chapitres (production végétale, êtres vivants, fermentations, alimentation, puberté, eau, air) + Révision | 101 |

Un chapitre commun à plusieurs classes est importé une fois par classe (une ligne par classe dans les Excel), avec une seule fiche PDF.

## Mettre le contenu en ligne (sur le serveur)

```bash
maxquiz migrate                       # ajoute l'EDHC aux matières du collège
maxquiz import_questions contenu/3eme/quiz.xlsx --shared --dry-run
maxquiz import_questions contenu/3eme/quiz.xlsx --shared
maxquiz import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches --dry-run
maxquiz import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches

# 4ème
maxquiz import_questions contenu/4eme/quiz.xlsx --shared
maxquiz import_cours contenu/4eme/cours.xlsx --fiches contenu/4eme/fiches

# 5ème
maxquiz import_questions contenu/5eme/quiz.xlsx --shared
maxquiz import_cours contenu/5eme/cours.xlsx --fiches contenu/5eme/fiches

# 6ème
maxquiz import_questions contenu/6eme/quiz.xlsx --shared
maxquiz import_cours contenu/6eme/cours.xlsx --fiches contenu/6eme/fiches

# Terminale
maxquiz import_questions contenu/terminale/quiz.xlsx --shared
maxquiz import_cours contenu/terminale/cours.xlsx --fiches contenu/terminale/fiches
```

On peut relancer les imports sans risque :
- les questions déjà présentes (même texte) ne sont pas recréées ;
- les cours existants sont mis à jour.

## Schémas et illustrations (contenu/schemas.py)

Les schémas (figures de géométrie, circuits, montages, courbes, drapeau, panneaux…) sont dessinés
en code dans `contenu/schemas.py`, qui écrit un SVG par schéma dans `game/static/game/schemas/`.
- Dans une fiche : une ligne `[[schema:thales|Configuration de Thalès]]` affiche le schéma et sa légende
  (dans l'application et dans le PDF).
- Dans une question : un 8e élément au tuple, le nom du schéma ; il s'affiche au-dessus des réponses
  pendant la partie, et dans la colonne `schema` de quiz.xlsx.
- En administration, le champ « Schéma ou image » d'une question accepte aussi une adresse https.

```bash
pip install svglib          # une fois, pour mettre les schémas dans les PDF
python contenu/schemas.py   # redessine les schémas
python contenu/generer.py 4eme
```
Sur le serveur, les schémas arrivent avec `collectstatic` ; ré-importer quiz.xlsx met à jour
le schéma des questions déjà en ligne.

## Ordre de l'année (contenu/progression.py)

Chaque matière y a la liste de ses chapitres dans l'ordre habituel des établissements ivoiriens,
avec le mois où chacun est étudié (10 = octobre). `generer.py` range les chapitres, numérote les
fiches et remplit la colonne `mois` de `cours.xlsx` à partir de ce fichier ; il refuse de
générer si un chapitre y manque. L'application s'en sert pour dire à l'élève s'il est « à jour »
ou « en retard » dans chaque matière. Une école peut ajuster le mois d'un cours dans
l'administration (Cours > Mois du programme).

## Corriger ou compléter

- **Petite correction** (une faute, une vidéo à ajouter) : corrige directement dans l'administration (Cours, Questions).
- **Correction en masse** : modifie `sources/*.py`, puis lance `python contenu/generer.py 3eme` ou `python contenu/generer.py terminale` (il vérifie chaque question et refait les Excel et les PDF), puis relance les imports. Attention : une question dont on a changé le texte est importée comme une nouvelle question. Désactive l'ancienne dans l'administration.
- **Vidéos** : renseigne la colonne `youtube` de `cours.xlsx` (lien YouTube public ou non répertorié), puis relance `import_cours`.

Avant toute mise en ligne, un professeur de la matière relit chaque chapitre.
