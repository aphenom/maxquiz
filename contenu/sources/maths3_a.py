NIVEAU, MATIERE = "3ème", "Mathématiques"

CHAPITRES = [
dict(
nom="Calcul littéral",
fiche="""## Ce qu'il faut savoir
• Développer, c'est transformer un produit en somme.
   k(a + b) = ka + kb
   (a + b)(c + d) = ac + ad + bc + bd
• Factoriser, c'est l'inverse : transformer une somme en produit.
   ka + kb = k(a + b)

## Les trois identités remarquables
• (a + b)² = a² + 2ab + b²
• (a − b)² = a² − 2ab + b²
• (a + b)(a − b) = a² − b²
Elles servent dans les deux sens : pour développer vite, et pour factoriser.

## Méthode pour factoriser
1. Cherche d'abord un facteur commun : (x + 1)(2x − 3) + (x + 1)(x + 4) = (x + 1)[(2x − 3) + (x + 4)] = (x + 1)(3x + 1).
2. Sinon, reconnais une identité remarquable :
   x² − 49 = (x − 7)(x + 7)   (forme a² − b²)
   x² + 6x + 9 = (x + 3)²   (forme a² + 2ab + b²)
3. Vérifie toujours en redéveloppant ton résultat.

## Exemple corrigé
Factoriser A = (2x + 1)² − 9.
A est de la forme a² − b² avec a = 2x + 1 et b = 3.
A = (2x + 1 − 3)(2x + 1 + 3) = (2x − 2)(2x + 4) = 4(x − 1)(x + 2).

## Astuce de calcul mental
101² = (100 + 1)² = 10 000 + 200 + 1 = 10 201
49 × 51 = (50 − 1)(50 + 1) = 2 500 − 1 = 2 499

## Pièges à éviter
• (a + b)² n'est PAS égal à a² + b² : n'oublie jamais le double produit 2ab.
• Un signe « − » devant une parenthèse change tous les signes à l'intérieur : −(x − 3) = −x + 3.
• (−3)² = 9 mais −3² = −9.

## Au BEPC
L'exercice classique enchaîne : développer une expression, la factoriser, puis résoudre l'équation produit nul obtenue ou calculer sa valeur pour un nombre donné. Utilise la forme la plus pratique pour chaque question.""",
questions=[
(1, "Développer 3(x + 4) donne :", "3x + 12", "3x + 4", "x + 12", "3x + 7",
 "On multiplie 3 par chaque terme : 3 × x + 3 × 4 = 3x + 12."),
(1, "Le développement de (x + 5)² est :", "x² + 10x + 25", "x² + 25", "x² + 5x + 25", "2x + 10",
 "(a + b)² = a² + 2ab + b² avec a = x et b = 5 : x² + 2 × x × 5 + 25 = x² + 10x + 25."),
(1, "Le développement de (x − 3)² est :", "x² − 6x + 9", "x² − 9", "x² + 6x + 9", "x² − 6x − 9",
 "(a − b)² = a² − 2ab + b² : x² − 2 × x × 3 + 9 = x² − 6x + 9. Le dernier terme b² est toujours positif."),
(1, "(x + 2)(x − 2) est égal à :", "x² − 4", "x² + 4", "x² − 4x + 4", "2x",
 "C'est l'identité (a + b)(a − b) = a² − b² : x² − 2² = x² − 4."),
(2, "Une factorisation de 5x + 15 est :", "5(x + 3)", "5(x + 15)", "x(5 + 15)", "15(x + 5)",
 "5 est le facteur commun : 5x + 15 = 5 × x + 5 × 3 = 5(x + 3)."),
(2, "Une factorisation de x² − 49 est :", "(x − 7)(x + 7)", "(x − 7)²", "(x + 7)²", "(x − 49)(x + 49)",
 "x² − 49 = x² − 7², de la forme a² − b² = (a − b)(a + b)."),
(2, "Une factorisation de x² + 6x + 9 est :", "(x + 3)²", "(x + 9)²", "(x + 3)(x − 3)", "x(x + 6) + 9",
 "x² + 6x + 9 = x² + 2 × x × 3 + 3², de la forme a² + 2ab + b² = (a + b)². « x(x + 6) + 9 » reste une somme, ce n'est pas une factorisation."),
(2, "Le développement de (2x + 1)(x − 3) est :", "2x² − 5x − 3", "2x² − 7x − 3", "2x² − 5x + 3", "2x² + x − 3",
 "(2x + 1)(x − 3) = 2x² − 6x + x − 3 = 2x² − 5x − 3."),
(3, "Une factorisation de (x + 1)(2x − 3) + (x + 1)(x + 4) est :", "(x + 1)(3x + 1)", "(x + 1)(3x + 7)", "(x + 1)(x − 7)", "(x + 1)²(3x + 1)",
 "(x + 1) est le facteur commun : (x + 1)[(2x − 3) + (x + 4)] = (x + 1)(3x + 1)."),
(3, "Une factorisation de (3x − 1)² − 16 est :", "(3x − 5)(3x + 3)", "(3x − 17)(3x + 15)", "(3x + 3)²", "(3x − 5)²",
 "Forme a² − b² avec a = 3x − 1 et b = 4 : (3x − 1 − 4)(3x − 1 + 4) = (3x − 5)(3x + 3)."),
(3, "La valeur de E = x² − 2x + 1 pour x = −2 est :", "9", "1", "−7", "5",
 "E = (−2)² − 2 × (−2) + 1 = 4 + 4 + 1 = 9. On peut aussi voir que E = (x − 1)² = (−3)² = 9."),
(4, "En utilisant une identité remarquable, 101² est égal à :", "10 201", "10 001", "10 101", "10 200",
 "101² = (100 + 1)² = 100² + 2 × 100 × 1 + 1² = 10 000 + 200 + 1 = 10 201."),
(4, "En utilisant une identité remarquable, 49 × 51 est égal à :", "2 499", "2 501", "2 450", "2 549",
 "49 × 51 = (50 − 1)(50 + 1) = 50² − 1² = 2 500 − 1 = 2 499."),
]),

dict(
nom="Racines carrées",
fiche="""## Définition
Pour un nombre a positif ou nul, √a est le nombre positif dont le carré est a.
√49 = 7 car 7² = 49 et 7 est positif.
Pour tout a ≥ 0 : (√a)² = a et √(a²) = a.
La racine carrée d'un nombre négatif n'existe pas.

## Propriétés (a ≥ 0 et b ≥ 0)
• √(a × b) = √a × √b
• √(a ÷ b) = √a ÷ √b   (b ≠ 0)
• ATTENTION : √(a + b) n'est PAS égal à √a + √b.
   √(16 + 9) = √25 = 5, alors que √16 + √9 = 4 + 3 = 7.

## Simplifier une racine
On fait apparaître le plus grand carré parfait (4, 9, 16, 25, 36, 49…).
√72 = √(36 × 2) = 6√2
√12 + √27 = 2√3 + 3√3 = 5√3

## Rendre rationnel un dénominateur
• Avec une racine seule : 6/√3 = (6 × √3)/(√3 × √3) = 6√3/3 = 2√3.
• Avec une somme ou une différence, on multiplie par la quantité conjuguée :
   1/(√2 − 1) = (√2 + 1)/[(√2 − 1)(√2 + 1)] = (√2 + 1)/(2 − 1) = √2 + 1.

## Équation x² = a
• Si a > 0 : deux solutions, √a et −√a.  x² = 81 donne x = 9 ou x = −9.
• Si a = 0 : une solution, 0.
• Si a < 0 : aucune solution.

## Exemple corrigé
Diagonale d'un carré de côté 5 cm : d² = 5² + 5² = 50, donc d = √50 = √(25 × 2) = 5√2 cm (environ 7,07 cm).

## Pièges à éviter
• √9 = 3, jamais « 3 ou −3 » : une racine carrée est toujours positive.
• (√5 + 1)² se développe avec l'identité remarquable : 5 + 2√5 + 1 = 6 + 2√5.""",
questions=[
(1, "√49 est égal à :", "7", "−7", "24,5", "7 ou −7",
 "7² = 49 et une racine carrée est toujours positive, donc √49 = 7."),
(1, "(√5)² est égal à :", "5", "25", "10", "2,5",
 "Pour tout a ≥ 0, (√a)² = a."),
(1, "√(9 × 16) est égal à :", "12", "25", "144", "7",
 "√(9 × 16) = √9 × √16 = 3 × 4 = 12."),
(2, "La forme simplifiée de √72 est :", "6√2", "8√3", "4√2", "36√2",
 "72 = 36 × 2 et 36 est un carré parfait : √72 = √36 × √2 = 6√2."),
(2, "√12 + √27 est égal à :", "5√3", "√39", "5√6", "6√3",
 "√12 = 2√3 et √27 = 3√3, donc la somme vaut 5√3. On n'additionne jamais les nombres sous les racines."),
(2, "√(16 + 9) est égal à :", "5", "7", "25", "12,5",
 "On calcule d'abord sous la racine : √25 = 5. Attention, √(16 + 9) n'est pas √16 + √9 = 7."),
(2, "6/√3 s'écrit sans racine au dénominateur :", "2√3", "6√3", "3√2", "3√3",
 "6/√3 = 6√3/3 = 2√3."),
(3, "Les solutions de l'équation x² = 81 sont :", "−9 et 9", "9 seulement", "40,5", "Il n'y en a pas",
 "81 > 0 : deux solutions, √81 = 9 et −√81 = −9. Vérifie : (−9)² = 81."),
(3, "L'équation x² = −4 :", "n'a pas de solution", "a pour solution −2", "a pour solutions 2 et −2", "a pour solution 16",
 "Un carré est toujours positif ou nul : il ne peut pas être égal à −4."),
(3, "(2 − √3)(2 + √3) est égal à :", "1", "7", "4 − √3", "−1",
 "Identité (a − b)(a + b) = a² − b² : 4 − 3 = 1."),
(3, "(√5 + 1)² est égal à :", "6 + 2√5", "6", "6 + √5", "4 + 2√5",
 "(a + b)² = a² + 2ab + b² : 5 + 2√5 + 1 = 6 + 2√5."),
(4, "1/(√2 − 1) s'écrit sans racine au dénominateur :", "√2 + 1", "√2 − 1", "(√2 + 1)/3", "−√2 − 1",
 "On multiplie par la quantité conjuguée √2 + 1 : le dénominateur devient (√2)² − 1² = 1."),
(4, "La diagonale d'un carré de côté 5 cm mesure :", "5√2 cm", "10 cm", "25 cm", "√10 cm",
 "Pythagore : d² = 5² + 5² = 50, donc d = √50 = 5√2 cm, environ 7,07 cm."),
]),

dict(
nom="Calcul numérique",
fiche="""## Puissances (a et b non nuls, n et m entiers)
• aⁿ × aᵐ = aⁿ⁺ᵐ      2³ × 2⁴ = 2⁷
• aⁿ ÷ aᵐ = aⁿ⁻ᵐ      10⁵ ÷ 10² = 10³
• (aⁿ)ᵐ = aⁿˣᵐ         (5²)³ = 5⁶
• (a × b)ⁿ = aⁿ × bⁿ
• a⁰ = 1 et a⁻ⁿ = 1/aⁿ     10⁻³ = 0,001
• Attention : (−3)² = 9 mais −3² = −9.

## Notation scientifique
Un nombre s'écrit a × 10ⁿ avec 1 ≤ a < 10.
45 000 = 4,5 × 10⁴      0,000 32 = 3,2 × 10⁻⁴
La Côte d'Ivoire compte environ 30 000 000 d'habitants, soit 3 × 10⁷.

## Fractions
• Additionner : même dénominateur d'abord. 2/3 + 1/4 = 8/12 + 3/12 = 11/12
• Multiplier : numérateurs entre eux, dénominateurs entre eux.
• Diviser : multiplier par l'inverse. (3/5) ÷ (9/10) = (3/5) × (10/9) = 30/45 = 2/3
• Toujours simplifier le résultat.

## Ordre et inégalités
• Ajouter ou retrancher un même nombre conserve l'ordre.
• Multiplier ou diviser par un nombre POSITIF conserve l'ordre.
• Multiplier ou diviser par un nombre NÉGATIF change le sens de l'inégalité.
   Si a < b alors −2a > −2b.
• On peut additionner des encadrements membre à membre :
   si 2 < x < 3 et 1 < y < 4, alors 3 < x + y < 7.

## Valeurs approchées
• Encadrement : 1,41 < √2 < 1,42 est un encadrement d'amplitude 0,01.
• Troncature : on coupe. Troncature au millième de 2,718 28 : 2,718.
• Arrondi : on regarde le chiffre suivant (5 ou plus, on augmente). Arrondi au centième de 3,146 : 3,15.

## Pièges à éviter
• 2³ × 2⁴ ne donne pas 2¹² : on additionne les exposants.
• 45 × 10³ n'est pas une notation scientifique, car 45 n'est pas entre 1 et 10.""",
questions=[
(1, "2³ × 2⁴ est égal à :", "2⁷", "2¹²", "4⁷", "2¹",
 "Même base : on additionne les exposants. 3 + 4 = 7."),
(1, "10⁻³ est égal à :", "0,001", "−1 000", "0,000 1", "−0,001",
 "10⁻³ = 1/10³ = 1/1 000 = 0,001. Un exposant négatif ne rend pas le nombre négatif."),
(1, "La notation scientifique de 45 000 est :", "4,5 × 10⁴", "45 × 10³", "4,5 × 10³", "0,45 × 10⁵",
 "Le premier facteur doit être entre 1 et 10 : 45 000 = 4,5 × 10 000 = 4,5 × 10⁴."),
(2, "La notation scientifique de 0,000 32 est :", "3,2 × 10⁻⁴", "3,2 × 10⁴", "32 × 10⁻⁵", "3,2 × 10⁻³",
 "On déplace la virgule de 4 rangs vers la droite pour obtenir 3,2 : l'exposant est −4."),
(2, "−3² est égal à :", "−9", "9", "6", "−6",
 "Le carré porte seulement sur 3 : −3² = −(3 × 3) = −9. Avec des parenthèses, (−3)² = 9."),
(2, "(5²)³ est égal à :", "5⁶", "5⁵", "5⁸", "5⁹",
 "Puissance d'une puissance : on multiplie les exposants, 2 × 3 = 6."),
(2, "2/3 + 1/4 est égal à :", "11/12", "3/7", "3/12", "2/12",
 "On met au même dénominateur 12 : 8/12 + 3/12 = 11/12. On n'additionne jamais les dénominateurs."),
(2, "(3/5) ÷ (9/10) est égal à :", "2/3", "27/50", "3/2", "9/50",
 "Diviser, c'est multiplier par l'inverse : (3/5) × (10/9) = 30/45 = 2/3."),
(3, "Si a < b, alors :", "−2a > −2b", "−2a < −2b", "−2a = −2b", "On ne peut pas comparer −2a et −2b",
 "Multiplier par un nombre négatif (−2) change le sens de l'inégalité."),
(3, "L'arrondi au millième de 2,718 28 est :", "2,718", "2,719", "2,71", "2,718 3",
 "Au millième, on garde 3 chiffres après la virgule. Le chiffre suivant est 2 (moins de 5) : on garde 2,718."),
(3, "L'amplitude de l'encadrement 1,41 < √2 < 1,42 est :", "0,01", "0,1", "1", "2,83",
 "L'amplitude est la différence entre les deux bornes : 1,42 − 1,41 = 0,01."),
(4, "Si 2 < x < 3 et 1 < y < 4, alors :", "3 < x + y < 7", "2 < x + y < 12", "3 < x + y < 5", "1 < x + y < 3",
 "On additionne membre à membre : 2 + 1 < x + y < 3 + 4."),
(4, "La lumière parcourt 3 × 10⁸ m par seconde. En une minute, elle parcourt :", "1,8 × 10¹⁰ m", "1,8 × 10⁹ m", "3 × 10⁹ m", "5 × 10⁶ m",
 "3 × 10⁸ × 60 = 180 × 10⁸ = 1,8 × 10² × 10⁸ = 1,8 × 10¹⁰ m."),
]),

dict(
nom="Équations et inéquations à une inconnue",
fiche="""## Équation du premier degré
On isole l'inconnue en faisant la même opération des deux côtés.
5x − 4 = 11  →  5x = 15  →  x = 3
Vérification : 5 × 3 − 4 = 11. ✔

## Équation produit nul
Un produit est nul si et seulement si l'un de ses facteurs est nul.
(x − 2)(x + 5) = 0  ⇔  x − 2 = 0 ou x + 5 = 0  ⇔  x = 2 ou x = −5
Si l'équation n'est pas sous cette forme, on factorise d'abord :
x² − 9 = 0  ⇔  (x − 3)(x + 3) = 0  ⇔  x = 3 ou x = −3

## Inéquation du premier degré
Même méthode que pour une équation, avec UNE règle de plus :
quand on multiplie ou divise par un nombre négatif, on change le sens.
−2x ≥ 8  →  x ≤ −4
Les solutions s'écrivent avec un intervalle :
x ≤ 3 : ]−∞ ; 3]      x > 4 : ]4 ; +∞[
Le crochet est tourné vers le nombre s'il est compris (≤ ou ≥), vers l'extérieur sinon (< ou >).

## Résoudre un problème en 5 étapes
1. Choisir l'inconnue (« soit x le prix d'un cahier »).
2. Traduire l'énoncé par une équation.
3. Résoudre.
4. Vérifier avec l'énoncé.
5. Rédiger une phrase de réponse.

## Exemple corrigé
Aya achète 3 cahiers identiques et un stylo à 150 F. Elle paie 1 050 F. Quel est le prix d'un cahier ?
Soit x le prix d'un cahier : 3x + 150 = 1 050, donc 3x = 900 et x = 300.
Vérification : 3 × 300 + 150 = 1 050. ✔
Un cahier coûte 300 F.

## Pièges à éviter
• Oublier de changer le sens d'une inéquation en divisant par un négatif.
• Ne donner qu'une solution d'une équation produit nul : il y en a souvent deux.""",
questions=[
(1, "La solution de 2x + 6 = 0 est :", "x = −3", "x = 3", "x = 4", "x = −8",
 "2x = −6, donc x = −6 ÷ 2 = −3."),
(1, "La solution de 5x − 4 = 11 est :", "x = 3", "x = 7/5", "x = −3", "x = 15",
 "5x = 11 + 4 = 15, donc x = 3. Vérification : 15 − 4 = 11."),
(2, "Les solutions de (x − 2)(x + 5) = 0 sont :", "x = 2 ou x = −5", "x = −2 ou x = 5", "x = 2 seulement", "x = −10",
 "Un produit est nul si l'un des facteurs est nul : x − 2 = 0 ou x + 5 = 0."),
(2, "Les solutions de 3x − 7 < 5 sont :", "x < 4", "x > 4", "x < −4/3", "x < 12",
 "3x < 12, et on divise par 3 (positif) sans changer le sens : x < 4."),
(2, "Les solutions de −2x ≥ 8 sont :", "x ≤ −4", "x ≥ −4", "x ≤ 4", "x ≥ 4",
 "On divise par −2, nombre négatif : le sens de l'inégalité change."),
(2, "L'ensemble des nombres x tels que x ≤ 3 s'écrit :", "]−∞ ; 3]", "]−∞ ; 3[", "[3 ; +∞[", "]3 ; +∞[",
 "3 est compris (≤), donc le crochet est tourné vers 3 : ]−∞ ; 3]."),
(3, "La solution de 4(x − 1) = 2x + 6 est :", "x = 5", "x = 3,5", "x = 1", "x = −5",
 "4x − 4 = 2x + 6, puis 2x = 10, donc x = 5. Vérification : 4 × 4 = 16 et 10 + 6 = 16."),
(3, "Les solutions de x² − 9 = 0 sont :", "x = −3 ou x = 3", "x = 3 seulement", "x = 9", "Il n'y en a pas",
 "x² − 9 = (x − 3)(x + 3) = 0, donc x = 3 ou x = −3."),
(3, "Aya achète 3 cahiers identiques et un stylo à 150 F. Elle paie 1 050 F. Un cahier coûte :", "300 F", "400 F", "350 F", "900 F",
 "3x + 150 = 1 050, donc 3x = 900 et x = 300. 900 F est le prix des 3 cahiers ensemble."),
(3, "Les solutions de (2x + 1)(x − 3) = 0 sont :", "x = −1/2 ou x = 3", "x = 1/2 ou x = −3", "x = −1/2 seulement", "x = 2 ou x = 3",
 "2x + 1 = 0 donne x = −1/2 ; x − 3 = 0 donne x = 3."),
(4, "Koffi a 15 ans et son père 41 ans. Dans combien d'années le père aura-t-il le double de l'âge de Koffi ?", "11 ans", "13 ans", "15 ans", "26 ans",
 "41 + x = 2(15 + x), donc 41 + x = 30 + 2x et x = 11. Vérification : Koffi aura 26 ans et son père 52 ans."),
(4, "La solution de x/2 + x/3 = 10 est :", "x = 12", "x = 2", "x = 25", "x = 60",
 "x/2 + x/3 = 3x/6 + 2x/6 = 5x/6 = 10, donc x = 60 ÷ 5 = 12."),
(4, "Le plus petit nombre entier qui vérifie 3x + 2 > 14 est :", "5", "4", "6", "3",
 "3x > 12, donc x > 4. 4 ne convient pas (inégalité stricte) : le plus petit entier est 5."),
]),

dict(
nom="Équations et inéquations à deux inconnues",
fiche="""## Système de deux équations
On cherche les couples (x ; y) qui vérifient les deux équations en même temps.
Exemple :  2x + y = 7  et  x − y = 2

## Méthode par combinaison (addition)
On additionne les équations pour faire disparaître une inconnue.
(2x + y) + (x − y) = 7 + 2  →  3x = 9  →  x = 3
Puis on remplace : 3 − y = 2  →  y = 1. Solution : (3 ; 1).

## Méthode par substitution
On exprime une inconnue en fonction de l'autre, puis on remplace.
y = 2x et x + y = 12  →  x + 2x = 12  →  x = 4 et y = 8.

## Méthode graphique
Chaque équation est une droite. La solution est le couple des coordonnées du point d'intersection.
• Droites sécantes : une seule solution.
• Droites parallèles : aucune solution (x + y = 3 et 2x + 2y = 5).
• Droites confondues : une infinité de solutions.

## Inéquation à deux inconnues
Les solutions de ax + by + c < 0 forment un demi-plan.
1. Trace la droite frontière ax + by + c = 0.
2. Teste un point qui n'est pas sur la droite, souvent O(0 ; 0).
3. S'il vérifie l'inéquation, son côté est la solution ; sinon, c'est l'autre côté.
Pour un système d'inéquations, la solution est la partie commune aux demi-plans.

## Exemple corrigé (au marché)
2 kg de riz et 1 L d'huile coûtent 2 100 F ; 1 kg de riz et 2 L d'huile coûtent 2 700 F.
Soit r le prix du kg de riz et h celui du litre d'huile : 2r + h = 2 100 et r + 2h = 2 700.
De la première, h = 2 100 − 2r. Dans la deuxième : r + 4 200 − 4r = 2 700, donc r = 500 et h = 1 100.
Vérification : 1 000 + 1 100 = 2 100 ✔ et 500 + 2 200 = 2 700 ✔.

## Pièges à éviter
• Vérifier la solution dans les DEUX équations, pas une seule.
• Donner la réponse sous forme de couple, dans l'ordre (x ; y).""",
questions=[
(1, "Le couple solution du système x + y = 5 et x − y = 1 est :", "(3 ; 2)", "(2 ; 3)", "(5 ; 0)", "(4 ; 1)",
 "En additionnant : 2x = 6, donc x = 3, puis y = 2. (4 ; 1) vérifie la première équation mais pas la deuxième."),
(1, "Le couple (2 ; −1) est solution de l'équation :", "3x + 2y = 4", "3x + 2y = 8", "x + y = 3", "2x − y = 3",
 "3 × 2 + 2 × (−1) = 6 − 2 = 4."),
(2, "La solution du système x + y = 10 et x − y = 4 est :", "(7 ; 3)", "(3 ; 7)", "(6 ; 4)", "(14 ; −4)",
 "2x = 14, donc x = 7 et y = 3."),
(2, "La solution du système 2x + y = 7 et x − y = 2 est :", "(3 ; 1)", "(1 ; 3)", "(2 ; 3)", "(3 ; −1)",
 "En additionnant : 3x = 9, donc x = 3, puis y = 1. (2 ; 3) ne vérifie que la première équation."),
(2, "La solution du système y = 2x et x + y = 12 est :", "(4 ; 8)", "(8 ; 4)", "(6 ; 6)", "(4 ; 6)",
 "Par substitution : x + 2x = 12, donc x = 4 et y = 8."),
(2, "La droite frontière de l'inéquation x + 2y ≤ 6 passe par les points :", "(0 ; 3) et (6 ; 0)", "(0 ; 6) et (3 ; 0)", "(0 ; 2) et (6 ; 0)", "(2 ; 0) et (0 ; 6)",
 "Pour x = 0 : 2y = 6, y = 3. Pour y = 0 : x = 6."),
(3, "2 kg de riz et 1 L d'huile coûtent 2 100 F ; 1 kg de riz et 2 L d'huile coûtent 2 700 F. Les prix sont :", "riz 500 F/kg, huile 1 100 F/L", "riz 600 F/kg, huile 900 F/L", "riz 700 F/kg, huile 700 F/L", "riz 1 100 F/kg, huile 500 F/L",
 "2r + h = 2 100 et r + 2h = 2 700 donnent r = 500 et h = 1 100. Les autres propositions ne vérifient qu'une des deux équations, ou aucune."),
(3, "Graphiquement, la solution d'un système de deux équations correspond :", "aux coordonnées du point d'intersection des deux droites", "au point où une droite coupe l'axe des abscisses", "au coefficient directeur des droites", "à l'origine du repère",
 "Le point d'intersection est sur les deux droites : ses coordonnées vérifient les deux équations."),
(3, "Dans un enclos, il y a 20 animaux, des poules et des chèvres, et 56 pattes. Combien y a-t-il de chèvres ?", "8", "12", "10", "14",
 "p + c = 20 et 2p + 4c = 56. En remplaçant p = 20 − c : 40 + 2c = 56, donc c = 8 (et 12 poules)."),
(3, "Pour l'inéquation x + y − 3 > 0, le point O(0 ; 0) :", "n'appartient pas au demi-plan solution", "appartient au demi-plan solution", "est sur la droite frontière", "ne permet pas de conclure",
 "0 + 0 − 3 = −3, qui n'est pas strictement positif : O est du mauvais côté, la solution est l'autre demi-plan."),
(4, "Le système x + y = 3 et 2x + 2y = 5 :", "n'a aucune solution", "a une infinité de solutions", "a pour solution (1 ; 2)", "a pour solution (1,5 ; 1,5)",
 "La deuxième équation donne x + y = 2,5, incompatible avec x + y = 3 : les deux droites sont parallèles."),
(4, "Pour un concert, le billet adulte coûte 2 000 F et le billet enfant 1 000 F. On a vendu 150 billets pour 230 000 F. Combien de billets adultes ?", "80", "70", "75", "115",
 "a + e = 150 et 2 000a + 1 000e = 230 000, soit 2a + e = 230. En soustrayant : a = 80 (et 70 enfants)."),
]),

dict(
nom="Applications affines",
fiche="""## Définitions
• Une application affine s'écrit f(x) = ax + b.
   a est le coefficient, b est l'ordonnée à l'origine.
• Si b = 0 : f(x) = ax est une application linéaire (situation de proportionnalité).
• Si a = 0 : f(x) = b est une application constante.

## Image et antécédent
• Image de 4 par f(x) = 3x − 2 : f(4) = 3 × 4 − 2 = 10.
• Antécédent de 7 par f(x) = 2x + 1 : on résout 2x + 1 = 7, donc x = 3.

## Représentation graphique
C'est une droite. Elle coupe l'axe des ordonnées au point (0 ; b).
Pour la tracer, il suffit de calculer deux points.

## Trouver a et b à partir de deux valeurs
a = [f(x₂) − f(x₁)] ÷ (x₂ − x₁)
Exemple : f(2) = 1 et f(4) = 7, donc a = (7 − 1) ÷ (4 − 2) = 3.
Puis f(2) = 3 × 2 + b = 1, donc b = −5 : f(x) = 3x − 5.

## Sens de variation
• a > 0 : f est croissante (la droite monte).
• a < 0 : f est décroissante (la droite descend).
• a = 0 : f est constante (droite horizontale).

## Exemple corrigé (taxi compteur)
Un taxi compte 500 F de prise en charge, puis 200 F par kilomètre. Prix pour x km : f(x) = 200x + 500.
Pour 7 km : f(7) = 1 400 + 500 = 1 900 F.

## Comparer deux offres
Offre A : 5 000 F par mois. Offre B : 2 000 F + 300 F par heure.
B coûte plus cher que A quand 2 000 + 300h > 5 000, c'est-à-dire h > 10.
Au-delà de 10 heures par mois, l'offre A est la plus avantageuse.

## Pièges à éviter
• Ne pas confondre image (on calcule f(x)) et antécédent (on résout f(x) = …).
• Dans f(x) = 5 − 2x, le coefficient est −2 et l'ordonnée à l'origine est 5.""",
questions=[
(1, "Pour f(x) = 3x − 2, f(4) est égal à :", "10", "14", "12", "2",
 "f(4) = 3 × 4 − 2 = 12 − 2 = 10."),
(1, "Dans f(x) = −2x + 5, le coefficient est :", "−2", "5", "2", "3",
 "Dans f(x) = ax + b, le coefficient est a, le nombre qui multiplie x : ici −2."),
(1, "Laquelle de ces applications est linéaire ?", "f(x) = 4x", "f(x) = 4x + 1", "f(x) = x²", "f(x) = 4",
 "Une application linéaire est de la forme f(x) = ax, sans terme constant."),
(2, "L'antécédent de 7 par f(x) = 2x + 1 est :", "3", "15", "4", "8",
 "On résout 2x + 1 = 7 : 2x = 6, donc x = 3. 15 est l'image de 7, pas son antécédent."),
(2, "f est affine avec f(1) = 5 et f(3) = 11. Son coefficient est :", "3", "6", "2", "4",
 "a = (11 − 5) ÷ (3 − 1) = 6 ÷ 2 = 3."),
(2, "f est affine avec f(0) = 4 et f(2) = 10. Alors f(x) est égal à :", "3x + 4", "4x + 3", "5x", "3x + 10",
 "f(0) = b = 4. Puis a = (10 − 4) ÷ 2 = 3."),
(2, "L'application f(x) = −x + 3 est :", "décroissante", "croissante", "constante", "linéaire",
 "Son coefficient −1 est négatif : la fonction est décroissante."),
(3, "Un taxi compte 500 F de prise en charge et 200 F par kilomètre. Une course de 7 km coûte :", "1 900 F", "1 400 F", "3 500 F", "1 200 F",
 "f(7) = 200 × 7 + 500 = 1 400 + 500 = 1 900 F."),
(3, "Offre A : 5 000 F par mois. Offre B : 2 000 F + 300 F par heure. L'offre A devient plus avantageuse :", "au-delà de 10 heures", "au-delà de 5 heures", "au-delà de 15 heures", "jamais",
 "B est plus chère quand 2 000 + 300h > 5 000, c'est-à-dire 300h > 3 000, soit h > 10."),
(3, "La droite représentant f(x) = 2x − 3 coupe l'axe des ordonnées au point :", "(0 ; −3)", "(−3 ; 0)", "(1,5 ; 0)", "(0 ; 2)",
 "Sur l'axe des ordonnées, x = 0, et f(0) = −3."),
(4, "La droite d'une application affine f passe par A(2 ; 1) et B(4 ; 7). Alors f(x) est égal à :", "3x − 5", "3x + 1", "2x − 3", "3x − 1",
 "a = (7 − 1) ÷ (4 − 2) = 3, puis 3 × 2 + b = 1, donc b = −5. 2x − 3 passe par A mais pas par B."),
(4, "3 litres d'essence coûtent 2 325 F. Le prix est proportionnel au nombre de litres. Le coefficient de l'application linéaire est :", "775", "6 975", "3 100", "700",
 "Le coefficient est le prix d'un litre : 2 325 ÷ 3 = 775 F."),
]),

dict(
nom="Propriété de Thalès",
fiche="""## La configuration
Deux droites (d) et (d') se coupent en A.
B et M sont sur (d), C et N sont sur (d').
Si (MN) est parallèle à (BC), alors :
   AM/AB = AN/AC = MN/BC
Cela marche aussi en configuration « papillon » (les points de part et d'autre de A).

## La propriété directe : calculer une longueur
AM = 3 cm, AB = 6 cm, AC = 8 cm et (MN) // (BC).
AM/AB = AN/AC, donc 3/6 = AN/8 et AN = 8 × 3 ÷ 6 = 4 cm.

## La réciproque : prouver que deux droites sont parallèles
Si AM/AB = AN/AC et si les points A, M, B et A, N, C sont alignés dans le même ordre, alors (MN) // (BC).
Exemple : AM/AB = 2/6 = 1/3 et AN/AC = 3/9 = 1/3. Les rapports sont égaux : (MN) // (BC).

## La contraposée : prouver que deux droites ne sont pas parallèles
Si AM/AB ≠ AN/AC, alors (MN) et (BC) ne sont pas parallèles.
Exemple : 4/10 = 0,4 et 5/12 ≈ 0,42 : rapports différents, droites non parallèles.

## Cas particulier : les milieux
Si M et N sont les milieux de [AB] et [AC], alors (MN) // (BC) et MN = BC/2.

## Agrandissement et réduction
Dans un agrandissement ou une réduction de rapport k :
• les longueurs sont multipliées par k ;
• les aires par k² ;
• les volumes par k³.

## Exemple corrigé (mesurer un fromager)
Un bâton de 1,5 m a une ombre de 2 m. Au même moment, l'ombre d'un fromager mesure 12 m.
Les rayons du soleil sont parallèles : hauteur/12 = 1,5/2, donc hauteur = 12 × 1,5 ÷ 2 = 9 m.

## Pièges à éviter
• Écrire les rapports dans le même ordre : petit triangle en haut, grand triangle en bas.
• Pour la réciproque, ne pas oublier de citer l'alignement des points dans le même ordre.""",
questions=[
(1, "(MN) // (BC), AM = 3 cm, AB = 6 cm et AC = 8 cm. AN mesure :", "4 cm", "5 cm", "16 cm", "11 cm",
 "AM/AB = AN/AC, donc AN = 8 × 3 ÷ 6 = 4 cm."),
(1, "Dans la configuration de Thalès, AM/AB = AN/AC est aussi égal à :", "MN/BC", "MB/AB", "AB/BC", "MN/AM",
 "Les trois rapports de Thalès sont AM/AB, AN/AC et MN/BC."),
(2, "(MN) // (BC), AM = 2 cm, AB = 5 cm et BC = 10 cm. MN mesure :", "4 cm", "25 cm", "5 cm", "20 cm",
 "MN/BC = AM/AB, donc MN = 10 × 2 ÷ 5 = 4 cm."),
(2, "AM = 2, AB = 6, AN = 3, AC = 9, et les points sont alignés dans le même ordre. On conclut que :", "(MN) et (BC) sont parallèles", "(MN) et (BC) sont perpendiculaires", "on ne peut rien conclure", "(MN) et (BC) sont sécantes",
 "AM/AB = 2/6 = 1/3 et AN/AC = 3/9 = 1/3 : d'après la réciproque de Thalès, (MN) // (BC)."),
(2, "M est sur [AB] et N sur [AC], avec AM = 4, AB = 10, AN = 5 et AC = 12. On conclut que :", "(MN) et (BC) ne sont pas parallèles", "(MN) et (BC) sont parallèles", "(MN) et (BC) sont perpendiculaires", "ABC est rectangle",
 "4/10 = 0,4 et 5/12 ≈ 0,417 : les rapports sont différents, donc les droites ne sont pas parallèles."),
(2, "M et N sont les milieux de [AB] et [AC], et BC = 9 cm. MN mesure :", "4,5 cm", "9 cm", "18 cm", "3 cm",
 "La droite des milieux est parallèle au troisième côté et mesure sa moitié."),
(3, "Un bâton de 1,5 m a une ombre de 2 m. Au même moment, l'ombre d'un fromager mesure 12 m. Le fromager mesure :", "9 m", "16 m", "8 m", "13,5 m",
 "hauteur/12 = 1,5/2, donc hauteur = 12 × 1,5 ÷ 2 = 9 m."),
(3, "Configuration papillon : (AB) // (CD), les droites (AD) et (BC) se coupent en O. OA = 3, OD = 6 et OC = 8. OB mesure :", "4", "16", "2,25", "5",
 "OA/OD = OB/OC, donc OB = 8 × 3 ÷ 6 = 4."),
(3, "Dans un agrandissement de rapport 3, une longueur de 4 cm devient :", "12 cm", "7 cm", "4/3 cm", "36 cm",
 "Les longueurs sont multipliées par le rapport : 4 × 3 = 12 cm."),
(3, "Dans une réduction de rapport 1/2, les aires sont multipliées par :", "1/4", "1/2", "2", "1/8",
 "Les aires sont multipliées par k² = (1/2)² = 1/4. Les volumes, eux, seraient multipliés par 1/8."),
(4, "M est sur [AB], N sur [AC], (MN) // (BC). AM = 4 cm, MB = 6 cm et AN = 5 cm. AC mesure :", "12,5 cm", "7,5 cm", "12 cm", "8 cm",
 "Attention : AB = AM + MB = 10 cm. AM/AB = AN/AC, donc AC = 5 × 10 ÷ 4 = 12,5 cm."),
(4, "Pour utiliser la propriété de Thalès, il faut que :", "les droites (MN) et (BC) soient parallèles", "le triangle soit rectangle", "AM soit égal à AN", "le triangle soit isocèle",
 "La condition de la propriété directe est le parallélisme. Le triangle rectangle, c'est pour Pythagore."),
]),
]
