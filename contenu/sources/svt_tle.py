NIVEAU, MATIERE = "Tle C", "SVT"
NIVEAUX = ["Tle C", "Tle D"]

CHAPITRES = [
dict(
nom="La cellule et ses échanges",
fiche="""## Organisation de la cellule
• Membrane plasmique : double couche de phospholipides avec des protéines ; elle contrôle les échanges.
• Cytoplasme avec ses organites : mitochondries (respiration), réticulum endoplasmique et ribosomes (synthèse des protéines), appareil de Golgi (maturation et sécrétion).
• Noyau : contient l'ADN.
• En plus, dans la cellule végétale : paroi pectocellulosique, chloroplastes, grande vacuole.

## Les échanges membranaires
• Diffusion simple : du milieu le plus concentré vers le moins concentré, sans énergie (O₂, CO₂).
• Osmose : passage de l'eau vers le milieu le plus concentré (hypertonique).
   Milieu hypotonique : la cellule animale gonfle et peut éclater ; la cellule végétale devient turgescente.
   Milieu hypertonique : plasmolyse (la cellule perd de l'eau).
• Transport actif : contre le gradient, avec consommation d'ATP (pompe Na⁺/K⁺).
• Endocytose et exocytose : entrée ou sortie de grosses molécules par des vésicules.

## Énergie cellulaire
• Respiration (mitochondrie) : glucose + 6 O₂ → 6 CO₂ + 6 H₂O + énergie ; environ 36 ATP par glucose.
• Fermentation (sans O₂, dans le cytoplasme) : environ 2 ATP par glucose ; lactique dans le muscle, alcoolique chez la levure.
• L'ATP est la molécule qui fournit l'énergie aux activités cellulaires (contraction, transport actif).""",
questions=[
(1, "L'organite où se déroule la respiration cellulaire est :", "la mitochondrie", "le noyau", "le chloroplaste", "l'appareil de Golgi",
 "Le cycle de Krebs et la chaîne respiratoire y ont lieu."),
(1, "La paroi pectocellulosique est présente chez :", "la cellule végétale", "la cellule animale", "les globules rouges", "les neurones",
 "Elle rigidifie la cellule végétale."),
(2, "Une cellule végétale placée dans un milieu hypertonique :", "se plasmolyse", "devient turgescente", "éclate", "ne change pas",
 "Elle perd son eau par osmose vers le milieu plus concentré."),
(2, "Un globule rouge placé dans de l'eau distillée :", "gonfle et peut éclater", "se ratatine", "reste identique", "se divise",
 "L'eau distillée est hypotonique : l'eau entre dans la cellule."),
(2, "Le transport actif se fait :", "contre le gradient de concentration, avec de l'ATP", "sans énergie", "uniquement pour l'eau", "par simple diffusion",
 "Exemple : la pompe sodium-potassium."),
(2, "La molécule qui fournit directement l'énergie aux activités cellulaires est :", "l'ATP", "le glucose", "l'ADN", "l'oxygène",
 "Son hydrolyse libère de l'énergie utilisable."),
(3, "La respiration produit, par molécule de glucose, environ :", "36 ATP", "2 ATP", "100 ATP", "6 ATP",
 "Bien plus que la fermentation."),
(3, "La fermentation lactique se produit dans le muscle lorsque :", "l'apport en oxygène est insuffisant", "il y a trop d'oxygène", "le muscle est au repos", "la glycémie est élevée",
 "Lors d'un effort intense, le muscle produit de l'acide lactique."),
(3, "L'osmose est le passage :", "de l'eau à travers une membrane vers le milieu le plus concentré", "des ions vers le milieu le moins concentré", "des protéines par des vésicules", "du glucose avec de l'ATP",
 "L'eau va du milieu hypotonique vers le milieu hypertonique."),
(4, "La sortie d'hormones protéiques hors de la cellule se fait par :", "exocytose", "endocytose", "osmose", "diffusion simple",
 "Des vésicules issues de l'appareil de Golgi fusionnent avec la membrane."),
(4, "La levure placée sans oxygène dans une solution sucrée produit :", "de l'éthanol et du CO₂", "de l'acide lactique seulement", "de l'O₂", "de l'amidon",
 "C'est la fermentation alcoolique."),
]),

dict(
nom="ADN et synthèse des protéines",
fiche="""## L'ADN
Double hélice de nucléotides ; quatre bases : A, T, C, G. Complémentarité : A avec T, C avec G.
Un gène est une portion d'ADN qui code une protéine.

## Réplication (avant la division)
Semi-conservative : chaque brin sert de modèle à un nouveau brin complémentaire (enzyme : ADN polymérase).

## Transcription (dans le noyau)
Un brin d'ADN est copié en ARN messager (ARNm). Dans l'ARN, U (uracile) remplace T.
ADN transcrit : TAC GGA → ARNm : AUG CCU.

## Traduction (dans le cytoplasme, sur les ribosomes)
L'ARNm est lu par codons (3 nucléotides). Chaque codon correspond à un acide aminé selon le code génétique.
• Codon d'initiation : AUG (méthionine). Codons stop : UAA, UAG, UGA.
• Le code est universel et redondant (plusieurs codons pour un même acide aminé).
Les ARN de transfert apportent les acides aminés ; le ribosome les assemble en chaîne.

## Mutations
Modification de la séquence d'ADN : substitution, délétion, insertion.
• Substitution : peut être silencieuse (même acide aminé), faux-sens, ou non-sens (codon stop).
• Délétion ou insertion d'un nucléotide : décalage du cadre de lecture.
Exemple : la drépanocytose est due à une substitution (acide glutamique remplacé par la valine dans l'hémoglobine).

## Relation gène – protéine – caractère
Un gène → une protéine → un caractère (couleur, groupe sanguin, maladie…).""",
questions=[
(1, "Dans l'ADN, l'adénine s'associe avec :", "la thymine", "la cytosine", "la guanine", "l'uracile",
 "Complémentarité A–T et C–G."),
(1, "La transcription a lieu :", "dans le noyau", "dans le cytoplasme sur les ribosomes", "dans la mitochondrie uniquement", "dans la membrane",
 "L'ARNm est ensuite exporté vers le cytoplasme."),
(2, "Le brin d'ADN transcrit TAC GGA donne l'ARNm :", "AUG CCU", "ATG CCT", "UAC GGA", "AUG GGU",
 "On prend les complémentaires, avec U à la place de T."),
(2, "Un codon est formé de :", "3 nucléotides", "2 nucléotides", "1 nucléotide", "4 nucléotides",
 "Le code génétique est lu par triplets."),
(2, "Le codon d'initiation de la traduction est :", "AUG", "UAA", "UGA", "GGG",
 "Il code la méthionine."),
(2, "La réplication de l'ADN est dite semi-conservative car :", "chaque molécule fille garde un brin de la molécule mère", "l'ADN est entièrement détruit", "seul un gène est copié", "elle se fait dans le cytoplasme",
 "Chaque double hélice fille contient un brin ancien et un brin nouveau."),
(3, "La traduction se déroule :", "dans le cytoplasme, sur les ribosomes", "dans le noyau", "dans l'appareil de Golgi uniquement", "dans la mitochondrie",
 "Les ribosomes assemblent les acides aminés."),
(3, "Le code génétique est dit redondant car :", "plusieurs codons peuvent coder le même acide aminé", "il change selon les espèces", "chaque codon code plusieurs acides aminés", "il n'a pas de codon stop",
 "61 codons codent seulement 20 acides aminés (les 3 autres sont des codons stop)."),
(3, "La drépanocytose est due à :", "une substitution d'un nucléotide dans le gène de l'hémoglobine", "une absence de chromosome", "un virus", "un manque de fer",
 "Un acide aminé est changé : l'hémoglobine S déforme les globules rouges."),
(4, "La délétion d'un nucléotide au début d'un gène entraîne généralement :", "un décalage du cadre de lecture", "aucun changement", "une substitution silencieuse", "l'ajout d'un chromosome",
 "Tous les codons suivants sont modifiés."),
(4, "Une mutation qui transforme un codon en UAA provoque :", "l'arrêt prématuré de la traduction", "l'ajout d'un acide aminé", "une protéine plus longue", "aucun effet",
 "UAA est un codon stop : la protéine est raccourcie."),
]),

dict(
nom="La reproduction : gamètes, méiose et fécondation",
fiche="""## Gamétogenèse
• Spermatogenèse (dans les tubes séminifères du testicule), en continu dès la puberté : multiplication, accroissement, maturation (méiose), différenciation (spermiogenèse).
   Un spermatocyte I donne, par méiose, 4 spermatides qui deviennent 4 spermatozoïdes.
• Ovogenèse (dans l'ovaire) : commence avant la naissance, se bloque, reprend à chaque cycle ; un ovocyte I donne, par méiose, une seule grosse cellule fécondable (ovocyte II) et des globules polaires.

## La méiose
Deux divisions successives après une seule réplication : une cellule diploïde (2n) donne 4 cellules haploïdes (n).
• Méiose I (réductionnelle) : les chromosomes homologues se séparent ; crossing-over possible en prophase I.
• Méiose II (équationnelle) : les chromatides se séparent.
Chez l'Homme : 2n = 46, gamètes à n = 23.

## La fécondation
Fusion d'un spermatozoïde et d'un ovocyte II dans le tiers supérieur de la trompe : la cellule-œuf est diploïde.
Étapes : rencontre, pénétration (réaction acrosomique), réaction corticale qui empêche la polyspermie, fusion des noyaux.

## Le sexe
Il est déterminé par le spermatozoïde : X donne une fille (XX), Y donne un garçon (XY).

## Développement
Segmentation, nidation dans l'utérus vers le 7ᵉ jour, embryon puis fœtus (à partir du 3ᵉ mois), placenta pour les échanges mère–fœtus.""",
questions=[
(1, "Chez l'Homme, un gamète contient :", "23 chromosomes", "46 chromosomes", "92 chromosomes", "22 chromosomes",
 "Les gamètes sont haploïdes (n = 23)."),
(1, "La spermatogenèse a lieu :", "dans les tubes séminifères du testicule", "dans la prostate", "dans l'ovaire", "dans l'urètre",
 "Elle commence à la puberté et se poursuit toute la vie."),
(2, "La méiose produit à partir d'une cellule diploïde :", "4 cellules haploïdes", "2 cellules diploïdes", "4 cellules diploïdes", "1 cellule haploïde",
 "Deux divisions successives après une seule réplication."),
(2, "La division réductionnelle de la méiose sépare :", "les chromosomes homologues", "les chromatides sœurs", "les noyaux de la cellule-œuf", "les mitochondries",
 "Le nombre de chromosomes passe de 2n à n."),
(2, "La fécondation a lieu en général :", "dans le tiers supérieur de la trompe", "dans l'utérus", "dans l'ovaire", "dans le vagin",
 "La cellule-œuf migre ensuite vers l'utérus."),
(2, "Le sexe de l'enfant est déterminé par :", "le chromosome sexuel du spermatozoïde", "l'ovocyte", "l'alimentation de la mère", "le placenta",
 "L'ovocyte apporte toujours un X."),
(3, "La réaction corticale de l'ovocyte permet :", "d'empêcher l'entrée d'autres spermatozoïdes", "la nidation", "la méiose", "la production de progestérone",
 "Elle évite la polyspermie."),
(3, "Au terme de la méiose, un ovocyte I donne :", "une seule cellule fécondable (ovocyte II)", "4 ovocytes II", "2 ovocytes II", "des spermatozoïdes",
 "Les autres cellules sont des globules polaires qui dégénèrent."),
(3, "Le crossing-over se produit :", "en prophase de la première division de méiose", "pendant la fécondation", "en mitose", "en méiose II",
 "Les chromosomes homologues appariés échangent des fragments."),
(4, "La nidation de l'embryon dans la muqueuse utérine a lieu environ :", "7 jours après la fécondation", "le jour même", "1 mois après", "au 3ᵉ mois",
 "L'embryon est alors au stade blastocyste."),
(4, "Le placenta permet :", "les échanges entre le sang de la mère et celui du fœtus sans mélange", "le mélange direct des sangs", "la fabrication des gamètes", "la fécondation",
 "Nutriments, O₂, déchets et anticorps traversent la barrière placentaire."),
]),

dict(
nom="Transmission des caractères héréditaires",
fiche="""## Vocabulaire
• Gène : unité d'information ; allèles : versions d'un gène ; locus : place sur le chromosome.
• Homozygote (deux allèles identiques), hétérozygote (deux allèles différents).
• Dominant : s'exprime chez l'hétérozygote ; récessif : ne s'exprime qu'à l'état homozygote (ou hémizygote chez le mâle pour un gène lié à X).
• Codominance : les deux allèles s'expriment (groupe sanguin AB).
• Génotype (allèles) et phénotype (caractère observé).

## Monohybridisme (un seul gène)
Croisement de deux lignées pures : F1 homogène (première loi de Mendel).
F1 × F1 : en F2, 3/4 – 1/4 si dominance complète ; 1/4 – 1/2 – 1/4 si codominance.
Test-cross (croisement avec un homozygote récessif) : 1/2 – 1/2 si l'individu testé est hétérozygote.

## Dihybridisme (deux gènes)
• Gènes indépendants (chromosomes différents) : F2 en 9/16 – 3/16 – 3/16 – 1/16 ; test-cross en 4 phénotypes à 25 %.
• Gènes liés (même chromosome) : au test-cross, les phénotypes parentaux sont majoritaires ; les recombinés, minoritaires, viennent du crossing-over.
   Pourcentage de recombinés = distance entre les gènes (en centimorgans).

## Hérédité liée au sexe
Gène porté par le chromosome X : les résultats diffèrent selon le sexe et selon le sens du croisement.

## Brassages
Interchromosomique (anaphase I, répartition au hasard) et intrachromosomique (crossing-over) : chaque gamète est unique.""",
questions=[
(1, "Les différentes versions d'un même gène s'appellent :", "des allèles", "des locus", "des chromatides", "des codons",
 "Exemple : allèle « fleur rouge » et allèle « fleur blanche »."),
(1, "Un individu homozygote possède :", "deux allèles identiques pour un gène", "deux allèles différents", "un seul chromosome", "trois allèles",
 "Exemple : AA ou aa."),
(2, "On croise deux lignées pures. Tous les individus de F1 se ressemblent. C'est :", "l'uniformité des hybrides de F1", "la ségrégation en F2", "un crossing-over", "une mutation",
 "Première loi de Mendel."),
(2, "Croisement F1 × F1 en monohybridisme avec dominance complète : les proportions de F2 sont :", "3/4 et 1/4", "1/2 et 1/2", "9/16, 3/16, 3/16, 1/16", "100 %",
 "Aa × Aa donne 3/4 [A] et 1/4 [a]."),
(2, "Le groupe sanguin AB illustre :", "la codominance", "la dominance complète", "un gène lié à X", "une mutation",
 "Les allèles A et B s'expriment tous les deux."),
(3, "Un test-cross donne 50 % de phénotypes dominants et 50 % de récessifs. L'individu testé est :", "hétérozygote", "homozygote dominant", "homozygote récessif", "haploïde",
 "Aa × aa donne 1/2 Aa et 1/2 aa."),
(3, "En dihybridisme avec gènes indépendants, la F2 se répartit en :", "9/16, 3/16, 3/16, 1/16", "3/4, 1/4", "1/4, 1/2, 1/4", "50 %, 50 %",
 "Combinaison au hasard de deux couples d'allèles."),
(3, "Un test-cross en dihybridisme donne 4 phénotypes à 25 % chacun. Les deux gènes sont :", "indépendants", "liés sans crossing-over", "sur le chromosome Y", "identiques",
 "Brassage interchromosomique : 4 types de gamètes équiprobables."),
(3, "Un test-cross donne 42 %, 42 %, 8 % et 8 %. On en conclut que les gènes sont :", "liés, avec 16 % de recombinés", "indépendants", "liés sans recombinaison", "liés, avec 8 % de recombinés",
 "Parentaux majoritaires ; 8 + 8 = 16 % de recombinés par crossing-over."),
(4, "Lorsque les résultats d'un croisement diffèrent selon le sexe des descendants, le gène est probablement :", "porté par un chromosome sexuel", "porté par un autosome", "mitochondrial", "dominant",
 "Les mâles XY n'ont qu'un exemplaire du chromosome X."),
(4, "Le brassage interchromosomique a lieu :", "en anaphase de la première division de méiose", "en prophase de mitose", "pendant la fécondation uniquement", "en méiose II",
 "Les chromosomes homologues se répartissent au hasard entre les deux cellules."),
]),

dict(
nom="Génétique humaine",
fiche="""## Étudier l'hérédité humaine
On ne fait pas de croisements : on étudie des arbres généalogiques (pedigrees).
Symboles : carré = homme, rond = femme, symbole plein = atteint.

## Raisonner sur un arbre
1. Dominant ou récessif ? Deux parents sains ayant un enfant atteint : l'allèle est récessif.
2. Autosomique ou lié à X ?
   • Récessif lié à X : surtout des garçons atteints, transmis par des mères saines conductrices ; un père atteint n'a jamais de fils atteint par lui.
   • Si une fille atteinte a un père sain, l'allèle récessif n'est pas lié à X.
3. Écrire les génotypes et calculer les risques.

## Exemples
• Drépanocytose : autosomique récessive. Deux parents AS ont 1 risque sur 4 d'avoir un enfant SS (malade).
   Le test d'électrophorèse de l'hémoglobine dépiste les porteurs AS.
• Albinisme : autosomique récessif.
• Hémophilie et daltonisme : récessifs liés à X.
• Groupes sanguins ABO : A et B codominants, O récessif.

## Anomalies chromosomiques
Trisomie 21 (47 chromosomes, non-disjonction lors de la méiose), syndrome de Turner (45, X0), syndrome de Klinefelter (47, XXY). On les repère sur le caryotype.

## Prévention
Conseil génétique, test prénuptial (électrophorèse), diagnostic prénatal.""",
questions=[
(1, "En génétique humaine, on étudie la transmission des caractères grâce :", "aux arbres généalogiques", "aux croisements expérimentaux", "aux cultures de bactéries", "au microscope uniquement",
 "On ne peut pas faire de croisements chez l'Homme."),
(2, "Deux parents sains ont un enfant atteint. L'allèle responsable est :", "récessif", "dominant", "codominant", "porté par Y",
 "L'allèle est présent chez au moins un parent sans s'exprimer : il est masqué, donc récessif."),
(2, "La drépanocytose est une maladie :", "autosomique récessive", "liée au chromosome Y", "dominante liée à X", "infectieuse",
 "Seuls les individus SS sont malades."),
(2, "Deux parents AS ont un enfant. La probabilité qu'il soit SS est :", "1/4", "1/2", "3/4", "0",
 "AS × AS donne 1/4 AA, 1/2 AS, 1/4 SS."),
(2, "L'hémophilie est une maladie :", "récessive liée au chromosome X", "autosomique dominante", "due à un virus", "liée au chromosome Y",
 "Elle touche surtout les garçons."),
(3, "Un homme du groupe AB et une femme du groupe O peuvent avoir des enfants :", "A ou B", "AB ou O", "O seulement", "A, B, AB ou O",
 "AB × OO donne AO (groupe A) ou BO (groupe B)."),
(3, "Une fille atteinte d'une maladie récessive a un père sain. On en déduit que l'allèle :", "n'est pas lié au chromosome X", "est lié à X", "est dominant", "est sur le chromosome Y",
 "Si l'allèle était lié à X, la fille atteinte (XᵃXᵃ) aurait reçu un Xᵃ de son père, qui serait donc lui aussi atteint."),
(3, "La trisomie 21 est due à :", "la présence de trois chromosomes 21", "l'absence de chromosome 21", "une mutation du gène de l'hémoglobine", "un virus",
 "Non-disjonction des chromosomes 21 au cours de la méiose."),
(3, "Le test qui permet de savoir si une personne est porteuse du trait drépanocytaire (AS) est :", "l'électrophorèse de l'hémoglobine", "le groupe sanguin", "la radiographie", "la glycémie",
 "Les hémoglobines A et S migrent différemment."),
(4, "Une mère conductrice de l'hémophilie (XᴴXʰ) et un père sain ont un fils. La probabilité qu'il soit hémophile est :", "1/2", "1/4", "0", "1",
 "Le fils reçoit le Y du père et l'un des deux X de la mère."),
(4, "Le syndrome de Turner correspond au caryotype :", "45, X0", "47, XXY", "47, +21", "46, XY",
 "Il manque un chromosome sexuel."),
]),

dict(
nom="Le neurone et le message nerveux",
fiche="""## Le neurone
Corps cellulaire (noyau), dendrites (reçoivent), axone (conduit) parfois entouré de myéline, terminaisons synaptiques.
Un nerf est un ensemble de fibres nerveuses.

## Potentiel de repos
La membrane est polarisée : environ −70 mV (intérieur négatif).
Il est dû à la répartition inégale des ions (K⁺ plus concentré dedans, Na⁺ dehors), maintenue par la pompe Na⁺/K⁺ (qui consomme de l'ATP).

## Potentiel d'action
Une stimulation suffisante (seuil) provoque :
1. Dépolarisation : entrée de Na⁺ (le potentiel atteint environ +30 mV).
2. Repolarisation : sortie de K⁺.
3. Hyperpolarisation brève, puis retour au repos.
Loi du tout ou rien : au-delà du seuil, l'amplitude du potentiel d'action est constante pour une fibre.
L'intensité du stimulus est codée par la fréquence des potentiels d'action.
Période réfractaire : la fibre ne répond pas juste après un potentiel d'action.

## Propagation
De proche en proche sur une fibre amyélinisée ; saltatoire (de nœud de Ranvier en nœud de Ranvier), plus rapide, sur une fibre myélinisée.

## La synapse chimique
Arrivée du potentiel d'action → entrée de Ca²⁺ → libération du neurotransmetteur (acétylcholine…) par exocytose → fixation sur les récepteurs postsynaptiques → nouveau message.
La transmission est unidirectionnelle et marque un retard synaptique. Certaines drogues et médicaments agissent sur les synapses.

## Réflexe
Récepteur → neurone sensitif → centre nerveux (moelle épinière) → neurone moteur → effecteur (muscle).""",
questions=[
(1, "Le potentiel de repos d'un neurone vaut environ :", "−70 mV", "+30 mV", "0 mV", "+70 mV",
 "L'intérieur de la cellule est négatif par rapport à l'extérieur."),
(1, "La partie du neurone qui conduit le message vers les terminaisons est :", "l'axone", "la dendrite", "le noyau", "la myéline",
 "Les dendrites reçoivent, l'axone conduit."),
(2, "La phase de dépolarisation du potentiel d'action est due à :", "l'entrée d'ions Na⁺", "la sortie d'ions K⁺", "l'entrée d'ions Cl⁻", "la sortie de Na⁺ par la pompe",
 "Des canaux sodium s'ouvrent brusquement."),
(2, "La loi du tout ou rien signifie que :", "au-delà du seuil, l'amplitude du potentiel d'action d'une fibre est constante", "toute stimulation donne une réponse", "l'amplitude augmente avec l'intensité", "la fibre ne répond jamais",
 "Une stimulation sous le seuil ne déclenche rien."),
(2, "L'intensité d'une stimulation est codée dans la fibre nerveuse par :", "la fréquence des potentiels d'action", "leur amplitude", "leur durée", "leur signe",
 "Plus le stimulus est fort, plus les potentiels d'action sont rapprochés."),
(2, "La pompe Na⁺/K⁺ :", "maintient les différences de concentration en consommant de l'ATP", "fonctionne sans énergie", "fait entrer le Na⁺", "fabrique l'acétylcholine",
 "Elle fait sortir 3 Na⁺ et entrer 2 K⁺."),
(3, "La conduction est plus rapide dans une fibre :", "myélinisée (conduction saltatoire)", "amyélinisée", "de petit diamètre sans myéline", "détruite",
 "Le message saute de nœud de Ranvier en nœud de Ranvier."),
(3, "Au niveau d'une synapse chimique, le message est transmis par :", "un neurotransmetteur", "un courant d'ions direct entre neurones", "une hormone sanguine", "l'ADN",
 "Exemple : l'acétylcholine."),
(3, "La libération du neurotransmetteur est déclenchée par l'entrée dans la terminaison de :", "Ca²⁺", "Na⁺ seulement", "glucose", "Cl⁻",
 "L'ion calcium provoque l'exocytose des vésicules."),
(4, "Le trajet d'un réflexe médullaire est :", "récepteur, neurone sensitif, moelle épinière, neurone moteur, muscle", "muscle, cerveau, récepteur", "récepteur, cerveau uniquement, muscle", "neurone moteur, récepteur, moelle",
 "C'est l'arc réflexe."),
(4, "Juste après un potentiel d'action, une fibre ne peut pas être stimulée à nouveau. C'est :", "la période réfractaire", "le potentiel de repos", "la sommation", "le seuil",
 "Elle impose une fréquence maximale et une propagation dans un seul sens."),
]),

dict(
nom="L'immunité et ses dysfonctionnements",
fiche="""## Le soi et le non-soi
Le système immunitaire reconnaît le soi (marqueurs du CMH/HLA à la surface des cellules) et élimine le non-soi (antigènes : microbes, cellules greffées, cellules cancéreuses).

## Immunité innée (non spécifique)
Barrières (peau, muqueuses), réaction inflammatoire (rougeur, chaleur, gonflement, douleur), phagocytose par les macrophages et les granulocytes.

## Immunité adaptative (spécifique)
Les macrophages présentent l'antigène aux lymphocytes T4 (auxiliaires), qui activent :
• Réponse humorale : les lymphocytes B se transforment en plasmocytes qui produisent des anticorps. L'anticorps se lie à l'antigène (complexe immun), qui est ensuite phagocyté.
• Réponse cellulaire : les lymphocytes T8 deviennent cytotoxiques et détruisent les cellules infectées.
Les lymphocytes B et T naissent dans la moelle osseuse ; les T mûrissent dans le thymus.

## Mémoire immunitaire
La réponse secondaire est plus rapide, plus forte et plus durable : c'est le principe de la vaccination (prévention).
La sérothérapie apporte des anticorps tout faits (action immédiate mais brève).

## Dysfonctionnements
• VIH (sida) : le virus infecte les lymphocytes T4 ; leur chute laisse place aux maladies opportunistes. Transmission : sang, rapports sexuels non protégés, mère à l'enfant. Les antirétroviraux bloquent la multiplication du virus.
• Allergies : réaction excessive à un antigène inoffensif (pollen, acariens), avec libération d'histamine.
• Maladies auto-immunes : attaque du soi.""",
questions=[
(1, "Les anticorps sont produits par :", "les plasmocytes", "les globules rouges", "les plaquettes", "les lymphocytes T8",
 "Les lymphocytes B activés se transforment en plasmocytes."),
(1, "La phagocytose est réalisée notamment par :", "les macrophages", "les plasmocytes", "les globules rouges", "les neurones",
 "Ils englobent et digèrent les éléments étrangers."),
(2, "Le VIH infecte principalement :", "les lymphocytes T4", "les globules rouges", "les neurones", "les plaquettes",
 "Il détruit les chefs d'orchestre de la réponse immunitaire."),
(2, "Les lymphocytes T8 cytotoxiques :", "détruisent les cellules infectées", "produisent des anticorps", "transportent l'oxygène", "fabriquent l'histamine",
 "C'est la réponse à médiation cellulaire."),
(2, "Les lymphocytes T achèvent leur maturation dans :", "le thymus", "la rate seulement", "le foie", "l'estomac",
 "Les lymphocytes B, eux, mûrissent dans la moelle osseuse."),
(2, "Les signes de la réaction inflammatoire sont :", "rougeur, chaleur, gonflement, douleur", "fièvre et toux uniquement", "pâleur et froid", "perte de cheveux",
 "Réaction rapide de l'immunité innée."),
(3, "La vaccination repose sur :", "la mémoire immunitaire", "l'apport d'anticorps tout faits", "la destruction des lymphocytes", "les antibiotiques",
 "Le vaccin prépare une réponse secondaire rapide et forte."),
(3, "La sérothérapie consiste à :", "injecter des anticorps déjà fabriqués", "injecter un microbe atténué", "donner des antibiotiques", "greffer un organe",
 "Action immédiate mais de courte durée."),
(3, "Le stade sida correspond à :", "une forte baisse des lymphocytes T4 avec maladies opportunistes", "la première semaine après la contamination", "une augmentation des T4", "une guérison",
 "Le système immunitaire ne protège plus contre des microbes habituellement bénins."),
(4, "La réponse immunitaire secondaire par rapport à la primaire est :", "plus rapide et plus intense", "plus lente", "identique", "absente",
 "Grâce aux lymphocytes mémoire."),
(4, "Une allergie est :", "une réaction immunitaire excessive contre un antigène inoffensif", "une absence de réponse immunitaire", "une infection bactérienne", "une maladie génétique liée à Y",
 "Elle fait intervenir l'histamine."),
]),

dict(
nom="Régulation hormonale de la reproduction",
fiche="""## Chez l'homme
• Les cellules de Leydig du testicule sécrètent la testostérone (caractères sexuels secondaires, spermatogenèse).
• L'hypothalamus sécrète la GnRH, qui stimule l'hypophyse ; l'hypophyse libère la LH (→ testostérone) et la FSH (→ spermatogenèse, avec les cellules de Sertoli).
• Rétrocontrôle négatif : la testostérone freine l'hypothalamus et l'hypophyse ; son taux reste à peu près constant.

## Chez la femme : le cycle (environ 28 jours)
• Phase folliculaire (J1 à J14) : le follicule mûrit et sécrète des œstrogènes ; la muqueuse utérine s'épaissit.
• Ovulation vers J14 : déclenchée par un pic de LH (rétrocontrôle positif des œstrogènes à forte dose).
• Phase lutéale (J14 à J28) : le corps jaune sécrète œstrogènes et progestérone ; la muqueuse devient « dentelle utérine ».
• Sans fécondation, le corps jaune régresse : la chute des hormones déclenche les règles.

## En cas de grossesse
L'embryon sécrète l'hormone HCG qui maintient le corps jaune. Les tests de grossesse détectent la HCG.

## Maîtrise de la reproduction
• Pilule contraceptive (œstrogènes et progestatifs de synthèse) : rétrocontrôle négatif, pas d'ovulation.
• Préservatif : seule méthode qui protège aussi des IST.
• Infertilité : causes variées (obstruction des trompes, faible nombre de spermatozoïdes) ; aides : stimulation ovarienne, insémination, fécondation in vitro (FIV).""",
questions=[
(1, "L'hormone sexuelle masculine est :", "la testostérone", "la progestérone", "l'œstradiol", "l'insuline",
 "Sécrétée par les cellules de Leydig."),
(1, "L'ovulation a lieu, dans un cycle de 28 jours, vers :", "le 14ᵉ jour", "le 1ᵉʳ jour", "le 28ᵉ jour", "le 7ᵉ jour",
 "Au milieu du cycle."),
(2, "L'ovulation est déclenchée par :", "un pic de LH", "une chute de FSH", "la progestérone", "la testostérone",
 "Le pic de LH provoque la rupture du follicule mûr."),
(2, "Le corps jaune sécrète :", "de la progestérone et des œstrogènes", "de la testostérone", "de la HCG", "de la LH",
 "Il prépare l'utérus à une éventuelle nidation."),
(2, "Les règles sont provoquées par :", "la chute des taux d'œstrogènes et de progestérone", "un pic de LH", "la fécondation", "une hausse de progestérone",
 "Le corps jaune régresse en l'absence de fécondation."),
(2, "Les tests de grossesse détectent l'hormone :", "HCG", "FSH", "testostérone", "insuline",
 "Elle est produite par l'embryon puis le placenta."),
(3, "Chez l'homme, la testostérone exerce sur l'hypothalamus et l'hypophyse :", "un rétrocontrôle négatif", "un rétrocontrôle positif", "aucun effet", "une destruction",
 "Elle freine la sécrétion de GnRH, LH et FSH."),
(3, "La pilule contraceptive agit principalement en :", "empêchant l'ovulation par rétrocontrôle négatif", "tuant les spermatozoïdes", "provoquant un pic de LH", "détruisant l'utérus",
 "Les hormones de synthèse freinent l'hypothalamus et l'hypophyse."),
(3, "La seule méthode contraceptive qui protège aussi des infections sexuellement transmissibles est :", "le préservatif", "la pilule", "le stérilet", "l'implant",
 "Il empêche le contact entre muqueuses et liquides."),
(4, "Une femme dont les trompes sont obstruées peut avoir un enfant grâce :", "à la fécondation in vitro", "à la pilule", "à un vaccin", "à l'insuline",
 "La fécondation a lieu en laboratoire, l'embryon est placé dans l'utérus."),
(4, "Le pic de LH est provoqué par :", "un taux élevé d'œstrogènes (rétrocontrôle positif)", "un faible taux d'œstrogènes", "la progestérone seule", "la HCG",
 "À forte concentration, les œstrogènes stimulent l'hypophyse."),
]),

dict(
nom="La régulation de la glycémie",
fiche="""## La glycémie
Taux de glucose dans le sang : environ 1 g/L à jeun (entre 0,8 et 1,2 g/L). C'est une constante régulée.

## Les organes
• Le pancréas (îlots de Langerhans) détecte la glycémie et sécrète les hormones.
• Le foie stocke le glucose sous forme de glycogène et peut le libérer ; les muscles (glycogène) et le tissu adipeux (lipides) stockent aussi, mais seul le foie libère du glucose dans le sang.

## Les hormones
• Insuline (cellules β) : hypoglycémiante. Elle favorise l'entrée du glucose dans les cellules et son stockage (glycogenèse dans le foie et les muscles, lipides dans le tissu adipeux).
• Glucagon (cellules α) : hyperglycémiante. Il stimule la glycogénolyse dans le foie (libération de glucose).
• D'autres hormones (adrénaline, cortisol) sont aussi hyperglycémiantes.

## La boucle de régulation
Après un repas, la glycémie monte → sécrétion d'insuline → stockage → la glycémie revient à 1 g/L.
Pendant un jeûne ou un effort, elle baisse → sécrétion de glucagon → libération de glucose.

## Dysfonctionnements : les diabètes
• Diabète de type 1 : destruction des cellules β (maladie auto-immune), plus d'insuline ; traitement par injections d'insuline.
• Diabète de type 2 : les cellules répondent mal à l'insuline ; favorisé par la sédentarité et le surpoids. Prévention : activité physique, alimentation équilibrée.
Signes : soif, urines abondantes, glucose dans les urines (glycosurie) au-delà d'environ 1,8 g/L.""",
questions=[
(1, "La glycémie normale à jeun est d'environ :", "1 g/L", "10 g/L", "0,1 g/L", "5 g/L",
 "Entre 0,8 et 1,2 g/L environ."),
(1, "L'hormone hypoglycémiante est :", "l'insuline", "le glucagon", "l'adrénaline", "la testostérone",
 "C'est la seule hormone qui fait baisser la glycémie."),
(2, "L'insuline est sécrétée par :", "les cellules β des îlots de Langerhans", "les cellules α du pancréas", "le foie", "l'hypophyse",
 "Le glucagon est sécrété par les cellules α."),
(2, "Le foie stocke le glucose sous forme de :", "glycogène", "amidon", "protéines", "acide lactique",
 "C'est la glycogenèse."),
(2, "Après un repas riche en sucre, le pancréas sécrète surtout :", "de l'insuline", "du glucagon", "de l'adrénaline", "de la HCG",
 "La glycémie monte : il faut la faire baisser."),
(2, "Le glucagon agit principalement sur :", "le foie, en libérant du glucose", "les muscles, en stockant du glucose", "les reins, en éliminant le glucose", "le cerveau",
 "Il stimule la glycogénolyse."),
(3, "Entre deux repas ou pendant un jeûne court, la glycémie est maintenue grâce :", "au glucagon qui libère le glucose du foie", "à l'insuline", "à la glycosurie", "à la digestion",
 "Le foie libère le glucose stocké."),
(3, "Le diabète de type 1 est dû :", "à la destruction des cellules productrices d'insuline", "à un excès d'insuline", "à un manque de glucagon", "à un virus de la grippe",
 "Il se soigne par des injections d'insuline."),
(3, "Le diabète de type 2 est favorisé par :", "la sédentarité et le surpoids", "un excès d'exercice physique", "le manque de sel", "la consommation d'eau",
 "Les cellules deviennent moins sensibles à l'insuline."),
(4, "On trouve du glucose dans les urines lorsque la glycémie dépasse environ :", "1,8 g/L", "0,5 g/L", "1 g/L", "0,8 g/L",
 "Au-delà de ce seuil, les reins ne réabsorbent plus tout le glucose."),
(4, "La régulation de la glycémie est un exemple de :", "boucle de régulation par rétrocontrôle", "réflexe médullaire", "réponse immunitaire", "mutation",
 "Une variation de la glycémie déclenche une réponse qui la corrige."),
]),

dict(
nom="Révision BAC",
fiche="""## Les points clés de SVT de Terminale

## Cellule et génétique moléculaire
• Osmose, transport actif, ATP ; respiration (≈ 36 ATP) et fermentation (2 ATP).
• ADN → transcription (noyau) → ARNm → traduction (ribosomes) → protéine. AUG début ; UAA, UAG, UGA stop.
• Mutation : substitution, délétion, insertion. Drépanocytose : substitution.

## Reproduction et hérédité
• Méiose : 2n → 4 cellules n ; brassages inter- et intrachromosomique.
• Monohybridisme : F2 3/4 – 1/4 ; test-cross 1/2 – 1/2. Dihybridisme indépendant : 9/3/3/1 ; test-cross 4 × 25 %.
• Gènes liés : recombinés minoritaires ; % recombinés = distance.
• Arbres généalogiques : parents sains, enfant atteint → récessif.

## Communication et régulation
• Potentiel de repos −70 mV ; potentiel d'action : entrée de Na⁺ puis sortie de K⁺ ; codage en fréquence ; synapse chimique.
• Hormones : testostérone, œstrogènes, progestérone, LH, FSH, HCG ; rétrocontrôles.
• Glycémie : insuline (baisse), glucagon (hausse).

## Immunité
• Innée (phagocytose, inflammation) ; adaptative (B → plasmocytes → anticorps ; T8 cytotoxiques ; T4 auxiliaires).
• VIH : T4 ; vaccination : mémoire.

## Méthode pour l'épreuve
• Exploiter un document : décrire (avec des valeurs), interpréter, conclure.
• Un schéma doit être titré, légendé et propre.""",
questions=[
(2, "La traduction de l'ARNm AUG UUU UAA donne :", "un peptide de 2 acides aminés", "un peptide de 3 acides aminés", "aucun acide aminé", "un acide aminé",
 "AUG et UUU sont traduits, UAA est un codon stop."),
(2, "Une cellule à 2n = 8 chromosomes produit par méiose des cellules à :", "4 chromosomes", "8 chromosomes", "16 chromosomes", "2 chromosomes",
 "La méiose divise par deux le nombre de chromosomes."),
(2, "Le message nerveux est codé en :", "fréquence de potentiels d'action", "amplitude de potentiels d'action", "couleur", "quantité d'ADN",
 "Loi du tout ou rien pour l'amplitude."),
(2, "L'hormone dont le pic déclenche l'ovulation est :", "la LH", "la progestérone", "l'insuline", "la HCG",
 "Pic de LH vers le 14ᵉ jour."),
(3, "Une personne non vaccinée reçoit un sérum antitétanique après une blessure. Elle est protégée :", "immédiatement mais pour peu de temps", "dans un mois et pour toujours", "jamais", "seulement contre la grippe",
 "La sérothérapie apporte des anticorps tout faits."),
(3, "Le test-cross d'un individu double hétérozygote donne 4 phénotypes en proportions égales. Les gènes sont :", "indépendants", "liés sans recombinaison", "portés par Y", "identiques",
 "Brassage interchromosomique."),
(3, "Une hyperglycémie chronique, une soif intense et du glucose dans les urines évoquent :", "un diabète", "une hémophilie", "une allergie", "une trisomie",
 "La glycémie dépasse le seuil rénal."),
(3, "Un garçon hémophile a des parents sains. L'allèle de l'hémophilie lui vient :", "de sa mère", "de son père", "de ses deux parents", "d'une infection",
 "Le père lui donne le chromosome Y, la mère est conductrice."),
(4, "Lors d'un effort très intense, un muscle produit de l'acide lactique car :", "il réalise une fermentation faute d'oxygène suffisant", "il respire plus", "il stocke du glycogène", "il fabrique de l'insuline",
 "La fermentation lactique fournit vite un peu d'ATP sans O₂."),
(4, "Chez une personne infectée par le VIH, la baisse du nombre de lymphocytes T4 entraîne :", "l'apparition de maladies opportunistes", "une meilleure immunité", "une hausse des anticorps contre tout", "une guérison",
 "Les T4 coordonnent les réponses humorale et cellulaire."),
(4, "Une drogue qui bloque les récepteurs de l'acétylcholine empêche :", "la transmission synaptique", "la naissance du potentiel de repos", "la méiose", "la sécrétion d'insuline",
 "Le neurotransmetteur ne peut plus se fixer sur le neurone postsynaptique ou le muscle."),
]),
]
