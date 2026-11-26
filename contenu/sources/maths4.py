NIVEAU, MATIERE = "4ème", "Mathématiques"

CHAPITRES = [
dict(
nom="Nombres décimaux relatifs et puissances de 10",
fiche="""## Puissances de 10
• 10ⁿ = 1 suivi de n zéros : 10³ = 1 000. 10⁻ⁿ = 0,0…01 avec n chiffres après la virgule : 10⁻² = 0,01.
• 10⁰ = 1.
• Règles : 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; 10ᵃ / 10ᵇ = 10ᵃ⁻ᵇ ; (10ᵃ)ᵇ = 10ᵃˣᵇ.

## Multiplier par 10ⁿ
Multiplier par 10³ décale la virgule de 3 rangs vers la droite ; par 10⁻³, de 3 rangs vers la gauche.
2,5 × 10³ = 2 500 ; 47 × 10⁻² = 0,47.

## Notation scientifique
a × 10ⁿ avec 1 ≤ a < 10 (un seul chiffre non nul avant la virgule).
• 45 000 = 4,5 × 10⁴ ; 0,0032 = 3,2 × 10⁻³.
• Utile pour les très grands ou très petits nombres (distance Terre-Soleil ≈ 1,5 × 10⁸ km).

## Relatifs
• Comparer : de deux négatifs, le plus grand est celui qui a la plus petite distance à zéro (−2 > −5).
• Produit : règle des signes (−) × (−) = (+) ; (−) × (+) = (−).
• Un produit de facteurs non nuls est positif s'il contient un nombre pair de facteurs négatifs, négatif si ce nombre est impair.

## Ordre de grandeur
Arrondir pour estimer : 4,8 × 10³ × 2,1 ≈ 5 × 10³ × 2 = 10⁴.""",
questions=[
(1, "10³ est égal à :", "1 000", "30", "100", "10 000",
 "1 suivi de 3 zéros."),
(1, "10⁻² est égal à :", "0,01", "−100", "0,1", "−20",
 "Une puissance négative de 10 donne un nombre décimal, pas un nombre négatif."),
(2, "La notation scientifique de 45 000 est :", "4,5 × 10⁴", "45 × 10³", "0,45 × 10⁵", "4,5 × 10³",
 "Un seul chiffre non nul avant la virgule."),
(2, "La notation scientifique de 0,0032 est :", "3,2 × 10⁻³", "32 × 10⁻⁴", "3,2 × 10³", "0,32 × 10⁻²",
 "On décale la virgule de 3 rangs."),
(2, "10⁵ × 10³ est égal à :", "10⁸", "10¹⁵", "10²", "100⁸",
 "On additionne les exposants."),
(2, "Quel nombre est le plus grand ?", "−2", "−5", "−7", "−10",
 "Le plus proche de zéro."),
(3, "10⁶ / 10⁴ est égal à :", "10²", "10¹⁰", "10²⁴", "10⁻²",
 "On soustrait les exposants."),
(3, "(−2) × (−3) × (−1) est égal à :", "−6", "6", "−5", "5",
 "Trois facteurs négatifs : le produit est négatif."),
(3, "47 × 10⁻² est égal à :", "0,47", "4 700", "4,7", "0,047",
 "Virgule décalée de 2 rangs vers la gauche."),
(4, "(10²)³ est égal à :", "10⁶", "10⁵", "10⁸", "10⁹",
 "On multiplie les exposants."),
(4, "Un ordre de grandeur de 4,8 × 10³ × 2,1 est :", "10⁴", "10³", "10⁶", "10²",
 "5 × 10³ × 2 = 10 × 10³."),
]),

dict(
nom="Angles et droites parallèles",
fiche="""## Deux droites coupées par une sécante
• Angles alternes-internes : de part et d'autre de la sécante, entre les deux droites.
• Angles correspondants : du même côté de la sécante, l'un entre les droites, l'autre à l'extérieur, « à la même place ».

## Propriétés
• Si les deux droites sont parallèles, les angles alternes-internes sont égaux et les angles correspondants sont égaux.
• Réciproque : si deux angles alternes-internes (ou correspondants) sont égaux, les droites sont parallèles.

[[schema:angles-paralleles|Angles alternes-internes]]
## Rappels
• Angles opposés par le sommet : égaux.
• Angles supplémentaires : somme 180° ; complémentaires : somme 90°.
• Somme des angles d'un triangle : 180°.

## Cercle
• Angle au centre : son sommet est le centre du cercle.
• Longueur d'un arc : proportionnelle à son angle au centre : longueur = (angle / 360) × 2πr.
• Dans un même cercle, deux cordes de même longueur interceptent des arcs de même longueur.

## Exemple
(d) // (d') coupées par (s). Un angle alterne-interne mesure 65° : l'autre aussi mesure 65°, et l'angle qui lui est adjacent sur la même droite mesure 180 − 65 = 115°.""",
questions=[
(2, 'Sur le schéma, d et d′ sont parallèles. Les angles a et b sont :', 'alternes-internes et égaux', 'correspondants et supplémentaires', 'opposés par le sommet', 'complémentaires',
 "Ils sont de part et d'autre de la sécante, entre les deux droites.", 'angles-paralleles'),
(1, "Deux angles opposés par le sommet sont :", "égaux", "supplémentaires", "complémentaires", "toujours droits",
 "Propriété à connaître."),
(2, "Deux droites parallèles coupées par une sécante forment des angles alternes-internes :", "égaux", "supplémentaires", "complémentaires", "toujours de 90°",
 "Propriété des droites parallèles."),
(2, "Si deux angles correspondants sont égaux, alors les deux droites sont :", "parallèles", "perpendiculaires", "sécantes en un point", "confondues forcément",
 "C'est la réciproque."),
(2, "Deux angles supplémentaires ont une somme de :", "180°", "90°", "360°", "100°",
 "Complémentaires : 90°."),
(2, "Dans un triangle, deux angles mesurent 50° et 60°. Le troisième mesure :", "70°", "80°", "90°", "110°",
 "180 − 50 − 60."),
(3, "(d) // (d'). Un angle alterne-interne mesure 65°. L'autre angle alterne-interne mesure :", "65°", "115°", "25°", "130°",
 "Ils sont égaux."),
(3, "Un angle au centre a son sommet :", "au centre du cercle", "sur le cercle", "à l'extérieur du cercle", "n'importe où",
 "D'où son nom."),
(3, "Dans un cercle de rayon 3 cm, un arc d'angle au centre 360° mesure :", "6π cm", "3π cm", "9π cm", "12π cm",
 "C'est le périmètre 2πr."),
(4, "Dans un cercle de rayon 6 cm, l'arc intercepté par un angle au centre de 60° mesure :", "2π cm", "6π cm", "π cm", "12π cm",
 "(60/360) × 2π × 6 = 2π."),
(4, "Un angle mesure 40°. Son complémentaire mesure :", "50°", "140°", "40°", "320°",
 "90 − 40."),
]),

dict(
nom="Nombres rationnels",
fiche="""## PGCD et PPCM
• PGCD (plus grand commun diviseur) : PGCD(12 ; 18) = 6. Il sert à simplifier une fraction au maximum : 12/18 = 2/3.
• PPCM (plus petit commun multiple) : PPCM(4 ; 6) = 12. Il sert à trouver le dénominateur commun.
• On les trouve avec la décomposition en facteurs premiers : 12 = 2² × 3 ; 18 = 2 × 3².
   PGCD : produit des facteurs communs avec le plus petit exposant (2 × 3 = 6).
   PPCM : tous les facteurs avec le plus grand exposant (2² × 3² = 36).

## Opérations sur les fractions
• Addition : même dénominateur. 1/4 + 1/6 = 3/12 + 2/12 = 5/12.
• Multiplication : numérateurs ensemble, dénominateurs ensemble. 2/3 × 5/7 = 10/21.
• Inverse de a/b (a ≠ 0) : b/a. Diviser, c'est multiplier par l'inverse : (2/3) ÷ (4/5) = (2/3) × (5/4) = 10/12 = 5/6.
• Priorités : parenthèses, puis multiplications et divisions, puis additions et soustractions.

## Approximations
• Troncature : on coupe (1/3 ≈ 0,33 au centième).
• Arrondi : on regarde le chiffre suivant (2/3 ≈ 0,67 au centième, car le chiffre suivant est 6).""",
questions=[
(1, "L'inverse de 3/5 est :", "5/3", "−3/5", "3/5", "1/15",
 "On échange numérateur et dénominateur."),
(2, "PGCD(12 ; 18) est égal à :", "6", "3", "36", "2",
 "12 = 6 × 2 et 18 = 6 × 3."),
(2, "PPCM(4 ; 6) est égal à :", "12", "24", "2", "10",
 "Le plus petit multiple commun."),
(2, "12/18 simplifiée au maximum donne :", "2/3", "6/9", "4/6", "3/2",
 "On divise par le PGCD 6."),
(2, "1/4 + 1/6 est égal à :", "5/12", "2/10", "1/5", "1/12",
 "Dénominateur commun 12 : 3/12 + 2/12."),
(2, "2/3 × 5/7 est égal à :", "10/21", "7/10", "10/7", "7/21",
 "On multiplie les numérateurs et les dénominateurs."),
(3, "(2/3) ÷ (4/5) est égal à :", "5/6", "8/15", "6/5", "10/3",
 "(2/3) × (5/4) = 10/12 = 5/6."),
(3, "L'arrondi de 2/3 au centième est :", "0,67", "0,66", "0,6", "0,7",
 "2/3 = 0,666… : le chiffre des millièmes est 6, on arrondit au-dessus."),
(3, "La troncature de 2/3 au centième est :", "0,66", "0,67", "0,7", "0,6",
 "On coupe sans arrondir."),
(4, "1 − 2/3 × 3/4 est égal à :", "1/2", "1/4", "1/12", "3/4",
 "Priorité à la multiplication : 2/3 × 3/4 = 1/2, puis 1 − 1/2."),
(4, "PPCM(12 ; 18) est égal à :", "36", "6", "216", "72",
 "2² × 3² = 36."),
]),

dict(
nom="Distances et bissectrice",
fiche="""## Distance d'un point à une droite
C'est la longueur du segment perpendiculaire mené du point à la droite : c'est la plus courte distance entre le point et la droite.
Si H est le pied de la perpendiculaire à (d) passant par A, la distance de A à (d) est AH.

[[schema:bissectrice|Bissectrice et distances aux côtés]]
## Distance entre deux droites parallèles
C'est la distance d'un point quelconque de l'une à l'autre (elle est la même partout).

## Médiatrice (rappel)
Ensemble des points situés à égale distance des deux extrémités d'un segment.

## Bissectrice d'un angle
• Droite (ou demi-droite) qui partage un angle en deux angles égaux.
• Propriété : tout point de la bissectrice est à égale distance des deux côtés de l'angle.
• Réciproque : un point situé à l'intérieur d'un angle et à égale distance de ses deux côtés est sur sa bissectrice.

## Construction au compas
1. Tracer un arc de centre le sommet coupant les deux côtés en M et N.
2. Tracer deux arcs de même rayon de centres M et N ; ils se coupent en P.
3. La demi-droite issue du sommet et passant par P est la bissectrice.

## Dans le triangle
Les trois bissectrices d'un triangle sont concourantes en un point, centre du cercle inscrit dans le triangle (tangent aux trois côtés).""",
questions=[
(1, "La bissectrice d'un angle le partage en :", "deux angles égaux", "deux angles droits", "trois angles égaux", "deux angles supplémentaires",
 "Définition."),
(2, "La distance d'un point A à une droite (d) se mesure :", "sur la perpendiculaire à (d) passant par A", "sur n'importe quelle droite passant par A", "sur la parallèle à (d)", "avec un rapporteur",
 "C'est la plus courte distance."),
(2, "Tout point de la bissectrice d'un angle est :", "à égale distance des deux côtés de l'angle", "à égale distance des extrémités d'un segment", "sur le cercle circonscrit", "le milieu d'un côté",
 "Propriété de la bissectrice."),
(2, "Tout point de la médiatrice d'un segment [AB] est :", "à égale distance de A et de B", "à égale distance des côtés d'un angle", "sur [AB]", "le milieu de [AB] seulement",
 "Ne pas confondre médiatrice et bissectrice."),
(2, "Un angle de 70° est partagé par sa bissectrice en deux angles de :", "35°", "70°", "140°", "20°",
 "70 / 2."),
(3, "Le point de rencontre des trois bissectrices d'un triangle est le centre du cercle :", "inscrit", "circonscrit", "de rayon nul", "passant par les sommets",
 "Le cercle inscrit est tangent aux trois côtés."),
(3, "La distance entre deux droites parallèles :", "est la même en tout point", "dépend du point choisi", "est toujours nulle", "n'existe pas",
 "On la mesure sur une perpendiculaire commune."),
(3, "Un point M, situé à l'intérieur d'un angle, est à 3 cm de ses deux côtés. On peut affirmer que M est :", "sur la bissectrice de l'angle", "sur la médiatrice", "au sommet de l'angle", "sur un côté",
 "C'est la réciproque de la propriété."),
(4, "Pour construire la bissectrice, la première étape est de tracer :", "un arc de centre le sommet coupant les deux côtés", "la médiatrice d'un côté", "un cercle passant par le sommet", "une perpendiculaire à un côté",
 "On obtient deux points M et N."),
(4, "H est le pied de la perpendiculaire à (d) passant par A ; AH = 4 cm et B est un autre point de (d). On a :", "AB > 4 cm", "AB = 4 cm", "AB < 4 cm", "AB = 0",
 "AH est la plus courte distance."),
]),

dict(
nom="Calcul littéral",
fiche="""## Expressions littérales
Une expression qui contient des lettres. Calculer sa valeur numérique, c'est remplacer les lettres par des nombres.
Pour x = 2 : 3x² − 1 = 3 × 4 − 1 = 11.

## Réduire
Regrouper les termes semblables : 3x + 5 − x + 2 = 2x + 7.

## Supprimer des parenthèses
• Précédées de + : on garde les signes. a + (b − c) = a + b − c.
• Précédées de − : on change tous les signes. a − (b − c) = a − b + c.

## Développer
• k(a + b) = ka + kb.
• (a + b)(c + d) = ac + ad + bc + bd.

## Produits remarquables
• (a + b)² = a² + 2ab + b²
• (a − b)² = a² − 2ab + b²
• (a + b)(a − b) = a² − b²

## Factoriser
Faire apparaître un facteur commun : 6x + 9 = 3(2x + 3) ; x² + 5x = x(x + 5).
Avec les produits remarquables : x² − 9 = (x + 3)(x − 3).

## Pièges
(a + b)² n'est pas a² + b² ; −(x − 3) = −x + 3.""",
questions=[
(1, "3x + 5 − x + 2 réduite donne :", "2x + 7", "4x + 7", "2x + 3", "3x + 7",
 "3x − x = 2x et 5 + 2 = 7."),
(1, "Pour x = 2, 3x² − 1 vaut :", "11", "35", "17", "5",
 "3 × 4 − 1."),
(2, "a − (b − c) est égal à :", "a − b + c", "a − b − c", "a + b − c", "a + b + c",
 "Le signe − change tous les signes."),
(2, "3(x + 4) développé donne :", "3x + 12", "3x + 4", "x + 12", "3x + 7",
 "On distribue le 3."),
(2, "(x + 3)² est égal à :", "x² + 6x + 9", "x² + 9", "x² + 3x + 9", "2x + 6",
 "(a + b)² = a² + 2ab + b²."),
(3, "(x − 5)(x + 5) est égal à :", "x² − 25", "x² + 25", "x² − 10x + 25", "2x",
 "(a − b)(a + b) = a² − b²."),
(3, "6x + 9 factorisé donne :", "3(2x + 3)", "6(x + 9)", "3(2x + 9)", "9(6x + 1)",
 "3 est le facteur commun."),
(3, "x² − 9 factorisé donne :", "(x + 3)(x − 3)", "(x − 3)²", "(x + 9)(x − 1)", "x(x − 9)",
 "Différence de deux carrés."),
(4, "(2x − 1)² est égal à :", "4x² − 4x + 1", "4x² + 1", "2x² − 4x + 1", "4x² − 2x + 1",
 "(2x)² − 2 × 2x × 1 + 1²."),
(4, "(x + 2)(x + 3) développé donne :", "x² + 5x + 6", "x² + 6", "x² + 6x + 5", "2x + 5",
 "x² + 3x + 2x + 6."),
]),

dict(
nom="Cercles et triangles",
fiche="""## Droite et cercle
Un cercle de centre O et de rayon r, une droite (d) à la distance d de O :
• d > r : la droite est extérieure au cercle ;
• d = r : la droite est tangente au cercle (un seul point commun) ;
• d < r : la droite est sécante (deux points communs).
La tangente en un point A du cercle est perpendiculaire au rayon [OA].

[[schema:cercle-triangle-rectangle|Triangle rectangle inscrit dans un demi-cercle]]
## Droite des milieux
• La droite qui passe par les milieux de deux côtés d'un triangle est parallèle au troisième côté.
• Le segment qui joint ces milieux mesure la moitié du troisième côté.
• Réciproque : la parallèle à un côté passant par le milieu d'un autre côté coupe le troisième en son milieu.

## Droites remarquables du triangle
• Médiatrices (perpendiculaires aux côtés en leur milieu) : concourantes au centre du cercle circonscrit.
• Hauteurs (issues d'un sommet, perpendiculaires au côté opposé) : concourantes à l'orthocentre.
• Médianes (d'un sommet au milieu du côté opposé) : concourantes au centre de gravité, situé aux 2/3 de chaque médiane à partir du sommet.
• Bissectrices : concourantes au centre du cercle inscrit.""",
questions=[
(3, 'Sur le schéma, [AB] est un diamètre et C est sur le cercle. Le triangle ABC est :', 'rectangle en C', 'équilatéral', 'rectangle en A', 'isocèle en B',
 'Un triangle inscrit dans un demi-cercle est rectangle.', 'cercle-triangle-rectangle'),
(1, "Une droite qui a un seul point commun avec un cercle est :", "tangente au cercle", "sécante", "extérieure", "un diamètre",
 "Elle « touche » le cercle."),
(2, "La tangente au cercle en un point A est :", "perpendiculaire au rayon [OA]", "parallèle au rayon [OA]", "confondue avec le rayon", "passant par le centre",
 "Propriété à connaître."),
(2, "Un cercle de rayon 5 cm et une droite à 3 cm du centre : la droite est :", "sécante au cercle", "tangente", "extérieure", "confondue avec le cercle",
 "3 < 5 : deux points communs."),
(2, "Dans un triangle ABC, I milieu de [AB] et J milieu de [AC]. La droite (IJ) est :", "parallèle à (BC)", "perpendiculaire à (BC)", "confondue avec (BC)", "sécante à (BC) en son milieu",
 "Propriété de la droite des milieux."),
(2, "Avec les mêmes points, si BC = 10 cm, alors IJ mesure :", "5 cm", "10 cm", "20 cm", "2,5 cm",
 "La moitié du troisième côté."),
(3, "Les médianes d'un triangle se coupent :", "au centre de gravité", "à l'orthocentre", "au centre du cercle circonscrit", "au centre du cercle inscrit",
 "Il est aux 2/3 de chaque médiane."),
(3, "Le point de rencontre des hauteurs s'appelle :", "l'orthocentre", "le centre de gravité", "le centre du cercle inscrit", "le milieu",
 "Les hauteurs sont perpendiculaires aux côtés."),
(3, "Le centre du cercle circonscrit à un triangle est le point de rencontre :", "des médiatrices", "des hauteurs", "des médianes", "des bissectrices",
 "Il est à égale distance des trois sommets."),
(4, "Une médiane mesure 9 cm. Le centre de gravité est situé à quelle distance du sommet ?", "6 cm", "3 cm", "4,5 cm", "9 cm",
 "Aux 2/3 : 2/3 × 9."),
(4, "Une hauteur d'un triangle est :", "issue d'un sommet et perpendiculaire au côté opposé", "issue d'un sommet et passant par le milieu du côté opposé", "perpendiculaire à un côté en son milieu", "la plus longue droite du triangle",
 "Ne pas confondre avec la médiane ou la médiatrice."),
]),

dict(
nom="Équations et inéquations",
fiche="""## Équation du premier degré
Une égalité avec une inconnue. Résoudre, c'est trouver la ou les valeurs qui la vérifient.
Règles : on peut ajouter (ou soustraire) un même nombre aux deux membres, et multiplier (ou diviser) par un même nombre non nul.
3x − 5 = 10 → 3x = 15 → x = 5. Vérification : 3 × 5 − 5 = 10 ✓.

## Mettre un problème en équation
1. Choisir l'inconnue (x = …).
2. Traduire l'énoncé par une équation.
3. Résoudre et vérifier.
4. Répondre par une phrase.
Exemple : « Le double d'un nombre augmenté de 7 donne 19 » : 2x + 7 = 19, x = 6.

## Inéquations
• On peut ajouter ou soustraire un même nombre sans changer le sens de l'inégalité.
• Multiplier ou diviser par un nombre strictement positif : le sens ne change pas.
• Multiplier ou diviser par un nombre strictement négatif : le sens CHANGE.
   −2x < 6 → x > −3.
• Les solutions forment un ensemble ; on les représente sur une droite graduée (crochet tourné vers les solutions ou vers l'extérieur selon que la borne est incluse ou non).""",
questions=[
(1, "La solution de x + 7 = 12 est :", "5", "19", "−5", "7",
 "x = 12 − 7."),
(2, "La solution de 3x − 5 = 10 est :", "5", "15", "5/3", "−5",
 "3x = 15."),
(2, "La solution de 2x + 7 = 19 est :", "6", "13", "12", "26",
 "2x = 12."),
(2, "Les solutions de x + 3 > 5 sont les nombres :", "x > 2", "x > 8", "x < 2", "x > −2",
 "On retire 3 des deux côtés."),
(3, "Les solutions de −2x < 6 sont les nombres :", "x > −3", "x < −3", "x < 3", "x > 3",
 "On divise par −2 : le sens change."),
(3, "La solution de 5x = 2x + 9 est :", "3", "9/7", "9", "−3",
 "3x = 9."),
(3, "Si on retire 4 au triple d'un nombre, on obtient 11. Ce nombre est :", "5", "7/3", "15", "3",
 "3x − 4 = 11, donc 3x = 15."),
(3, "Quand on multiplie les deux membres d'une inégalité par un nombre négatif :", "on change le sens de l'inégalité", "le sens ne change pas", "l'inégalité devient une égalité", "on ne peut pas le faire",
 "−1 < 2 devient 1 > −2."),
(4, "La solution de 2(x − 1) = x + 3 est :", "5", "1", "4", "−5",
 "2x − 2 = x + 3, donc x = 5."),
(4, "Les solutions de 4 − x ≥ 1 sont les nombres :", "x ≤ 3", "x ≥ 3", "x ≤ −3", "x ≥ −3",
 "−x ≥ −3, puis on multiplie par −1 en changeant le sens."),
]),

dict(
nom="Propriété de Pythagore",
fiche="""## Le triangle rectangle
Il a un angle droit. Le côté opposé à l'angle droit est l'hypoténuse : c'est le plus long côté.

[[schema:pythagore|Triangle rectangle et hypoténuse]]
## La propriété de Pythagore
Si le triangle ABC est rectangle en A, alors BC² = AB² + AC².
(Le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.)

## Calculer une longueur
• L'hypoténuse : AB = 3, AC = 4 → BC² = 9 + 16 = 25 → BC = 5.
• Un autre côté : BC = 13, AB = 5 → AC² = 169 − 25 = 144 → AC = 12.
On utilise la racine carrée (touche √ de la calculatrice).

## La réciproque
Si BC² = AB² + AC², alors le triangle ABC est rectangle en A.
Exemple : 6, 8, 10 : 10² = 100 et 6² + 8² = 36 + 64 = 100 : triangle rectangle.
Si l'égalité est fausse, le triangle n'est pas rectangle.

## Applications
Diagonale d'un rectangle, hauteur d'une échelle contre un mur, distance sur un terrain.
Diagonale d'un carré de côté c : c√2.""",
questions=[
(2, "Sur le schéma, a = 3 cm et b = 4 cm. L'hypoténuse c mesure :", '5 cm', '7 cm', '25 cm', '12 cm',
 'c² = 9 + 16 = 25.', 'pythagore'),
(1, "Dans un triangle rectangle, l'hypoténuse est :", "le côté opposé à l'angle droit", "le plus petit côté", "un côté de l'angle droit", "la hauteur",
 "C'est le plus long côté."),
(2, "ABC est rectangle en A, AB = 3 et AC = 4. BC mesure :", "5", "7", "25", "12",
 "BC² = 9 + 16 = 25."),
(2, "Si ABC est rectangle en A, la propriété de Pythagore s'écrit :", "BC² = AB² + AC²", "AB² = BC² + AC²", "BC = AB + AC", "AC² = AB² + BC²",
 "L'hypoténuse est [BC]."),
(2, "ABC est rectangle en A, BC = 13 et AB = 5. AC mesure :", "12", "8", "18", "144",
 "AC² = 169 − 25 = 144."),
(3, "Un triangle de côtés 6, 8 et 10 est :", "rectangle", "équilatéral", "isocèle", "non rectangle",
 "100 = 36 + 64 : réciproque de Pythagore."),
(3, "Un triangle de côtés 4, 5 et 6 est :", "non rectangle", "rectangle", "isocèle", "équilatéral",
 "36 ≠ 16 + 25 = 41."),
(3, "La diagonale d'un rectangle de 6 m sur 8 m mesure :", "10 m", "14 m", "48 m", "12 m",
 "√(36 + 64)."),
(3, "On connaît les longueurs des trois côtés d'un triangle. Pour démontrer qu'il est rectangle, on utilise :", "la réciproque de la propriété de Pythagore", "la propriété de Thalès", "la somme des angles uniquement", "la droite des milieux",
 "On compare le carré du plus grand côté à la somme des autres carrés."),
(4, "Une échelle de 5 m est posée contre un mur, son pied à 3 m du mur. Elle touche le mur à une hauteur de :", "4 m", "2 m", "8 m", "√34 m",
 "√(25 − 9) = 4."),
(4, "La diagonale d'un carré de côté 1 cm mesure :", "√2 cm", "2 cm", "1 cm", "√3 cm",
 "√(1 + 1)."),
]),

dict(
nom="Statistique",
fiche="""## Vocabulaire
Population (l'ensemble étudié), individu, caractère (ce qu'on observe), modalité (valeur du caractère), effectif (nombre d'individus d'une modalité), effectif total.

## Fréquence
Fréquence = effectif / effectif total. En pourcentage : × 100.
10 élèves sur 40 ont 12 : fréquence 10/40 = 0,25 = 25 %.

## Mode et moyenne
• Mode : la modalité qui a le plus grand effectif.
• Moyenne : somme des (valeur × effectif) divisée par l'effectif total.
   Notes 8 (2 élèves), 10 (5 élèves), 14 (3 élèves) : (16 + 50 + 42) / 10 = 10,8.

## Diagrammes
• Diagramme en bâtons : hauteur proportionnelle à l'effectif.
• Diagramme circulaire : angle = fréquence × 360°.
• Diagramme semi-circulaire : angle = fréquence × 180°.
   Une modalité de fréquence 25 % occupe 0,25 × 180 = 45° d'un demi-disque.

## Lire un tableau
Toujours vérifier que la somme des effectifs est égale à l'effectif total et que la somme des fréquences fait 100 %.""",
questions=[
(1, "Le mode d'une série est :", "la valeur qui a le plus grand effectif", "la valeur du milieu", "la moyenne", "la plus grande valeur",
 "La valeur la plus fréquente."),
(2, "10 élèves sur 40 ont la note 12. La fréquence de la note 12 est :", "25 %", "10 %", "40 %", "4 %",
 "10 / 40 = 0,25."),
(2, "La moyenne de 8, 10 et 12 est :", "10", "30", "12", "9",
 "30 / 3."),
(2, "Dans un diagramme circulaire, une modalité de fréquence 50 % occupe :", "180°", "90°", "50°", "360°",
 "0,5 × 360."),
(3, "Notes : 8 (2 élèves), 10 (5 élèves), 14 (3 élèves). La moyenne est :", "10,8", "10,67", "11", "32",
 "(16 + 50 + 42) / 10."),
(3, "Dans un diagramme semi-circulaire, une modalité de fréquence 25 % occupe :", "45°", "90°", "25°", "180°",
 "0,25 × 180."),
(3, "Notes : 8 (2 élèves), 10 (5 élèves), 14 (3 élèves). Le mode est :", "10", "8", "14", "5",
 "C'est la note qui a le plus grand effectif."),
(3, "La somme des fréquences d'une série est toujours égale à :", "100 %", "50 %", "l'effectif total", "la moyenne",
 "Ou 1 en écriture décimale."),
(4, "La moyenne de 5 notes est 12. La somme de ces notes est :", "60", "12", "17", "2,4",
 "Moyenne × effectif."),
(4, "Dans une enquête sur la couleur préférée, le caractère étudié est :", "la couleur préférée", "le nombre d'élèves", "la classe", "le pourcentage",
 "Les modalités sont les couleurs."),
]),

dict(
nom="Perspective cavalière",
fiche="""## Le principe
Représenter un solide (cube, pavé, prisme) sur une feuille plane en donnant une impression de relief.

[[schema:perspective-cube|Cube en perspective cavalière]]
## Les règles
• La face avant (de face) est dessinée en vraie grandeur (ou à l'échelle), sans déformation.
• Les arêtes « fuyantes » (qui partent vers l'arrière) sont parallèles entre elles, inclinées d'un angle α (souvent 30° ou 45°) et réduites par un coefficient c (souvent 0,5).
• Les arêtes parallèles dans la réalité restent parallèles sur le dessin.
• Les arêtes cachées sont dessinées en pointillés.

## Exemple
Un cube de 4 cm avec c = 0,5 et α = 45° : face avant = carré de 4 cm ; arêtes fuyantes de 4 × 0,5 = 2 cm, inclinées à 45°.

## Ce qui est conservé
• Le parallélisme.
• Les longueurs des arêtes de la face avant.
• Les milieux.
Les angles droits des faces latérales ne sont pas conservés (avec α = 45°, ils apparaissent comme des angles de 45° ou 135°).""",
questions=[
(2, 'Sur le schéma, les arêtes en pointillés représentent :', 'les arêtes cachées', 'les arêtes plus longues', 'les diagonales', 'les arêtes de la face avant',
 'On ne les verrait pas en regardant le solide.', 'perspective-cube'),
(1, "En perspective cavalière, les arêtes cachées sont dessinées :", "en pointillés", "en rouge", "en trait épais", "elles ne sont pas dessinées",
 "Convention à respecter."),
(2, "La face avant d'un cube en perspective cavalière est dessinée :", "en vraie grandeur, sans déformation", "réduite de moitié", "comme un losange", "en pointillés",
 "Seules les fuyantes sont réduites."),
(2, "Les arêtes fuyantes sont :", "parallèles entre elles", "perpendiculaires entre elles", "toutes verticales", "de longueur réelle",
 "Le parallélisme est conservé."),
(2, "Un cube de 4 cm dessiné avec un coefficient de réduction de 0,5 a des fuyantes de :", "2 cm", "4 cm", "8 cm", "0,5 cm",
 "4 × 0,5."),
(3, "Une propriété conservée en perspective cavalière est :", "le parallélisme", "tous les angles droits", "toutes les longueurs", "la forme carrée de toutes les faces",
 "Les droites parallèles restent parallèles."),
(3, "L'angle de fuite le plus souvent utilisé est :", "45° ou 30°", "90°", "180°", "0°",
 "Il donne l'impression de profondeur."),
(3, "En perspective cavalière, les faces latérales d'un cube apparaissent comme :", "des parallélogrammes", "des carrés", "des cercles", "des triangles",
 "Les angles droits ne sont pas conservés."),
(4, "Un pavé de 6 cm × 3 cm × 4 cm est dessiné avec la face 6 cm × 3 cm devant et c = 0,5. Les fuyantes mesurent :", "2 cm", "4 cm", "3 cm", "1,5 cm",
 "La profondeur 4 cm est réduite : 4 × 0,5."),
(4, "Le milieu d'une arête fuyante sur le dessin correspond :", "au milieu de l'arête réelle", "au tiers de l'arête", "à son extrémité", "à rien de précis",
 "Les milieux sont conservés."),
(4, "Le coefficient de réduction s'applique :", "aux arêtes fuyantes seulement", "à toutes les arêtes", "à la face avant seulement", "aux arêtes verticales",
 "La face avant reste en vraie grandeur."),
]),

dict(
nom="Révision de l'année",
fiche="""## Nombres
• Puissances de 10 : 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; notation scientifique a × 10ⁿ avec 1 ≤ a < 10.
• Fractions : même dénominateur pour additionner ; diviser = multiplier par l'inverse ; simplifier avec le PGCD.
• Calcul littéral : (a + b)² = a² + 2ab + b² ; (a − b)² = a² − 2ab + b² ; (a + b)(a − b) = a² − b².
• Équations : isoler x ; inéquations : changer le sens si on multiplie par un négatif.

## Géométrie
• Parallèles et sécante : angles alternes-internes et correspondants égaux.
• Pythagore : triangle rectangle en A ⇔ BC² = AB² + AC².
• Droite des milieux : parallèle au 3ᵉ côté, moitié de sa longueur.
• Droites du triangle : médiatrices (cercle circonscrit), hauteurs (orthocentre), médianes (centre de gravité aux 2/3), bissectrices (cercle inscrit).
• Tangente : perpendiculaire au rayon.

## Statistique
Mode, moyenne pondérée, fréquence, diagrammes circulaires (× 360°) et semi-circulaires (× 180°).

## Méthode
Toujours écrire la propriété utilisée : « D'après la propriété de Pythagore… », « Comme (d) // (d')… ».""",
questions=[
(2, "2,5 × 10³ est égal à :", "2 500", "250", "25 000", "0,0025",
 "Virgule décalée de 3 rangs vers la droite."),
(2, "(x + 4)² est égal à :", "x² + 8x + 16", "x² + 16", "x² + 4x + 16", "2x + 8",
 "Produit remarquable."),
(2, "ABC est rectangle en B. L'hypoténuse est :", "[AC]", "[AB]", "[BC]", "on ne peut pas savoir",
 "Le côté opposé à l'angle droit en B."),
(3, "La solution de 4x − 3 = 2x + 7 est :", "5", "2", "10", "−5",
 "2x = 10."),
(3, "3/4 − 1/3 est égal à :", "5/12", "2/1", "2/12", "1/12",
 "9/12 − 4/12."),
(3, "Les solutions de −3x ≥ 12 sont :", "x ≤ −4", "x ≥ −4", "x ≤ 4", "x ≥ 4",
 "On divise par −3 : le sens change."),
(3, "Un triangle de côtés 5, 12 et 13 est :", "rectangle", "équilatéral", "isocèle", "non rectangle",
 "169 = 25 + 144."),
(4, "Notes : 10 (4 élèves) et 15 (1 élève). La moyenne est :", "11", "12,5", "10", "25",
 "(40 + 15) / 5."),
(4, "x² − 16 factorisé donne :", "(x − 4)(x + 4)", "(x − 4)²", "(x − 8)(x + 2)", "x(x − 16)",
 "Différence de deux carrés."),
(4, "Le centre de gravité d'un triangle est le point de rencontre :", "des médianes", "des hauteurs", "des médiatrices", "des bissectrices",
 "Situé aux 2/3 de chaque médiane."),
]),
]
