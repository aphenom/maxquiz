NIVEAU, MATIERE = "5ème", "Mathématiques"

CHAPITRES = [
dict(
nom="Nombres décimaux relatifs",
fiche="""## Définition
Un nombre relatif est formé d'un signe (+ ou −) et d'une distance à zéro. Exemples : +3,5 ; −2. Le nombre 0 est à la fois positif et négatif ; il s'écrit sans signe.
• Deux nombres opposés ont la même distance à zéro et des signes contraires : 4 et −4.
• Sur une droite graduée, chaque point a pour abscisse un nombre relatif.

## Comparer
• Un nombre positif est plus grand qu'un nombre négatif : +1 > −8.
• De deux nombres négatifs, le plus grand est celui qui a la plus petite distance à zéro : −2 > −5.

## Additionner
• Même signe : on additionne les distances à zéro et on garde le signe. (−3) + (−4) = −7.
• Signes contraires : on soustrait les distances à zéro et on prend le signe de celui qui a la plus grande distance à zéro. (−7) + (+2) = −5.
• La somme de deux nombres opposés est nulle.

## Soustraire
Soustraire un nombre, c'est additionner son opposé : 3 − (−5) = 3 + 5 = 8 ; (−2) − 6 = (−2) + (−6) = −8.

## Exemple de la vie courante
À Abidjan il fait +30 °C, sur un sommet lointain −5 °C : l'écart est 30 − (−5) = 35 °C.""",
questions=[
(1, "L'opposé de −4 est :", "4", "−4", "0", "1/4",
 "Même distance à zéro, signe contraire."),
(1, "Quel nombre est le plus grand ?", "+1", "−8", "−1", "−0,5",
 "Un positif est plus grand qu'un négatif."),
(2, "(−3) + (−4) est égal à :", "−7", "7", "−1", "1",
 "Même signe : on additionne et on garde le signe −."),
(2, "(−7) + (+2) est égal à :", "−5", "5", "−9", "9",
 "7 − 2 = 5, signe du nombre de plus grande distance à zéro."),
(2, "Quel nombre est le plus petit ?", "−5", "−2", "0", "−3",
 "Le plus éloigné de zéro parmi les négatifs."),
(2, "(+6) + (−6) est égal à :", "0", "12", "−12", "6",
 "La somme de deux opposés est nulle."),
(3, "3 − (−5) est égal à :", "8", "−2", "2", "−8",
 "On additionne l'opposé : 3 + 5."),
(3, "(−2) − 6 est égal à :", "−8", "4", "−4", "8",
 "(−2) + (−6)."),
(3, "Il fait 30 °C à Abidjan et −5 °C sur un sommet. L'écart de température est :", "35 °C", "25 °C", "−35 °C", "5 °C",
 "30 − (−5) = 35."),
(4, "(−1,5) + (+4) − (−2,5) est égal à :", "5", "0", "−5", "3",
 "−1,5 + 4 + 2,5."),
]),

dict(
nom="Symétrie centrale",
fiche="""## Définition
Le symétrique d'un point M par rapport à un point O est le point M' tel que O soit le milieu de [MM'].
Le symétrique de O est O lui-même. On parle aussi de demi-tour autour de O.

[[schema:symetrie-centrale|Triangle et son symétrique par rapport à O]]
## Construction
Tracer la demi-droite [MO), puis reporter au compas la longueur OM de l'autre côté de O.

## Propriétés (la symétrie centrale conserve)
• Les longueurs : le symétrique d'un segment est un segment de même longueur.
• Les angles : même mesure.
• L'alignement, et les aires.
• Le symétrique d'une droite est une droite qui lui est PARALLÈLE.
• Le symétrique d'un cercle de centre A est un cercle de même rayon, de centre A' (symétrique de A).

## Centre de symétrie
Une figure a un centre de symétrie O si elle est sa propre symétrique par rapport à O.
Exemples : le parallélogramme (centre = intersection des diagonales), le cercle (son centre), le rectangle, le losange, le carré. Le triangle n'a pas de centre de symétrie.

## Ne pas confondre
La symétrie axiale (pliage le long d'une droite) et la symétrie centrale (demi-tour autour d'un point).""",
questions=[
(2, 'Sur le schéma, le point O est :', 'le milieu de [AA′]', 'un sommet du triangle', 'sur [BC]', 'le symétrique de A',
 'O est le centre de la symétrie.', 'symetrie-centrale'),
(1, "M' est le symétrique de M par rapport à O. Alors O est :", "le milieu de [MM']", "un point quelconque", "une extrémité du segment [MM']", "le symétrique de M",
 "C'est la définition."),
(2, "Le symétrique d'une droite par rapport à un point est :", "une droite parallèle", "une droite perpendiculaire", "un cercle", "un point",
 "La symétrie centrale transforme une droite en une droite parallèle."),
(2, "Le symétrique d'un segment de 5 cm mesure :", "5 cm", "10 cm", "2,5 cm", "cela dépend du centre",
 "Les longueurs sont conservées."),
(2, "Quelle figure n'a pas de centre de symétrie ?", "le triangle", "le carré", "le cercle", "le parallélogramme",
 "Un triangle n'est jamais sa propre image par un demi-tour."),
(2, "Le centre de symétrie d'un parallélogramme est :", "le point d'intersection des diagonales", "un de ses sommets", "le milieu d'un côté", "il n'en a pas",
 "Les diagonales se coupent en leur milieu."),
(3, "Le symétrique d'un angle de 40° mesure :", "40°", "140°", "80°", "320°",
 "Les angles sont conservés."),
(3, "Le symétrique de O par rapport à O est :", "O lui-même", "un point à l'infini", "il n'existe pas", "le point opposé",
 "Le centre de symétrie est son propre symétrique."),
(3, "Le symétrique d'un cercle de rayon 3 cm est :", "un cercle de rayon 3 cm", "un cercle de rayon 6 cm", "une droite", "un carré",
 "Même rayon, centre symétrique."),
(3, "La symétrie centrale correspond à :", "un demi-tour autour d'un point", "un pliage le long d'une droite", "un agrandissement", "un glissement",
 "La symétrie axiale est un pliage."),
(4, "A(2 ; 1) et O l'origine du repère. Le symétrique de A par rapport à O est :", "(−2 ; −1)", "(2 ; −1)", "(−2 ; 1)", "(1 ; 2)",
 "O est le milieu de [AA']."),
]),

dict(
nom="Les fractions",
fiche="""## Égalité de fractions
On ne change pas une fraction en multipliant (ou divisant) numérateur et dénominateur par un même nombre non nul : 3/4 = 6/8 = 15/20.
Simplifier : 12/18 = 2/3 (on divise par 6).

## Comparer
• Même dénominateur : la plus grande est celle qui a le plus grand numérateur.
• Sinon, on réduit au même dénominateur : 2/3 = 8/12 et 3/4 = 9/12, donc 2/3 < 3/4.

## Additionner et soustraire
On réduit au même dénominateur, puis on additionne les numérateurs :
1/4 + 2/3 = 3/12 + 8/12 = 11/12.

## Multiplier
On multiplie les numérateurs entre eux et les dénominateurs entre eux : 2/3 × 5/7 = 10/21.
Prendre une fraction d'une quantité : 3/4 de 20 = 3/4 × 20 = 15.

## Exemple
Une famille dépense 2/5 de son budget pour la nourriture et 1/4 pour le loyer : 2/5 + 1/4 = 8/20 + 5/20 = 13/20 du budget.""",
questions=[
(1, "3/4 est égal à :", "6/8", "3/8", "6/4", "4/3",
 "On multiplie haut et bas par 2."),
(2, "La forme irréductible de 12/18 est :", "2/3", "3/2", "6/9", "4/9",
 "On divise par 6."),
(2, "2/7 + 3/7 est égal à :", "5/7", "5/14", "6/7", "1",
 "Même dénominateur : on additionne les numérateurs."),
(2, "2/3 × 5/7 est égal à :", "10/21", "7/10", "10/7", "7/21",
 "Numérateurs entre eux, dénominateurs entre eux."),
(2, "3/4 de 20 est égal à :", "15", "12", "60", "5",
 "20 ÷ 4 × 3."),
(3, "1/4 + 2/3 est égal à :", "11/12", "3/7", "3/12", "2/12",
 "3/12 + 8/12."),
(3, "Quelle fraction est la plus grande ?", "3/4", "2/3", "5/8", "1/2",
 "Au dénominateur 24 : 18, 16, 15, 12."),
(3, "5/6 − 1/3 est égal à :", "1/2", "4/3", "1/3", "2/3",
 "5/6 − 2/6 = 3/6."),
(3, "2/5 + 1/4 est égal à :", "13/20", "3/9", "3/20", "2/20",
 "8/20 + 5/20."),
(4, "Un élève a lu 3/8 d'un livre de 240 pages. Il lui reste à lire :", "150 pages", "90 pages", "80 pages", "160 pages",
 "Il a lu 90 pages ; 240 − 90."),
]),

dict(
nom="Les angles",
fiche="""## Vocabulaire
• Angle aigu : entre 0° et 90° ; droit : 90° ; obtus : entre 90° et 180° ; plat : 180°.

## Angles associés
• Deux angles sont complémentaires si leur somme vaut 90°.
• Deux angles sont supplémentaires si leur somme vaut 180°.
• Deux angles adjacents ont le même sommet, un côté commun et sont situés de part et d'autre de ce côté.
• Deux angles opposés par le sommet sont formés par deux droites sécantes ; ils ont la même mesure.

[[schema:angles-opposes|Angles opposés par le sommet]]
## La bissectrice
La bissectrice d'un angle est la demi-droite qui le partage en deux angles de même mesure. On la construit au compas ou au rapporteur.

## Exemples
• Le complémentaire de 35° est 55°.
• Le supplémentaire de 110° est 70°.
• Deux droites se coupent ; un angle mesure 50°. Son opposé par le sommet mesure 50°, ses voisins mesurent 130°.

## Piège
Complémentaire → 90° (comme le « c » de coin droit) ; supplémentaire → 180°.""",
questions=[
(1, "Un angle de 120° est :", "obtus", "aigu", "droit", "plat",
 "Entre 90° et 180°."),
(1, "Un angle plat mesure :", "180°", "90°", "360°", "0°",
 "Ses côtés sont dans le prolongement l'un de l'autre."),
(2, "Le complémentaire d'un angle de 35° mesure :", "55°", "145°", "35°", "65°",
 "90 − 35."),
(2, "Le supplémentaire d'un angle de 110° mesure :", "70°", "20°", "250°", "110°",
 "180 − 110."),
(2, "Deux angles opposés par le sommet :", "ont la même mesure", "sont toujours droits", "sont complémentaires", "ont une somme de 360°",
 "Ils sont formés par deux droites sécantes."),
(2, "La demi-droite qui partage un angle en deux angles égaux s'appelle :", "la bissectrice", "la médiatrice", "la médiane", "la hauteur",
 "Elle part du sommet."),
(3, "Deux droites se coupent et forment un angle de 50°. L'angle voisin mesure :", "130°", "50°", "40°", "310°",
 "Les angles voisins sont supplémentaires."),
(3, "Un angle de 64° est coupé par sa bissectrice. Chaque angle obtenu mesure :", "32°", "64°", "128°", "26°",
 "64 ÷ 2."),
(3, "Deux angles complémentaires et égaux mesurent chacun :", "45°", "90°", "30°", "60°",
 "90 ÷ 2."),
(4, "Un angle mesure le double de son supplémentaire. Il mesure :", "120°", "60°", "90°", "135°",
 "x + x/2 = 180, donc x = 120."),
]),

dict(
nom="Le parallélogramme",
fiche="""## Définition
Un parallélogramme est un quadrilatère qui a ses côtés opposés parallèles deux à deux.

## Propriétés
Dans un parallélogramme :
• les côtés opposés ont la même longueur ;
• les diagonales se coupent en leur milieu (ce point est le centre de symétrie) ;
• les angles opposés ont la même mesure ;
• deux angles consécutifs sont supplémentaires (somme 180°).

[[schema:parallelogramme|Propriétés du parallélogramme]]
## Reconnaître un parallélogramme
Un quadrilatère est un parallélogramme si :
• ses côtés opposés sont parallèles deux à deux ;
• OU ses diagonales se coupent en leur milieu ;
• OU ses côtés opposés ont deux à deux la même longueur (s'il n'est pas croisé) ;
• OU deux côtés opposés sont parallèles et de même longueur (s'il n'est pas croisé).

## Parallélogrammes particuliers
• Rectangle : 4 angles droits ; diagonales de même longueur.
• Losange : 4 côtés égaux ; diagonales perpendiculaires.
• Carré : à la fois rectangle et losange.
• Un parallélogramme dont les diagonales ont la même longueur est un rectangle ; un parallélogramme dont les diagonales sont perpendiculaires est un losange.

## Aire
Aire = base × hauteur (la hauteur est perpendiculaire à la base). Base 8 cm, hauteur 5 cm : A = 40 cm².""",
questions=[
(2, 'Sur le schéma, les diagonales [AC] et [BD] :', 'se coupent en leur milieu O', 'sont perpendiculaires', 'ont toujours la même longueur', 'sont parallèles',
 "C'est une propriété de tout parallélogramme.", 'parallelogramme'),
(1, "Un parallélogramme a ses côtés opposés :", "parallèles deux à deux", "perpendiculaires", "sécants", "toujours égaux à ses diagonales",
 "C'est la définition."),
(2, "Les diagonales d'un parallélogramme :", "se coupent en leur milieu", "sont toujours perpendiculaires", "sont toujours égales", "ne se coupent pas",
 "Leur point commun est le centre de symétrie."),
(2, "Dans le parallélogramme ABCD, AB = 6 cm. CD mesure :", "6 cm", "3 cm", "12 cm", "on ne peut pas savoir",
 "Les côtés opposés ont la même longueur."),
(2, "Un losange a :", "quatre côtés de même longueur", "quatre angles droits", "des diagonales de même longueur seulement", "trois côtés égaux",
 "Ses diagonales sont perpendiculaires."),
(2, "L'aire d'un parallélogramme de base 8 cm et de hauteur 5 cm est :", "40 cm²", "13 cm²", "26 cm²", "20 cm²",
 "Base × hauteur."),
(3, "Dans un parallélogramme, un angle mesure 70°. L'angle consécutif mesure :", "110°", "70°", "20°", "290°",
 "Deux angles consécutifs sont supplémentaires."),
(3, "Un parallélogramme dont les diagonales ont la même longueur est :", "un rectangle", "un losange", "un trapèze", "un triangle",
 "Un parallélogramme qui a des diagonales de même longueur est un rectangle."),
(3, "Un parallélogramme dont les diagonales sont perpendiculaires est :", "un losange", "un rectangle", "toujours un carré", "un trapèze",
 "Un parallélogramme qui a des diagonales perpendiculaires est un losange."),
(3, "Un quadrilatère dont les diagonales se coupent en leur milieu est :", "un parallélogramme", "un trapèze quelconque", "un cerf-volant", "un triangle",
 "C'est une propriété caractéristique."),
(4, "Un carré est :", "à la fois un rectangle et un losange", "un rectangle mais pas un losange", "un losange mais pas un parallélogramme", "un trapèze sans côtés parallèles",
 "Il a quatre angles droits et quatre côtés égaux."),
]),

dict(
nom="Expressions littérales",
fiche="""## Écrire avec des lettres
Une lettre remplace un nombre inconnu ou qui peut varier.
Le signe × peut être sous-entendu entre un nombre et une lettre : 3 × a = 3a ; a × b = ab.
a × a = a² ; a × a × a = a³.

## Calculer la valeur d'une expression
On remplace la lettre par sa valeur : pour x = 4, 3x + 2 = 3 × 4 + 2 = 14.

## Réduire
On regroupe les termes de même nature : 5x + 3x = 8x ; 7a − 2 + a = 8a − 2. Mais 3x + 2 ne se réduit pas.

## Développer (distributivité)
k(a + b) = ka + kb : 3(x + 4) = 3x + 12.
k(a − b) = ka − kb : 5(2 − y) = 10 − 5y.

## Factoriser
ka + kb = k(a + b) : 6x + 9 = 3(2x + 3).

## Formules utiles
Périmètre du carré : P = 4c ; aire du rectangle : A = L × l ; périmètre du cercle : P = 2πr.

## Tester une égalité
On remplace la lettre par une valeur et on calcule chaque membre séparément.""",
questions=[
(1, "3 × a s'écrit aussi :", "3a", "a3", "3 + a", "a³",
 "Le signe × est sous-entendu."),
(2, "Pour x = 4, 3x + 2 vaut :", "14", "34", "9", "20",
 "3 × 4 + 2."),
(2, "5x + 3x est égal à :", "8x", "8x²", "15x", "8",
 "On additionne les coefficients."),
(2, "3(x + 4) est égal à :", "3x + 12", "3x + 4", "x + 12", "3x + 7",
 "On distribue 3 sur x et sur 4."),
(2, "a × a s'écrit :", "a²", "2a", "aa²", "a + a",
 "a au carré."),
(3, "7a − 2 + a est égal à :", "8a − 2", "6a", "7a − 1", "8a + 2",
 "7a + a = 8a."),
(3, "5(2 − y) est égal à :", "10 − 5y", "10 − y", "7 − 5y", "10 + 5y",
 "5 × 2 − 5 × y."),
(3, "La forme factorisée de 6x + 9 est :", "3(2x + 3)", "6(x + 9)", "3(2x + 9)", "9(x + 6)",
 "3 est un facteur commun."),
(3, "Le périmètre d'un carré de côté c est :", "4c", "c²", "2c", "c + 4",
 "Quatre côtés égaux."),
(4, "Pour a = 2 et b = 3, l'expression 2a² − b vaut :", "5", "13", "1", "9",
 "2 × 4 − 3."),
]),

dict(
nom="Les triangles",
fiche="""## Somme des angles
Dans tout triangle, la somme des mesures des trois angles est égale à 180°.
Exemple : deux angles de 50° et 70° → le troisième mesure 180 − 50 − 70 = 60°.

## Triangles particuliers
• Isocèle : deux côtés égaux ; les deux angles à la base sont égaux.
• Équilatéral : trois côtés égaux ; trois angles de 60°.
• Rectangle : un angle droit ; les deux autres angles sont complémentaires.

## Inégalité triangulaire
Dans un triangle, chaque côté est plus petit que la somme des deux autres. On ne peut pas construire un triangle de côtés 2 cm, 3 cm et 7 cm (2 + 3 < 7).

## Droites remarquables
• Médiatrices (perpendiculaires aux côtés en leur milieu) : elles se coupent au centre du cercle circonscrit (cercle qui passe par les trois sommets).
• Hauteurs : issues d'un sommet, perpendiculaires à la droite qui porte le côté opposé ; elles se coupent en l'orthocentre.
• Médianes : joignent un sommet au milieu du côté opposé ; elles se coupent au centre de gravité.

## Aire
Aire du triangle = (base × hauteur) ÷ 2. Base 6 cm, hauteur 4 cm : A = 12 cm².
[[schema:triangle-hauteur|Hauteur et aire du triangle]]""",
questions=[
(1, "La somme des angles d'un triangle est égale à :", "180°", "360°", "90°", "270°",
 "Pour tout triangle."),
(2, "Un triangle a deux angles de 50° et 70°. Le troisième mesure :", "60°", "120°", "80°", "50°",
 "180 − 50 − 70."),
(2, "Chaque angle d'un triangle équilatéral mesure :", "60°", "90°", "45°", "30°",
 "180 ÷ 3."),
(2, "L'aire d'un triangle de base 6 cm et de hauteur 4 cm est :", "12 cm²", "24 cm²", "10 cm²", "20 cm²",
 "(6 × 4) ÷ 2."),
(2, "Dans un triangle rectangle, un angle aigu mesure 30°. L'autre angle aigu mesure :", "60°", "30°", "150°", "90°",
 "Ils sont complémentaires."),
(3, "Peut-on construire un triangle de côtés 2 cm, 3 cm et 7 cm ?", "non", "oui", "seulement s'il est rectangle", "seulement s'il est isocèle",
 "2 + 3 = 5 < 7 : inégalité triangulaire non respectée."),
(3, "Le centre du cercle circonscrit à un triangle est le point de concours :", "des médiatrices", "des hauteurs", "des médianes", "des bissectrices",
 "Il est à égale distance des trois sommets."),
(3, "Un triangle isocèle a un angle au sommet principal de 40°. Chaque angle à la base mesure :", "70°", "40°", "140°", "50°",
 "(180 − 40) ÷ 2."),
(3, "La droite issue d'un sommet et perpendiculaire au côté opposé s'appelle :", "la hauteur", "la médiane", "la médiatrice", "la bissectrice",
 "Les hauteurs se coupent en l'orthocentre."),
(4, "Le point de concours des médianes d'un triangle s'appelle :", "le centre de gravité", "l'orthocentre", "le centre du cercle circonscrit", "le sommet principal",
 "Les médianes joignent un sommet au milieu du côté opposé."),
]),

dict(
nom="Proportionnalité et pourcentages",
fiche="""## Tableau de proportionnalité
Deux grandeurs sont proportionnelles si l'on passe de l'une à l'autre en multipliant toujours par le même nombre (coefficient de proportionnalité).
Exemple : 1 kg de riz coûte 500 F. 3 kg coûtent 1 500 F, 5 kg coûtent 2 500 F.

## Calculer une quatrième proportionnelle
• Par le passage à l'unité : 4 cahiers coûtent 1 200 F → 1 cahier coûte 300 F → 7 cahiers coûtent 2 100 F.
• Par le produit en croix : a/b = c/d ⇔ a × d = b × c.

## Pourcentages
• Prendre t % d'une quantité : multiplier par t/100. 20 % de 15 000 F = 3 000 F.
• Une réduction de 10 % sur un article de 8 000 F : 800 F de réduction, prix final 7 200 F.
• Exprimer en pourcentage : 9 filles sur 30 élèves → 9/30 = 0,3 = 30 %.

## Échelles
Sur une carte à l'échelle 1/100 000, 1 cm représente 100 000 cm = 1 km.

## Vitesse moyenne
Distance = vitesse × durée. À 60 km/h, en 2 h on parcourt 120 km.""",
questions=[
(1, "1 kg de riz coûte 500 F. 3 kg coûtent :", "1 500 F", "503 F", "1 000 F", "2 000 F",
 "500 × 3."),
(2, "4 cahiers coûtent 1 200 F. 7 cahiers coûtent :", "2 100 F", "1 500 F", "2 800 F", "8 400 F",
 "Un cahier : 300 F."),
(2, "20 % de 15 000 F est égal à :", "3 000 F", "1 500 F", "300 F", "7 500 F",
 "15 000 × 20 / 100."),
(2, "Sur une carte au 1/100 000, 1 cm représente :", "1 km", "100 m", "10 km", "100 km",
 "100 000 cm = 1 km."),
(2, "À 60 km/h pendant 2 h, on parcourt :", "120 km", "30 km", "62 km", "240 km",
 "Distance = vitesse × durée."),
(3, "Un article de 8 000 F est soldé à −10 %. Son nouveau prix est :", "7 200 F", "7 990 F", "800 F", "8 800 F",
 "8 000 − 800."),
(3, "Dans une classe de 30 élèves, il y a 9 filles. Le pourcentage de filles est :", "30 %", "9 %", "27 %", "70 %",
 "9 / 30 = 0,3."),
(3, "Lequel de ces tableaux est proportionnel ?", "2 → 6 ; 5 → 15", "2 → 4 ; 5 → 8", "2 → 5 ; 5 → 8", "2 → 3 ; 5 → 6",
 "On multiplie toujours par 3."),
(3, "Si 3/x = 6/10, alors x vaut :", "5", "20", "18", "2",
 "Produit en croix : 6x = 30."),
(4, "Un prix passe de 2 000 F à 2 500 F. L'augmentation est de :", "25 %", "50 %", "20 %", "500 %",
 "500 / 2 000 = 0,25."),
]),

dict(
nom="Repérage dans le plan",
fiche="""## Le repère
Un repère du plan est formé de deux droites graduées perpendiculaires qui se coupent en O, l'origine :
• l'axe horizontal est l'axe des abscisses ;
• l'axe vertical est l'axe des ordonnées.

## Coordonnées d'un point
Chaque point est repéré par un couple (abscisse ; ordonnée), toujours dans cet ordre.
A(3 ; −2) : on avance de 3 vers la droite, puis on descend de 2.
• O a pour coordonnées (0 ; 0).
• Un point de l'axe des abscisses a une ordonnée nulle : B(4 ; 0).
• Un point de l'axe des ordonnées a une abscisse nulle : C(0 ; −1).

[[schema:repere-points|Lire les coordonnées d'un point]]
## Les quatre zones
• (+ ; +) en haut à droite ; (− ; +) en haut à gauche ; (− ; −) en bas à gauche ; (+ ; −) en bas à droite.

## Symétries et repère
• Symétrique de (x ; y) par rapport à O : (−x ; −y).
• Par rapport à l'axe des abscisses : (x ; −y).
• Par rapport à l'axe des ordonnées : (−x ; y).

## Milieu
Le milieu de [AB] a pour coordonnées la moyenne des abscisses et la moyenne des ordonnées : A(2 ; 4) et B(6 ; 0) → milieu (4 ; 2).""",
questions=[
(2, 'Sur le schéma, le point B a pour coordonnées :', '(4 ; 0)', '(0 ; 4)', '(4 ; 4)', '(3 ; −2)',
 "Il est sur l'axe des abscisses.", 'repere-points'),
(1, "Dans un couple de coordonnées, on écrit d'abord :", "l'abscisse", "l'ordonnée", "la plus grande valeur", "la distance à O",
 "(abscisse ; ordonnée)."),
(1, "Les coordonnées de l'origine O sont :", "(0 ; 0)", "(1 ; 1)", "(0 ; 1)", "(1 ; 0)",
 "Point d'intersection des axes."),
(2, "Le point B(4 ; 0) est situé :", "sur l'axe des abscisses", "sur l'axe des ordonnées", "à l'origine", "en bas à gauche",
 "Son ordonnée est nulle."),
(2, "Le point A(3 ; −2) est situé :", "en bas à droite", "en haut à droite", "en haut à gauche", "en bas à gauche",
 "Abscisse positive, ordonnée négative."),
(2, "Le point C(0 ; −1) est situé :", "sur l'axe des ordonnées", "sur l'axe des abscisses", "à l'origine", "en haut à droite",
 "Son abscisse est nulle."),
(3, "Le symétrique de (2 ; 5) par rapport à O est :", "(−2 ; −5)", "(2 ; −5)", "(−2 ; 5)", "(5 ; 2)",
 "On change les deux signes."),
(3, "Le symétrique de (3 ; 1) par rapport à l'axe des abscisses est :", "(3 ; −1)", "(−3 ; 1)", "(−3 ; −1)", "(1 ; 3)",
 "L'abscisse ne change pas."),
(3, "Le milieu de [AB] avec A(2 ; 4) et B(6 ; 0) est :", "(4 ; 2)", "(8 ; 4)", "(2 ; 4)", "(3 ; 3)",
 "Moyenne des abscisses et des ordonnées."),
(3, "Un point d'abscisse négative et d'ordonnée positive est :", "en haut à gauche", "en bas à droite", "en haut à droite", "en bas à gauche",
 "(− ; +)."),
(4, "M est le milieu de [AB] avec A(−1 ; 3) et M(2 ; 1). Les coordonnées de B sont :", "(5 ; −1)", "(0,5 ; 2)", "(3 ; −2)", "(1 ; 4)",
 "2 × 2 − (−1) = 5 ; 2 × 1 − 3 = −1."),
]),

dict(
nom="Statistique",
fiche="""## Vocabulaire
• Population : l'ensemble étudié (les élèves d'une classe).
• Caractère : ce que l'on observe (la note, la taille, le sport préféré). Il est quantitatif (un nombre) ou qualitatif (un mot).
• Effectif d'une valeur : nombre de fois où elle apparaît. Effectif total : nombre total d'individus.

## La fréquence
Fréquence = effectif de la valeur ÷ effectif total. On peut l'exprimer en pourcentage.
12 élèves sur 40 préfèrent le football : fréquence 12/40 = 0,3 = 30 %.
La somme des fréquences vaut 1 (100 %).

## La moyenne
Moyenne = somme des valeurs ÷ nombre de valeurs. Notes 8, 12, 10, 14 : (8 + 12 + 10 + 14) ÷ 4 = 11.
Avec un tableau d'effectifs : on multiplie chaque valeur par son effectif, on additionne, on divise par l'effectif total.

## Les graphiques
• Diagramme en bâtons : hauteur proportionnelle à l'effectif.
• Diagramme circulaire : angle proportionnel à l'effectif ; 360° pour l'effectif total. 30 % → 0,3 × 360 = 108°.
• Histogramme pour des valeurs regroupées en classes.
[[schema:diagramme-circulaire|Diagramme circulaire]]""",
questions=[
(3, 'Sur le diagramme, le secteur « Basket » représente 45 %. Son angle est :', '162°', '45°', '90°', '108°',
 '0,45 × 360 = 162°.', 'diagramme-circulaire'),
(1, "Le nombre de fois où une valeur apparaît s'appelle :", "l'effectif", "la fréquence", "la moyenne", "le caractère",
 "L'effectif total est le nombre d'individus."),
(2, "La moyenne de 8, 12, 10 et 14 est :", "11", "10", "12", "44",
 "44 ÷ 4."),
(2, "12 élèves sur 40 préfèrent le football. La fréquence est :", "30 %", "12 %", "40 %", "3 %",
 "12 / 40 = 0,3."),
(2, "La somme de toutes les fréquences est égale à :", "100 %", "50 %", "l'effectif total", "0",
 "Soit 1."),
(2, "Le « sport préféré » est un caractère :", "qualitatif", "quantitatif", "numérique", "continu",
 "Il s'exprime par un mot."),
(3, "Dans un diagramme circulaire, une fréquence de 30 % correspond à un angle de :", "108°", "30°", "120°", "90°",
 "0,3 × 360."),
(3, "Notes : 10 (3 fois) et 14 (1 fois). La moyenne est :", "11", "12", "24", "13",
 "(30 + 14) ÷ 4."),
(3, "Dans un diagramme en bâtons, la hauteur d'un bâton est proportionnelle :", "à l'effectif", "à la valeur", "au nombre de bâtons", "à 360°",
 "Plus l'effectif est grand, plus le bâton est haut."),
(3, "Sur 25 élèves, 5 viennent à pied. Le pourcentage est :", "20 %", "5 %", "25 %", "50 %",
 "5 / 25 = 0,2."),
(4, "La moyenne de 4 notes est 12. Trois notes sont 10, 11 et 13. La quatrième est :", "14", "12", "15", "10",
 "Total 48 ; 48 − 34."),
]),

dict(
nom="Prisme droit et cylindre",
fiche="""## Le prisme droit
• Deux bases superposables et parallèles (triangles, rectangles…).
• Des faces latérales rectangulaires, perpendiculaires aux bases.
• La hauteur est la distance entre les deux bases.
Le pavé droit et le cube sont des prismes droits particuliers.

## Le cylindre de révolution
Deux bases qui sont des disques de même rayon, parallèles ; une surface latérale qui, déroulée, donne un rectangle de longueur 2πr (périmètre du disque) et de largeur h.

## Aires latérales
• Prisme droit : périmètre de la base × hauteur.
• Cylindre : 2πr × h.
Aire totale = aire latérale + aires des deux bases.

## Volumes
V = aire de la base × hauteur.
• Prisme à base triangulaire (base 6 cm², hauteur 10 cm) : V = 60 cm³.
• Cylindre de rayon 2 cm et hauteur 5 cm : V = π × 2² × 5 = 20π ≈ 62,8 cm³.
1 dm³ = 1 L ; 1 m³ = 1 000 L.

[[schema:prisme-cylindre|Prisme droit et cylindre]]
## Patron
Le patron d'un prisme droit à base triangulaire : 2 triangles et 3 rectangles.""",
questions=[
(1, "Les faces latérales d'un prisme droit sont des :", "rectangles", "triangles", "disques", "cercles",
 "Elles sont perpendiculaires aux bases."),
(1, "Les bases d'un cylindre sont des :", "disques", "carrés", "triangles", "rectangles",
 "Deux disques de même rayon."),
(2, "Le volume d'un prisme droit est égal à :", "aire de la base × hauteur", "périmètre de la base × hauteur", "aire de la base ÷ 3", "base + hauteur",
 "Comme pour le cylindre."),
(2, "Un prisme a une base de 6 cm² et une hauteur de 10 cm. Son volume est :", "60 cm³", "16 cm³", "600 cm³", "20 cm³",
 "6 × 10."),
(2, "1 dm³ est égal à :", "1 L", "10 L", "100 L", "1 mL",
 "1 m³ = 1 000 L."),
(3, "Le volume d'un cylindre de rayon 2 cm et de hauteur 5 cm est :", "20π cm³", "10π cm³", "4π cm³", "50π cm³",
 "π × 4 × 5."),
(3, "Déroulée, la surface latérale d'un cylindre donne :", "un rectangle", "un disque", "un triangle", "un cercle",
 "De longueur 2πr et de largeur h."),
(3, "Le patron d'un prisme droit à base triangulaire comprend :", "2 triangles et 3 rectangles", "3 triangles et 2 rectangles", "6 rectangles", "4 triangles",
 "Deux bases et trois faces latérales."),
(3, "L'aire latérale d'un prisme droit dont la base a un périmètre de 12 cm et la hauteur 5 cm est :", "60 cm²", "17 cm²", "30 cm²", "120 cm²",
 "Périmètre × hauteur."),
(4, "Une citerne cylindrique a un volume de 2 m³. Elle contient :", "2 000 L", "200 L", "20 L", "20 000 L",
 "1 m³ = 1 000 L."),
]),

dict(
nom="Révision de l'année",
fiche="""## Nombres
• Relatifs : (−3) + (−4) = −7 ; 3 − (−5) = 8.
• Fractions : même dénominateur pour additionner ; produit : on multiplie les numérateurs entre eux et les dénominateurs entre eux.
• Proportionnalité, passage à l'unité, pourcentages (t/100), échelles.
• Expressions littérales : réduire, développer k(a + b) = ka + kb, factoriser.

## Géométrie
• Symétrie centrale : conserve longueurs et angles ; une droite devient une droite parallèle.
• Angles : complémentaires (90°), supplémentaires (180°), opposés par le sommet (égaux).
• Triangle : somme des angles 180° ; aire = b × h ÷ 2.
• Parallélogramme : diagonales qui se coupent en leur milieu ; aire = b × h.
• Repère : (abscisse ; ordonnée).
• Prisme droit et cylindre : V = aire de la base × hauteur.

## Statistique
Effectif, fréquence (effectif ÷ total), moyenne, diagramme circulaire (fréquence × 360°).""",
questions=[
(2, "(−5) + (+8) est égal à :", "3", "−3", "13", "−13",
 "8 − 5, signe de +8."),
(2, "Le supplémentaire d'un angle de 75° mesure :", "105°", "15°", "75°", "285°",
 "180 − 75."),
(2, "2(3x − 1) est égal à :", "6x − 2", "6x − 1", "5x − 2", "6x + 2",
 "On distribue 2."),
(3, "1/2 + 1/3 est égal à :", "5/6", "2/5", "1/6", "2/6",
 "3/6 + 2/6."),
(3, "Un triangle a deux angles de 45°. Il est :", "rectangle et isocèle", "équilatéral", "obtusangle", "quelconque",
 "Le troisième angle mesure 90°."),
(3, "15 % de 2 000 F est égal à :", "300 F", "150 F", "30 F", "1 700 F",
 "2 000 × 0,15."),
(3, "Le symétrique du point (−4 ; 1) par rapport à O est :", "(4 ; −1)", "(−4 ; −1)", "(4 ; 1)", "(1 ; −4)",
 "On change les deux signes."),
(3, "Un cube d'arête 3 cm a un volume de :", "27 cm³", "9 cm³", "18 cm³", "12 cm³",
 "3 × 3 × 3."),
(4, "Moyenne de la série : 6 (2 fois), 9 (1 fois), 12 (1 fois) :", "8,25", "9", "7,5", "11",
 "(6 × 2 + 9 + 12) ÷ 4 = 33 ÷ 4."),
(4, "Un parallélogramme a une base de 7 cm et une aire de 28 cm². Sa hauteur est :", "4 cm", "21 cm", "196 cm", "3,5 cm",
 "28 ÷ 7."),
]),
]
