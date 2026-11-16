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

Chaque chapitre comprend :
- une **fiche de cours** affichée dans l'application. Elle contient l'essentiel, la méthode, un exemple corrigé, les pièges à éviter et ce qui tombe au BEPC ;
- la même fiche en **PDF** (à garder ou à imprimer), avec 4 questions « Teste-toi » corrigées ;
- un **quiz** de 12 à 15 questions de difficulté 1 à 4, avec une explication pour chaque réponse.

Le premier chapitre de chaque matière est ouvert sans abonnement, pour faire découvrir.

## Ce qui est livré : Terminale (dossier `terminale/`)

| Matière | Classes | Chapitres | Questions |
| --- | --- | --- | --- |
| Mathématiques | Tle C et D | 10 communs + Arithmétique et Similitudes (Tle C) + Statistiques à deux variables (Tle D) + Révision BAC | 149 |
| Mathématiques | Tle A | 7 chapitres + Révision BAC | 87 |
| Physique-Chimie | Tle C et D | 7 de physique + 7 de chimie + Révision BAC | 159 |
| SVT | Tle C et D | 9 chapitres + Révision BAC | 110 |
| Histoire-Géographie | Tle A, C et D | 7 d'histoire + 7 de géographie + Révision BAC | 165 |
| Philosophie | Tle A, C et D | 14 leçons + Méthode et révision BAC | 164 |
| Anglais | Tle A, C et D | 8 unités + Révision BAC | 101 |

Un chapitre commun à plusieurs classes est importé une fois par classe (une ligne par classe dans les Excel), avec une seule fiche PDF.

## Mettre le contenu en ligne (sur le serveur)

```bash
maxquiz migrate                       # ajoute l'EDHC aux matières du collège
maxquiz import_questions contenu/3eme/quiz.xlsx --shared --dry-run
maxquiz import_questions contenu/3eme/quiz.xlsx --shared
maxquiz import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches --dry-run
maxquiz import_cours contenu/3eme/cours.xlsx --fiches contenu/3eme/fiches

# Terminale
maxquiz import_questions contenu/terminale/quiz.xlsx --shared
maxquiz import_cours contenu/terminale/cours.xlsx --fiches contenu/terminale/fiches
```

On peut relancer les imports sans risque :
- les questions déjà présentes (même texte) ne sont pas recréées ;
- les cours existants sont mis à jour.

## Corriger ou compléter

- **Petite correction** (une faute, une vidéo à ajouter) : corrige directement dans l'administration (Cours, Questions).
- **Correction en masse** : modifie `sources/*.py`, puis lance `python contenu/generer.py 3eme` ou `python contenu/generer.py terminale` (il vérifie chaque question et refait les Excel et les PDF), puis relance les imports. Attention : une question dont on a changé le texte est importée comme une nouvelle question. Désactive l'ancienne dans l'administration.
- **Vidéos** : renseigne la colonne `youtube` de `cours.xlsx` (lien YouTube public ou non répertorié), puis relance `import_cours`.

Avant toute mise en ligne, un professeur de la matière relit chaque chapitre.
