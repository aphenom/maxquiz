NIVEAU, MATIERE = "3ème", "Mathématiques"

CHAPITRES = [
dict(
nom="Relations trigonométriques",
fiche="""## Dans un triangle rectangle
ABC est rectangle en A. [BC] est l'hypoténuse (le plus grand côté, en face de l'angle droit).
Pour l'angle B :
• le côté adjacent est [AB] (il touche B et n'est pas l'hypoténuse) ;
• le côté opposé est [AC] (il est en face de B).

## Les trois formules
• cos B = adjacent ÷ hypoténuse = AB/BC
• sin B = opposé ÷ hypoténuse = AC/BC
• tan B = opposé ÷ adjacent = AC/AB
Pour retenir : « SOH CAH TOA » (Sinus = Opposé/Hypoténuse, Cosinus = Adjacent/Hypoténuse, Tangente = Opposé/Adjacent).

## Relations à connaître
• cos² x + sin² x = 1
• tan x = sin x ÷ cos x
• Pour un angle aigu, cos x et sin x sont compris entre 0 et 1.

## Valeurs remarquables
• 30° : cos = √3/2   sin = 1/2   tan = √3/3
• 45° : cos = √2/2   sin = √2/2   tan = 1
• 60° : cos = 1/2   sin = √3/2   tan = √3

## Méthode
1. Repère l'angle droit et l'hypoténuse.
2. Repère, par rapport à l'angle étudié, les côtés que tu connais et celui que tu cherches.
3. Choisis la formule qui relie ces trois éléments.
4. Calculatrice en mode degrés : cos⁻¹, sin⁻¹ ou tan⁻¹ pour retrouver un angle.

## Exemple corrigé
Une échelle de 5 m est posée contre un mur ; elle fait un angle de 60° avec le sol.
Hauteur atteinte = 5 × sin 60° = 5 × √3/2 ≈ 4,33 m.

## Pièges à éviter
• Ces formules ne marchent QUE dans un triangle rectangle.
• L'adjacent et l'opposé changent selon l'angle choisi : pour l'angle C, l'adjacent est [AC].""",
questions=[
(1, "ABC est rectangle en A. cos B est égal à :", "AB/BC", "AC/BC", "AC/AB", "BC/AB",
 "cos = adjacent ÷ hypoténuse. Pour l'angle B, l'adjacent est AB et l'hypoténuse BC."),
(1, "ABC est rectangle en A. tan B est égal à :", "AC/AB", "AB/AC", "AC/BC", "AB/BC",
 "tan = opposé ÷ adjacent : AC est opposé à B, AB lui est adjacent."),
(1, "cos 60° est égal à :", "1/2", "√3/2", "√2/2", "1",
 "Valeur remarquable : cos 60° = 1/2 (et sin 60° = √3/2)."),
(2, "sin 45° est égal à :", "√2/2", "1/2", "√3/2", "1",
 "À 45°, le sinus et le cosinus sont égaux : √2/2, environ 0,71."),
(2, "ABC est rectangle en A, BC = 10 cm et l'angle B mesure 30°. AC mesure :", "5 cm", "5√3 cm", "10 cm", "20 cm",
 "AC est opposé à B : AC = BC × sin 30° = 10 × 1/2 = 5 cm. 5√3 cm serait AB, le côté adjacent."),
(2, "x est un angle aigu avec sin x = 0,6. Alors cos x est égal à :", "0,8", "0,4", "0,36", "0,64",
 "cos² x = 1 − sin² x = 1 − 0,36 = 0,64, donc cos x = √0,64 = 0,8."),
(2, "ABC est rectangle en A, AB = 4 cm et AC = 3 cm. tan B est égal à :", "0,75", "4/3", "0,6", "0,8",
 "tan B = AC/AB = 3/4 = 0,75."),
(3, "Une échelle de 5 m fait un angle de 60° avec le sol. Elle atteint sur le mur une hauteur d'environ :", "4,33 m", "2,5 m", "5 m", "8,66 m",
 "Hauteur = 5 × sin 60° = 5 × √3/2 ≈ 4,33 m. 2,5 m est la distance au pied du mur (5 × cos 60°)."),
(3, "x est un angle aigu avec cos x = 0,8. Alors tan x est égal à :", "0,75", "1,33", "0,6", "0,48",
 "sin x = √(1 − 0,64) = 0,6, puis tan x = 0,6 ÷ 0,8 = 0,75."),
(3, "Une rampe de 2 m de long monte à 1 m de hauteur. Elle fait avec le sol un angle de :", "30°", "60°", "45°", "90°",
 "sin x = opposé ÷ hypoténuse = 1/2, donc x = 30°."),
(4, "cos² x + sin² x + 1 est égal à :", "2", "1", "0", "2cos² x",
 "cos² x + sin² x = 1 pour tout angle x, donc l'expression vaut 1 + 1 = 2."),
(4, "Tu es à 20 m du pied d'un arbre et tu vois son sommet sous un angle de 45° depuis le sol. L'arbre mesure :", "20 m", "10 m", "20√2 m", "14,1 m",
 "tan 45° = hauteur ÷ 20 = 1, donc la hauteur est 20 m."),
]),

dict(
nom="Angles inscrits",
fiche="""## Vocabulaire
• Un angle inscrit a son sommet SUR le cercle et ses côtés coupent le cercle.
• Un angle au centre a son sommet au centre O du cercle.
• On dit que les angles interceptent (ou « regardent ») un arc.

## Propriété 1
Un angle inscrit mesure la moitié de l'angle au centre qui intercepte le même arc.
Angle au centre 80° → angle inscrit 40°.

## Propriété 2
Deux angles inscrits qui interceptent le même arc sont égaux.

## Propriété 3 (cas du demi-cercle)
Si [AB] est un diamètre et M un point du cercle, l'angle AMB est droit (90°).
Réciproquement, si l'angle ACB est droit, C est sur le cercle de diamètre [AB].

## Polygones réguliers
Un polygone régulier a tous ses côtés égaux et tous ses angles égaux. Il est inscrit dans un cercle.
• Angle au centre : 360° ÷ n (n = nombre de côtés).
• Triangle équilatéral : 120°   carré : 90°   pentagone : 72°   hexagone : 60°
• Dans l'hexagone régulier, le côté est égal au rayon du cercle, et chaque angle intérieur mesure 120°.

## Méthode pour construire un hexagone régulier
Trace un cercle, puis reporte six fois son rayon au compas sur le cercle.

## Exemple corrigé
ABC est inscrit dans un cercle de centre O et l'angle BOC mesure 110°. A est sur le grand arc BC.
L'angle BAC intercepte le même arc que BOC, donc il mesure 110° ÷ 2 = 55°.

## Pièges à éviter
• Vérifier que les deux angles interceptent bien le MÊME arc.
• Ne pas confondre l'angle au centre (360° ÷ n) et l'angle intérieur d'un polygone.""",
questions=[
(1, "Un angle au centre mesure 80°. L'angle inscrit qui intercepte le même arc mesure :", "40°", "80°", "160°", "20°",
 "L'angle inscrit vaut la moitié de l'angle au centre : 80 ÷ 2 = 40°."),
(1, "Un angle inscrit mesure 35°. L'angle au centre qui intercepte le même arc mesure :", "70°", "17,5°", "35°", "145°",
 "L'angle au centre est le double de l'angle inscrit : 35 × 2 = 70°."),
(2, "Deux angles inscrits qui interceptent le même arc sont :", "égaux", "supplémentaires", "complémentaires", "l'un le double de l'autre",
 "Ils valent tous les deux la moitié du même angle au centre."),
(2, "[AB] est un diamètre et M un point du cercle, distinct de A et de B. L'angle AMB mesure :", "90°", "180°", "45°", "60°",
 "Un angle inscrit qui intercepte un demi-cercle est droit."),
(2, "L'angle au centre d'un hexagone régulier mesure :", "60°", "120°", "45°", "72°",
 "360° ÷ 6 = 60°. 120° est l'angle intérieur de l'hexagone."),
(2, "L'angle au centre d'un pentagone régulier mesure :", "72°", "108°", "60°", "36°",
 "360° ÷ 5 = 72°. 108° est l'angle intérieur du pentagone."),
(3, "ABC est inscrit dans un cercle de centre O, l'angle BOC mesure 110° et A est sur le grand arc BC. L'angle BAC mesure :", "55°", "110°", "125°", "70°",
 "BAC et BOC interceptent le même arc BC : BAC = 110 ÷ 2 = 55°."),
(3, "Un angle inscrit a son sommet :", "sur le cercle", "au centre du cercle", "à l'intérieur du cercle", "à l'extérieur du cercle",
 "C'est la définition. Un angle dont le sommet est au centre est un angle au centre."),
(3, "Un hexagone régulier est inscrit dans un cercle de rayon 4 cm. Son côté mesure :", "4 cm", "8 cm", "2 cm", "6 cm",
 "L'hexagone régulier est formé de 6 triangles équilatéraux : son côté est égal au rayon."),
(3, "Un angle intérieur d'un hexagone régulier mesure :", "120°", "60°", "90°", "135°",
 "Chaque angle intérieur réunit deux angles de 60° des triangles équilatéraux : 120°."),
(4, "Un polygone régulier a un angle au centre de 30°. Il a :", "12 côtés", "6 côtés", "10 côtés", "30 côtés",
 "n = 360° ÷ 30° = 12."),
(4, "Le triangle ABC est inscrit dans un cercle de centre O et l'angle ACB est droit. On peut affirmer que :", "[AB] est un diamètre du cercle", "AB = AC", "O est le milieu de [AC]", "ABC est équilatéral",
 "Un triangle inscrit dont un angle est droit a pour hypoténuse un diamètre du cercle."),
]),

dict(
nom="Vecteurs",
fiche="""## Notation
On note →AB le vecteur qui va de A vers B. Il est défini par :
• sa direction (celle de la droite (AB)) ;
• son sens (de A vers B) ;
• sa longueur (la distance AB).

## Égalité de deux vecteurs
→AB = →DC  ⇔  ABCD est un parallélogramme (éventuellement aplati).
I est le milieu de [AB]  ⇔  →AI = →IB.

## Vecteurs particuliers
• Vecteur nul : →AA = →0.
• Vecteur opposé : −→AB = →BA (même direction, même longueur, sens contraire).

## Somme : la relation de Chasles
→AB + →BC = →AC  (la fin du premier vecteur est le début du second).
Exemple : →MA + →AB + →BN = →MN.
Règle du parallélogramme : si ABCD est un parallélogramme, →AB + →AD = →AC.
Différence : →AC − →AB = →AC + →BA = →BA + →AC = →BC.

## Produit par un nombre k
k→AB a la même direction que →AB et une longueur multipliée par |k| ;
• si k > 0, même sens ;
• si k < 0, sens contraire.
Exemple : −2→AB a la même direction que →AB, le sens contraire et une longueur double.

## Vecteurs colinéaires
→u et →v sont colinéaires s'il existe k tel que →v = k→u (ils ont la même direction).
A, B et C sont alignés  ⇔  →AB et →AC sont colinéaires.
(AB) // (CD)  ⇔  →AB et →CD sont colinéaires.

## Exemple corrigé
→AM = ⅓ →AB avec AB = 6 cm : M est sur [AB], du côté de B par rapport à A, à 2 cm de A.

## Pièges à éviter
• Attention à l'ordre des lettres : →AB = →DC donne le parallélogramme ABCD, alors que →AB = →CD donne le parallélogramme ABDC.
• →AB et →BA ont la même longueur mais ne sont PAS égaux.""",
questions=[
(1, "→AB + →BC est égal à :", "→AC", "→CA", "→BA", "→AB",
 "Relation de Chasles : la fin du premier vecteur (B) est le début du second."),
(1, "→AB = →DC signifie que ABCD est :", "un parallélogramme", "un rectangle", "un trapèze", "un losange",
 "C'est la caractérisation du parallélogramme par les vecteurs."),
(1, "Le vecteur opposé de →AB est :", "→BA", "→AB", "→AA", "2→AB",
 "Même direction et même longueur, mais sens contraire : de B vers A."),
(2, "I est le milieu de [AB] si et seulement si :", "→AI = →IB", "→AI = →BI", "→AI = →AB", "→IA = →IB",
 "Les deux vecteurs →AI et →IB ont même direction, même sens et même longueur."),
(2, "→AB + →BA est égal à :", "le vecteur nul", "2→AB", "→AB", "2→BA",
 "→AB + →BA = →AA, le vecteur nul : on part de A et on revient en A."),
(2, "Par rapport à →AB, le vecteur −2→AB a :", "la même direction, le sens contraire et une longueur double", "la même direction, le même sens et une longueur double", "une direction perpendiculaire", "la même direction, le sens contraire et la même longueur",
 "k = −2 est négatif (sens contraire) et |k| = 2 (longueur doublée)."),
(3, "→MA + →AB + →BN est égal à :", "→MN", "→NM", "→AN", "→MB",
 "On enchaîne Chasles : →MA + →AB = →MB, puis →MB + →BN = →MN."),
(3, "ABCD est un parallélogramme. →AB + →AD est égal à :", "→AC", "→BD", "→DB", "→CA",
 "Règle du parallélogramme : la somme est la diagonale issue de A."),
(3, "→AC − →AB est égal à :", "→BC", "→CB", "→AB", "→CA",
 "→AC − →AB = →AC + →BA = →BA + →AC = →BC."),
(3, "M vérifie →AM = ⅓ →AB et AB = 6 cm. AM mesure :", "2 cm", "18 cm", "3 cm", "6 cm",
 "AM = ⅓ × 6 = 2 cm."),
(4, "Les points A, B et C sont alignés si et seulement si :", "→AB et →AC sont colinéaires", "→AB et →AC sont égaux", "→AB et →AC sont opposés", "→AB et →AC ont la même longueur",
 "Colinéaires = même direction ; comme les deux vecteurs partent de A, les points sont sur une même droite."),
(4, "ABCD est un parallélogramme de centre O. →OA + →OC est égal à :", "le vecteur nul", "→AC", "2→OA", "→BD",
 "Les diagonales se coupent en leur milieu O : →OC = −→OA, donc la somme est nulle."),
]),

dict(
nom="Coordonnées d'un vecteur",
fiche="""## Dans un repère
Si A(xA ; yA) et B(xB ; yB), alors :
• →AB a pour coordonnées (xB − xA ; yB − yA) ;
• le milieu I de [AB] a pour coordonnées ((xA + xB)/2 ; (yA + yB)/2) ;
• dans un repère orthonormé, AB = √[(xB − xA)² + (yB − yA)²].

## Calculs sur les coordonnées
→u(x ; y) et →v(x' ; y') :
• →u + →v a pour coordonnées (x + x' ; y + y') ;
• k→u a pour coordonnées (kx ; ky) ;
• →u = →v ⇔ x = x' et y = y'.

## Colinéarité et orthogonalité
• →u et →v sont colinéaires ⇔ xy' − yx' = 0.
• Dans un repère orthonormé, →u et →v sont orthogonaux ⇔ xx' + yy' = 0.

## Exemple corrigé
A(1 ; 2) et B(4 ; 6).
→AB (4 − 1 ; 6 − 2) = (3 ; 4).
AB = √(3² + 4²) = √25 = 5.
Milieu I((1 + 4)/2 ; (2 + 6)/2) = (2,5 ; 4).

## Trouver le 4ᵉ sommet d'un parallélogramme
ABCD est un parallélogramme ⇔ →AD = →BC.
A(0 ; 0), B(3 ; 1), C(5 ; 4) : →BC(2 ; 3), donc D(0 + 2 ; 0 + 3) = D(2 ; 3).

## Prouver un alignement
A(1 ; 1), B(3 ; 5), C(4 ; 7) : →AB(2 ; 4), →AC(3 ; 6).
2 × 6 − 4 × 3 = 0 : les vecteurs sont colinéaires, A, B et C sont alignés.

## Pièges à éviter
• Toujours « arrivée moins départ » : xB − xA, pas xA − xB.
• La formule de distance n'est valable que dans un repère orthonormé.""",
questions=[
(1, "A(1 ; 2) et B(4 ; 6). Les coordonnées de →AB sont :", "(3 ; 4)", "(5 ; 8)", "(−3 ; −4)", "(4 ; 3)",
 "(xB − xA ; yB − yA) = (4 − 1 ; 6 − 2) = (3 ; 4)."),
(1, "A(2 ; 4) et B(6 ; 0). Le milieu de [AB] a pour coordonnées :", "(4 ; 2)", "(8 ; 4)", "(2 ; −2)", "(4 ; 4)",
 "((2 + 6)/2 ; (4 + 0)/2) = (4 ; 2)."),
(2, "Dans un repère orthonormé, A(1 ; 2) et B(4 ; 6). AB est égal à :", "5", "7", "25", "√7",
 "AB = √(3² + 4²) = √25 = 5. 25 est AB², il faut prendre la racine."),
(2, "→u(2 ; 3) et →v(1 ; −5). →u + →v a pour coordonnées :", "(3 ; −2)", "(3 ; 8)", "(1 ; 8)", "(2 ; −15)",
 "On additionne abscisses et ordonnées : (2 + 1 ; 3 − 5) = (3 ; −2)."),
(2, "→u(2 ; −1). 3→u a pour coordonnées :", "(6 ; −3)", "(6 ; −1)", "(5 ; 2)", "(2 ; −3)",
 "On multiplie chaque coordonnée par 3."),
(2, "A(5 ; 1) et →AB(−3 ; 2). Le point B a pour coordonnées :", "(2 ; 3)", "(8 ; −1)", "(−2 ; 3)", "(2 ; −1)",
 "xB = 5 + (−3) = 2 et yB = 1 + 2 = 3."),
(3, "Lequel de ces vecteurs est colinéaire à →u(2 ; 3) ?", "(−4 ; −6)", "(3 ; 2)", "(4 ; 3)", "(2 ; −3)",
 "(−4 ; −6) = −2 × (2 ; 3). Test : 2 × (−6) − 3 × (−4) = −12 + 12 = 0."),
(3, "Dans un repère orthonormé, lequel de ces vecteurs est orthogonal à →u(2 ; 3) ?", "(3 ; −2)", "(2 ; 3)", "(−2 ; 3)", "(4 ; 6)",
 "2 × 3 + 3 × (−2) = 6 − 6 = 0."),
(3, "ABCD est un parallélogramme avec A(0 ; 0), B(3 ; 1) et C(5 ; 4). D a pour coordonnées :", "(2 ; 3)", "(8 ; 5)", "(2 ; 5)", "(−2 ; −3)",
 "→AD = →BC = (2 ; 3), donc D(2 ; 3)."),
(3, "M(2 ; 1) est le milieu de [AB] avec A(−1 ; 3). B a pour coordonnées :", "(5 ; −1)", "(0,5 ; 2)", "(3 ; −2)", "(1 ; 4)",
 "xB = 2 × 2 − (−1) = 5 et yB = 2 × 1 − 3 = −1."),
(4, "Dans un repère orthonormé, A(0 ; 0), B(4 ; 0) et C(0 ; 3). Le périmètre du triangle ABC est :", "12", "7", "10", "25",
 "AB = 4, AC = 3 et BC = √(16 + 9) = 5. Périmètre : 4 + 3 + 5 = 12."),
(4, "Les points A(1 ; 1), B(3 ; 5) et C(4 ; 7) :", "sont alignés", "forment un triangle rectangle", "forment un triangle équilatéral", "sont confondus",
 "→AB(2 ; 4) et →AC(3 ; 6) : 2 × 6 − 4 × 3 = 0, les vecteurs sont colinéaires."),
]),

dict(
nom="Équation de droite",
fiche="""## Les deux formes
• Une droite non parallèle à l'axe des ordonnées a une équation y = ax + b.
   a est le coefficient directeur, b l'ordonnée à l'origine.
• Une droite parallèle à l'axe des ordonnées a une équation x = c.
• y = c est une droite parallèle à l'axe des abscisses (a = 0).

## Un point appartient-il à une droite ?
Ses coordonnées doivent vérifier l'équation.
(1 ; 5) est sur y = 2x + 3 car 2 × 1 + 3 = 5.

## Trouver l'équation à partir de deux points
A(1 ; 2) et B(3 ; 8).
a = (yB − yA) ÷ (xB − xA) = (8 − 2) ÷ (3 − 1) = 3.
On remplace avec A : 2 = 3 × 1 + b, donc b = −1. Équation : y = 3x − 1.

## Vecteur directeur
La droite y = ax + b a pour vecteur directeur →u(1 ; a).
Une droite passant par A(2 ; −1) de vecteur directeur (1 ; 2) a pour coefficient 2 : y = 2x + b avec −1 = 4 + b, d'où y = 2x − 5.

## Droites parallèles et perpendiculaires
• Parallèles ⇔ même coefficient directeur.
• Perpendiculaires (repère orthonormé) ⇔ a × a' = −1.
   La perpendiculaire à y = 2x + 1 a pour coefficient −1/2.

## Intersection de deux droites
On résout le système formé par les deux équations.
y = x + 1 et y = −x + 5 : x + 1 = −x + 5, donc x = 2 et y = 3. Point (2 ; 3).

## Pièges à éviter
• Dans y = 5 − 2x, le coefficient directeur est −2 et l'ordonnée à l'origine 5.
• Calculer a toujours dans le même ordre : (yB − yA) ÷ (xB − xA).""",
questions=[
(1, "Le coefficient directeur de la droite y = 2x + 3 est :", "2", "3", "5", "2x",
 "Dans y = ax + b, le coefficient directeur est a = 2."),
(1, "Quel point appartient à la droite y = 2x + 3 ?", "(1 ; 5)", "(5 ; 1)", "(0 ; 2)", "(2 ; 5)",
 "Pour x = 1 : y = 2 + 3 = 5. Pour (2 ; 5), on aurait y = 7."),
(1, "La droite d'équation y = −4 est :", "parallèle à l'axe des abscisses", "parallèle à l'axe des ordonnées", "passant par l'origine", "de coefficient directeur −4",
 "y = −4 pour tout x : c'est une droite horizontale, de coefficient directeur 0."),
(2, "L'ordonnée à l'origine de la droite y = 5 − 2x est :", "5", "−2", "2,5", "−5",
 "y = −2x + 5 : l'ordonnée à l'origine est b = 5 (valeur de y quand x = 0)."),
(2, "L'équation de la droite passant par A(1 ; 2) et B(3 ; 8) est :", "y = 3x − 1", "y = 3x + 2", "y = 2x + 1", "y = 6x − 4",
 "a = (8 − 2) ÷ (3 − 1) = 3, puis 2 = 3 + b donne b = −1."),
(2, "La droite parallèle à y = −x + 4 passant par l'origine a pour équation :", "y = −x", "y = x", "y = −x + 4", "y = 4x",
 "Même coefficient directeur (−1) et ordonnée à l'origine 0."),
(2, "La droite parallèle à l'axe des ordonnées passant par (3 ; −2) a pour équation :", "x = 3", "y = 3", "y = −2", "x = −2",
 "Tous ses points ont pour abscisse 3."),
(3, "Dans un repère orthonormé, une droite perpendiculaire à y = 2x + 1 a pour coefficient directeur :", "−1/2", "−2", "1/2", "2",
 "a × a' = −1, donc a' = −1 ÷ 2 = −1/2."),
(3, "Les droites y = x + 1 et y = −x + 5 se coupent au point :", "(2 ; 3)", "(3 ; 2)", "(1 ; 4)", "(4 ; 5)",
 "x + 1 = −x + 5 donne x = 2, puis y = 3."),
(3, "Un vecteur directeur de la droite y = 3x − 2 est :", "(1 ; 3)", "(3 ; 1)", "(1 ; −2)", "(−2 ; 3)",
 "La droite y = ax + b a pour vecteur directeur (1 ; a)."),
(4, "La droite passant par A(2 ; −1) de vecteur directeur (1 ; 2) a pour équation :", "y = 2x − 5", "y = 2x − 1", "y = −x + 1", "y = 2x + 5",
 "Coefficient directeur 2 ; −1 = 2 × 2 + b donne b = −5. y = −x + 1 passe par A, mais n'a pas la bonne direction."),
(4, "Le coefficient directeur de la droite passant par A(−1 ; 4) et B(3 ; −4) est :", "−2", "2", "−1/2", "0",
 "a = (−4 − 4) ÷ (3 − (−1)) = −8 ÷ 4 = −2."),
]),

dict(
nom="Statistiques",
fiche="""## Vocabulaire
• Population : l'ensemble étudié (les élèves d'une classe).
• Caractère : ce qu'on étudie. Qualitatif (matière préférée) ou quantitatif (note, âge).
• Modalités : les valeurs possibles du caractère.
• Effectif : nombre d'individus pour une modalité. Effectif total : N.
• Fréquence = effectif ÷ effectif total, souvent en % : 12 filles sur 40 élèves = 30 %.

## Effectifs cumulés croissants (ECC)
On additionne les effectifs au fur et à mesure.
Effectifs 4, 6, 10 → ECC 4, 10, 20.

## Regroupement en classes
Classe [0 ; 5[ : de 0 compris à 5 exclu. Son centre est (0 + 5) ÷ 2 = 2,5.
La classe modale est celle qui a le plus grand effectif.

## Les indicateurs
• Mode : la modalité la plus fréquente.
• Moyenne : somme des valeurs ÷ nombre de valeurs.
   Moyenne pondérée : (somme des valeur × effectif ou coefficient) ÷ (somme des effectifs ou coefficients).
   Avec des classes, on utilise les centres.
• Médiane : la valeur du milieu, la série étant rangée dans l'ordre.
   2, 4, 7, 9, 11 → médiane 7.   3, 5, 8, 10 → médiane (5 + 8) ÷ 2 = 6,5.

## Diagrammes
• Diagramme en bâtons (caractère quantitatif discret).
• Diagramme circulaire : angle = fréquence × 360°. 25 % → 90°.
• Histogramme pour des classes.

## Exemple corrigé (moyenne de la classe)
25 garçons ont 11 de moyenne et 15 filles ont 13 de moyenne.
Moyenne de la classe = (25 × 11 + 15 × 13) ÷ 40 = 470 ÷ 40 = 11,75.
Attention : ce n'est pas (11 + 13) ÷ 2 = 12, car les groupes n'ont pas le même effectif.

## Pièges à éviter
• Pour la médiane, ranger la série d'abord.
• Ne pas confondre la valeur d'une modalité et son effectif.""",
questions=[
(1, "La moyenne des notes 10, 12 et 14 est :", "12", "36", "13", "11",
 "(10 + 12 + 14) ÷ 3 = 36 ÷ 3 = 12."),
(1, "Le mode de la série 3 ; 5 ; 5 ; 7 ; 9 est :", "5", "7", "9", "5,8",
 "Le mode est la valeur la plus fréquente : 5 apparaît deux fois. 5,8 est la moyenne."),
(2, "La médiane de la série 2 ; 4 ; 7 ; 9 ; 11 est :", "7", "6,6", "9", "4",
 "Série rangée de 5 valeurs : la médiane est la 3ᵉ, 7. 6,6 est la moyenne."),
(2, "La médiane de la série 3 ; 5 ; 8 ; 10 est :", "6,5", "5", "8", "6",
 "Nombre pair de valeurs : moyenne des deux valeurs du milieu, (5 + 8) ÷ 2 = 6,5."),
(2, "Dans une classe de 40 élèves, il y a 12 filles. La fréquence des filles est :", "30 %", "12 %", "40 %", "28 %",
 "12 ÷ 40 = 0,3 = 30 %."),
(2, "Dans un diagramme circulaire, une modalité de fréquence 25 % est représentée par un angle de :", "90°", "25°", "45°", "180°",
 "Angle = 0,25 × 360° = 90°."),
(3, "Note 10 au coefficient 2 et note 16 au coefficient 1. La moyenne est :", "12", "13", "11", "36",
 "(10 × 2 + 16 × 1) ÷ (2 + 1) = 36 ÷ 3 = 12. Sans les coefficients, on trouverait 13."),
(3, "Le centre de la classe [0 ; 5[ est :", "2,5", "5", "0", "2",
 "Centre = (0 + 5) ÷ 2 = 2,5."),
(3, "Les effectifs de trois modalités sont 4, 6 et 10. L'effectif cumulé croissant de la 3ᵉ modalité est :", "20", "10", "16", "14",
 "4 + 6 + 10 = 20. C'est aussi l'effectif total."),
(3, "Lequel de ces caractères est qualitatif ?", "la matière préférée", "la taille", "l'âge", "la note au BEPC",
 "Un caractère qualitatif ne se mesure pas par un nombre."),
(4, "Ta moyenne est 12 après 4 devoirs. Quelle note te faut-il au 5ᵉ devoir pour avoir 13 de moyenne ?", "17", "13", "14", "16",
 "Il faut 13 × 5 = 65 points au total. Tu en as 12 × 4 = 48, il manque 65 − 48 = 17."),
(4, "25 garçons ont 11 de moyenne et 15 filles ont 13 de moyenne. La moyenne de la classe est :", "11,75", "12", "11,5", "12,25",
 "(25 × 11 + 15 × 13) ÷ 40 = (275 + 195) ÷ 40 = 470 ÷ 40 = 11,75."),
]),

dict(
nom="Pyramide et cône",
fiche="""## La pyramide
• Une base (polygone), un sommet, des faces latérales triangulaires.
• La hauteur est la distance du sommet au plan de la base.
• Pyramide régulière : la base est un polygone régulier et les faces latérales sont des triangles isocèles superposables.
• Une pyramide à base hexagonale a 7 faces (6 latérales + la base).

## Le cône de révolution
• Une base en forme de disque de rayon r, un sommet, une hauteur h.
• La génératrice g relie le sommet à un point du cercle de base.
• Pythagore donne : g² = r² + h².

## Les formules
• Volume d'une pyramide : V = (aire de la base × hauteur) ÷ 3.
• Volume d'un cône : V = (π × r² × h) ÷ 3.
• Aire latérale d'un cône : π × r × g.
• 1 L = 1 dm³ = 1 000 cm³.

## Section parallèle à la base
Couper une pyramide ou un cône parallèlement à sa base donne une petite pyramide (ou un petit cône), réduction de la grande de rapport k :
• longueurs × k ;
• aires × k² ;
• volumes × k³.
À mi-hauteur, k = 1/2 et le volume est divisé par 8.

## Exemple corrigé (toit de case)
Le toit conique d'une case a un diamètre de 6 m et une hauteur de 4 m.
Rayon r = 3 m. Génératrice : g² = 3² + 4² = 25, donc g = 5 m.
Volume sous le toit : π × 9 × 4 ÷ 3 = 12π ≈ 37,7 m³.

## Pièges à éviter
• Utiliser le RAYON (et non le diamètre) dans les formules.
• Ne pas oublier la division par 3 dans le volume.""",
questions=[
(1, "Une pyramide a une base de 12 cm² et une hauteur de 5 cm. Son volume est :", "20 cm³", "60 cm³", "17 cm³", "30 cm³",
 "V = 12 × 5 ÷ 3 = 20 cm³. 60 cm³ serait le volume d'un prisme de même base."),
(1, "Le volume d'une pyramide de base B et de hauteur h est :", "B × h ÷ 3", "B × h", "B × h ÷ 2", "3 × B × h",
 "On divise par 3 le produit de l'aire de la base par la hauteur."),
(2, "Un cône a un rayon de 3 cm et une hauteur de 4 cm. Sa génératrice mesure :", "5 cm", "7 cm", "25 cm", "√7 cm",
 "g² = 3² + 4² = 25, donc g = 5 cm."),
(2, "Un cône a un rayon de 3 cm et une hauteur de 4 cm. Son volume est :", "12π cm³", "36π cm³", "4π cm³", "9π cm³",
 "V = π × 3² × 4 ÷ 3 = 12π cm³ (environ 37,7 cm³)."),
(2, "Une pyramide a une base carrée de 6 cm de côté et une hauteur de 10 cm. Son volume est :", "120 cm³", "360 cm³", "60 cm³", "200 cm³",
 "Base : 6 × 6 = 36 cm². V = 36 × 10 ÷ 3 = 120 cm³."),
(2, "Une pyramide à base hexagonale a :", "7 faces", "6 faces", "8 faces", "12 faces",
 "6 faces latérales plus la base."),
(3, "On coupe un cône à mi-hauteur, parallèlement à sa base. Le volume du petit cône est celui du grand multiplié par :", "1/8", "1/2", "1/4", "1/6",
 "Réduction de rapport k = 1/2 : le volume est multiplié par k³ = 1/8."),
(3, "Une pyramide de 270 cm³ est réduite au rapport 1/3. Le volume de la réduction est :", "10 cm³", "90 cm³", "30 cm³", "3 cm³",
 "270 × (1/3)³ = 270 ÷ 27 = 10 cm³."),
(3, "Un cône a un rayon de 3 cm et une génératrice de 5 cm. Son aire latérale est :", "15π cm²", "9π cm²", "30π cm²", "24π cm²",
 "Aire latérale = π × r × g = 15π cm². 24π cm² est l'aire totale, base comprise."),
(3, "Les faces latérales d'une pyramide régulière sont :", "des triangles isocèles superposables", "des carrés", "des rectangles", "des triangles rectangles",
 "Le sommet est à égale distance des sommets de la base régulière."),
(4, "Le toit conique d'une case a un diamètre de 6 m et une hauteur de 4 m. Sa génératrice mesure :", "5 m", "√52 m, environ 7,2 m", "10 m", "4 m",
 "Rayon = 3 m (et non 6 m) : g² = 9 + 16 = 25, donc g = 5 m."),
(4, "Un cône a un rayon de 10 cm et une hauteur de 30 cm (π ≈ 3,14). Il contient :", "3,14 L", "9,42 L", "31,4 L", "0,314 L",
 "V = 3,14 × 100 × 30 ÷ 3 = 3 140 cm³ = 3,14 L."),
]),

dict(
nom="Révision BEPC",
fiche="""## Formulaire de 3ème : tout ce qu'il faut savoir par cœur

## Calcul
• (a + b)² = a² + 2ab + b²   (a − b)² = a² − 2ab + b²   (a + b)(a − b) = a² − b²
• √(ab) = √a × √b    √(a/b) = √a/√b    √(a + b) ≠ √a + √b
• aⁿ × aᵐ = aⁿ⁺ᵐ   aⁿ ÷ aᵐ = aⁿ⁻ᵐ   (aⁿ)ᵐ = aⁿˣᵐ   a⁻ⁿ = 1/aⁿ
• Produit nul : A × B = 0 ⇔ A = 0 ou B = 0
• Inéquation : on change le sens si on multiplie ou divise par un négatif.

## Fonctions et repère
• Affine : f(x) = ax + b ; a = [f(x₂) − f(x₁)] ÷ (x₂ − x₁)
• →AB (xB − xA ; yB − yA)   milieu ((xA + xB)/2 ; (yA + yB)/2)
• AB = √[(xB − xA)² + (yB − yA)²]
• Colinéaires : xy' − yx' = 0   orthogonaux : xx' + yy' = 0
• Droites parallèles : même a ; perpendiculaires : a × a' = −1

## Géométrie
• Pythagore : ABC rectangle en A ⇔ BC² = AB² + AC²
• Thalès : AM/AB = AN/AC = MN/BC si (MN) // (BC)
• cos = adj/hyp   sin = opp/hyp   tan = opp/adj   cos² + sin² = 1
• Angle inscrit = angle au centre ÷ 2 ; demi-cercle → 90°
• Polygone régulier à n côtés : angle au centre 360° ÷ n

## Aires et volumes
• Disque : π r²   cercle : 2π r
• Pavé : L × l × h   cylindre : π r² h   pyramide : B × h ÷ 3   cône : π r² h ÷ 3
• Agrandissement de rapport k : longueurs × k, aires × k², volumes × k³

## Statistiques
• Fréquence = effectif ÷ effectif total
• Moyenne pondérée = Σ(valeur × effectif) ÷ Σ effectifs
• Médiane : valeur du milieu de la série rangée

## Conseils pour le jour de l'épreuve
• Lis tout le sujet avant de commencer et commence par ce que tu maîtrises le mieux.
• Recopie chaque résultat important : il sert souvent à la question suivante.
• Rédige : propriété utilisée, calcul, phrase de conclusion avec l'unité.
• Garde 10 minutes à la fin pour relire et vérifier tes calculs.""",
questions=[
(2, "Le développement de (x − 4)² est :", "x² − 8x + 16", "x² − 16", "x² + 16", "x² − 8x − 16",
 "(a − b)² = a² − 2ab + b² : x² − 8x + 16."),
(2, "√50 s'écrit sous forme simplifiée :", "5√2", "25√2", "2√5", "10√5",
 "50 = 25 × 2, donc √50 = 5√2."),
(2, "Les solutions de (x + 3)(2x − 8) = 0 sont :", "x = −3 ou x = 4", "x = 3 ou x = −4", "x = −3 seulement", "x = −3 ou x = 8",
 "x + 3 = 0 donne −3 ; 2x − 8 = 0 donne x = 4."),
(2, "Un triangle rectangle a des côtés de l'angle droit de 6 cm et 8 cm. Son hypoténuse mesure :", "10 cm", "14 cm", "48 cm", "100 cm",
 "Pythagore : 36 + 64 = 100, donc l'hypoténuse mesure √100 = 10 cm."),
(2, "L'antécédent de 0 par f(x) = −3x + 6 est :", "2", "6", "−2", "0",
 "−3x + 6 = 0 donne x = 2."),
(3, "Un triangle a des côtés de 5 cm, 12 cm et 13 cm. Il est :", "rectangle", "isocèle", "équilatéral", "ni rectangle, ni isocèle",
 "13² = 169 et 5² + 12² = 25 + 144 = 169 : d'après la réciproque de Pythagore, il est rectangle."),
(3, "Dans un repère orthonormé, A(−2 ; 1) et B(2 ; 4). AB est égal à :", "5", "3", "7", "√7",
 "AB = √(4² + 3²) = √25 = 5."),
(3, "Dans un triangle rectangle d'hypoténuse 10 cm, le côté opposé à l'angle x mesure 6 cm. sin x est égal à :", "0,6", "0,8", "0,75", "1,67",
 "sin x = opposé ÷ hypoténuse = 6 ÷ 10 = 0,6."),
(3, "La moyenne de la série 8 ; 12 ; 15 ; 9 ; 11 est :", "11", "12", "10", "15",
 "(8 + 12 + 15 + 9 + 11) ÷ 5 = 55 ÷ 5 = 11."),
(3, "Un angle au centre mesure 140°. L'angle inscrit qui intercepte le même arc mesure :", "70°", "140°", "280°", "40°",
 "140 ÷ 2 = 70°."),
(3, "La solution du système x + 2y = 8 et x − y = 2 est :", "(4 ; 2)", "(2 ; 4)", "(6 ; 1)", "(2 ; 3)",
 "En soustrayant : 3y = 6, donc y = 2, puis x = 4. Vérification : 4 + 4 = 8 et 4 − 2 = 2."),
(4, "Un cône a un rayon de 6 cm et une hauteur de 5 cm. Son volume est :", "60π cm³", "180π cm³", "30π cm³", "20π cm³",
 "V = π × 36 × 5 ÷ 3 = 60π cm³."),
(4, "(2 × 10³) × (4 × 10⁻⁵) est égal à :", "8 × 10⁻²", "8 × 10⁻¹⁵", "8 × 10²", "6 × 10⁻²",
 "2 × 4 = 8 et 10³ × 10⁻⁵ = 10⁻²."),
(4, "La droite passant par (0 ; 2) et (2 ; 6) a pour équation :", "y = 2x + 2", "y = 3x + 2", "y = 2x + 6", "y = x + 2",
 "b = 2 (point sur l'axe des ordonnées) et a = (6 − 2) ÷ 2 = 2."),
(4, "Si −1 < x < 2, alors :", "−4 < −2x < 2", "−2 < −2x < 4", "−4 < −2x < −2", "2 < −2x < 4",
 "On multiplie par −2 : le sens change. 2 > −2x > −4, c'est-à-dire −4 < −2x < 2."),
]),
]
