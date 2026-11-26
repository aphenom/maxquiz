NIVEAU, MATIERE = "4ème", "Physique-Chimie"

CHAPITRES = [
dict(
nom="Le circuit électrique",
fiche="""## Les éléments d'un circuit
• Un générateur (pile, batterie, prise de courant) fournit le courant.
• Des récepteurs (lampe, moteur, sonnerie, DEL) l'utilisent.
• Des fils de connexion et un interrupteur relient le tout.
Le courant ne circule que si le circuit est fermé (une boucle sans coupure). Interrupteur ouvert : circuit ouvert, la lampe s'éteint.

## Conducteurs et isolants
• Conducteurs : laissent passer le courant (métaux : cuivre, fer, aluminium ; graphite ; eau salée ; corps humain).
• Isolants : ne le laissent pas passer (plastique, verre, caoutchouc, bois sec, air sec).
Les fils électriques ont un cœur en cuivre (conducteur) entouré de plastique (isolant).

## Le schéma
On représente chaque dipôle par un symbole normalisé, les fils par des traits droits.
Pile : un grand trait (borne +) et un petit trait épais (borne −).

## Le sens du courant
Par convention, le courant sort par la borne + du générateur et revient par la borne −.
La diode ne laisse passer le courant que dans un sens (sens passant) ; une DEL est une diode qui éclaire.""",
questions=[
(1, "Un circuit dans lequel le courant circule est :", "fermé", "ouvert", "coupé", "isolé",
 "Il forme une boucle sans interruption."),
(1, "Lequel de ces matériaux est un conducteur ?", "le cuivre", "le plastique", "le verre", "le caoutchouc",
 "Les métaux sont conducteurs."),
(2, "Lequel de ces matériaux est un isolant ?", "le verre", "le fer", "l'aluminium", "le graphite",
 "Le verre ne laisse pas passer le courant."),
(2, "Par convention, le courant sort du générateur par :", "la borne +", "la borne −", "les deux bornes", "l'interrupteur",
 "Il revient par la borne −."),
(2, "Dans un circuit, une lampe et un moteur sont des :", "récepteurs", "générateurs", "isolants", "interrupteurs",
 "Ils utilisent le courant."),
(2, "Quand on ouvre l'interrupteur, la lampe :", "s'éteint", "brille plus fort", "brille moins fort", "reste allumée",
 "Le circuit est ouvert."),
(3, "Une diode branchée dans le mauvais sens :", "empêche le courant de passer", "brille plus fort", "fait doubler le courant", "n'a aucun effet",
 "Elle ne laisse passer le courant que dans un sens."),
(3, "Le fil électrique d'une rallonge est entouré de plastique pour :", "isoler et protéger des chocs électriques", "conduire plus de courant", "le rendre plus lourd", "le colorer seulement",
 "Le cuivre conduit, le plastique isole."),
(3, "Une DEL est :", "une diode qui émet de la lumière", "une pile", "un isolant", "un moteur",
 "Diode électroluminescente."),
(4, "Dans le schéma d'une pile, la borne + est représentée par :", "le grand trait fin", "le petit trait épais", "un cercle", "une flèche",
 "Le petit trait épais est la borne −."),
]),

dict(
nom="Circuits en série et en dérivation",
fiche="""## Circuit en série
Tous les dipôles forment une seule boucle.
• Si une lampe grille, toutes les autres s'éteignent.
• Plus on ajoute de lampes, moins elles brillent.

## Circuit en dérivation (parallèle)
Le circuit comporte plusieurs boucles ; les points où les fils se séparent s'appellent des nœuds.
• Chaque branche fonctionne indépendamment : si une lampe grille, les autres restent allumées.
• Les appareils de la maison sont branchés en dérivation.

## Le court-circuit
Relier les deux bornes d'un dipôle par un fil (presque sans résistance) : le courant passe par le fil et non plus par le dipôle, qui s'éteint.
Court-circuiter le générateur est dangereux : le courant devient très intense, les fils chauffent et peuvent provoquer un incendie.

## Les dangers de l'électricité
• Le courant du secteur (220 V en Côte d'Ivoire) peut électrocuter : ne jamais toucher un fil dénudé, ni manipuler un appareil avec les mains mouillées.
• Ne pas surcharger une multiprise.
• Le fusible et le disjoncteur coupent le courant en cas de surintensité.""",
questions=[
(1, "Dans un circuit en série, si une lampe grille :", "toutes les lampes s'éteignent", "les autres brillent plus fort", "rien ne change", "seule cette lampe s'éteint",
 "Il n'y a qu'une seule boucle."),
(2, "Les appareils électriques d'une maison sont branchés :", "en dérivation", "en série", "en court-circuit", "sans fil",
 "Chacun fonctionne indépendamment."),
(2, "Les points où les fils se séparent dans un circuit en dérivation s'appellent :", "des nœuds", "des bornes", "des boucles", "des pôles",
 "Le courant s'y partage."),
(2, "Quand on ajoute des lampes en série, elles brillent :", "moins fort", "plus fort", "de la même façon", "en clignotant",
 "La tension se partage entre elles."),
(2, "La tension du secteur en Côte d'Ivoire est d'environ :", "220 V", "12 V", "1,5 V", "1 000 V",
 "C'est la tension des prises de la maison."),
(3, "On relie les deux bornes d'une lampe par un fil. La lampe :", "s'éteint car elle est court-circuitée", "brille plus fort", "explose", "ne change pas",
 "Le courant passe par le fil."),
(3, "Court-circuiter une pile est dangereux car :", "le courant devient très intense et les fils chauffent", "la pile se recharge", "le courant s'arrête", "la tension augmente",
 "Risque d'incendie."),
(3, "En dérivation, si une lampe grille, les autres :", "restent allumées", "s'éteignent toutes", "brillent moins", "clignotent",
 "Chaque branche est indépendante."),
(3, "Le rôle d'un fusible est de :", "couper le courant en cas de surintensité", "augmenter la tension", "allumer les lampes", "produire du courant",
 "Il protège l'installation."),
(4, "Pourquoi ne faut-il pas toucher un appareil électrique avec les mains mouillées ?", "l'eau rend le corps meilleur conducteur", "l'eau isole le courant", "l'appareil s'arrête", "c'est sans danger",
 "Le risque d'électrocution augmente."),
]),

dict(
nom="L'intensité du courant",
fiche="""## Définition et unité
L'intensité mesure le « débit » du courant électrique. Symbole I, unité l'ampère (A). 1 A = 1 000 mA.

## La mesure
• Appareil : l'ampèremètre (ou un multimètre en position A ou mA).
• Il se branche EN SÉRIE, le courant entrant par la borne A (ou mA) et sortant par la borne COM.
• Commencer par le plus grand calibre, puis descendre pour plus de précision.

## Les lois
• En série : l'intensité est la même en tout point du circuit (I = I₁ = I₂).
• En dérivation (loi des nœuds) : l'intensité dans la branche principale est égale à la somme des intensités dans les branches dérivées (I = I₁ + I₂).

## Exemples
Deux lampes en dérivation parcourues par 0,2 A et 0,3 A : la branche principale reçoit 0,5 A.
Une lampe en série dans un circuit où passe 150 mA : elle est traversée par 150 mA, comme le moteur placé à côté.

## Ordres de grandeur
Lampe de poche : quelques centaines de mA. Fer à repasser : environ 5 A.""",
questions=[
(1, "L'unité de l'intensité du courant est :", "l'ampère", "le volt", "l'ohm", "le watt",
 "Symbole A."),
(1, "L'intensité se mesure avec :", "un ampèremètre", "un voltmètre", "un thermomètre", "un ohmmètre",
 "Ou un multimètre réglé sur A."),
(2, "L'ampèremètre se branche :", "en série", "en dérivation", "aux bornes du générateur seulement", "n'importe comment",
 "Le courant doit le traverser."),
(2, "0,25 A est égal à :", "250 mA", "25 mA", "2,5 mA", "2 500 mA",
 "1 A = 1 000 mA."),
(2, "Dans un circuit en série, l'intensité :", "est la même en tout point", "diminue après chaque lampe", "augmente après chaque lampe", "est nulle",
 "Loi de l'unicité de l'intensité."),
(3, "Deux lampes en dérivation sont traversées par 0,2 A et 0,3 A. La branche principale est traversée par :", "0,5 A", "0,1 A", "0,06 A", "0,3 A",
 "Loi des nœuds : I = I₁ + I₂."),
(3, "On commence une mesure au multimètre par :", "le plus grand calibre", "le plus petit calibre", "n'importe quel calibre", "la position ohm",
 "Pour ne pas abîmer l'appareil."),
(3, "Dans la branche principale passe 0,8 A ; une branche dérivée reçoit 0,5 A. L'autre branche reçoit :", "0,3 A", "1,3 A", "0,5 A", "0,8 A",
 "0,8 − 0,5."),
(4, "Avec un multimètre en ampèremètre, le courant entre par la borne :", "A (ou mA)", "COM", "V", "Ω",
 "Il ressort par COM."),
(4, "Un moteur et une lampe sont en série ; la lampe est traversée par 150 mA. Le moteur est traversé par :", "150 mA", "75 mA", "300 mA", "0 mA",
 "Même intensité partout en série."),
]),

dict(
nom="La tension électrique",
fiche="""## Définition et unité
La tension (U) est ce qui « pousse » le courant ; elle existe entre deux points. Unité : le volt (V). 1 kV = 1 000 V.

## La mesure
• Appareil : le voltmètre (ou multimètre en position V).
• Il se branche EN DÉRIVATION, aux bornes du dipôle (borne V du côté +, borne COM du côté −).
• Une pile neuve de 4,5 V affiche environ 4,5 V même hors circuit.

## Les lois
• En dérivation : la tension est la même aux bornes de toutes les branches (U = U₁ = U₂).
• En série : la tension du générateur est égale à la somme des tensions aux bornes des récepteurs (U = U₁ + U₂).
• La tension aux bornes d'un fil de connexion (ou d'un interrupteur fermé) est nulle ; aux bornes d'un interrupteur ouvert, elle est égale à celle du générateur.

## Adapter
Un appareil fonctionne normalement sous sa tension nominale (inscrite dessus). Sous-tension : il fonctionne mal ; surtension : il risque d'être détruit.

## Exemple
Pile de 6 V, deux lampes en série : si l'une a 2,5 V à ses bornes, l'autre a 3,5 V.""",
questions=[
(1, "L'unité de la tension est :", "le volt", "l'ampère", "l'ohm", "le joule",
 "Symbole V."),
(1, "La tension se mesure avec :", "un voltmètre", "un ampèremètre", "une balance", "un chronomètre",
 "Ou un multimètre réglé sur V."),
(2, "Le voltmètre se branche :", "en dérivation, aux bornes du dipôle", "en série", "à la place du générateur", "sur un seul fil",
 "La tension existe entre deux points."),
(2, "En dérivation, la tension aux bornes des branches est :", "la même", "partagée", "nulle", "doublée",
 "U = U₁ = U₂."),
(2, "La tension aux bornes d'un fil de connexion est :", "nulle", "égale à celle de la pile", "très grande", "négative",
 "Pratiquement 0 V."),
(3, "Pile de 6 V, deux lampes en série ; l'une a 2,5 V à ses bornes. L'autre a :", "3,5 V", "6 V", "2,5 V", "8,5 V",
 "Loi d'additivité : 6 − 2,5."),
(3, "La tension aux bornes d'un interrupteur ouvert dans un circuit en série est :", "égale à celle du générateur", "nulle", "la moitié", "impossible à mesurer",
 "Aucun courant ne passe dans les récepteurs."),
(3, "Une lampe prévue pour 6 V branchée sur 12 V :", "risque d'être détruite (surtension)", "brille faiblement", "s'éteint", "fonctionne normalement",
 "Il faut respecter la tension nominale."),
(3, "La tension inscrite sur un appareil s'appelle :", "la tension nominale", "la tension maximale", "la tension minimale", "la tension nulle",
 "C'est sa tension de fonctionnement normal."),
(4, "1,2 kV est égal à :", "1 200 V", "120 V", "12 V", "0,012 V",
 "1 kV = 1 000 V."),
]),

dict(
nom="La résistance et la loi d'Ohm",
fiche="""## La résistance
Un résistor (ou « résistance ») s'oppose plus ou moins au passage du courant.
Symbole R, unité l'ohm (Ω). 1 kΩ = 1 000 Ω. Se mesure avec un ohmmètre, hors circuit.
Plus la résistance est grande, plus l'intensité du courant est faible.

## La loi d'Ohm
La tension aux bornes d'un résistor est proportionnelle à l'intensité qui le traverse :
U = R × I (U en volts, R en ohms, I en ampères).
• R = U / I ; I = U / R.
• Graphique : la caractéristique U = f(I) est une droite passant par l'origine.

## Exemples
• R = 100 Ω, I = 0,05 A : U = 100 × 0,05 = 5 V.
• U = 12 V, R = 60 Ω : I = 12 / 60 = 0,2 A.

## De quoi dépend la résistance d'un fil ?
• Du matériau (le cuivre conduit mieux que le fer).
• De la longueur : plus le fil est long, plus sa résistance est grande.
• De la section : plus le fil est épais, plus sa résistance est faible.

## L'effet Joule
Un conducteur traversé par un courant chauffe : c'est utilisé dans le fer à repasser, la bouilloire, le fusible.""",
questions=[
(1, "L'unité de la résistance électrique est :", "l'ohm", "le volt", "l'ampère", "le watt",
 "Symbole Ω."),
(2, "La loi d'Ohm s'écrit :", "U = R × I", "U = R / I", "I = R × U", "R = U × I",
 "Tension = résistance × intensité."),
(2, "R = 100 Ω et I = 0,05 A. La tension vaut :", "5 V", "2 000 V", "0,0005 V", "100,05 V",
 "100 × 0,05."),
(2, "U = 12 V et R = 60 Ω. L'intensité vaut :", "0,2 A", "5 A", "720 A", "72 A",
 "I = U / R."),
(2, "Plus la résistance d'un circuit est grande, plus l'intensité est :", "faible", "grande", "constante", "négative",
 "La résistance s'oppose au courant."),
(3, "U = 9 V et I = 0,3 A. La résistance vaut :", "30 Ω", "2,7 Ω", "3 Ω", "90 Ω",
 "R = U / I."),
(3, "La caractéristique U = f(I) d'un résistor est :", "une droite passant par l'origine", "une courbe en cloche", "une droite horizontale", "un cercle",
 "La tension est proportionnelle à l'intensité."),
(3, "Plus un fil est long, plus sa résistance est :", "grande", "petite", "nulle", "constante",
 "La longueur augmente la résistance."),
(3, "1,5 kΩ est égal à :", "1 500 Ω", "150 Ω", "15 Ω", "0,0015 Ω",
 "1 kΩ = 1 000 Ω."),
(4, "Le fait qu'un conducteur parcouru par un courant chauffe s'appelle :", "l'effet Joule", "l'effet de serre", "la loi d'Ohm", "la loi des nœuds",
 "Utilisé dans le fer à repasser, la bouilloire."),
]),

dict(
nom="La tension alternative",
fiche="""## Continu et alternatif
• Une pile fournit une tension continue : toujours le même sens, valeur constante.
• Le secteur fournit une tension alternative : elle change de sens régulièrement.

## L'oscilloscope
Il affiche la tension en fonction du temps. Une tension continue donne une droite horizontale ; une tension alternative sinusoïdale donne une courbe en vagues.

## Les grandeurs d'une tension alternative
• Tension maximale Umax : valeur la plus haute atteinte.
• Période T : durée d'un motif complet (en secondes).
• Fréquence f : nombre de motifs par seconde, en hertz (Hz). f = 1 / T.
• Tension efficace Ueff : celle qu'affiche un voltmètre en position alternative (AC) ; pour une tension sinusoïdale, Ueff = Umax / √2.
Le secteur en Côte d'Ivoire : 220 V efficaces, 50 Hz (période 0,02 s).

## Produire et transformer
• Un alternateur (aimant qui tourne devant une bobine) produit une tension alternative : centrales hydroélectriques (Kossou, Soubré), thermiques, dynamo de vélo.
• Un transformateur élève ou abaisse une tension alternative sans changer sa fréquence.
• Un adaptateur (chargeur) abaisse la tension, la redresse avec des diodes et la lisse pour obtenir du continu.""",
questions=[
(1, "Une pile fournit une tension :", "continue", "alternative", "nulle", "variable en sens",
 "Elle garde toujours le même sens."),
(1, "L'unité de la fréquence est :", "le hertz", "le volt", "la seconde", "l'ampère",
 "Symbole Hz."),
(2, "La fréquence du secteur en Côte d'Ivoire est :", "50 Hz", "220 Hz", "1 Hz", "60 Hz",
 "La tension efficace est 220 V."),
(2, "La relation entre fréquence et période est :", "f = 1 / T", "f = T", "f = T × 2", "f = U / I",
 "Fréquence en hertz, période en secondes."),
(2, "L'appareil qui permet de visualiser une tension au cours du temps est :", "l'oscilloscope", "l'ampèremètre", "l'ohmmètre", "le fusible",
 "Il trace la courbe de la tension."),
(3, "Une tension de période 0,02 s a une fréquence de :", "50 Hz", "0,02 Hz", "20 Hz", "500 Hz",
 "1 / 0,02 = 50."),
(3, "Un transformateur permet de :", "modifier la valeur d'une tension alternative", "changer la fréquence", "produire de la tension continue sans diode", "stocker l'électricité",
 "La fréquence reste la même."),
(3, "Un voltmètre en position alternative affiche :", "la tension efficace", "la tension maximale", "la période", "la fréquence",
 "Ueff = Umax / √2 pour une tension sinusoïdale."),
(3, "Un alternateur produit une tension alternative grâce :", "à un aimant qui tourne devant une bobine", "à une réaction chimique", "à la lumière", "à une pile",
 "Principe des centrales électriques."),
(4, "Le chargeur d'un téléphone sert notamment à :", "abaisser et redresser la tension du secteur", "augmenter la tension à 1 000 V", "produire du courant alternatif", "changer la fréquence à 100 Hz",
 "Le téléphone fonctionne en continu sous quelques volts."),
]),

dict(
nom="L'installation électrique de la maison",
fiche="""## Les fils
• La phase : fil sous tension, dangereux (souvent rouge, marron ou noir).
• Le neutre : fil de retour (souvent bleu).
• La terre : fil de protection (vert et jaune), relié à la carcasse métallique des appareils.

## Les protections
• Le fusible : un fil fin qui fond et coupe le circuit en cas de surintensité ; il faut le remplacer.
• Le disjoncteur : coupe le courant en cas de surintensité ou de court-circuit ; on le réenclenche.
• Le disjoncteur différentiel : coupe si une fuite de courant passe par une personne ou par la terre.
• La prise de terre : évacue le courant de fuite d'un appareil défectueux.

## Le compteur
Il mesure l'énergie électrique consommée (en kilowattheures, kWh), facturée par le distributeur (la CIE en Côte d'Ivoire).

## Puissance et énergie
• Puissance P (en watts, W), inscrite sur l'appareil. Pour une lampe ou un appareil de chauffage : P = U × I.
• Énergie E = P × t. Une ampoule de 60 W allumée 10 h consomme 600 Wh = 0,6 kWh.

## Les bons gestes
Couper le disjoncteur avant toute intervention ; ne jamais remplacer un fusible par un fil de cuivre ; ne pas surcharger une multiprise ; éloigner l'eau des prises.""",
questions=[
(1, "Le fil dangereux, sous tension, est :", "la phase", "le neutre", "la terre", "le fil vert et jaune",
 "Il ne faut jamais le toucher."),
(2, "Le fil de terre est de couleur :", "vert et jaune", "bleu", "rouge", "noir",
 "Il protège des fuites de courant."),
(2, "Le compteur électrique mesure :", "l'énergie consommée", "la tension", "la fréquence", "la résistance",
 "En kilowattheures (kWh)."),
(2, "En Côte d'Ivoire, l'électricité est distribuée aux foyers par :", "la CIE", "la SODECI", "Orange", "la SIR",
 "Compagnie ivoirienne d'électricité."),
(2, "Un disjoncteur sert à :", "couper le courant en cas de surintensité ou de court-circuit", "augmenter la puissance", "mesurer la tension", "allumer les lampes",
 "Il protège l'installation."),
(3, "Une ampoule de 60 W allumée 10 heures consomme :", "0,6 kWh", "6 kWh", "60 kWh", "0,06 kWh",
 "60 × 10 = 600 Wh."),
(3, "Le disjoncteur différentiel protège surtout :", "les personnes contre l'électrocution", "les lampes contre l'usure", "le compteur contre la pluie", "les fils contre la rouille",
 "Il coupe dès qu'une fuite de courant est détectée."),
(3, "Remplacer un fusible grillé par un fil de cuivre est :", "dangereux car il n'y a plus de protection", "conseillé", "plus économique et sans risque", "obligatoire",
 "Le fil de cuivre ne fondrait pas en cas de surintensité."),
(4, "Un fer à repasser de 1 000 W branché sur 220 V est traversé par environ :", "4,5 A", "0,2 A", "220 A", "1 000 A",
 "I = P / U = 1 000 / 220."),
(4, "Avant de changer une prise, il faut d'abord :", "couper le disjoncteur", "mouiller ses mains", "allumer tous les appareils", "débrancher le compteur",
 "On travaille toujours hors tension."),
]),

dict(
nom="La lumière : sources, propagation et ombres",
fiche="""## Les sources de lumière
• Sources primaires : produisent leur propre lumière (Soleil, lampe, flamme, écran allumé).
• Objets diffusants : renvoient la lumière qu'ils reçoivent (Lune, mur, cahier). On les voit parce qu'ils diffusent la lumière vers notre œil.

## La propagation
Dans un milieu transparent et homogène (air, eau, verre), la lumière se propage en ligne droite. On la représente par un rayon (droite fléchée) ; un faisceau est un ensemble de rayons.
Vitesse de la lumière : environ 300 000 km/s.
Les milieux : transparents (verre), translucides (papier calque), opaques (bois).

## Les ombres
Un objet opaque éclairé présente :
• une ombre propre : sa partie non éclairée ;
• une ombre portée : la zone sombre derrière lui sur un écran.
• Le cône d'ombre : la zone de l'espace non éclairée derrière l'objet.

## La Lune et les éclipses
• La Lune ne produit pas de lumière : elle est éclairée par le Soleil. Ses phases (nouvelle lune, premier quartier, pleine lune, dernier quartier) dépendent de la partie éclairée visible depuis la Terre ; cycle d'environ 29,5 jours.
• Éclipse de Soleil : la Lune passe entre le Soleil et la Terre (à la nouvelle lune).
• Éclipse de Lune : la Terre passe entre le Soleil et la Lune ; la Lune entre dans l'ombre de la Terre (à la pleine lune).""",
questions=[
(1, "Lequel est une source primaire de lumière ?", "le Soleil", "la Lune", "un miroir", "un mur blanc",
 "Il produit sa propre lumière."),
(1, "Dans un milieu transparent et homogène, la lumière se propage :", "en ligne droite", "en zigzag", "en cercle", "elle ne se propage pas",
 "Propagation rectiligne."),
(2, "La Lune est visible la nuit parce que :", "elle diffuse la lumière du Soleil", "elle produit sa lumière", "elle reflète la lumière de la Terre seulement", "elle brûle",
 "C'est un objet diffusant."),
(2, "Un matériau qui ne laisse pas passer la lumière est :", "opaque", "transparent", "translucide", "lumineux",
 "Exemple : le bois."),
(2, "La vitesse de la lumière est d'environ :", "300 000 km/s", "340 m/s", "300 km/h", "3 000 km/s",
 "340 m/s est la vitesse du son dans l'air."),
(3, "La zone sombre derrière un objet, sur un écran, s'appelle :", "l'ombre portée", "l'ombre propre", "la source", "le faisceau",
 "L'ombre propre est sur l'objet."),
(3, "Une éclipse de Soleil se produit quand :", "la Lune passe entre le Soleil et la Terre", "la Terre passe entre le Soleil et la Lune", "le Soleil passe entre la Terre et la Lune", "la Lune est pleine",
 "Elle cache le Soleil."),
(3, "Une éclipse de Lune se produit :", "quand la Lune entre dans l'ombre de la Terre", "à la nouvelle lune", "quand la Lune cache le Soleil", "chaque mois",
 "Elle a lieu à la pleine lune."),
(3, "Le cycle des phases de la Lune dure environ :", "29,5 jours", "7 jours", "365 jours", "24 heures",
 "D'une nouvelle lune à la suivante."),
(4, "Le papier calque laisse passer la lumière sans qu'on voie nettement à travers. Il est :", "translucide", "transparent", "opaque", "une source primaire",
 "La lumière passe mais est diffusée."),
]),

dict(
nom="Révision de l'année",
fiche="""## Électricité
• Circuit fermé ; conducteurs (métaux) et isolants (plastique, verre).
• Série : une seule boucle, I identique partout, U = U₁ + U₂.
• Dérivation : plusieurs boucles, U identique, I = I₁ + I₂ (loi des nœuds).
• Ampèremètre en série ; voltmètre en dérivation.
• Loi d'Ohm : U = R × I.
• Alternatif : f = 1 / T ; secteur 220 V, 50 Hz ; transformateur ; alternateur.
• Maison : phase, neutre, terre ; fusible, disjoncteur ; E = P × t.

## Lumière
• Sources primaires et objets diffusants ; propagation rectiligne ; 300 000 km/s.
• Ombre propre, ombre portée, cône d'ombre ; éclipses de Soleil et de Lune ; phases de la Lune.

## Méthode
Écris la loi littérale, remplace par les valeurs avec leurs unités, donne le résultat avec l'unité. Convertis d'abord : mA → A, kΩ → Ω.""",
questions=[
(2, "Dans un circuit en série, I = 0,4 A dans la lampe. Dans le moteur, I vaut :", "0,4 A", "0,2 A", "0,8 A", "0 A",
 "Même intensité en série."),
(2, "Le voltmètre se branche :", "en dérivation", "en série", "à la place d'une lampe", "sur le compteur",
 "Aux bornes du dipôle."),
(2, "Une période de 0,01 s correspond à une fréquence de :", "100 Hz", "50 Hz", "0,01 Hz", "10 Hz",
 "f = 1 / T."),
(3, "R = 50 Ω et I = 200 mA. U vaut :", "10 V", "10 000 V", "250 V", "0,25 V",
 "On convertit : 0,2 A × 50."),
(3, "Pile de 9 V, trois lampes identiques en série. Chaque lampe a à ses bornes :", "3 V", "9 V", "27 V", "1 V",
 "9 / 3."),
(3, "Trois branches en dérivation sont parcourues par 0,1 A, 0,2 A et 0,3 A. La branche principale reçoit :", "0,6 A", "0,3 A", "0,1 A", "0,006 A",
 "Loi des nœuds."),
(3, "Un appareil de 2 000 W fonctionne 30 min. Il consomme :", "1 kWh", "60 kWh", "2 kWh", "0,5 kWh",
 "2 kW × 0,5 h."),
(4, "Une éclipse de Soleil n'est possible qu'à :", "la nouvelle lune", "la pleine lune", "le premier quartier", "n'importe quelle phase",
 "La Lune est alors entre le Soleil et la Terre."),
(4, "U = 4,5 V et I = 0,15 A. La résistance vaut :", "30 Ω", "0,675 Ω", "3 Ω", "300 Ω",
 "R = U / I."),
(4, "Le fil qui relie la carcasse métallique d'un appareil au sol est :", "la terre", "la phase", "le neutre", "le fusible",
 "Il évacue les courants de fuite."),
]),
]
