NIVEAU, MATIERE = "6ème", "Physique-Chimie"

CHAPITRES = [
dict(
nom="Grandeurs physiques et unités",
fiche="""## Qu'est-ce qu'une grandeur physique ?
C'est une propriété que l'on peut mesurer et exprimer par un nombre suivi d'une unité : longueur, aire, volume, masse, durée, température.
« La table mesure 1,2 m » : la grandeur est la longueur, 1,2 est la valeur, m (mètre) est l'unité.

## Les unités du Système international (SI)
• Longueur : le mètre (m), mesurée avec une règle ou un mètre ruban.
• Masse : le kilogramme (kg), mesurée avec une balance.
• Durée : la seconde (s), mesurée avec un chronomètre.
• Température : le kelvin (K) ; dans la vie courante, le degré Celsius (°C) ; elle est mesurée avec un thermomètre.
Le mètre carré (m²), unité d'aire, et le mètre cube (m³), unité de volume, sont des unités dérivées du mètre.

## Préfixes
kilo (k) = 1 000 ; hecto (h) = 100 ; déca (da) = 10 ; déci (d) = 1/10 ; centi (c) = 1/100 ; milli (m) = 1/1 000.
1 km = 1 000 m ; 1 cm = 0,01 m ; 1 mg = 0,001 g.

## Bien mesurer
Choisir le bon instrument, le bon calibre, placer l'œil en face de la graduation, toujours écrire l'unité. Une mesure n'est jamais parfaite : on peut la répéter et faire la moyenne.""",
questions=[
(1, "L'unité de longueur du Système international est :", "le mètre", "le kilogramme", "la seconde", "le litre",
 "Symbole m."),
(1, "L'unité de masse du Système international est :", "le kilogramme", "le gramme", "le mètre", "le litre",
 "Symbole kg."),
(2, "La durée se mesure avec :", "un chronomètre", "une balance", "un thermomètre", "une règle",
 "L'unité SI est la seconde."),
(2, "Le préfixe « kilo » signifie :", "1 000", "100", "10", "1/1 000",
 "1 km = 1 000 m."),
(2, "Le préfixe « milli » signifie :", "un millième (1/1 000)", "mille", "un centième", "un million",
 "1 mm = 0,001 m."),
(2, "Dans « la table mesure 1,2 m », 1,2 est :", "la valeur de la mesure", "l'unité", "l'instrument", "la grandeur",
 "m est l'unité, la longueur est la grandeur."),
(1, "La température se mesure avec :", "un thermomètre", "un baromètre", "un chronomètre", "une éprouvette",
 "En degrés Celsius dans la vie courante."),
(3, "Laquelle n'est PAS une grandeur physique ?", "la couleur préférée d'un élève", "la masse d'un sac", "la longueur d'une table", "la durée d'un cours",
 "Elle ne se mesure pas avec un nombre et une unité."),
(3, "1 cm est égal à :", "0,01 m", "0,1 m", "100 m", "10 m",
 "Centi = 1/100."),
(4, "Pour obtenir une mesure plus fiable, on peut :", "répéter la mesure et faire la moyenne", "changer d'unité au hasard", "ne pas écrire l'unité", "regarder la graduation de côté",
 "Cela réduit l'effet des erreurs."),
]),

dict(
nom="Les longueurs et leur mesure",
fiche="""## Les unités de longueur
km — hm — dam — m — dm — cm — mm : chaque unité vaut 10 fois l'unité suivante.
1 m = 10 dm = 100 cm = 1 000 mm ; 1 km = 1 000 m.

## Les instruments
• Règle graduée et double décimètre (petits objets).
• Mètre ruban ou décamètre (une salle, un terrain).
• Pied à coulisse (diamètre d'un fil, d'un crayon, au dixième de millimètre près).
• Pour les grandes distances : le compteur kilométrique, la carte (avec son échelle).

## Bien utiliser une règle
Placer le zéro de la règle à l'une des extrémités de l'objet, l'œil perpendiculaire à la règle, lire la graduation à l'autre extrémité.
Si le zéro est abîmé, on part de la graduation 1 cm et on retranche 1 cm.

[[schema:regle-mesure|Mesurer avec une règle]]
## Mesurer une longueur courbe
On place un fil le long de la courbe, puis on mesure le fil tendu sur une règle.

## Mesurer une très petite épaisseur
On mesure l'épaisseur de 100 feuilles empilées (par exemple 1 cm), puis on divise par 100 : une feuille fait 0,1 mm.""",
questions=[
(1, "1 m est égal à :", "100 cm", "10 cm", "1 000 cm", "1 cm",
 "1 m = 100 cm = 1 000 mm."),
(1, "Pour mesurer la longueur de la cour de l'école, on utilise :", "un mètre ruban ou un décamètre", "un pied à coulisse", "une balance", "un thermomètre",
 "La règle serait trop courte."),
(2, "2,5 km est égal à :", "2 500 m", "250 m", "25 m", "25 000 m",
 "1 km = 1 000 m."),
(2, "35 mm est égal à :", "3,5 cm", "35 cm", "0,35 cm", "350 cm",
 "1 cm = 10 mm."),
(2, "Pour mesurer précisément le diamètre d'un crayon, on utilise :", "un pied à coulisse", "un décamètre", "un compteur kilométrique", "un chronomètre",
 "Il mesure au dixième de millimètre."),
(3, "Le zéro d'une règle est abîmé. On place l'objet à partir de 1 cm et on lit 8,5 cm. L'objet mesure :", "7,5 cm", "8,5 cm", "9,5 cm", "1 cm",
 "8,5 − 1."),
(3, "Pour mesurer la longueur d'un chemin courbe sur une carte, on peut :", "utiliser un fil puis le mesurer tendu", "utiliser une balance", "mesurer seulement la ligne droite entre les extrémités", "compter les couleurs",
 "Le fil épouse la courbe."),
(3, "100 feuilles empilées mesurent 1 cm d'épaisseur. Une feuille mesure :", "0,1 mm", "1 mm", "0,01 mm", "1 cm",
 "10 mm ÷ 100."),
(3, "Pour bien lire une règle, l'œil doit être :", "perpendiculaire à la règle, en face de la graduation", "très loin de la règle", "sur le côté", "fermé",
 "Pour éviter l'erreur de parallaxe."),
(4, "Un élève fait 10 pas qui mesurent au total 6 m. Un pas mesure :", "60 cm", "6 cm", "0,6 cm", "1,6 m",
 "6 m ÷ 10 = 0,6 m."),
]),

dict(
nom="Les aires et leur mesure",
fiche="""## L'aire
L'aire mesure l'étendue d'une surface. Unité SI : le mètre carré (m²), aire d'un carré de 1 m de côté.

## Les unités
km² — hm² — dam² — m² — dm² — cm² — mm² : chaque unité vaut 100 fois l'unité suivante.
1 m² = 100 dm² = 10 000 cm².
Unités agraires : 1 hectare (ha) = 1 hm² = 10 000 m² ; 1 are (a) = 100 m². On les utilise pour les champs et les plantations.

## Calculer une aire
• Rectangle : longueur × largeur. Une salle de 8 m sur 6 m : 48 m².
• Carré : côté × côté. 5 cm de côté : 25 cm².
• Surface irrégulière : on la décompose en rectangles, ou on compte les carreaux d'un quadrillage.

## Attention
Les deux longueurs doivent être dans la même unité avant de multiplier : 2 m × 50 cm = 2 m × 0,5 m = 1 m².
Aire et périmètre sont différents : le périmètre (en m) est la longueur du contour.""",
questions=[
(1, "L'unité SI d'aire est :", "le mètre carré", "le mètre", "le litre", "le mètre cube",
 "Symbole m²."),
(2, "L'aire d'une salle rectangulaire de 8 m sur 6 m est :", "48 m²", "28 m²", "14 m²", "48 m",
 "Longueur × largeur."),
(2, "L'aire d'un carré de 5 cm de côté est :", "25 cm²", "20 cm²", "10 cm²", "25 cm",
 "5 × 5."),
(2, "1 m² est égal à :", "10 000 cm²", "100 cm²", "1 000 cm²", "10 cm²",
 "1 m = 100 cm et 100 × 100 = 10 000."),
(2, "1 hectare est égal à :", "10 000 m²", "100 m²", "1 000 m²", "1 000 000 m²",
 "1 ha = 1 hm²."),
(3, "Un champ de cacao mesure 3 ha. Son aire est :", "30 000 m²", "300 m²", "3 000 m²", "300 000 m²",
 "3 × 10 000."),
(3, "Un rectangle mesure 2 m sur 50 cm. Son aire est :", "1 m²", "100 m²", "10 m²", "0,1 m²",
 "2 m × 0,5 m."),
(3, "Le périmètre d'un rectangle de 8 m sur 6 m est :", "28 m", "48 m", "14 m", "48 m²",
 "2 × (8 + 6). Ce n'est pas l'aire."),
(3, "1 are est égal à :", "100 m²", "10 m²", "1 000 m²", "10 000 m²",
 "1 a = 1 dam²."),
(4, "Un carré a une aire de 49 m². Son côté mesure :", "7 m", "49 m", "24,5 m", "12,25 m",
 "7 × 7 = 49."),
]),

dict(
nom="Les volumes et leur mesure",
fiche="""## Le volume
Le volume mesure la place occupée par un objet. Unité SI : le mètre cube (m³), volume d'un cube de 1 m d'arête.

## Les unités
m³ — dm³ — cm³ — mm³ : chaque unité vaut 1 000 fois l'unité suivante. 1 m³ = 1 000 dm³ ; 1 dm³ = 1 000 cm³.
Pour les liquides, on utilise le litre : 1 L = 1 dm³ ; 1 mL = 1 cm³ ; 1 m³ = 1 000 L.
L ; dL ; cL ; mL : 1 L = 10 dL = 100 cL = 1 000 mL.

## Mesurer le volume d'un liquide
Avec une éprouvette graduée (ou un verre doseur) posée sur une table horizontale. La surface du liquide forme un ménisque : on lit au bas du ménisque, l'œil à sa hauteur.

[[schema:eprouvette-menisque|Lecture d'une éprouvette graduée]]
## Volume d'un solide
• Forme régulière (pavé) : longueur × largeur × hauteur. 10 cm × 5 cm × 2 cm = 100 cm³.
• Forme quelconque : on le plonge dans l'eau d'une éprouvette ; le volume du solide est la différence des deux niveaux.

## Exemples
Une bouteille d'eau minérale : 1,5 L ; une canette : 33 cL ; un seau : environ 10 L.""",
questions=[
(2, "D'après le schéma, le volume de liquide dans l'éprouvette est :", '60 mL', '75 mL', '50 mL', '100 mL',
 'On lit au bas du ménisque.', 'eprouvette-menisque'),
(1, "L'unité SI de volume est :", "le mètre cube", "le mètre carré", "le kilogramme", "le mètre",
 "Symbole m³."),
(1, "Le volume d'un liquide se mesure avec :", "une éprouvette graduée", "une règle", "une balance", "un chronomètre",
 "On lit au bas du ménisque."),
(2, "1 L est égal à :", "1 000 mL", "100 mL", "10 mL", "1 mL",
 "Et 1 L = 1 dm³."),
(2, "1 mL est égal à :", "1 cm³", "1 dm³", "1 m³", "10 cm³",
 "1 L = 1 dm³ = 1 000 cm³."),
(2, "Une canette de 33 cL contient :", "330 mL", "33 mL", "3,3 mL", "3 300 mL",
 "1 cL = 10 mL."),
(3, "Le volume d'un pavé de 10 cm × 5 cm × 2 cm est :", "100 cm³", "17 cm³", "50 cm³", "100 cm²",
 "Longueur × largeur × hauteur."),
(3, "L'eau d'une éprouvette passe de 40 mL à 55 mL quand on y plonge un caillou. Le volume du caillou est :", "15 cm³", "55 cm³", "95 cm³", "40 cm³",
 "55 − 40 = 15 mL = 15 cm³."),
(3, "1 m³ d'eau correspond à :", "1 000 L", "100 L", "10 L", "1 L",
 "1 m³ = 1 000 dm³."),
(3, "Pour lire le volume dans une éprouvette, l'œil doit être :", "à la hauteur du bas du ménisque", "au-dessus de l'éprouvette", "sous la table", "n'importe où",
 "Sinon la lecture est fausse."),
(4, "Une citerne de 2 m³ remplit combien de seaux de 10 L ?", "200", "20", "2 000", "2",
 "2 000 L ÷ 10 L."),
]),

dict(
nom="La masse et sa mesure",
fiche="""## La masse
La masse mesure la quantité de matière d'un objet. Unité SI : le kilogramme (kg).
t (tonne) — kg — hg — dag — g — dg — cg — mg : 1 t = 1 000 kg ; 1 kg = 1 000 g ; 1 g = 1 000 mg.

## Les balances
• Balance électronique : on pose l'objet, on lit la masse. La touche « tare » remet l'affichage à zéro avec le récipient vide.
• Balance de Roberval (à plateaux) : l'équilibre est atteint quand les masses marquées compensent l'objet.
• Pèse-personne, bascule du marché, peson.

[[schema:balance-roberval|Balance de Roberval à l'équilibre]]
## Mesurer la masse d'un liquide
On pèse le récipient vide (ou on fait la tare), puis le récipient plein ; la masse du liquide est la différence.
Récipient vide 150 g, plein 400 g → 250 g de liquide.

## La masse se conserve
Quand on découpe une feuille ou qu'on dissout du sucre, la masse totale ne change pas.

## Ordres de grandeur
Un sac de riz : 25 kg ou 50 kg ; un cahier : environ 100 g ; un élève de 6ème : environ 35 kg ; un camion : plusieurs tonnes.""",
questions=[
(3, "Sur le schéma, la balance est à l'équilibre. La masse de l'objet est :", '270 g', '200 g', '250 g', '70 g',
 '200 + 50 + 20 = 270 g.', 'balance-roberval'),
(1, "La masse se mesure avec :", "une balance", "une règle", "une éprouvette", "un thermomètre",
 "L'unité SI est le kilogramme."),
(1, "1 kg est égal à :", "1 000 g", "100 g", "10 g", "10 000 g",
 "Kilo = 1 000."),
(2, "1 t est égale à :", "1 000 kg", "100 kg", "10 000 kg", "10 kg",
 "La tonne sert pour les camions et les récoltes."),
(2, "500 g est égal à :", "0,5 kg", "5 kg", "50 kg", "0,05 kg",
 "500 ÷ 1 000."),
(2, "La touche « tare » d'une balance électronique sert à :", "remettre l'affichage à zéro avec le récipient", "augmenter la masse", "mesurer la température", "allumer l'écran seulement",
 "On pèse ensuite seulement le contenu."),
(3, "Un récipient vide a une masse de 150 g ; plein de jus, sa masse est de 400 g. La masse du jus est :", "250 g", "550 g", "400 g", "150 g",
 "400 − 150."),
(3, "On découpe une feuille de 5 g en petits morceaux. La masse de tous les morceaux est :", "5 g", "moins de 5 g", "plus de 5 g", "0 g",
 "La masse se conserve."),
(3, "La masse d'un cahier est d'environ :", "100 g", "100 kg", "1 t", "1 mg",
 "C'est un ordre de grandeur."),
(3, "3,2 kg est égal à :", "3 200 g", "320 g", "32 g", "32 000 g",
 "3,2 × 1 000."),
(4, "Sur une balance de Roberval, l'objet est équilibré par des masses de 200 g, 50 g et 20 g. Sa masse est :", "270 g", "250 g", "220 g", "2 700 g",
 "200 + 50 + 20."),
]),

dict(
nom="Le temps et sa mesure",
fiche="""## Instant et durée
• Un instant (une date, une heure) repère un moment : « le cours commence à 7 h 30 ».
• Une durée est l'intervalle entre deux instants : « le cours dure 55 min ».
Durée = instant final − instant initial.

## Les unités
L'unité SI est la seconde (s). 1 min = 60 s ; 1 h = 60 min = 3 600 s ; 1 jour = 24 h.
Attention : le système n'est pas décimal. 1,5 h = 1 h 30 min (et non 1 h 50 min).

## Les instruments
Montre, horloge, chronomètre (au centième de seconde), sablier, clepsydre et cadran solaire autrefois.

## Les phénomènes réguliers
• Le jour et la nuit : rotation de la Terre sur elle-même en environ 24 h.
• L'année : révolution de la Terre autour du Soleil en environ 365 jours et 6 heures (d'où une année bissextile de 366 jours tous les 4 ans).
• Le pendule : il oscille régulièrement ; sa période dépend de sa longueur.

## Exemple
Départ d'Abidjan à 6 h 45, arrivée à Yamoussoukro à 9 h 15 : durée 2 h 30 min.""",
questions=[
(1, "L'unité SI de durée est :", "la seconde", "la minute", "l'heure", "le jour",
 "Symbole s."),
(1, "1 heure est égale à :", "60 minutes", "100 minutes", "30 minutes", "24 minutes",
 "Et 1 min = 60 s."),
(2, "1 h est égale à :", "3 600 s", "360 s", "60 s", "1 000 s",
 "60 × 60."),
(2, "1,5 h est égale à :", "1 h 30 min", "1 h 50 min", "1 h 05 min", "1 h 15 min",
 "0,5 h = 30 min."),
(2, "Pour mesurer la durée d'une course de 100 m, on utilise :", "un chronomètre", "un calendrier", "un cadran solaire", "une balance",
 "Au centième de seconde."),
(3, "Un car part d'Abidjan à 6 h 45 et arrive à Yamoussoukro à 9 h 15. Le trajet a duré :", "2 h 30 min", "3 h 30 min", "2 h 70 min", "3 h",
 "De 6 h 45 à 9 h 15."),
(3, "« Le cours commence à 7 h 30 » indique :", "un instant", "une durée", "une masse", "une vitesse",
 "C'est un moment précis."),
(3, "La Terre tourne sur elle-même en environ :", "24 heures", "365 jours", "1 heure", "1 mois",
 "C'est ce qui produit le jour et la nuit."),
(3, "Une année bissextile compte :", "366 jours", "365 jours", "360 jours", "400 jours",
 "Elle revient tous les 4 ans."),
(4, "Un film de 135 minutes dure :", "2 h 15 min", "1 h 35 min", "2 h 35 min", "1 h 15 min",
 "135 = 120 + 15."),
]),

dict(
nom="La température et le thermomètre",
fiche="""## Chaud et froid
Le toucher ne suffit pas pour connaître la température : une même eau tiède paraît chaude à une main sortant d'eau froide, et froide à une main sortant d'eau chaude. Il faut un thermomètre.

## L'unité
Dans la vie courante, on utilise le degré Celsius (°C). Repères : la glace fond à 0 °C ; l'eau pure bout à 100 °C (sous la pression normale).
Températures négatives : en dessous de 0 °C (−5 °C).
L'unité SI est le kelvin (K) : 0 °C correspond à environ 273 K.

## Les thermomètres
• Thermomètre à liquide (alcool coloré) : le liquide se dilate quand il chauffe et monte dans le tube.
• Thermomètre électronique (affichage numérique).
• Thermomètre médical : la température normale du corps humain est d'environ 37 °C ; au-dessus de 38 °C, on a de la fièvre.

[[schema:thermometre|Lecture d'un thermomètre]]
## Bien mesurer
Plonger le réservoir dans le liquide sans toucher le fond ni les parois, attendre la stabilisation, lire l'œil en face du niveau.

## Repères
Abidjan : environ 25 à 32 °C toute l'année. L'harmattan, dans le nord, provoque des nuits plus fraîches.""",
questions=[
(2, 'Le thermomètre du schéma indique :', '37 °C', '40 °C', '30 °C', '50 °C',
 'On lit en face du haut de la colonne.', 'thermometre'),
(1, "La température se mesure avec :", "un thermomètre", "une balance", "un baromètre", "une règle",
 "Le toucher ne suffit pas."),
(1, "La glace fond à :", "0 °C", "100 °C", "37 °C", "−10 °C",
 "C'est un repère de l'échelle Celsius."),
(2, "L'eau pure bout à :", "100 °C", "0 °C", "37 °C", "50 °C",
 "Sous la pression atmosphérique normale."),
(2, "La température normale du corps humain est d'environ :", "37 °C", "30 °C", "40 °C", "25 °C",
 "Au-dessus de 38 °C, c'est la fièvre."),
(2, "Dans un thermomètre à alcool, le liquide monte quand il chauffe car :", "il se dilate", "il gèle", "il s'évapore entièrement", "il devient plus lourd",
 "Son volume augmente."),
(3, "Pourquoi le toucher ne suffit-il pas pour connaître une température ?", "la sensation dépend de ce qu'on a touché avant", "la peau ne sent rien", "l'eau n'a pas de température", "les mains sont toujours à 0 °C",
 "La sensation est trompeuse."),
(3, "Pour mesurer la température d'un liquide, le réservoir du thermomètre doit :", "être plongé sans toucher le fond ni les parois", "toucher le fond du récipient", "rester hors du liquide", "être tenu dans la main",
 "Sinon on mesure la température du récipient."),
(3, "Une température de −5 °C est :", "inférieure à 0 °C", "supérieure à 0 °C", "égale à 5 °C", "impossible",
 "C'est une température négative."),
(3, "L'unité de température du Système international est :", "le kelvin", "le degré Celsius", "le degré Fahrenheit", "le joule",
 "Le degré Celsius est utilisé dans la vie courante."),
(4, "Le matin il fait 24 °C, l'après-midi 31 °C. La température a augmenté de :", "7 °C", "55 °C", "31 °C", "5 °C",
 "31 − 24."),
]),

dict(
nom="Révision de l'année",
fiche="""## Grandeurs et unités SI
Longueur : mètre (m), règle ; aire : m² ; volume : m³ (1 L = 1 dm³) ; masse : kilogramme (kg), balance ; durée : seconde (s), chronomètre ; température : kelvin (K), en pratique degré Celsius, thermomètre.

## Conversions
• Longueurs : ×10 d'une unité à la suivante. 1 km = 1 000 m ; 1 m = 100 cm.
• Aires : ×100. 1 m² = 10 000 cm² ; 1 ha = 10 000 m².
• Volumes : ×1 000. 1 m³ = 1 000 L ; 1 L = 1 000 mL = 1 000 cm³.
• Masses : 1 t = 1 000 kg ; 1 kg = 1 000 g.
• Durées : 1 h = 60 min = 3 600 s (pas décimal).

## Méthodes
Lecture au bas du ménisque ; tare de la balance ; volume d'un solide par déplacement d'eau ; durée = instant final − instant initial ; repères 0 °C, 100 °C, 37 °C.""",
questions=[
(2, "4,2 m est égal à :", "420 cm", "42 cm", "4 200 cm", "0,42 cm",
 "1 m = 100 cm."),
(2, "2 L est égal à :", "2 000 mL", "200 mL", "20 mL", "20 000 mL",
 "1 L = 1 000 mL."),
(2, "L'instrument qui mesure la masse est :", "la balance", "l'éprouvette", "le chronomètre", "le thermomètre",
 "En kilogrammes."),
(3, "L'aire d'un terrain de 20 m sur 15 m est :", "300 m²", "70 m²", "35 m²", "300 m",
 "20 × 15."),
(3, "L'eau d'une éprouvette passe de 60 mL à 72 mL avec un objet. Le volume de l'objet est :", "12 cm³", "72 cm³", "132 cm³", "60 cm³",
 "72 − 60."),
(3, "Un match commence à 15 h 30 et se termine à 17 h 15. Il a duré :", "1 h 45 min", "2 h 15 min", "1 h 85 min", "2 h 45 min",
 "De 15 h 30 à 17 h 15."),
(3, "Un élève a 39 °C de température. Il :", "a de la fièvre", "a une température normale", "a trop froid", "n'a rien",
 "Au-dessus de 38 °C."),
(3, "2 500 kg est égal à :", "2,5 t", "25 t", "0,25 t", "250 t",
 "1 t = 1 000 kg."),
(4, "Une boîte en forme de pavé mesure 20 cm × 10 cm × 5 cm. Elle peut contenir :", "1 L", "10 L", "100 mL", "35 L",
 "1 000 cm³ = 1 dm³ = 1 L."),
(4, "Un champ de 2,5 ha a une aire de :", "25 000 m²", "2 500 m²", "250 m²", "250 000 m²",
 "2,5 × 10 000."),
]),
]
