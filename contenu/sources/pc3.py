NIVEAU, MATIERE = "3ème", "Physique-Chimie"

CHAPITRES = [
dict(
nom="Lentilles minces",
fiche="""## Deux types de lentilles
• Lentille convergente : bords minces, centre épais. Elle fait converger la lumière. Vue de près à travers elle, une écriture paraît agrandie.
• Lentille divergente : bords épais, centre mince. Elle fait diverger la lumière. L'écriture paraît plus petite.

## Vocabulaire
• Centre optique O : le centre de la lentille.
• Axe optique principal : la droite qui passe par O, perpendiculaire à la lentille.
• Foyer image F' : point où convergent les rayons arrivant parallèles à l'axe. Foyer objet F : son symétrique par rapport à O.
• Distance focale f = OF', en mètres.
• Vergence C = 1 ÷ f, en dioptries (δ). Positive pour une convergente, négative pour une divergente.
   f = 20 cm = 0,2 m → C = 1 ÷ 0,2 = 5 δ.
• Deux lentilles accolées : leurs vergences s'additionnent.

## Les trois rayons particuliers (lentille convergente)
1. Un rayon qui passe par O n'est pas dévié.
2. Un rayon parallèle à l'axe ressort en passant par F'.
3. Un rayon qui passe par F ressort parallèle à l'axe.
Deux de ces rayons suffisent pour construire l'image d'un point.

## Position de l'objet et image obtenue (lentille convergente)
• Objet au-delà de 2f : image réelle, renversée, plus petite (appareil photo, œil).
• Objet à 2f : image réelle, renversée, de même taille, à 2f de l'autre côté.
• Objet entre F et 2f : image réelle, renversée, plus grande (projecteur).
• Objet au foyer F : pas d'image nette, elle est rejetée à l'infini.
• Objet entre F et O : image virtuelle, droite, agrandie (loupe).
Une image réelle se recueille sur un écran ; une image virtuelle ne se voit qu'à travers la lentille.

## Exemple corrigé
Une lentille a une vergence de −4 δ. Elle est divergente et f = 1 ÷ 4 = 0,25 m = 25 cm.

## Pièges à éviter
• Convertir la distance focale en mètres avant de calculer la vergence.
• Une loupe est une lentille convergente : l'objet doit être placé entre le foyer et la lentille.""",
questions=[
(1, "Une lentille à bords minces est :", "convergente", "divergente", "plane", "un miroir",
 "Bords minces, centre épais : la lentille fait converger la lumière."),
(1, "La vergence d'une lentille s'exprime en :", "dioptries (δ)", "mètres", "watts", "newtons",
 "C = 1 ÷ f, avec f en mètres : l'unité est la dioptrie."),
(1, "Un rayon lumineux qui passe par le centre optique O d'une lentille :", "n'est pas dévié", "passe ensuite par le foyer F'", "ressort parallèle à l'axe", "est réfléchi",
 "Au centre, la lentille se comporte comme une lame à faces parallèles très mince : le rayon continue tout droit."),
(2, "Une lentille a une distance focale de 20 cm. Sa vergence est :", "5 δ", "20 δ", "0,05 δ", "0,2 δ",
 "f = 0,2 m, donc C = 1 ÷ 0,2 = 5 δ. Il faut convertir en mètres d'abord."),
(2, "Une lentille a une vergence de −4 δ. Elle est :", "divergente, de distance focale 25 cm", "convergente, de distance focale 25 cm", "convergente, de distance focale 4 m", "divergente, de distance focale 4 cm",
 "Vergence négative : lentille divergente. f = 1 ÷ 4 = 0,25 m = 25 cm."),
(2, "Pour une lentille convergente, un rayon arrivant parallèle à l'axe optique :", "ressort en passant par le foyer image F'", "ressort en passant par le foyer objet F", "n'est pas dévié", "ressort parallèle à l'axe",
 "C'est la définition du foyer image F'."),
(2, "Pour utiliser une lentille convergente comme loupe, on place l'objet :", "entre le foyer objet et la lentille", "au-delà de deux fois la distance focale", "exactement au foyer", "derrière la lentille",
 "Entre F et O, l'image est virtuelle, droite et agrandie."),
(3, "Une image réelle :", "peut être recueillie sur un écran", "ne peut jamais être recueillie sur un écran", "est toujours droite", "est toujours plus grande que l'objet",
 "L'image réelle se forme là où les rayons se croisent vraiment, on peut donc l'obtenir sur un écran."),
(3, "Un objet est placé à deux fois la distance focale d'une lentille convergente. L'image est :", "réelle, renversée et de même taille", "virtuelle, droite et agrandie", "rejetée à l'infini", "réelle, droite et plus petite",
 "À 2f, l'image se forme à 2f de l'autre côté, renversée et de même taille que l'objet."),
(3, "Un objet est placé au foyer objet F d'une lentille convergente. Son image :", "est rejetée à l'infini", "a la même taille que l'objet", "est virtuelle et droite", "se forme au foyer image F'",
 "Les rayons issus d'un point du plan focal objet ressortent parallèles entre eux : ils ne se rencontrent qu'à l'infini. On dit que l'image est rejetée à l'infini ; on ne peut pas la recueillir sur un écran."),
(4, "On accole une lentille de +3 δ et une lentille de +2 δ. La vergence de l'ensemble est :", "5 δ", "6 δ", "1 δ", "1,5 δ",
 "Les vergences de lentilles accolées s'additionnent : 3 + 2 = 5 δ (distance focale 20 cm)."),
(4, "En regardant un texte de près à travers une lentille, les lettres paraissent plus petites. La lentille est :", "divergente", "convergente", "une loupe", "plane",
 "Une lentille divergente donne d'un objet une image droite et plus petite."),
]),

dict(
nom="Vision et défauts de l'œil",
fiche="""## L'œil, un appareil optique
• La cornée et le cristallin jouent le rôle d'une lentille convergente.
• L'iris joue le rôle d'un diaphragme : la pupille, au centre, s'agrandit dans le noir et se rétrécit en pleine lumière.
• La rétine joue le rôle d'écran : l'image s'y forme, réelle et renversée.
• Le nerf optique transmet l'information au cerveau, qui « redresse » l'image.

## L'accommodation
Pour voir net un objet proche, le cristallin se bombe : sa vergence augmente.
• Punctum remotum (PR) : point le plus éloigné vu net sans accommoder. Œil normal : à l'infini.
• Punctum proximum (PP) : point le plus proche vu net en accommodant au maximum. Œil normal : environ 25 cm.

## Les défauts et leur correction
• Myopie : l'œil est trop convergent. L'image d'un objet éloigné se forme en avant de la rétine. Le myope voit mal de loin.
   Correction : lentille DIVERGENTE (vergence négative, par exemple −2,5 δ).
• Hypermétropie : l'œil n'est pas assez convergent. L'image se forme en arrière de la rétine. L'hypermétrope voit mal de près.
   Correction : lentille CONVERGENTE.
• Presbytie : avec l'âge (souvent après 45 ans), le cristallin perd sa souplesse et l'œil accommode mal. On voit mal de près.
   Correction : lentille convergente pour la lecture.

## Exemple corrigé
Une ordonnance indique −2,5 δ pour chaque œil. La vergence est négative : ce sont des lentilles divergentes, la personne est myope.

## Bien prendre soin de ses yeux
• Ne jamais regarder le soleil directement, même avec des lunettes de soleil.
• Faire des pauses régulières devant un écran.
• Si tu plisses les yeux pour lire le tableau, parles-en à tes parents : un contrôle de la vue s'impose.

## Pièges à éviter
• Myope : voit mal de LOIN, corrigé par une DIVERGENTE.
• Hypermétrope et presbyte : voient mal de PRÈS, corrigés par une CONVERGENTE.""",
questions=[
(1, "Dans l'œil, la rétine joue le rôle :", "d'écran, où se forme l'image", "de lentille", "de diaphragme", "de protection",
 "L'image se forme sur la rétine, puis le nerf optique la transmet au cerveau."),
(1, "Le cristallin joue le rôle :", "d'une lentille convergente", "d'une lentille divergente", "d'un écran", "d'un diaphragme",
 "Avec la cornée, le cristallin fait converger la lumière sur la rétine."),
(1, "Une personne myope voit mal :", "les objets éloignés", "les objets proches", "les couleurs", "dans le noir",
 "Chez le myope, l'image d'un objet lointain se forme en avant de la rétine : elle est floue."),
(2, "La myopie se corrige avec :", "une lentille divergente", "une lentille convergente", "un miroir", "une lentille plane",
 "L'œil myope est trop convergent : on compense avec une lentille divergente."),
(2, "L'hypermétropie se corrige avec :", "une lentille convergente", "une lentille divergente", "un filtre coloré", "une lentille plane",
 "L'œil hypermétrope n'est pas assez convergent : on ajoute une lentille convergente."),
(2, "Chez une personne myope, l'image d'un objet éloigné se forme :", "en avant de la rétine", "sur la rétine", "en arrière de la rétine", "sur le cristallin",
 "L'œil myope fait converger trop tôt les rayons."),
(2, "L'accommodation, c'est :", "le cristallin qui se bombe pour voir net de près", "la pupille qui s'agrandit dans le noir", "la rétine qui se rapproche du cristallin", "l'œil qui tourne vers l'objet",
 "En se bombant, le cristallin augmente sa vergence."),
(3, "La presbytie est due :", "à la perte de souplesse du cristallin avec l'âge", "à un œil trop long", "à une rétine abîmée", "à une pupille trop petite",
 "Le cristallin n'arrive plus à se bomber assez : on voit mal de près. On corrige avec une lentille convergente."),
(3, "Une ordonnance indique −2,5 δ. La personne est :", "myope", "hypermétrope", "presbyte", "sans défaut de vision",
 "Vergence négative : lentilles divergentes, qui corrigent la myopie."),
(3, "L'iris joue le rôle :", "d'un diaphragme", "d'une lentille", "d'un écran", "du nerf optique",
 "L'iris règle l'ouverture de la pupille, donc la quantité de lumière qui entre."),
(4, "Pour un œil normal, le punctum remotum se trouve :", "à l'infini", "à 25 cm", "sur la rétine", "au foyer du cristallin",
 "Au repos, sans accommoder, l'œil normal voit net les objets très éloignés."),
(4, "Ton grand-père de 60 ans éloigne son journal pour le lire. Il est probablement :", "presbyte, et il lui faut des verres convergents", "myope, et il lui faut des verres divergents", "presbyte, et il lui faut des verres divergents", "myope, et il lui faut des verres convergents",
 "Avec l'âge, l'accommodation diminue : on voit mal de près. Des verres convergents l'aident à lire."),
]),

dict(
nom="Travail et puissance mécaniques",
fiche="""## Le poids
P = m × g, avec m en kg, g ≈ 10 N/kg (intensité de la pesanteur) et P en newtons (N).
Un sac de riz de 25 kg pèse 25 × 10 = 250 N.

## Le travail d'une force
Une force constante F dont le point d'application se déplace de d dans sa direction effectue un travail :
W = F × d, avec F en newtons, d en mètres et W en joules (J).
• Travail moteur (positif) : la force est dans le sens du déplacement (tu pousses une brouette).
• Travail résistant (négatif) : la force est opposée au déplacement (les frottements).
• Travail nul : la force est perpendiculaire au déplacement (porter un sac en marchant à plat).

## Travail du poids
Quand on monte un objet d'une hauteur h : W = m × g × h.
Monter un sac de 20 kg sur 3 m demande 20 × 10 × 3 = 600 J.

## La puissance mécanique
C'est le travail effectué par seconde : P = W ÷ t, avec W en joules, t en secondes et P en watts (W).
1 kW = 1 000 W.
Inversement : W = P × t.

## Exemple corrigé (au chantier)
Une grue monte 500 kg de parpaings à 12 m de hauteur en 20 s.
W = 500 × 10 × 12 = 60 000 J ; P = 60 000 ÷ 20 = 3 000 W = 3 kW.

## Pièges à éviter
• Ne pas confondre la masse (kg) et le poids (N).
• Convertir les minutes en secondes avant de calculer une puissance : 2 min = 120 s.
• Le symbole W désigne à la fois le travail (en formule) et le watt (unité) : bien lire le contexte.""",
questions=[
(1, "Le travail d'une force s'exprime en :", "joules (J)", "watts (W)", "newtons (N)", "kilogrammes (kg)",
 "Le travail est une énergie : il se mesure en joules."),
(1, "Une force de 50 N déplace son point d'application de 10 m dans sa direction. Son travail est :", "500 J", "5 J", "60 J", "0,2 J",
 "W = F × d = 50 × 10 = 500 J."),
(1, "La puissance s'exprime en :", "watts (W)", "joules (J)", "newtons (N)", "mètres par seconde",
 "La puissance est un travail par seconde : 1 W = 1 J/s."),
(2, "Un travail de 600 J est effectué en 30 s. La puissance est :", "20 W", "18 000 W", "630 W", "0,05 W",
 "P = W ÷ t = 600 ÷ 30 = 20 W."),
(2, "Avec g = 10 N/kg, le poids d'un objet de 20 kg est :", "200 N", "20 N", "2 N", "30 N",
 "P = m × g = 20 × 10 = 200 N."),
(2, "On monte un sac de 20 kg à 3 m de hauteur (g = 10 N/kg). Le travail nécessaire est :", "600 J", "60 J", "200 J", "6 000 J",
 "W = m × g × h = 20 × 10 × 3 = 600 J."),
(2, "Une force perpendiculaire au déplacement effectue un travail :", "nul", "moteur", "résistant", "maximal",
 "Elle ne fait ni avancer ni reculer l'objet dans la direction du déplacement."),
(3, "Le travail des forces de frottement est en général :", "résistant (négatif)", "moteur (positif)", "toujours nul", "égal au poids",
 "Les frottements s'opposent au mouvement."),
(3, "Une grue monte 500 kg de parpaings à 12 m de hauteur en 20 s (g = 10 N/kg). Sa puissance est :", "3 000 W", "60 000 W", "300 W", "3 W",
 "W = 500 × 10 × 12 = 60 000 J, puis P = 60 000 ÷ 20 = 3 000 W."),
(3, "2,5 kW est égal à :", "2 500 W", "250 W", "25 W", "0,0025 W",
 "1 kW = 1 000 W, donc 2,5 kW = 2 500 W."),
(4, "Un moteur de 1 500 W fonctionne pendant 2 minutes. Il effectue un travail de :", "180 000 J", "3 000 J", "750 J", "180 J",
 "t = 2 min = 120 s. W = P × t = 1 500 × 120 = 180 000 J."),
(4, "Tu pousses une brouette avec une force de 80 N sur 25 m, en 50 s. Ta puissance est :", "40 W", "2 000 W", "100 W", "160 W",
 "W = 80 × 25 = 2 000 J, puis P = 2 000 ÷ 50 = 40 W."),
]),

dict(
nom="Puissance et énergie électriques",
fiche="""## Les indications d'un appareil
Sur une lampe : « 220 V – 60 W ».
• 220 V est sa tension nominale (celle du secteur).
• 60 W est sa puissance nominale, quand elle fonctionne normalement.

## Puissance électrique
Pour un appareil de chauffage ou une lampe : P = U × I (P en W, U en V, I en A).
Un fer à repasser de 1 100 W sous 220 V est traversé par I = P ÷ U = 1 100 ÷ 220 = 5 A.
Pour un conducteur ohmique (résistance R) : P = R × I².

## Énergie électrique
E = P × t
• En joules (J) si P est en watts et t en secondes.
• En kilowattheures (kWh) si P est en kW et t en heures. C'est l'unité de la facture d'électricité.
• 1 kWh = 1 000 W × 3 600 s = 3 600 000 J.
Le compteur électrique de la maison mesure l'énergie consommée en kWh.

## Calculer le coût
Coût = énergie (kWh) × prix du kWh.
Un fer de 1 000 W utilisé 2 h consomme 1 kW × 2 h = 2 kWh. À 80 F le kWh, cela coûte 160 F.

## Sécurité dans l'installation
• Sur une même prise multiple, les intensités des appareils s'additionnent : trop d'appareils provoquent une surintensité et un échauffement des fils.
• Le fusible et le disjoncteur coupent le courant en cas de surintensité ou de court-circuit.
• Ne jamais toucher un appareil électrique avec les mains mouillées.

## Économiser l'énergie
Une lampe LED de 10 W éclaire autant qu'une ampoule classique de 60 W.
Allumée 6 h par jour pendant 30 jours (180 h), elle fait économiser 50 W × 180 h = 9 kWh.

## Pièges à éviter
• Convertir les W en kW (÷ 1 000) et les minutes en heures avant de calculer des kWh.
• Le kW est une puissance, le kWh est une énergie.""",
questions=[
(1, "L'unité de l'énergie électrique sur la facture est :", "le kilowattheure (kWh)", "le kilowatt (kW)", "le volt (V)", "l'ampère (A)",
 "Le compteur et la facture comptent l'énergie consommée en kWh."),
(1, "Sur une lampe on lit « 220 V – 60 W ». 60 W est :", "sa puissance nominale", "sa tension nominale", "l'intensité qui la traverse", "l'énergie consommée en une heure",
 "Le watt est l'unité de puissance ; 220 V est la tension nominale."),
(2, "Un appareil fonctionne sous 220 V et il est traversé par un courant de 5 A. Sa puissance est :", "1 100 W", "44 W", "225 W", "215 W",
 "P = U × I = 220 × 5 = 1 100 W."),
(2, "Un appareil de 2 200 W fonctionne sous 220 V. L'intensité qui le traverse est :", "10 A", "0,1 A", "484 000 A", "2 420 A",
 "I = P ÷ U = 2 200 ÷ 220 = 10 A."),
(2, "Une lampe de 100 W reste allumée 5 h. Elle consomme :", "0,5 kWh", "500 kWh", "20 kWh", "0,05 kWh",
 "E = 0,1 kW × 5 h = 0,5 kWh (soit 500 Wh)."),
(2, "1 kWh est égal à :", "3 600 000 J", "1 000 J", "3 600 J", "60 J",
 "1 kWh = 1 000 W × 3 600 s = 3 600 000 J."),
(3, "Un fer à repasser de 1 000 W est utilisé 2 h. Le kWh coûte 80 F. Le coût est :", "160 F", "80 F", "2 000 F", "160 000 F",
 "E = 1 kW × 2 h = 2 kWh, et 2 × 80 = 160 F."),
(3, "Un conducteur ohmique de résistance 50 Ω est traversé par un courant de 2 A. Sa puissance est :", "200 W", "100 W", "25 W", "400 W",
 "U = R × I = 50 × 2 = 100 V, puis P = U × I = 100 × 2 = 200 W (ou directement P = R × I² = 50 × 4 = 200 W)."),
(3, "Sur une même prise multiple : ventilateur 1 A, téléviseur 0,5 A et réfrigérateur 1,5 A. L'intensité dans le câble de la prise est :", "3 A", "1,5 A", "1 A", "0,75 A",
 "Les appareils sont en dérivation : les intensités s'additionnent, 1 + 0,5 + 1,5 = 3 A."),
(3, "Le disjoncteur sert à :", "couper le courant en cas de surintensité", "augmenter la tension", "mesurer l'énergie consommée", "économiser de l'énergie",
 "Il protège l'installation contre les surintensités et les courts-circuits."),
(4, "Un climatiseur de 1 500 W fonctionne 8 h par jour pendant 30 jours. Il consomme :", "360 kWh", "12 kWh", "45 000 kWh", "3 600 kWh",
 "E = 1,5 kW × (8 × 30) h = 1,5 × 240 = 360 kWh."),
(4, "On remplace une ampoule de 60 W par une LED de 10 W, allumée 6 h par jour pendant 30 jours. L'économie est de :", "9 kWh", "50 kWh", "1,8 kWh", "10,8 kWh",
 "Durée : 180 h. Économie : (60 − 10) W × 180 h = 9 000 Wh = 9 kWh."),
]),

dict(
nom="Oxydation des métaux",
fiche="""## Le fer
• À l'air humide, le fer rouille lentement : il réagit avec le dioxygène et l'eau. La rouille est un oxyde de fer hydraté, brun-rouge.
• La rouille est poreuse et friable : elle laisse passer l'air et l'eau, et le fer continue de rouiller jusqu'au cœur.
• Combustion vive : la laine de fer brûle dans le dioxygène pur avec des étincelles. Il se forme de l'oxyde magnétique Fe₃O₄.
   3 Fe + 2 O₂ → Fe₃O₄

## L'aluminium
L'aluminium s'oxyde à l'air et se couvre d'une fine couche d'alumine Al₂O₃.
Cette couche est imperméable : elle protège le métal. C'est pourquoi les marmites en aluminium durent longtemps.
   4 Al + 3 O₂ → 2 Al₂O₃

## Le cuivre
• Chauffé à l'air, le cuivre se couvre d'oxyde de cuivre II, noir : 2 Cu + O₂ → 2 CuO.
• Il existe aussi un oxyde de cuivre I, rouge : Cu₂O.
• À l'air humide, le cuivre se couvre lentement d'une couche verte (vert-de-gris).

## Équilibrer une équation
Pendant une réaction chimique, les atomes se conservent : il y a autant d'atomes de chaque sorte avant et après.
La masse aussi se conserve : masse des réactifs = masse des produits.
Exemple : 16,8 g de fer brûlent avec 6,4 g de dioxygène et donnent 23,2 g d'oxyde magnétique.

## Protéger le fer de la rouille
• Peinture, vernis, graisse : on empêche l'air et l'eau d'atteindre le fer.
• Galvanisation : on recouvre le fer de zinc. Les tôles galvanisées des toits résistent bien à notre climat humide.
• Chromage, nickelage : on le recouvre d'un autre métal.

## Pièges à éviter
• L'alumine protège l'aluminium, alors que la rouille ne protège pas le fer.
• Dans une équation, on ne change jamais une formule : on ajoute seulement des coefficients devant.""",
questions=[
(1, "La rouille se forme lorsque le fer est en contact avec :", "le dioxygène et l'eau", "le diazote seul", "le dioxyde de carbone seul", "la lumière",
 "La rouille est un oxyde de fer hydraté : il faut du dioxygène et de l'eau (air humide)."),
(1, "La combustion vive du fer dans le dioxygène produit :", "de l'oxyde magnétique Fe₃O₄", "de la rouille", "de l'alumine", "du dioxyde de carbone",
 "3 Fe + 2 O₂ → Fe₃O₄."),
(1, "La formule de l'oxyde de cuivre II est :", "CuO", "Cu₂O", "CuO₂", "Cu₂O₃",
 "L'oxyde de cuivre II, noir, contient un atome de cuivre pour un atome d'oxygène. Cu₂O est l'oxyde de cuivre I, rouge."),
(2, "L'équation équilibrée de la combustion du fer est :", "3 Fe + 2 O₂ → Fe₃O₄", "Fe + O₂ → Fe₃O₄", "2 Fe + O₂ → Fe₃O₄", "3 Fe + O₂ → Fe₃O₄",
 "3 atomes de fer et 4 atomes d'oxygène de chaque côté."),
(2, "La couche d'alumine qui se forme sur l'aluminium :", "protège le métal", "ronge le métal jusqu'au cœur", "est poreuse et friable", "le rend magnétique",
 "Elle est imperméable à l'air et à l'eau : l'oxydation s'arrête."),
(2, "Quand on chauffe du cuivre à l'air, il se couvre :", "d'oxyde de cuivre II, noir", "de rouille", "d'alumine, blanche", "de zinc",
 "2 Cu + O₂ → 2 CuO, un solide noir."),
(2, "La galvanisation consiste à :", "recouvrir le fer d'une couche de zinc", "peindre le fer", "chauffer le fer", "plonger le fer dans l'eau",
 "Le zinc protège le fer de la rouille, c'est le cas des tôles galvanisées."),
(3, "Dans l'équation 4 Al + … O₂ → 2 Al₂O₃, le coefficient manquant est :", "3", "2", "4", "6",
 "À droite : 2 × 3 = 6 atomes d'oxygène, donc 3 molécules O₂ à gauche."),
(3, "Le fer rouillé continue de se dégrader car :", "la rouille est poreuse et laisse passer l'air et l'eau", "la rouille attire le dioxygène", "la rouille est imperméable", "le fer fond lentement",
 "Contrairement à l'alumine, la rouille ne forme pas une barrière."),
(3, "16,8 g de fer brûlent entièrement avec 6,4 g de dioxygène. La masse d'oxyde formé est :", "23,2 g", "10,4 g", "16,8 g", "6,4 g",
 "La masse se conserve : 16,8 + 6,4 = 23,2 g."),
(4, "Selon l'équation 2 Cu + O₂ → 2 CuO, pour oxyder 10 atomes de cuivre il faut :", "5 molécules de dioxygène", "10 molécules de dioxygène", "20 molécules de dioxygène", "2 molécules de dioxygène",
 "Une molécule O₂ pour 2 atomes de cuivre : 10 ÷ 2 = 5."),
(4, "Pourquoi utilise-t-on des tôles galvanisées pour les toits ?", "Le zinc protège le fer de la rouille dans un climat humide", "Le zinc rend les tôles plus légères", "Le zinc empêche la chaleur d'entrer", "Le zinc rend les tôles magnétiques",
 "Avec la pluie et l'humidité, le fer nu rouillerait vite."),
]),

dict(
nom="Réduction des oxydes",
fiche="""## Définitions
• Une oxydation est un gain d'oxygène.
• Une réduction est une perte d'oxygène : on enlève l'oxygène d'un oxyde.
• Le réducteur est le corps qui capte l'oxygène (carbone, aluminium, dihydrogène, monoxyde de carbone) : il est oxydé.
• L'oxydant est le corps qui cède son oxygène (l'oxyde) : il est réduit.
• Une oxydoréduction est une réaction où une oxydation et une réduction ont lieu en même temps.

## Réduction de l'oxyde de cuivre par le carbone
On chauffe un mélange de poudre d'oxyde de cuivre II (noir) et de carbone.
2 CuO + C → 2 Cu + CO₂
• Le solide devient rouge brique : il s'est formé du cuivre.
• Le gaz trouble l'eau de chaux : c'est du dioxyde de carbone.
• CuO est réduit (oxydant), C est oxydé (réducteur).

## Avec le dihydrogène
CuO + H₂ → Cu + H₂O : il se forme du cuivre et de l'eau.

## L'aluminothermie
Fe₂O₃ + 2 Al → 2 Fe + Al₂O₃
La réaction est très exothermique : le fer obtenu est liquide. On l'utilise pour souder les rails.
L'aluminium réduit l'oxyde de fer parce qu'il a plus d'affinité pour l'oxygène que le fer.

## Le haut fourneau
On obtient la fonte (fer + un peu de carbone) en réduisant les minerais d'oxydes de fer par le monoxyde de carbone :
Fe₂O₃ + 3 CO → 2 Fe + 3 CO₂

## Exemple corrigé
16 g d'oxyde de cuivre réagissent avec 1,2 g de carbone et donnent 12,8 g de cuivre.
Conservation de la masse : masse de CO₂ = 16 + 1,2 − 12,8 = 4,4 g.

## Pièges à éviter
• Le réducteur est OXYDÉ et l'oxydant est RÉDUIT : c'est croisé.
• Bien vérifier que l'équation est équilibrée, oxygène compris.""",
questions=[
(1, "Une réduction est :", "une perte d'oxygène", "un gain d'oxygène", "une combustion", "une dissolution",
 "On enlève l'oxygène d'un oxyde."),
(1, "Dans la réaction 2 CuO + C → 2 Cu + CO₂, le réducteur est :", "le carbone", "l'oxyde de cuivre", "le cuivre", "le dioxyde de carbone",
 "Le carbone capte l'oxygène de l'oxyde de cuivre : c'est le réducteur, il est oxydé."),
(2, "Dans la réaction 2 CuO + C → 2 Cu + CO₂, l'oxyde de cuivre :", "est réduit", "est oxydé", "est le réducteur", "ne réagit pas",
 "Il perd son oxygène : il est réduit, c'est l'oxydant."),
(2, "Le gaz qui trouble l'eau de chaux est :", "le dioxyde de carbone", "le dioxygène", "le dihydrogène", "le diazote",
 "C'est le test du CO₂."),
(2, "À la fin de la réduction de l'oxyde de cuivre par le carbone, il reste un solide rouge brique. C'est :", "du cuivre", "de l'oxyde de cuivre II", "du carbone", "de la rouille",
 "L'oxyde de cuivre II est noir, le cuivre métallique est rouge brique."),
(2, "Une oxydoréduction est une réaction au cours de laquelle :", "une oxydation et une réduction ont lieu en même temps", "il y a seulement une oxydation", "il y a seulement une réduction", "aucun oxygène n'est échangé",
 "L'oxygène perdu par l'un est gagné par l'autre."),
(3, "Dans l'aluminothermie Fe₂O₃ + 2 Al → 2 Fe + Al₂O₃, l'aluminium :", "est oxydé, c'est le réducteur", "est réduit, c'est l'oxydant", "ne réagit pas", "est un produit",
 "L'aluminium gagne de l'oxygène (il devient Al₂O₃)."),
(3, "Dans un haut fourneau, le principal réducteur des oxydes de fer est :", "le monoxyde de carbone", "le dioxygène", "l'eau", "le diazote",
 "Fe₂O₃ + 3 CO → 2 Fe + 3 CO₂."),
(3, "Dans l'équation Fe₂O₃ + 3 CO → 2 Fe + … CO₂, le coefficient manquant est :", "3", "2", "1", "6",
 "À gauche : 3 + 3 = 6 atomes d'oxygène. À droite, il en faut 6 : 3 CO₂."),
(3, "Quand le dihydrogène réduit l'oxyde de cuivre, il se forme du cuivre et :", "de l'eau", "du dioxyde de carbone", "du dioxygène", "de la rouille",
 "CuO + H₂ → Cu + H₂O."),
(4, "16 g d'oxyde de cuivre réagissent avec 1,2 g de carbone ; il se forme 12,8 g de cuivre. La masse de dioxyde de carbone formé est :", "4,4 g", "17,2 g", "3,2 g", "12,8 g",
 "Conservation de la masse : 16 + 1,2 − 12,8 = 4,4 g."),
(4, "L'aluminium peut réduire l'oxyde de fer parce que :", "il a plus d'affinité pour l'oxygène que le fer", "il est plus lourd que le fer", "il est magnétique", "il fond à basse température",
 "Le corps qui « attire » le plus l'oxygène l'arrache à l'autre."),
]),

dict(
nom="Solutions acides, basiques et neutres",
fiche="""## Le pH
Le pH indique si une solution aqueuse est acide, neutre ou basique. À 25 °C, il va de 0 à 14.
• pH < 7 : solution acide (jus de citron, vinaigre, jus de bissap).
• pH = 7 : solution neutre (eau pure).
• pH > 7 : solution basique (eau savonneuse, eau de Javel, soude).
Plus le pH est loin de 7, plus la solution est acide ou basique.

## Les ions responsables
• Une solution acide contient plus d'ions hydrogène H⁺ que d'ions hydroxyde OH⁻.
• Une solution basique contient plus d'ions OH⁻ que d'ions H⁺.
• Une solution neutre en contient autant.

## Mesurer le pH
• Papier pH : on dépose une goutte et on compare la couleur à une échelle. Mesure approchée.
• pH-mètre : mesure précise.
• Indicateurs colorés, par exemple le bleu de bromothymol (BBT) : jaune en milieu acide, vert en milieu neutre, bleu en milieu basique.

## La dilution
Ajouter de l'eau à une solution rapproche son pH de 7 :
• le pH d'une solution acide augmente ;
• le pH d'une solution basique diminue.

## Réactions à connaître
• Acide + base : réaction de neutralisation, qui dégage de la chaleur ; le pH se rapproche de 7.
• Acide chlorhydrique + fer : il se dégage du dihydrogène (petite détonation à l'approche d'une flamme).

## Sécurité
• Porter des lunettes et des gants avec les acides et les bases concentrés.
• Pour diluer : TOUJOURS verser l'acide dans l'eau, jamais l'eau dans l'acide (risque de projections).
• Ne jamais mélanger l'eau de Javel avec un produit acide (détartrant, vinaigre) : il se dégage du dichlore, un gaz toxique.

## Pièges à éviter
• Un pH de 1 est PLUS acide qu'un pH de 4.
• Diluer ne rend pas une solution neutre : son pH s'approche de 7 sans le dépasser.""",
questions=[
(1, "Une solution de pH 7 est :", "neutre", "acide", "basique", "concentrée",
 "À 25 °C, pH = 7 correspond à une solution neutre, comme l'eau pure."),
(1, "Le jus de citron a un pH d'environ 2. Il est :", "acide", "basique", "neutre", "salé",
 "pH inférieur à 7 : solution acide."),
(1, "Une solution de pH 12 est :", "basique", "acide", "neutre", "pure",
 "pH supérieur à 7 : solution basique."),
(2, "Pour mesurer précisément le pH d'une solution, on utilise :", "un pH-mètre", "un thermomètre", "un ampèremètre", "une balance",
 "Le papier pH donne une valeur approchée, le pH-mètre une valeur précise."),
(2, "Une solution acide contient en excès des ions :", "hydrogène H⁺", "hydroxyde OH⁻", "chlorure Cl⁻", "sodium Na⁺",
 "Ce sont les ions H⁺ qui sont responsables de l'acidité."),
(2, "Quand on dilue une solution acide, son pH :", "augmente et se rapproche de 7", "diminue", "ne change pas", "devient égal à 0",
 "L'eau ajoutée rend la solution moins acide."),
(2, "En milieu basique, le bleu de bromothymol (BBT) est :", "bleu", "jaune", "vert", "rouge",
 "BBT : jaune en milieu acide, vert en milieu neutre, bleu en milieu basique."),
(3, "Pour diluer un acide concentré, il faut :", "verser l'acide dans l'eau", "verser l'eau dans l'acide", "chauffer l'acide", "agiter l'acide sans eau",
 "Verser l'eau dans l'acide peut provoquer des projections dangereuses."),
(3, "Quand on verse de l'acide chlorhydrique sur du fer :", "il se dégage du dihydrogène", "il se dégage du dioxygène", "il ne se passe rien", "il se forme du cuivre",
 "Le gaz produit une petite détonation à l'approche d'une flamme : c'est le test du dihydrogène."),
(3, "Trois solutions ont pour pH : A = 3, B = 9 et C = 1. La plus acide est :", "C", "A", "B", "A et C de la même façon",
 "Plus le pH est petit (sous 7), plus la solution est acide."),
(4, "Quand on mélange une solution acide et une solution basique :", "le pH se rapproche de 7 et le mélange s'échauffe", "le pH devient toujours égal à 0", "il ne se passe rien", "il se forme toujours un gaz",
 "C'est une réaction de neutralisation, qui dégage de la chaleur."),
(4, "Pourquoi ne faut-il jamais mélanger l'eau de Javel avec un détartrant acide ?", "Il se dégage du dichlore, un gaz toxique", "Le mélange devient neutre et ne nettoie plus", "Le mélange gèle", "L'eau de Javel devient de l'eau pure",
 "C'est une cause fréquente d'intoxication à la maison."),
]),

dict(
nom="Électrolyse et synthèse de l'eau",
fiche="""## L'électrolyse de l'eau
• On utilise un électrolyseur relié à un générateur de courant continu.
• On ajoute un peu de soude à l'eau pour la rendre conductrice.
• À la cathode (borne −) se dégage du dihydrogène H₂.
• À l'anode (borne +) se dégage du dioxygène O₂.
• Le volume de dihydrogène est le double du volume de dioxygène.
   2 H₂O → 2 H₂ + O₂

## Identifier les gaz
• Dihydrogène : il produit une petite détonation à l'approche d'une flamme.
• Dioxygène : il ravive une bûchette incandescente (elle se rallume).

## La synthèse de l'eau
Le dihydrogène brûle dans le dioxygène et donne de l'eau :
2 H₂ + O₂ → 2 H₂O
• Les volumes qui réagissent : 2 volumes de H₂ pour 1 volume de O₂.
• Le mélange des deux gaz est explosif : manipulation réservée au laboratoire (eudiomètre).

## Identifier l'eau
Le sulfate de cuivre anhydre, blanc, devient bleu au contact de l'eau.

## Conclusion
L'électrolyse décompose l'eau, la synthèse la reforme : l'eau est un corps composé, formé d'hydrogène et d'oxygène (formule H₂O).

## Exemple corrigé
On fait exploser 40 cm³ de dihydrogène avec 30 cm³ de dioxygène.
40 cm³ de H₂ réagissent avec 20 cm³ de O₂. Il reste 30 − 20 = 10 cm³ de dioxygène.

## Pièges à éviter
• Cathode = borne − = dihydrogène ; anode = borne + = dioxygène.
• C'est le dihydrogène qui a le plus grand volume (le double).""",
questions=[
(1, "Lors de l'électrolyse de l'eau, le gaz qui se dégage à la cathode (borne −) est :", "le dihydrogène", "le dioxygène", "le dioxyde de carbone", "le diazote",
 "Cathode = borne − = dihydrogène, en plus grand volume."),
(1, "Lors de l'électrolyse de l'eau, le gaz qui se dégage à l'anode (borne +) est :", "le dioxygène", "le dihydrogène", "la vapeur d'eau", "le dichlore",
 "Anode = borne + = dioxygène."),
(2, "Lors d'une électrolyse, on recueille 20 cm³ de dihydrogène. Le volume de dioxygène est :", "10 cm³", "20 cm³", "40 cm³", "5 cm³",
 "Le volume de dioxygène est la moitié de celui du dihydrogène."),
(2, "On identifie le dioxygène parce qu'il :", "ravive une bûchette incandescente", "trouble l'eau de chaux", "produit une détonation", "bleuit le sulfate de cuivre anhydre",
 "La bûchette qui rougeoie se rallume dans le dioxygène."),
(2, "On identifie le dihydrogène parce qu'il :", "produit une petite détonation à l'approche d'une flamme", "ravive une bûchette incandescente", "trouble l'eau de chaux", "a une odeur forte",
 "C'est le test caractéristique du dihydrogène."),
(2, "On ajoute un peu de soude à l'eau de l'électrolyseur pour :", "rendre l'eau conductrice", "colorer l'eau", "refroidir l'eau", "produire du dioxyde de carbone",
 "L'eau pure conduit très mal le courant."),
(3, "L'équation de l'électrolyse de l'eau est :", "2 H₂O → 2 H₂ + O₂", "H₂O → H₂ + O₂", "2 H₂ + O₂ → 2 H₂O", "H₂O → 2 H + O",
 "Elle est équilibrée : 4 atomes H et 2 atomes O de chaque côté. 2 H₂ + O₂ → 2 H₂O est la synthèse."),
(3, "Le sulfate de cuivre anhydre permet d'identifier l'eau car :", "il passe du blanc au bleu", "il passe du bleu au blanc", "il fait une détonation", "il trouble",
 "C'est le test de l'eau."),
(3, "Pour la synthèse de l'eau, 30 cm³ de dihydrogène réagissent avec :", "15 cm³ de dioxygène", "30 cm³ de dioxygène", "60 cm³ de dioxygène", "10 cm³ de dioxygène",
 "2 volumes de H₂ pour 1 volume de O₂ : 30 ÷ 2 = 15 cm³."),
(3, "D'après l'électrolyse et la synthèse, l'eau est :", "un corps composé d'hydrogène et d'oxygène", "un corps simple", "un mélange de deux gaz", "un métal",
 "On peut la décomposer en H₂ et O₂, et la reformer à partir d'eux."),
(4, "On fait exploser 40 cm³ de dihydrogène avec 30 cm³ de dioxygène. À la fin, il reste :", "10 cm³ de dioxygène", "10 cm³ de dihydrogène", "aucun gaz", "20 cm³ de dioxygène",
 "40 cm³ de H₂ consomment 20 cm³ de O₂ : il reste 30 − 20 = 10 cm³ de O₂."),
(4, "Le générateur utilisé pour l'électrolyse de l'eau délivre un courant :", "continu", "alternatif", "nul", "variable au hasard",
 "Il faut une borne + et une borne − fixes pour séparer les deux gaz."),
]),

dict(
nom="Les alcanes",
fiche="""## Les hydrocarbures
Ce sont des composés formés uniquement de carbone (C) et d'hydrogène (H). On les trouve dans le pétrole et le gaz naturel.

## Les alcanes
Formule générale : CₙH₂ₙ₊₂.
• Méthane CH₄ : principal constituant du gaz naturel.
• Éthane C₂H₆.
• Propane C₃H₈.
• Butane C₄H₁₀ : le gaz des bouteilles de cuisine.
• Pentane C₅H₁₂.
Le pétrole brut est séparé en coupes (gaz, essence, pétrole lampant, gasoil…) par distillation fractionnée.

## Combustion complète
Avec assez de dioxygène, la flamme est bleue et les produits sont le dioxyde de carbone et l'eau.
• CH₄ + 2 O₂ → CO₂ + 2 H₂O
• C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O
• 2 C₄H₁₀ + 13 O₂ → 8 CO₂ + 10 H₂O
Identification : le CO₂ trouble l'eau de chaux ; l'eau bleuit le sulfate de cuivre anhydre.

## Combustion incomplète
Quand le dioxygène manque, la flamme est jaune et fumante. Il se forme du carbone (suie, qui noircit les marmites) et du monoxyde de carbone CO.
Le monoxyde de carbone est un gaz incolore, inodore et mortel.

## Sécurité à la maison
• Ne jamais laisser un réchaud, un foyer à charbon ou un groupe électrogène fonctionner dans une pièce fermée.
• Bien aérer la cuisine.
• Fermer le robinet de la bouteille de gaz après usage ; vérifier le tuyau.

## Exemple corrigé
Équilibrer la combustion du propane : C₃H₈ + 5 O₂ → 3 CO₂ + … H₂O.
8 atomes H à gauche → 4 H₂O. Oxygène à droite : 6 + 4 = 10, soit 5 O₂. ✔

## Pièges à éviter
• Flamme BLEUE : combustion complète. Flamme JAUNE : combustion incomplète.
• Équilibrer dans l'ordre : C, puis H, puis O.""",
questions=[
(1, "Les alcanes sont formés uniquement :", "de carbone et d'hydrogène", "de carbone et d'oxygène", "d'hydrogène et d'oxygène", "de carbone, d'hydrogène et d'azote",
 "Ce sont des hydrocarbures : C et H seulement."),
(1, "La formule du méthane est :", "CH₄", "C₂H₆", "CH₂", "C₄H₁₀",
 "Le méthane est l'alcane le plus simple : n = 1, donc CH₄."),
(1, "Le gaz des bouteilles de cuisine contient principalement :", "du butane", "du dioxygène", "du dihydrogène", "du dioxyde de carbone",
 "On parle couramment de « gaz butane », de formule C₄H₁₀."),
(2, "La formule générale des alcanes est :", "CₙH₂ₙ₊₂", "CₙH₂ₙ", "CₙHₙ", "CₙH₂ₙ₋₂",
 "Par exemple, pour n = 3 : C₃H₈."),
(2, "La formule du propane est :", "C₃H₈", "C₃H₆", "C₃H₃", "C₈H₃",
 "n = 3, donc 2 × 3 + 2 = 8 atomes d'hydrogène."),
(2, "La combustion complète d'un alcane produit :", "du dioxyde de carbone et de l'eau", "du monoxyde de carbone et de la suie", "du dihydrogène et du dioxygène", "seulement de l'eau",
 "Avec assez de dioxygène, tout le carbone devient CO₂ et tout l'hydrogène devient H₂O."),
(2, "Une flamme bleue indique une combustion :", "complète", "incomplète", "impossible", "sans dioxygène",
 "La flamme jaune et fumante est le signe d'une combustion incomplète."),
(3, "L'équation équilibrée de la combustion complète du méthane est :", "CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄ + O₂ → CO₂ + H₂O", "CH₄ + 2 O₂ → CO + 2 H₂O", "2 CH₄ + O₂ → 2 CO₂ + H₂O",
 "1 C, 4 H et 4 O de chaque côté."),
(3, "Le principal danger d'une combustion incomplète est :", "le monoxyde de carbone, gaz mortel incolore et inodore", "le dioxyde de carbone, qui trouble l'eau de chaux", "la vapeur d'eau", "le dioxygène",
 "Le monoxyde de carbone empêche le sang de transporter le dioxygène."),
(3, "L'alcane qui possède 5 atomes de carbone a pour formule :", "C₅H₁₂", "C₅H₁₀", "C₅H₅", "C₅H₁₁",
 "2 × 5 + 2 = 12 : c'est le pentane."),
(4, "Dans l'équation C₃H₈ + 5 O₂ → 3 CO₂ + … H₂O, le coefficient manquant est :", "4", "3", "8", "5",
 "8 atomes H à gauche, donc 4 molécules H₂O. Vérification de l'oxygène : 6 + 4 = 10 = 5 × 2."),
(4, "Pourquoi ne faut-il jamais faire fonctionner un réchaud à gaz butane dans une pièce fermée ?", "La combustion devient incomplète et produit du monoxyde de carbone", "Le réchaud s'éteint aussitôt", "La pièce se remplit de dihydrogène", "Le butane produit de l'eau de Javel",
 "Sans aération, le dioxygène manque : il se forme du monoxyde de carbone, qui peut tuer pendant le sommeil."),
]),

dict(
nom="Révision BEPC",
fiche="""## Formulaire de Physique-Chimie de 3ème

## Optique
• Vergence : C = 1 ÷ f (C en dioptries δ, f en mètres). C > 0 : convergente ; C < 0 : divergente.
• Rayons particuliers : par O, non dévié ; parallèle à l'axe → passe par F' ; passant par F → ressort parallèle.
• Myopie : voit mal de loin → lentille divergente.
• Hypermétropie et presbytie : voient mal de près → lentille convergente.

## Mécanique
• Poids : P = m × g (g ≈ 10 N/kg)
• Travail : W = F × d ; travail du poids : W = m × g × h (en joules)
• Puissance : P = W ÷ t (en watts)

## Électricité
• Puissance : P = U × I ; conducteur ohmique : P = R × I²
• Énergie : E = P × t (J avec W et s ; kWh avec kW et h)
• 1 kWh = 3 600 000 J
• Coût = énergie en kWh × prix du kWh

## Chimie
• Rouille : fer + dioxygène + eau. Alumine Al₂O₃ : protège l'aluminium.
• 3 Fe + 2 O₂ → Fe₃O₄   2 Cu + O₂ → 2 CuO   4 Al + 3 O₂ → 2 Al₂O₃
• Réduction : 2 CuO + C → 2 Cu + CO₂ (le réducteur est oxydé, l'oxydant est réduit)
• pH < 7 acide ; pH = 7 neutre ; pH > 7 basique. Diluer rapproche le pH de 7.
• Électrolyse : 2 H₂O → 2 H₂ + O₂ ; V(H₂) = 2 × V(O₂)
• Alcanes : CₙH₂ₙ₊₂ ; combustion complète → CO₂ + H₂O

## Les tests à connaître
• Dioxyde de carbone : trouble l'eau de chaux.
• Eau : bleuit le sulfate de cuivre anhydre.
• Dihydrogène : détonation à l'approche d'une flamme.
• Dioxygène : ravive une bûchette incandescente.

## Conseils pour l'épreuve
• Écris toujours la formule littérale, puis le calcul, puis le résultat avec son unité.
• Vérifie les unités avant de calculer : mètres pour la vergence, secondes pour la puissance, kW et heures pour les kWh.
• Pour une équation chimique, compte les atomes de chaque côté avant de passer à la suite.""",
questions=[
(2, "Une lentille a une distance focale de 50 cm. Sa vergence est :", "2 δ", "50 δ", "0,5 δ", "0,02 δ",
 "f = 0,5 m, donc C = 1 ÷ 0,5 = 2 δ."),
(2, "Pour corriger la myopie, on utilise :", "une lentille divergente", "une lentille convergente", "une loupe", "un miroir",
 "L'œil myope est trop convergent."),
(2, "Une force de 30 N déplace son point d'application de 4 m dans sa direction. Le travail est :", "120 J", "7,5 J", "34 J", "26 J",
 "W = F × d = 30 × 4 = 120 J."),
(2, "Un travail de 900 J est effectué en 15 s. La puissance est :", "60 W", "13 500 W", "915 W", "0,016 W",
 "P = W ÷ t = 900 ÷ 15 = 60 W."),
(2, "Avec g = 10 N/kg, le poids d'un élève de 50 kg est :", "500 N", "50 N", "5 N", "60 N",
 "P = m × g = 50 × 10 = 500 N."),
(3, "Un appareil de 2 kW fonctionne pendant 3 h. Il consomme :", "6 kWh", "1,5 kWh", "6 000 kWh", "5 kWh",
 "E = P × t = 2 kW × 3 h = 6 kWh."),
(3, "Un appareil de 1 100 W fonctionne sous 220 V. L'intensité qui le traverse est :", "5 A", "0,2 A", "242 000 A", "880 A",
 "I = P ÷ U = 1 100 ÷ 220 = 5 A."),
(2, "Pour que le fer rouille, il faut :", "du dioxygène et de l'eau", "uniquement de la chaleur", "du dioxyde de carbone seul", "de la lumière seule",
 "La rouille se forme à l'air humide."),
(3, "Dans la réaction 2 CuO + C → 2 Cu + CO₂, le carbone :", "est oxydé", "est réduit", "ne réagit pas", "est l'oxydant",
 "Il gagne de l'oxygène et devient CO₂ : c'est le réducteur, il est oxydé."),
(2, "Une solution de pH 4 est :", "acide", "basique", "neutre", "pure",
 "pH inférieur à 7."),
(3, "Lors d'une électrolyse de l'eau, on recueille 12 cm³ de dioxygène. Le volume de dihydrogène est :", "24 cm³", "6 cm³", "12 cm³", "36 cm³",
 "Le volume de dihydrogène est le double de celui de dioxygène."),
(2, "La formule du butane est :", "C₄H₁₀", "C₄H₈", "C₄H₄", "CH₄",
 "Alcane à 4 carbones : 2 × 4 + 2 = 10 hydrogènes."),
(3, "Une flamme jaune qui noircit les marmites indique :", "une combustion incomplète", "une combustion complète", "l'absence de combustion", "une électrolyse",
 "Le dioxygène manque : il se forme de la suie (carbone) et du monoxyde de carbone."),
(3, "Un objet est placé au-delà de deux fois la distance focale d'une lentille convergente. Son image est :", "réelle, renversée et plus petite", "virtuelle, droite et agrandie", "réelle, droite et plus grande", "rejetée à l'infini",
 "C'est le cas de l'appareil photo et de l'œil."),
(4, "On dilue une solution basique de pH 12. Son pH :", "diminue et se rapproche de 7", "augmente", "devient égal à 7 exactement", "devient acide",
 "La dilution rapproche le pH de 7 sans jamais le dépasser."),
]),
]
