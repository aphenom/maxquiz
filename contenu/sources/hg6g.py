"""Géographie 6ème (même matière que l'histoire : Histoire-Géographie)."""
NIVEAU, MATIERE = "6ème", "Histoire-Géographie"

CHAPITRES = [
dict(
nom="La géographie et son objet",
fiche="""## Définition
La géographie est la science qui décrit et explique les phénomènes physiques et humains à la surface de la Terre, et les relations entre les hommes et leur milieu.
Le mot vient du grec gê (la Terre) et graphein (écrire, dessiner).

## Les branches de la géographie
• La géographie physique : le relief, le climat, les sols, les cours d'eau (hydrographie), la végétation.
• La géographie humaine : la population, les villes et les villages, les migrations.
• La géographie économique : l'agriculture, la pêche, l'industrie, le commerce, les transports.

## La démarche du géographe
1. Observer (sur le terrain, sur une carte, une photographie).
2. Localiser (où ? avec une carte, les points cardinaux).
3. Décrire.
4. Expliquer (pourquoi ?).
5. Comparer avec d'autres régions.

## Les outils
Cartes, plans, globe, photographies, croquis, tableaux de chiffres, graphiques, boussole.

## À quoi sert la géographie ?
À connaître son pays et le monde, à s'orienter, à comprendre comment vivent les autres peuples, à mieux aménager et protéger son environnement.""",
questions=[
(1, "La géographie étudie :", "la surface de la Terre et la vie des hommes dans leur milieu", "seulement le passé des hommes", "les étoiles", "le corps humain",
 "Elle décrit et explique."),
(2, "Le mot « géographie » vient du grec gê qui signifie :", "la Terre", "l'eau", "le soleil", "l'homme",
 "Et graphein : écrire, dessiner."),
(2, "Le relief, le climat et la végétation relèvent de la géographie :", "physique", "humaine", "économique", "historique",
 "Ce sont des éléments naturels."),
(2, "L'étude de la population relève de la géographie :", "humaine", "physique", "astronomique", "géologique",
 "Population, villes, migrations."),
(2, "L'agriculture et le commerce relèvent de la géographie :", "économique", "physique", "religieuse", "médicale",
 "Ce sont des activités de production et d'échange."),
(3, "La première étape de la démarche géographique est :", "observer", "comparer", "expliquer", "conclure",
 "On observe, localise, décrit, explique, compare."),
(3, "Répondre à la question « où ? », c'est :", "localiser", "expliquer", "comparer", "dater",
 "On situe sur une carte."),
(3, "Lequel est un outil du géographe ?", "la carte", "le thermomètre médical", "le microscope de biologie", "le stéthoscope",
 "Avec le globe, les photographies, les croquis."),
(3, "Répondre à la question « pourquoi ? », c'est :", "expliquer", "localiser", "observer", "dessiner",
 "On cherche les causes."),
(4, "Un intérêt de la géographie est de :", "mieux comprendre les autres peuples et protéger l'environnement", "connaître la date des batailles", "soigner les malades", "apprendre une langue étrangère",
 "Elle ouvre l'esprit."),
]),

dict(
nom="Le relief",
fiche="""## Définition
Le relief est l'ensemble des formes (creux et bosses) de la surface de la Terre, sur les continents et au fond des océans.

## Les grandes formes de relief
• La montagne : relief élevé, aux pentes raides et aux vallées profondes. Exemple : les montagnes de l'ouest de la Côte d'Ivoire (région de Man, mont Nimba, 1 752 m).
• Le plateau : surface assez plane située en hauteur, souvent entaillée par des cours d'eau. Exemple : les plateaux du centre et du nord.
• La plaine : surface plane et basse, où les cours d'eau coulent lentement. Exemple : les plaines du sud, près de la côte.
[[schema:formes-relief|Montagne, plateau et plaine]]

## Les formes élémentaires
La colline (sommet arrondi), la butte (sommet plat), la vallée (creux où coule un cours d'eau), la cuvette (creux fermé), le versant (pente d'une vallée).

## Mesurer le relief
• L'altitude : hauteur d'un point par rapport au niveau de la mer (0 m).
• La dénivellation : différence d'altitude entre deux points. Un point à 70 m et un autre à 50 m : dénivellation de 20 m.
• La pente : inclinaison du terrain.

## Le relief et les hommes
Les plaines et les plateaux favorisent l'agriculture, les routes et les villes ; les montagnes rendent les déplacements plus difficiles mais offrent pluies et paysages (tourisme).""",
questions=[
(1, "Le relief est l'ensemble :", "des formes de la surface de la Terre", "des cours d'eau", "des villes", "des pluies",
 "Creux et bosses."),
(2, "Une surface plane et basse, près de la mer, est :", "une plaine", "une montagne", "un plateau", "une colline",
 "Les cours d'eau y coulent lentement."),
(2, "Un relief élevé aux pentes raides est :", "une montagne", "une plaine", "une cuvette", "une lagune",
 "Exemple : la région de Man."),
(2, "Une surface assez plane, située en hauteur, est :", "un plateau", "une plaine", "une vallée", "une cuvette",
 "Les cours d'eau l'entaillent."),
(2, "L'altitude se mesure à partir :", "du niveau de la mer", "du sommet le plus haut", "du centre de la Terre", "du sol de la classe",
 "Le niveau de la mer est à 0 m."),
(3, "Un point est à 70 m, un autre à 50 m. La dénivellation est :", "20 m", "120 m", "50 m", "70 m",
 "70 − 50."),
(3, "Un creux allongé où coule un cours d'eau s'appelle :", "une vallée", "une butte", "un plateau", "un sommet",
 "Ses pentes sont les versants."),
(3, "Une colline au sommet plat s'appelle :", "une butte", "une vallée", "une cuvette", "une plaine",
 "La colline a un sommet arrondi."),
(3, "Le point culminant de la Côte d'Ivoire est :", "le mont Nimba", "le mont Cameroun", "le Kilimandjaro", "le plateau de Bouaké",
 "1 752 m, à l'ouest."),
(4, "Pourquoi les grandes villes s'installent-elles souvent en plaine ?", "le terrain plat facilite la construction et les transports", "il y fait toujours froid", "il n'y a jamais d'eau", "les montagnes sont interdites",
 "Le relief influence l'installation des hommes."),
(2, "Sur le schéma, le relief le plus bas, près de la mer, est :", "la plaine", "la montagne", "le plateau", "la colline",
 "Altitude proche de 0 m.", "formes-relief"),
]),

dict(
nom="Le climat",
fiche="""## Définition
Le climat est l'état moyen de l'atmosphère (températures, pluies, vents) dans une région, observé sur une longue période (au moins 30 ans). Il ne faut pas le confondre avec le temps qu'il fait un jour donné (la météo).

## Les éléments du climat et leurs instruments
• La température : le thermomètre (°C).
• Les précipitations (pluie, grêle, neige) : le pluviomètre (en millimètres).
• Le vent : la girouette (direction) et l'anémomètre (vitesse).
• La pression atmosphérique : le baromètre.

## Les vents en Côte d'Ivoire
• L'harmattan : vent sec et poussiéreux venu du Sahara (nord-est), en saison sèche.
• La mousson : vent humide venu de l'océan (sud-ouest), qui apporte les pluies.

## Les grandes zones climatiques du monde
• La zone chaude (entre les deux tropiques) : climats équatorial (pluvieux toute l'année), tropical (une saison des pluies et une saison sèche), désertique (très peu de pluie).
• Les zones tempérées : quatre saisons (printemps, été, automne, hiver).
• Les zones froides (près des pôles) : un long hiver et un court été.
La Côte d'Ivoire est dans la zone chaude.

## Lire et calculer
• Amplitude thermique = température la plus élevée − température la plus basse. Exemple : 29 °C − 24,7 °C = 4,3 °C.
• Le diagramme ombrothermique montre les pluies (bâtons) et les températures (courbe) mois par mois.""",
questions=[
(1, "L'instrument qui mesure les pluies est :", "le pluviomètre", "le thermomètre", "le baromètre", "l'anémomètre",
 "Il mesure en millimètres."),
(1, "L'instrument qui mesure la vitesse du vent est :", "l'anémomètre", "le pluviomètre", "le thermomètre", "la balance",
 "La girouette indique sa direction."),
(2, "Le climat se définit sur :", "une longue période", "une seule journée", "une heure", "une semaine",
 "Au moins 30 ans d'observations."),
(2, "L'harmattan est un vent :", "sec et poussiéreux venu du Sahara", "humide venu de l'océan", "froid venu du pôle", "chaud venu de la lagune",
 "Il souffle en saison sèche."),
(2, "La Côte d'Ivoire se trouve dans la zone :", "chaude", "tempérée", "froide", "polaire",
 "Entre les tropiques."),
(3, "Dans les zones tempérées, on compte :", "quatre saisons", "une seule saison", "deux saisons sèches seulement", "aucune saison",
 "Printemps, été, automne, hiver."),
(3, "Le mois le plus chaud fait 29 °C, le plus frais 24,7 °C. L'amplitude thermique est :", "4,3 °C", "53,7 °C", "24,7 °C", "5,3 °C",
 "29 − 24,7."),
(3, "La mousson apporte :", "les pluies", "la neige", "la sécheresse", "la poussière du désert",
 "Elle vient de l'océan."),
(3, "Dans un diagramme ombrothermique, les pluies sont représentées par :", "des bâtons", "une courbe", "des points", "un cercle",
 "Les températures par une courbe."),
(4, "« Aujourd'hui il pleut à Abidjan » décrit :", "le temps qu'il fait (météo)", "le climat", "le relief", "la végétation",
 "Le climat est une moyenne sur une longue période."),
]),

dict(
nom="Le sol, le climat et la végétation",
fiche="""## Définitions
• La végétation est l'ensemble des plantes (arbres, herbes, lianes) qui poussent dans une région.
• Le sol est la couche superficielle de la terre, où poussent les plantes et vivent de nombreux êtres vivants.

## Les végétations de Côte d'Ivoire
• La forêt dense (beaucoup de grands arbres serrés) : au sud et à l'ouest.
• La forêt claire et la savane arborée : au centre.
• La savane (plus d'herbes que d'arbres) : au nord.

## Les sols de Côte d'Ivoire
• Les sols ferralitiques : épais, rougeâtres, au sud et à l'ouest ; cultures de cacao, café, palmier à huile, hévéa, banane.
• Les sols ferrugineux : moins épais et moins riches, au centre et au nord ; cultures de coton, anacarde, igname, maïs, arachide, mil.
• Les sols hydromorphes : gorgés d'eau, dans les bas-fonds et près des lagunes ; riziculture.

## Les climats de Côte d'Ivoire
Attiéen au sud (très pluvieux), baouléen au centre, soudanien au nord (sec), climat de montagne à l'ouest.

## Les relations entre sol, climat et végétation
• Climat humide + sol riche → végétation dense (forêt).
• Climat plus sec + sol pauvre → végétation clairsemée (savane).
• La végétation protège le sol et l'enrichit en humus ; si on la détruit (déforestation, feux de brousse), le sol s'appauvrit et s'érode.""",
questions=[
(1, "La forêt dense se trouve surtout :", "au sud et à l'ouest", "au nord", "dans le désert", "sur les plages uniquement",
 "Là où il pleut beaucoup."),
(2, "La savane se caractérise par :", "plus d'herbes que d'arbres", "plus d'arbres que d'herbes", "aucune plante", "des arbres serrés et très hauts",
 "On la trouve au nord."),
(2, "Les sols ferralitiques sont :", "épais et rougeâtres", "gorgés d'eau en permanence", "inexistants en Côte d'Ivoire", "blancs et sableux",
 "Au sud et à l'ouest."),
(2, "Le cacao est cultivé surtout sur les sols :", "ferralitiques", "ferrugineux du nord", "du désert", "gelés",
 "Dans la zone forestière."),
(2, "Les sols gorgés d'eau des bas-fonds sont dits :", "hydromorphes", "ferralitiques", "ferrugineux", "désertiques",
 "On y cultive le riz."),
(3, "Le climat du nord de la Côte d'Ivoire est :", "soudanien", "attiéen", "équatorial", "polaire",
 "Plus sec, avec une longue saison sèche."),
(3, "Un climat humide et un sol riche donnent :", "une forêt dense", "un désert", "une savane herbeuse", "une banquise",
 "La végétation est abondante."),
(3, "La végétation protège le sol car elle :", "l'enrichit en humus et le retient", "le rend plus sec", "le pollue", "le fait disparaître",
 "Ses racines retiennent la terre."),
(3, "Le coton est cultivé surtout :", "au centre et au nord", "dans la lagune", "en forêt dense", "sur la côte",
 "Sur les sols ferrugineux."),
(4, "Quand on détruit la forêt, le sol :", "s'appauvrit et s'érode", "devient plus fertile", "se couvre de neige", "ne change pas",
 "La pluie emporte la terre nue."),
]),

dict(
nom="Représenter la Terre : globe, cartes et échelle",
fiche="""## La Terre et le globe
La Terre est une sphère légèrement aplatie aux pôles. Le globe terrestre la représente en réduction, sans déformer les formes.

## Les lignes imaginaires
• L'équateur partage la Terre en deux hémisphères : nord et sud.
• Les parallèles sont des cercles parallèles à l'équateur : tropique du Cancer (nord), tropique du Capricorne (sud), cercles polaires.
• Les méridiens sont des demi-cercles qui joignent les deux pôles ; le méridien de Greenwich est le méridien d'origine (0°).
• La latitude d'un lieu est sa distance angulaire à l'équateur (nord ou sud) ; sa longitude, sa distance au méridien de Greenwich (est ou ouest).
• La Côte d'Ivoire est dans l'hémisphère nord, entre environ 4° et 11° de latitude nord.
[[schema:globe-reperes|Les principales lignes du globe]]

## Les cartes
• Une carte représente tout ou partie de la Terre sur une surface plane (ce qui déforme un peu les formes).
• Le planisphère représente toute la Terre sur une seule carte.
• Les éléments d'une carte : un titre, une légende (les signes et couleurs utilisés), une échelle, l'orientation (la flèche du nord).

## L'échelle
Elle indique le rapport entre une distance sur la carte et la distance réelle.
• Échelle numérique : 1/100 000 signifie que 1 cm sur la carte = 100 000 cm = 1 km en réalité.
• Calcul : distance réelle = distance sur la carte × dénominateur de l'échelle. 5 cm à 1/100 000 → 500 000 cm = 5 km.
• Échelle graphique : un segment gradué (par exemple 1 cm = 10 km).""",
questions=[
(1, "La ligne qui partage la Terre en hémisphère nord et hémisphère sud est :", "l'équateur", "le méridien de Greenwich", "le tropique du Cancer", "le cercle polaire",
 "C'est la latitude 0°."),
(2, "Le méridien d'origine (0°) est le méridien de :", "Greenwich", "Abidjan", "Paris", "l'équateur",
 "Les longitudes se comptent à partir de lui."),
(2, "Une carte qui représente toute la Terre s'appelle :", "un planisphère", "un plan de ville", "un croquis de quartier", "une légende",
 "Le monde entier sur une seule carte."),
(2, "La partie de la carte qui explique les signes et les couleurs est :", "la légende", "le titre", "l'échelle", "l'orientation",
 "Elle permet de lire la carte."),
(2, "La Côte d'Ivoire est située dans l'hémisphère :", "nord", "sud", "est uniquement", "aucun",
 "Entre environ 4° et 11° de latitude nord."),
(3, "À l'échelle 1/100 000, 1 cm sur la carte représente :", "1 km", "100 m", "10 km", "100 km",
 "100 000 cm = 1 km."),
(3, "À l'échelle 1/100 000, 5 cm sur la carte représentent :", "5 km", "500 m", "50 km", "0,5 km",
 "5 × 100 000 cm = 500 000 cm = 5 km."),
(3, "Les demi-cercles qui joignent les deux pôles sont :", "les méridiens", "les parallèles", "les tropiques", "les équateurs",
 "Les parallèles sont parallèles à l'équateur."),
(3, "La distance d'un lieu par rapport à l'équateur s'appelle :", "la latitude", "la longitude", "l'altitude", "l'échelle",
 "Elle est nord ou sud."),
(4, "Pourquoi une carte déforme-t-elle un peu la Terre ?", "on représente une sphère sur une surface plane", "les cartographes se trompent", "la Terre est plate", "les couleurs sont fausses",
 "Seul le globe ne déforme pas les formes."),
(2, "Sur le schéma, la ligne située au nord de l'équateur dans la zone chaude est :", "le tropique du Cancer", "le tropique du Capricorne", "le cercle polaire antarctique", "le méridien de Greenwich",
 "Le tropique du Capricorne est au sud.", "globe-reperes"),
]),

dict(
nom="Les mouvements de la Terre",
fiche="""## La Terre dans le système solaire
La Terre est la troisième planète en partant du Soleil. Elle a deux mouvements.

## La rotation
• La Terre tourne sur elle-même, d'ouest en est, autour d'un axe qui passe par les pôles, en 24 heures (une journée).
• Conséquences :
  – la succession du jour (face éclairée) et de la nuit (face dans l'ombre) ;
  – le Soleil semble se lever à l'est et se coucher à l'ouest ;
  – les heures ne sont pas les mêmes partout : la Terre est découpée en 24 fuseaux horaires d'une heure. La Côte d'Ivoire est à l'heure de Greenwich (GMT, UTC+0).
• Les points cardinaux : nord, sud, est, ouest ; pour s'orienter, le Soleil se lève à l'est.

## La révolution
• La Terre tourne autour du Soleil en un an : 365 jours et environ 6 heures. Tous les 4 ans, on ajoute un jour : l'année bissextile compte 366 jours (29 février).
• L'axe de la Terre est incliné : les rayons du Soleil n'arrivent pas de la même façon toute l'année.
• Conséquences : la durée du jour et de la nuit varie selon les saisons (surtout loin de l'équateur) ; la succession des saisons.
Près de l'équateur, comme en Côte d'Ivoire, le jour et la nuit durent environ 12 heures toute l'année.""",
questions=[
(1, "La Terre tourne sur elle-même en :", "24 heures", "365 jours", "un mois", "une semaine",
 "C'est la rotation."),
(1, "La Terre tourne autour du Soleil en :", "un an", "24 heures", "un mois", "dix ans",
 "C'est la révolution."),
(2, "La succession du jour et de la nuit est due à :", "la rotation de la Terre", "la révolution de la Terre", "la Lune", "les nuages",
 "Une face est éclairée, l'autre dans l'ombre."),
(2, "Le Soleil se lève :", "à l'est", "à l'ouest", "au nord", "au sud",
 "La Terre tourne d'ouest en est."),
(2, "La Terre est la planète numéro … en partant du Soleil :", "3", "1", "5", "9",
 "Après Mercure et Vénus."),
(3, "Une année bissextile compte :", "366 jours", "365 jours", "360 jours", "364 jours",
 "On ajoute le 29 février tous les 4 ans."),
(3, "Le nombre de fuseaux horaires sur la Terre est :", "24", "12", "365", "4",
 "Un fuseau par heure."),
(3, "La Côte d'Ivoire est à l'heure :", "de Greenwich (GMT)", "de Paris en hiver", "de New York", "de Tokyo",
 "UTC+0."),
(3, "La succession des saisons est due à :", "la révolution et l'inclinaison de l'axe de la Terre", "la rotation seule", "la Lune", "les vents",
 "Les rayons du Soleil changent d'inclinaison au cours de l'année."),
(4, "Près de l'équateur, comme en Côte d'Ivoire, le jour dure :", "environ 12 heures toute l'année", "24 heures en été", "6 heures en hiver", "presque rien en décembre",
 "Les variations sont faibles près de l'équateur."),
]),

dict(
nom="Population et environnement local",
fiche="""## Définitions
• La population est l'ensemble des personnes qui vivent dans un espace donné.
• L'environnement est l'ensemble des éléments naturels et humains qui nous entourent.

## L'exemple du district d'Abidjan
• Un milieu favorable : relief bas (plateaux et cordon littoral) facile à aménager, climat chaud et humide (attiéen), lagune Ébrié et mer, ressources (pétrole et gaz au large).
• Un grand port, des industries, des services : beaucoup de personnes viennent y vivre et travailler.

## Les effets de la forte croissance de la population
Quartiers précaires, constructions dans des zones dangereuses, manque de logements, d'écoles et d'hôpitaux, embouteillages, insalubrité, inondations, pollution.

## Les activités qui dégradent l'environnement
Déforestation pour l'agriculture et le bois, feux de brousse, chasse et pêche excessives, ordures et eaux usées, fumées des usines et des véhicules, exploitation minière sauvage, extraction de sable sur les plages.

## Les solutions
Reboisement, parcs nationaux et réserves, ramassage et recyclage des ordures, assainissement, utilisation du gaz domestique à la place du bois, sensibilisation, maîtrise de la croissance des villes.""",
questions=[
(1, "L'ensemble des personnes qui vivent dans un espace est :", "la population", "l'environnement", "le relief", "le climat",
 "On la compte lors des recensements."),
(2, "Un élément favorable à l'installation des hommes à Abidjan est :", "la lagune et la mer", "la neige", "le désert", "les hautes montagnes",
 "Pêche, port, transport."),
(2, "Une conséquence de la forte croissance de la population en ville est :", "les embouteillages", "la disparition des écoles", "la baisse des besoins", "la fin du commerce",
 "Et les quartiers précaires."),
(2, "Une activité qui dégrade l'environnement est :", "la déforestation", "le reboisement", "le recyclage", "l'assainissement",
 "On coupe les arbres."),
(2, "Une solution pour protéger l'environnement est :", "le reboisement", "les feux de brousse", "l'extraction de sable des plages", "les dépôts d'ordures",
 "On replante des arbres."),
(3, "Utiliser le gaz domestique plutôt que le bois permet :", "de réduire la déforestation", "d'augmenter les feux de brousse", "de polluer la lagune", "de détruire les parcs",
 "On coupe moins d'arbres."),
(3, "Construire dans des zones dangereuses expose surtout :", "aux inondations et aux glissements de terrain", "à la neige", "au gel", "aux éruptions volcaniques",
 "Surtout en saison des pluies."),
(3, "Extraire le sable des plages provoque :", "l'érosion du littoral", "plus de plages", "la baisse des pluies", "le froid",
 "La mer avance sur la côte."),
(3, "Le climat d'Abidjan est :", "attiéen (chaud et humide)", "soudanien (sec)", "désertique", "polaire",
 "C'est le climat du sud."),
(4, "Pourquoi beaucoup de personnes viennent-elles vivre à Abidjan ?", "pour le port, les industries et les emplois", "pour la neige", "pour les montagnes", "parce qu'il n'y a pas de bruit",
 "Les activités économiques attirent la population."),
]),

dict(
nom="L'homme et le cycle de l'eau",
fiche="""## Définition
Le cycle de l'eau est le mouvement permanent de l'eau entre les océans, l'atmosphère et les continents. L'eau change d'état mais ne disparaît pas.

## Les étapes
1. L'évaporation : sous l'effet de la chaleur du Soleil, l'eau des océans, des lacs, des fleuves et des plantes devient vapeur.
2. La condensation : en s'élevant, la vapeur se refroidit et forme de fines gouttelettes : les nuages.
3. Les précipitations : l'eau retombe sous forme de pluie, de grêle ou de neige.
4. Le ruissellement : une partie de l'eau coule à la surface vers les rivières, les fleuves et la mer.
5. L'infiltration : une autre partie pénètre dans le sol et forme les nappes souterraines.
[[schema:cycle-eau|Le cycle de l'eau]]

## L'homme et l'eau
• Usages : boire, cuisiner, se laver, irriguer les cultures, abreuver le bétail, produire de l'électricité (barrages), pêcher, transporter.
• L'eau potable est précieuse : le gaspillage et la pollution menacent les réserves.
• Une mauvaise gestion entraîne pénuries, maladies et conflits.

## Les bons gestes
Fermer les robinets, réparer les fuites, récupérer l'eau de pluie, ne pas jeter les ordures dans les cours d'eau, protéger les sources et les forêts.""",
questions=[
(1, "Sous l'effet de la chaleur, l'eau des océans devient vapeur : c'est :", "l'évaporation", "la condensation", "l'infiltration", "le ruissellement",
 "Première étape du cycle."),
(2, "La formation des nuages correspond à :", "la condensation", "l'évaporation", "l'infiltration", "le ruissellement",
 "La vapeur se refroidit en gouttelettes."),
(2, "L'eau qui coule à la surface du sol vers les rivières :", "ruisselle", "s'infiltre", "s'évapore", "se condense",
 "C'est le ruissellement."),
(2, "L'eau qui pénètre dans le sol forme :", "les nappes souterraines", "les nuages", "la grêle", "les vagues",
 "C'est l'infiltration."),
(2, "La pluie, la grêle et la neige sont des :", "précipitations", "évaporations", "infiltrations", "condensations",
 "L'eau retombe des nuages."),
(3, "Le moteur du cycle de l'eau est :", "la chaleur du Soleil", "le vent seul", "la Lune", "les montagnes",
 "Elle provoque l'évaporation."),
(3, "Produire de l'électricité avec l'eau d'un barrage est un usage :", "énergétique", "domestique", "agricole", "touristique",
 "Comme à Kossou ou Soubré."),
(3, "Dans le cycle de l'eau, l'eau :", "change d'état mais ne disparaît pas", "disparaît chaque année", "se crée dans les nuages à partir de rien", "reste toujours liquide",
 "Elle circule en permanence."),
(3, "Un bon geste pour économiser l'eau est :", "réparer les fuites", "laisser couler le robinet", "laver la cour au tuyau chaque jour", "jeter les ordures dans la rivière",
 "Et récupérer l'eau de pluie."),
(4, "Pourquoi protéger les forêts aide-t-il le cycle de l'eau ?", "les arbres favorisent l'infiltration et les pluies", "les arbres boivent toute l'eau", "les forêts empêchent la pluie", "cela n'a aucun lien",
 "La forêt retient l'eau et rejette de la vapeur."),
(2, "Sur le schéma, la flèche qui descend des nuages représente :", "les précipitations", "l'évaporation", "l'infiltration", "la condensation",
 "La pluie retombe sur le sol et la mer.", "cycle-eau"),
]),

dict(
nom="L'impôt et le développement de ma région",
fiche="""## Définition
L'impôt est une somme d'argent que les habitants et les entreprises versent obligatoirement à l'État et aux collectivités (région, commune) pour financer les dépenses publiques. Celui qui paie l'impôt est le contribuable.

## Les formes d'impôt
• Impôts directs : payés directement par le contribuable sur ses revenus ou ses biens (impôt sur le salaire, impôt foncier sur les maisons et terrains, patente des commerçants).
• Impôts indirects : inclus dans le prix des produits (TVA, taxes sur les carburants, timbres).
• Taxes communales : taxes de marché, d'enlèvement des ordures.

## À quoi sert l'impôt dans ma région ?
Construire et entretenir les écoles, les centres de santé et les hôpitaux, les routes et les ponts, les marchés, l'éclairage public, l'adduction d'eau ; payer les enseignants, les médecins, les policiers ; offrir des bourses.

## Qui collecte l'impôt ?
La Direction générale des impôts (DGI) ; elle informe et sensibilise aussi les contribuables. Les communes et les régions perçoivent les taxes locales.

## Le rôle du citoyen
Payer ses impôts à temps, refuser la fraude, protéger les équipements publics, sensibiliser son entourage : « Payer ses impôts, c'est construire son pays. »""",
questions=[
(1, "La personne qui paie l'impôt s'appelle :", "le contribuable", "le maire", "le percepteur", "le préfet",
 "Elle contribue aux dépenses publiques."),
(2, "La TVA est un impôt :", "indirect", "direct", "communal facultatif", "interdit",
 "Elle est incluse dans le prix des produits."),
(2, "L'impôt payé sur les maisons et les terrains est :", "l'impôt foncier", "la TVA", "la taxe sur les carburants", "le timbre",
 "C'est un impôt direct."),
(2, "L'organisme qui collecte la plupart des impôts est :", "la DGI", "la SODECI", "la CIE", "l'UNICEF",
 "Direction générale des impôts."),
(2, "Lequel est financé par l'impôt ?", "l'éclairage public", "le téléphone d'un particulier", "la fête d'anniversaire d'un voisin", "la voiture d'un commerçant",
 "C'est un équipement public."),
(3, "La taxe de marché est perçue par :", "la commune", "la CEDEAO", "une banque", "l'ONU",
 "C'est une taxe locale."),
(3, "La patente est payée par :", "les commerçants et les entreprises", "les élèves", "les nouveau-nés", "les touristes seulement",
 "Pour exercer une activité."),
(3, "Ne pas payer ses impôts a pour conséquence :", "moins d'écoles, de routes et d'hôpitaux", "plus d'infrastructures", "des salaires plus élevés", "aucune conséquence",
 "L'État et la commune manquent de moyens."),
(3, "« Payer ses impôts, c'est construire son pays » est :", "un slogan de civisme fiscal", "une loi de la route", "un proverbe sur l'eau", "une règle de football",
 "Il encourage le paiement de l'impôt."),
(4, "Un commerçant qui cache une partie de ses ventes pour payer moins d'impôts commet :", "une fraude fiscale", "un acte civique", "une économie légale", "un don",
 "La fraude est punie par la loi."),
]),

dict(
nom="Révision de géographie",
fiche="""## Les bases
• La géographie étudie la surface de la Terre et la vie des hommes ; branches physique, humaine, économique ; démarche : observer, localiser, décrire, expliquer, comparer.
• Relief : montagne, plateau, plaine ; altitude (par rapport au niveau de la mer), dénivellation.
• Climat : thermomètre, pluviomètre, anémomètre, baromètre ; harmattan et mousson ; zones chaude, tempérées, froides ; amplitude thermique.
• Sol, climat, végétation : forêt dense au sud (sols ferralitiques), savane au nord (sols ferrugineux), sols hydromorphes des bas-fonds.
• Globe et cartes : équateur, tropiques, méridien de Greenwich, latitude, longitude ; légende, échelle (1/100 000 : 1 cm = 1 km).
• Rotation (24 h : jour et nuit) ; révolution (365 jours ¼ : saisons) ; GMT.

## L'homme et son milieu
• Population et environnement à Abidjan ; dégradations et solutions.
• Cycle de l'eau : évaporation, condensation, précipitations, ruissellement, infiltration.
• L'impôt : direct, indirect, taxes communales ; DGI ; il finance les équipements de la région.""",
questions=[
(2, "La vitesse du vent se mesure avec :", "un anémomètre", "un pluviomètre", "un baromètre", "un thermomètre",
 "La girouette donne la direction."),
(2, "La succession des saisons est due à :", "la révolution de la Terre et l'inclinaison de son axe", "la rotation seule", "le vent", "la Lune",
 "La Terre tourne autour du Soleil en un an."),
(2, "La savane se trouve surtout :", "au nord de la Côte d'Ivoire", "au sud-ouest", "sur la lagune", "dans la région de Man uniquement",
 "Climat soudanien, plus sec."),
(3, "À l'échelle 1/50 000, 2 cm sur la carte représentent :", "1 km", "100 m", "10 km", "2 km",
 "2 × 50 000 = 100 000 cm = 1 km."),
(3, "Un sommet à 300 m et une vallée à 120 m : la dénivellation est :", "180 m", "420 m", "120 m", "300 m",
 "300 − 120."),
(3, "La formation des nuages s'appelle :", "la condensation", "l'infiltration", "la précipitation", "le ruissellement",
 "La vapeur se refroidit."),
(3, "La patente est un impôt :", "direct", "indirect", "sur les carburants", "interdit",
 "Payé directement par le commerçant."),
(3, "L'équateur correspond à la latitude :", "0°", "90°", "23°", "180°",
 "Les pôles sont à 90°."),
(4, "Un mois à 30 °C et un mois à 18 °C : l'amplitude thermique est :", "12 °C", "48 °C", "24 °C", "18 °C",
 "30 − 18."),
(4, "Pourquoi le sud de la Côte d'Ivoire est-il couvert de forêt dense ?", "pluies abondantes et sols épais", "climat sec et sols pauvres", "présence de neige", "altitude très élevée",
 "Climat attiéen et sols ferralitiques."),
]),
]
