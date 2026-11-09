NIVEAU, MATIERE = "3ème", "SVT"

CHAPITRES = [
dict(
nom="Les micro-organismes et les maladies infectieuses",
fiche="""## Les micro-organismes (microbes)
Ce sont des êtres vivants visibles seulement au microscope.
• Les bactéries : une seule cellule, sans noyau, de quelques micromètres. Elles se multiplient très vite par division. Exemples : bacille du tétanos, bacille de la tuberculose, vibrion du choléra.
• Les virus : beaucoup plus petits, ce ne sont pas des cellules. Ils ne se multiplient qu'à l'intérieur d'une cellule qu'ils parasitent. Exemples : virus de la rougeole, de la grippe, le VIH.
• Les champignons microscopiques : levures, moisissures (mycoses).
• Les protozoaires : êtres unicellulaires à noyau. Exemple : le Plasmodium, responsable du paludisme, transmis par la piqûre de l'anophèle femelle.
Beaucoup de microbes sont utiles (fabrication du yaourt, du pain, digestion). Ceux qui provoquent des maladies sont dits pathogènes.

## Contamination et infection
• La contamination est l'entrée des microbes dans l'organisme : par une plaie, par les voies respiratoires, par la bouche (eau et aliments souillés), par voie sexuelle, par le sang, par une piqûre d'insecte.
• L'infection est la multiplication des microbes dans l'organisme.
• Certains microbes produisent des toxines, des poisons (cas du tétanos).

## Se protéger
• Hygiène : se laver les mains au savon, boire de l'eau potable, couvrir les aliments.
• Asepsie : éviter l'entrée des microbes (matériel stérilisé).
• Antiseptiques (alcool, eau oxygénée) : ils détruisent les microbes sur la peau et les plaies.
• Moustiquaire imprégnée contre le paludisme.

## Les antibiotiques
Ils détruisent les bactéries ou bloquent leur multiplication. Ils sont SANS EFFET sur les virus.
On les prend sur ordonnance et jusqu'au bout du traitement.

## Pièges à éviter
• Le paludisme n'est pas dû à un virus ni à une bactérie : c'est un protozoaire.
• Un antibiotique ne guérit pas la grippe.""",
questions=[
(1, "Un être vivant visible seulement au microscope est appelé :", "un micro-organisme", "un organe", "un tissu", "un vecteur",
 "On dit aussi microbe : bactéries, virus, champignons microscopiques, protozoaires."),
(1, "Le paludisme est causé par :", "un protozoaire, le Plasmodium", "un virus", "une bactérie", "un ver",
 "Le Plasmodium est transmis par la piqûre de l'anophèle femelle."),
(1, "Le moustique qui transmet le paludisme est :", "l'anophèle femelle", "l'anophèle mâle", "la mouche tsé-tsé", "le cafard",
 "Seule la femelle pique, car elle a besoin de sang pour ses œufs."),
(2, "Les virus se multiplient :", "seulement à l'intérieur d'une cellule qu'ils parasitent", "seuls, dans l'eau", "par division, comme les bactéries", "dans l'air",
 "Un virus n'est pas une cellule : il utilise la cellule infectée pour se reproduire."),
(2, "La multiplication des microbes dans l'organisme s'appelle :", "l'infection", "la contamination", "la vaccination", "l'asepsie",
 "La contamination est l'entrée des microbes ; l'infection est leur multiplication."),
(2, "Les antibiotiques sont efficaces contre :", "les bactéries", "les virus", "tous les microbes", "le paludisme uniquement",
 "Ils n'agissent pas sur les virus : inutile d'en prendre contre la grippe."),
(2, "Le choléra se transmet surtout par :", "l'eau et les aliments souillés", "la piqûre de moustique", "la poignée de main", "l'air",
 "Le vibrion du choléra est rejeté dans les selles des malades ; boire de l'eau potable protège."),
(3, "Le tétanos est dangereux parce que la bactérie :", "produit une toxine qui agit sur les nerfs et les muscles", "détruit les globules rouges", "attaque les poumons", "se transmet par le moustique",
 "La bactérie entre par une plaie souillée et fabrique une toxine qui provoque des contractures."),
(3, "Un antiseptique sert à :", "détruire les microbes sur la peau et les plaies", "fabriquer des anticorps", "remplacer un vaccin", "soigner une infection virale",
 "Exemple : l'alcool à 70° ou l'eau oxygénée sur une plaie."),
(3, "L'asepsie consiste à :", "empêcher l'entrée des microbes dans l'organisme", "détruire les microbes déjà dans le sang", "multiplier les microbes utiles", "injecter des anticorps",
 "Matériel stérilisé, gants, mains propres : on évite la contamination."),
(4, "Pourquoi faut-il prendre un antibiotique jusqu'au bout du traitement ?", "Pour éliminer toutes les bactéries et éviter qu'elles deviennent résistantes", "Parce qu'il agit aussi sur les virus", "Pour fabriquer un vaccin", "Parce qu'il est sans danger",
 "Arrêter trop tôt laisse survivre les bactéries les plus résistantes, qui se multiplient."),
(4, "Dormir sous une moustiquaire imprégnée protège du paludisme car :", "elle empêche la piqûre de l'anophèle qui transmet le Plasmodium", "elle tue le Plasmodium dans le sang", "elle remplace un vaccin", "elle filtre l'air",
 "On coupe la transmission : pas de piqûre, pas de contamination."),
]),

dict(
nom="La défense de l'organisme",
fiche="""## Les barrières naturelles
La peau et les muqueuses empêchent l'entrée des microbes. Les larmes, la salive et le mucus contiennent des substances qui les détruisent. Une blessure ouvre une porte d'entrée.

## La réaction inflammatoire
Au niveau d'une plaie infectée apparaissent : rougeur, chaleur, gonflement et douleur. Les vaisseaux sanguins se dilatent et laissent passer des globules blancs.

## La phagocytose (réponse non spécifique)
Certains globules blancs, les phagocytes (polynucléaires, macrophages), avalent et digèrent les microbes, quels qu'ils soient.
Les étapes : 1. adhésion du microbe ; 2. ingestion ; 3. digestion ; 4. rejet des déchets.
Le pus est fait de phagocytes morts et de débris de microbes.

## La réponse spécifique : les lymphocytes
Un antigène est une substance reconnue comme étrangère (un microbe, une toxine).
• Les lymphocytes B fabriquent des anticorps. Chaque anticorps reconnaît un seul antigène et se fixe dessus : il se forme un complexe antigène-anticorps qui neutralise l'antigène, ensuite éliminé par phagocytose. C'est l'immunité humorale (par le sang).
• Les lymphocytes T cytotoxiques détruisent les cellules infectées par un virus. C'est l'immunité cellulaire.
• Les lymphocytes T4 coordonnent la réponse : ils activent les lymphocytes B et T.

## La mémoire immunitaire
Après une première rencontre, il reste des lymphocytes mémoire. Au deuxième contact avec le même antigène, la réponse est plus rapide et plus forte : on est immunisé. C'est le principe du vaccin.

## Les organes du système immunitaire
Moelle osseuse (fabrication des globules blancs), thymus, ganglions lymphatiques, rate.

## Pièges à éviter
• La phagocytose est non spécifique ; les anticorps sont spécifiques.
• Les anticorps sont fabriqués par les lymphocytes B, pas par les phagocytes.""",
questions=[
(1, "La première barrière contre les microbes est :", "la peau et les muqueuses", "les anticorps", "les lymphocytes T", "la rate",
 "Une peau intacte empêche l'entrée des microbes."),
(1, "Rougeur, chaleur, gonflement et douleur sont les signes :", "de la réaction inflammatoire", "de la vaccination", "de la sérothérapie", "d'une allergie alimentaire",
 "Ce sont les quatre signes d'une inflammation au niveau d'une plaie infectée."),
(1, "Les anticorps sont fabriqués par :", "les lymphocytes B", "les globules rouges", "les plaquettes", "les phagocytes",
 "Les lymphocytes B produisent des anticorps spécifiques d'un antigène."),
(2, "La phagocytose est réalisée par :", "des globules blancs appelés phagocytes", "les globules rouges", "les anticorps", "les plaquettes",
 "Polynucléaires et macrophages avalent et digèrent les microbes."),
(2, "L'ordre des étapes de la phagocytose est :", "adhésion, ingestion, digestion, rejet", "ingestion, adhésion, rejet, digestion", "digestion, adhésion, ingestion, rejet", "rejet, digestion, ingestion, adhésion",
 "Le phagocyte se colle au microbe, l'avale, le digère puis rejette les déchets."),
(2, "Un antigène est :", "une substance reconnue comme étrangère par l'organisme", "un globule blanc", "un médicament", "un organe de défense",
 "Un microbe ou une toxine porte des antigènes qui déclenchent la réponse immunitaire."),
(2, "Le pus est formé principalement :", "de phagocytes morts et de débris de microbes", "de globules rouges", "d'anticorps", "de lymphe pure",
 "Il témoigne du combat entre les phagocytes et les microbes."),
(3, "Une réponse immunitaire spécifique est dirigée :", "contre un antigène précis", "contre tous les microbes à la fois", "contre les cellules saines", "contre les globules rouges",
 "Chaque anticorps et chaque lymphocyte reconnaît un antigène particulier."),
(3, "Les lymphocytes T cytotoxiques :", "détruisent les cellules infectées par un virus", "fabriquent des anticorps", "transportent le dioxygène", "coagulent le sang",
 "C'est l'immunité cellulaire, complémentaire des anticorps."),
(3, "Le rôle des lymphocytes T4 est :", "de coordonner la réponse immunitaire en activant les lymphocytes B et T", "de fabriquer des globules rouges", "de transporter les anticorps", "de digérer les microbes",
 "Ce sont eux que détruit le VIH, d'où l'affaiblissement des défenses."),
(4, "Lors d'un deuxième contact avec le même antigène, la réponse immunitaire est :", "plus rapide et plus forte, grâce à la mémoire immunitaire", "plus lente", "identique à la première", "inexistante",
 "Les lymphocytes mémoire réagissent tout de suite : c'est le principe de la vaccination."),
(4, "Un complexe antigène-anticorps :", "neutralise l'antigène, ensuite éliminé par phagocytose", "multiplie le microbe", "fabrique des lymphocytes", "provoque toujours une allergie",
 "L'anticorps se fixe sur l'antigène et le rend inoffensif ; les phagocytes font le ménage."),
]),

dict(
nom="Vaccination et sérothérapie",
fiche="""## La vaccination
• On injecte (ou on fait avaler) un vaccin : un microbe tué ou atténué, ou une toxine rendue inoffensive (anatoxine).
• L'organisme fabrique lui-même des anticorps et des lymphocytes mémoire.
• Action lente (quelques jours ou semaines), mais durable : protection pendant des années. Des rappels entretiennent la mémoire.
• Rôle PRÉVENTIF : on vaccine avant la maladie.
• Quand une grande partie de la population est vaccinée, le microbe circule moins : on protège aussi ceux qui ne peuvent pas être vaccinés.

## La sérothérapie
• On injecte un sérum qui contient des anticorps déjà fabriqués (par un animal ou une autre personne).
• Action immédiate, mais de courte durée (quelques semaines) : pas de mémoire.
• Rôle CURATIF, en urgence : sérum antivenimeux après une morsure de serpent, sérum antitétanique après une plaie souillée chez une personne non vaccinée.

## Tableau comparatif
• Vaccin : on apporte l'antigène → immunité active, lente, durable, préventive.
• Sérum : on apporte les anticorps → immunité passive, immédiate, brève, curative.

## Un peu d'histoire
• 1796 : Edward Jenner protège contre la variole.
• 1885 : Louis Pasteur réussit la vaccination contre la rage.
La variole a été éradiquée dans le monde grâce à la vaccination.

## En pratique
Le carnet de vaccination de l'enfant suit le calendrier du Programme élargi de vaccination (tuberculose, poliomyélite, rougeole, fièvre jaune, tétanos…). Le vaccin contre la fièvre jaune est exigé pour voyager dans de nombreux pays.

## Pièges à éviter
• Le vaccin apporte des antigènes, le sérum apporte des anticorps.
• Un sérum ne protège pas durablement.""",
questions=[
(1, "Un vaccin contient :", "un microbe tué ou atténué, ou une toxine rendue inoffensive", "des anticorps tout prêts", "des globules rouges", "un antibiotique",
 "Le vaccin apporte l'antigène ; l'organisme fabrique lui-même ses défenses."),
(1, "La sérothérapie consiste à injecter :", "des anticorps déjà fabriqués", "un microbe atténué", "un antibiotique", "des vitamines",
 "Le sérum contient des anticorps prêts à agir."),
(1, "La vaccination a un rôle :", "préventif", "curatif", "uniquement contre les bactéries", "uniquement chez l'adulte",
 "On vaccine avant le contact avec le microbe."),
(2, "Après une morsure de serpent, on injecte en urgence :", "un sérum antivenimeux", "un vaccin", "un antibiotique", "de l'eau oxygénée",
 "Il faut des anticorps qui agissent tout de suite contre le venin."),
(2, "La protection donnée par un sérum est :", "immédiate mais de courte durée", "lente mais durable", "définitive", "inexistante",
 "Les anticorps injectés disparaissent en quelques semaines ; il n'y a pas de mémoire."),
(2, "La protection donnée par un vaccin est :", "lente à s'installer mais durable", "immédiate et brève", "immédiate et définitive", "nulle sans sérum",
 "L'organisme met du temps à produire anticorps et lymphocytes mémoire, mais ils durent."),
(2, "La première vaccination réussie contre la rage est due à :", "Louis Pasteur, en 1885", "Edward Jenner, en 1796", "Alexander Fleming, en 1928", "Robert Koch, en 1882",
 "Jenner travaillait sur la variole ; Fleming a découvert la pénicilline."),
(3, "Les rappels de vaccin servent à :", "entretenir la mémoire immunitaire", "guérir une maladie déclarée", "remplacer la sérothérapie", "détruire les virus dans le sang",
 "Chaque rappel relance la production de lymphocytes mémoire."),
(3, "Avec un vaccin, l'immunité est dite active parce que :", "l'organisme fabrique lui-même ses anticorps", "les anticorps viennent d'un animal", "elle agit tout de suite", "elle ne dure que quelques jours",
 "Avec un sérum, au contraire, l'immunité est passive : on reçoit des anticorps tout faits."),
(3, "La variole a disparu dans le monde grâce :", "à la vaccination", "aux antibiotiques", "à la sérothérapie", "aux moustiquaires",
 "C'est la première maladie éradiquée par une campagne mondiale de vaccination."),
(4, "Un jeune non vacciné se blesse avec un clou rouillé dans la terre. Le médecin lui injecte un sérum antitétanique et commence la vaccination. Pourquoi les deux ?", "Le sérum protège tout de suite, le vaccin protégera durablement", "Le sérum guérit et le vaccin calme la douleur", "Les deux font la même chose", "Le vaccin agit tout de suite et le sérum plus tard",
 "On combine l'action immédiate du sérum et la mémoire durable du vaccin."),
(4, "Quand une grande partie de la population est vaccinée :", "le microbe circule moins et même les non-vaccinés sont mieux protégés", "le vaccin ne sert plus à rien", "les antibiotiques deviennent inutiles", "la maladie devient plus grave",
 "C'est l'immunité collective."),
]),

dict(
nom="Le VIH-SIDA et les IST",
fiche="""## Le VIH et le SIDA
• Le VIH (virus de l'immunodéficience humaine) attaque surtout les lymphocytes T4, qui coordonnent les défenses.
• Les défenses s'affaiblissent peu à peu. Au stade SIDA (syndrome d'immunodéficience acquise), des maladies dites opportunistes apparaissent (tuberculose, diarrhées graves, infections de la peau…).
• Une personne séropositive a des anticorps anti-VIH dans le sang : elle est porteuse du virus, même si elle n'a aucun signe.

## Comment le VIH se transmet
• Par voie sexuelle (rapports non protégés).
• Par le sang (seringues, lames, objets tranchants partagés, transfusion non contrôlée).
• De la mère à l'enfant (pendant la grossesse, l'accouchement ou l'allaitement).
Le VIH ne se transmet PAS par la poignée de main, les repas partagés, la piqûre de moustique, la toux ou les toilettes.

## Dépistage et traitement
• Seul un test de dépistage permet de savoir si on est infecté. Il est confidentiel.
• Après une prise de risque, il faut attendre quelques semaines (la « fenêtre sérologique ») pour qu'un test soit fiable.
• Les médicaments antirétroviraux (ARV) ne guérissent pas, mais empêchent le virus de se multiplier : la personne vit longtemps et transmet beaucoup moins le virus.
• Le traitement de la mère pendant la grossesse protège le bébé.

## Les autres IST (infections sexuellement transmissibles)
• Gonococcie (« chaude-pisse ») et syphilis : dues à des bactéries, se soignent avec des antibiotiques.
• Hépatite B : due à un virus ; il existe un vaccin.
Une IST non soignée peut rendre stérile. Un écoulement ou une plaie aux organes génitaux doit faire consulter.

## Se protéger
Abstinence, fidélité réciproque après dépistage, préservatif, pas de partage d'objets tranchants.
Les personnes vivant avec le VIH ont droit au respect : on ne doit pas les rejeter.

## Pièges à éviter
• Séropositif ne veut pas dire malade du SIDA.
• Le moustique ne transmet pas le VIH.""",
questions=[
(1, "Le VIH attaque principalement :", "les lymphocytes T4", "les globules rouges", "les plaquettes", "les neurones",
 "Les T4 coordonnent les défenses : leur destruction affaiblit tout le système immunitaire."),
(1, "SIDA signifie :", "syndrome d'immunodéficience acquise", "système immunitaire de défense active", "syndrome infectieux des adultes", "sérum d'immunité directe acquise",
 "« Acquise » : on n'est pas né avec, on l'a contractée."),
(1, "Le VIH ne se transmet pas par :", "la piqûre de moustique", "les rapports sexuels non protégés", "le partage de seringues", "la mère à l'enfant",
 "Le virus ne survit pas et ne se multiplie pas dans le moustique."),
(2, "Une personne séropositive au VIH :", "a des anticorps anti-VIH : elle porte le virus", "est forcément au stade SIDA", "est guérie", "ne peut pas transmettre le virus",
 "Elle peut n'avoir aucun signe pendant des années, tout en étant porteuse."),
(2, "Les maladies qui profitent de l'affaiblissement des défenses sont dites :", "opportunistes", "héréditaires", "chroniques", "vaccinables",
 "Exemples : tuberculose, diarrhées graves, infections de la peau."),
(2, "Pour savoir si l'on est infecté par le VIH, il faut :", "faire un test de dépistage", "observer ses symptômes", "prendre sa température", "attendre de tomber malade",
 "Une personne infectée peut se sentir en parfaite santé."),
(2, "La gonococcie et la syphilis sont dues à :", "des bactéries", "des virus", "des champignons", "des protozoaires",
 "Elles se soignent avec des antibiotiques prescrits par un médecin."),
(3, "Les médicaments antirétroviraux (ARV) :", "empêchent le virus de se multiplier mais ne guérissent pas", "guérissent définitivement du SIDA", "sont un vaccin contre le VIH", "détruisent les lymphocytes T4",
 "Pris régulièrement, ils permettent de vivre longtemps et réduisent fortement la transmission."),
(3, "La « fenêtre sérologique », c'est :", "la période après la contamination où le test peut encore être négatif", "la durée d'un traitement ARV", "le stade final du SIDA", "le temps de fabrication d'un vaccin",
 "Les anticorps mettent quelques semaines à apparaître : il faut parfois refaire le test."),
(3, "Contre l'hépatite B, il existe :", "un vaccin", "seulement des antibiotiques", "aucun moyen de prévention", "un sérum antivenimeux",
 "L'hépatite B est due à un virus ; la vaccination protège."),
(4, "Pour réduire le risque de transmission du VIH de la mère à l'enfant, on :", "traite la mère pendant la grossesse et suit le bébé", "vaccine le bébé contre le VIH", "donne des antibiotiques au père", "évite tout contact avec le bébé",
 "Le traitement de la mère diminue fortement la quantité de virus et donc le risque pour l'enfant."),
(4, "Une IST non soignée peut entraîner :", "la stérilité", "une immunité définitive", "une guérison spontanée assurée", "une meilleure santé",
 "D'où l'importance de consulter dès qu'un signe apparaît."),
]),

dict(
nom="Le système nerveux",
fiche="""## Organisation
• Le système nerveux central : l'encéphale (cerveau, cervelet, tronc cérébral), protégé par le crâne, et la moelle épinière, protégée par la colonne vertébrale.
• Le système nerveux périphérique : les nerfs, qui relient les centres nerveux aux organes.
• Nerfs sensitifs : ils conduisent le message des récepteurs (peau, œil, oreille…) vers les centres.
• Nerfs moteurs : ils conduisent le message des centres vers les effecteurs (muscles).

## Le neurone
La cellule nerveuse : un corps cellulaire avec un noyau, des dendrites et un long prolongement, l'axone. Les neurones transmettent un message nerveux de nature électrique.

## Le réflexe (acte involontaire)
• Réponse rapide, involontaire et automatique à une stimulation : retirer la main d'une marmite chaude, réflexe rotulien.
• Son centre nerveux est la moelle épinière.
• L'arc réflexe : récepteur → nerf sensitif → moelle épinière → nerf moteur → muscle effecteur.

## L'acte volontaire
Il est décidé : écrire, marcher vers quelqu'un. Son centre est le cerveau (le cortex). Le message descend ensuite par la moelle épinière vers les muscles.

## Rôles des parties de l'encéphale
• Cerveau : sensations conscientes, mouvements volontaires, mémoire, réflexion.
• Cervelet : équilibre et coordination des mouvements.
• Tronc cérébral : respiration, rythme cardiaque.

## Hygiène du système nerveux
L'alcool, le tabac et les drogues perturbent le fonctionnement des neurones (réflexes ralentis, dépendance). Le manque de sommeil diminue l'attention et la mémoire. Le casque protège l'encéphale à moto.

## Pièges à éviter
• Le centre d'un réflexe comme le retrait de la main ou le réflexe rotulien est la MOELLE ÉPINIÈRE, pas le cerveau.
• Le nerf sensitif va vers le centre, le nerf moteur part du centre.""",
questions=[
(1, "Le système nerveux central comprend :", "l'encéphale et la moelle épinière", "les nerfs et les muscles", "le cœur et les vaisseaux", "les os et les articulations",
 "Les nerfs forment le système nerveux périphérique."),
(1, "La cellule nerveuse s'appelle :", "le neurone", "le lymphocyte", "l'hématie", "le néphron",
 "Le neurone a un corps cellulaire, des dendrites et un axone."),
(1, "Retirer brusquement sa main d'une marmite chaude est :", "un réflexe", "un acte volontaire", "une réaction allergique", "une phagocytose",
 "La réponse est rapide, involontaire et automatique."),
(2, "Le centre nerveux d'un réflexe comme le réflexe rotulien est :", "la moelle épinière", "le cerveau", "le cervelet", "le muscle",
 "Le message n'a pas besoin de monter jusqu'au cerveau, d'où sa rapidité."),
(2, "Le centre nerveux d'un acte volontaire est :", "le cerveau", "la moelle épinière seule", "le cervelet", "le nerf moteur",
 "Le mouvement est décidé dans le cortex cérébral."),
(2, "Le nerf qui conduit le message des récepteurs vers les centres nerveux est :", "un nerf sensitif", "un nerf moteur", "un muscle", "un tendon",
 "Le nerf moteur conduit dans l'autre sens, vers les muscles."),
(2, "Le cervelet contrôle surtout :", "l'équilibre et la coordination des mouvements", "la digestion", "la mémoire", "la vision",
 "Une atteinte du cervelet rend les gestes maladroits et la marche instable."),
(3, "L'ordre correct de l'arc réflexe est :", "récepteur, nerf sensitif, moelle épinière, nerf moteur, muscle", "muscle, nerf moteur, cerveau, nerf sensitif, récepteur", "récepteur, nerf moteur, cerveau, nerf sensitif, muscle", "nerf sensitif, récepteur, muscle, moelle épinière, nerf moteur",
 "Le message part du récepteur, passe par le centre et arrive au muscle effecteur."),
(3, "Le prolongement long du neurone qui conduit le message est :", "l'axone", "la dendrite", "le noyau", "la synapse",
 "Les dendrites sont des prolongements courts qui reçoivent les messages."),
(3, "Le tronc cérébral commande notamment :", "la respiration et le rythme cardiaque", "l'écriture", "la réflexion", "la vision des couleurs",
 "Ces fonctions vitales continuent même pendant le sommeil."),
(4, "Après avoir bu de l'alcool, un conducteur freine plus tard. C'est parce que l'alcool :", "ralentit la transmission des messages nerveux", "renforce les muscles", "accélère les réflexes", "agit seulement sur l'estomac",
 "Le temps de réaction augmente : c'est une cause majeure d'accidents."),
(4, "Une personne a la moelle épinière sectionnée au niveau du dos. Ses jambes :", "ne peuvent plus être commandées volontairement", "fonctionnent normalement", "bougent seulement de façon volontaire", "deviennent plus rapides",
 "Les messages du cerveau ne peuvent plus descendre jusqu'aux muscles des jambes."),
]),

dict(
nom="L'hérédité",
fiche="""## Caractères héréditaires
Certains caractères se transmettent des parents aux enfants : groupe sanguin, forme du lobe de l'oreille, couleur naturelle des yeux. D'autres dépendent du mode de vie (cicatrice, musculation, langue parlée) : ils ne sont pas héréditaires.

## Les chromosomes
• Ils se trouvent dans le noyau de chaque cellule et portent l'information héréditaire.
• Une cellule humaine en a 46, soit 23 paires.
• 22 paires d'autosomes, identiques chez l'homme et la femme, et 1 paire de chromosomes sexuels : XX chez la femme, XY chez l'homme.
• Le caryotype est la photographie des chromosomes rangés par paires.

## Les gènes
Un gène est une portion de chromosome (d'ADN) qui détermine un caractère. Un même gène peut exister en plusieurs versions, les allèles (par exemple, les allèles A, B et O du groupe sanguin).

## Transmission
• Les gamètes (spermatozoïdes, ovules) n'ont que 23 chromosomes, un de chaque paire.
• La fécondation réunit un spermatozoïde et un ovule : la cellule-œuf a de nouveau 46 chromosomes, la moitié venant du père, la moitié de la mère.
• Chaque enfant reçoit une combinaison unique : c'est pourquoi frères et sœurs se ressemblent sans être identiques (sauf les vrais jumeaux).

## Le sexe de l'enfant
L'ovule porte toujours un X. Le spermatozoïde porte un X ou un Y.
• X + X → fille ; X + Y → garçon.
C'est donc le spermatozoïde qui détermine le sexe, avec une chance sur deux à chaque naissance.

## Anomalie chromosomique
La trisomie 21 est due à un chromosome 21 en trop : la personne a 47 chromosomes.

## Pièges à éviter
• « Une chance sur deux » vaut pour chaque naissance : avoir déjà trois filles ne rend pas un garçon plus probable.
• Les gamètes ont 23 chromosomes, pas 46.""",
questions=[
(1, "Une cellule humaine ordinaire, avec un noyau (hors gamètes), contient :", "46 chromosomes", "23 chromosomes", "48 chromosomes", "92 chromosomes",
 "46 chromosomes, soit 23 paires."),
(1, "Les chromosomes se trouvent :", "dans le noyau de la cellule", "dans la membrane", "dans le sang uniquement", "dans les muscles uniquement",
 "Le noyau contient l'information héréditaire."),
(1, "Chez un individu de sexe masculin, la paire de chromosomes sexuels est :", "XY", "XX", "YY", "XO",
 "La femme est XX, l'homme XY."),
(2, "Un spermatozoïde contient :", "23 chromosomes", "46 chromosomes", "22 chromosomes", "47 chromosomes",
 "Les gamètes n'ont qu'un chromosome de chaque paire."),
(2, "Lequel de ces caractères n'est pas héréditaire ?", "une cicatrice", "le groupe sanguin", "la forme du lobe de l'oreille", "la couleur naturelle des yeux",
 "Une cicatrice est acquise au cours de la vie, elle ne se transmet pas aux enfants."),
(2, "Le caryotype est :", "l'image des chromosomes d'une cellule rangés par paires", "une cellule sexuelle", "un gène", "une maladie",
 "Il permet de compter les chromosomes et de repérer une anomalie."),
(2, "Un gène est :", "une portion de chromosome qui détermine un caractère", "une cellule", "un organe", "un chromosome entier",
 "Chaque chromosome porte de très nombreux gènes."),
(3, "Le sexe de l'enfant est déterminé par :", "le chromosome sexuel apporté par le spermatozoïde", "le chromosome apporté par l'ovule", "l'alimentation de la mère", "le mois de la conception",
 "L'ovule porte toujours un X ; le spermatozoïde porte X ou Y."),
(3, "La fécondation permet :", "de rétablir le nombre de 46 chromosomes", "de diviser par deux le nombre de chromosomes", "de produire des gamètes", "de supprimer les chromosomes sexuels",
 "23 chromosomes du père + 23 de la mère = 46."),
(3, "La trisomie 21 se caractérise par :", "47 chromosomes, avec un chromosome 21 en trop", "45 chromosomes", "l'absence de chromosome sexuel", "46 chromosomes normaux",
 "Le caryotype montre trois chromosomes 21 au lieu de deux."),
(4, "Un couple a déjà trois filles. La probabilité que le quatrième enfant soit un garçon est :", "1 chance sur 2", "1 chance sur 4", "presque certaine", "nulle",
 "Chaque naissance est indépendante des précédentes."),
(4, "Deux frères (non jumeaux) ne sont pas identiques parce que :", "chacun reçoit une combinaison différente des chromosomes de ses parents", "ils n'ont pas les mêmes parents", "ils n'ont pas le même nombre de chromosomes", "l'un a reçu des chromosomes de ses grands-parents seulement",
 "Chaque gamète emporte un chromosome de chaque paire, choisi au hasard."),
]),

dict(
nom="Le sol",
fiche="""## Qu'est-ce que le sol ?
C'est la couche superficielle et meuble de la Terre, qui permet la vie des plantes.

## Sa composition
• Une fraction minérale : sables, limons et argiles, issus de la roche.
• Une fraction organique : débris de végétaux et d'animaux (la litière) et l'humus.
• De l'eau et de l'air, dans les espaces entre les particules.
• Des êtres vivants : vers de terre, termites, champignons, bactéries.

## Sa formation
1. La roche mère se désagrège (pluie, chaleur, racines) et s'altère : c'est l'altération.
2. La litière est décomposée par les êtres vivants du sol en humus : c'est l'humification.
3. L'humus est ensuite transformé en sels minéraux utilisables par les plantes : c'est la minéralisation.
Il faut des centaines, voire des milliers d'années pour former quelques centimètres de sol.

## Le profil du sol
De haut en bas :
• Horizon A : sombre, riche en humus.
• Horizon B : accumulation d'argiles et d'oxydes (souvent rouge en zone tropicale).
• Horizon C : roche mère altérée.
• En dessous : la roche mère.
En zone tropicale humide, les sols ferrallitiques, rouges, sont riches en oxydes de fer.

## La fertilité
L'argile et l'humus forment le complexe argilo-humique, qui retient l'eau et les sels minéraux nourrissant les plantes.

## Dégradation et protection
• Causes d'appauvrissement : déforestation, feux de brousse, érosion par la pluie et le vent, cultures répétées sans repos.
• Protection : reboisement, jachère, cultures en courbes de niveau, apport de compost ou de fumier, rotation des cultures, lutte contre les feux de brousse.

## Pièges à éviter
• L'humus vient de la matière organique, pas de la roche.
• L'horizon le plus riche en humus est en surface (A).""",
questions=[
(1, "La couche superficielle et meuble de la Terre où poussent les plantes est :", "le sol", "la roche mère", "le sous-sol rocheux", "la nappe phréatique",
 "Le sol se forme à partir de la roche mère et de la matière organique."),
(1, "L'humus provient :", "de la décomposition de la matière organique", "de la roche mère", "de l'eau de pluie", "du sable",
 "Les êtres vivants du sol transforment la litière en humus."),
(1, "Lequel de ces éléments appartient à la fraction minérale du sol ?", "l'argile", "l'humus", "la litière", "le ver de terre",
 "Sables, limons et argiles proviennent de la roche."),
(2, "La transformation de la litière en humus s'appelle :", "l'humification", "la minéralisation", "l'érosion", "l'altération",
 "La minéralisation est l'étape suivante : l'humus devient sels minéraux."),
(2, "La désagrégation et l'altération de la roche mère sont dues notamment :", "à la pluie, à la chaleur et aux racines", "aux engrais chimiques", "à la lumière de la Lune", "aux feux de brousse uniquement",
 "Les variations de température, l'eau et les racines fragmentent la roche."),
(2, "L'horizon du sol le plus riche en humus est :", "l'horizon A, en surface", "l'horizon B", "l'horizon C", "la roche mère",
 "La matière organique s'accumule en surface, d'où sa couleur sombre."),
(2, "Les vers de terre et les termites sont utiles au sol car :", "ils mélangent et aèrent le sol et participent à la décomposition", "ils détruisent l'humus", "ils empêchent l'eau d'entrer", "ils produisent de l'argile",
 "Ils creusent des galeries et fragmentent la matière organique."),
(3, "Le complexe argilo-humique est important car il :", "retient l'eau et les sels minéraux nécessaires aux plantes", "durcit le sol", "empêche toute vie dans le sol", "transforme le sol en roche",
 "C'est un réservoir de nourriture pour les plantes : il fait la fertilité du sol."),
(3, "La couleur rouge de nombreux sols tropicaux est due :", "aux oxydes de fer", "à l'humus", "au calcaire", "au sel",
 "Ce sont les sols ferrallitiques, typiques des régions chaudes et humides."),
(3, "Laquelle de ces pratiques appauvrit le sol ?", "les feux de brousse répétés", "la jachère", "l'apport de compost", "le reboisement",
 "Le feu détruit la matière organique et laisse le sol nu face à l'érosion."),
(4, "Sur une pente, cultiver en courbes de niveau permet :", "de freiner le ruissellement de l'eau et donc l'érosion", "d'augmenter la pente", "de supprimer l'humus", "d'accélérer l'écoulement de l'eau",
 "Les sillons perpendiculaires à la pente retiennent l'eau et la terre."),
(4, "Pourquoi laisse-t-on une parcelle en jachère ?", "Pour que le sol se repose et reconstitue sa fertilité", "Pour l'urbaniser", "Pour augmenter l'érosion", "Pour la transformer en roche",
 "La végétation qui repousse enrichit le sol en matière organique."),
]),

dict(
nom="Révision BEPC",
fiche="""## Fiche mémo de SVT 3ème

## Microbes et défense
• Bactérie : cellule sans noyau, sensible aux antibiotiques. Virus : pas une cellule, insensible aux antibiotiques. Paludisme : protozoaire (Plasmodium), transmis par l'anophèle femelle.
• Contamination = entrée des microbes ; infection = leur multiplication.
• Barrières : peau, muqueuses. Inflammation : rougeur, chaleur, gonflement, douleur.
• Phagocytose (non spécifique) : adhésion, ingestion, digestion, rejet.
• Lymphocytes B → anticorps ; lymphocytes T cytotoxiques → destruction des cellules infectées ; T4 → coordination.
• Vaccin : antigène, immunité active, lente, durable, préventive. Sérum : anticorps, immunité passive, immédiate, brève, curative.

## VIH et IST
• Le VIH détruit les lymphocytes T4. Transmission : sexuelle, sang, mère-enfant. Prévention : abstinence, fidélité, préservatif, objets tranchants non partagés. Dépistage par test.

## Système nerveux
• Réflexe : involontaire, centre = moelle épinière. Arc réflexe : récepteur, nerf sensitif, moelle, nerf moteur, muscle.
• Acte volontaire : centre = cerveau. Cervelet : équilibre.

## Hérédité
• 46 chromosomes (23 paires) ; gamètes : 23. Femme XX, homme XY. Le spermatozoïde détermine le sexe.
• Gène = portion de chromosome ; trisomie 21 = 47 chromosomes.

## Le sol
• Minéral (sable, limon, argile) + organique (litière, humus) + eau + air + êtres vivants.
• Humification puis minéralisation. Horizons A (humus), B, C, roche mère.
• Protection : reboisement, jachère, courbes de niveau, compost.

## Conseils pour l'épreuve
• Utilise le vocabulaire exact (antigène, anticorps, phagocytose, arc réflexe…).
• Pour un schéma : titre, légendes à la règle, flèches dans le bon sens.
• Pour un document : décris d'abord ce que tu vois (chiffres à l'appui), puis explique.""",
questions=[
(2, "Contre une infection bactérienne, un médecin peut prescrire :", "un antibiotique", "un antiseptique à avaler", "un sérum antivenimeux", "un vaccin contre la rage",
 "L'antibiotique agit sur les bactéries."),
(2, "Les phagocytes détruisent les microbes par :", "phagocytose", "sérothérapie", "fécondation", "humification",
 "Ils les ingèrent puis les digèrent."),
(2, "Un vaccin agit :", "en apportant un antigène inoffensif qui provoque la fabrication d'anticorps", "en apportant des anticorps tout prêts", "en tuant directement les virus", "en remplaçant les globules rouges",
 "C'est une immunité active et durable."),
(2, "Le VIH se transmet par :", "le sang, les rapports sexuels non protégés et de la mère à l'enfant", "la piqûre de moustique", "la poignée de main", "les repas partagés",
 "Ce sont les trois seules voies de transmission."),
(2, "Le centre nerveux d'un réflexe médullaire, comme le réflexe rotulien, est :", "la moelle épinière", "le cerveau", "le cœur", "le muscle",
 "C'est pourquoi le réflexe est si rapide."),
(3, "Une femme transmet à son enfant :", "toujours un chromosome X", "toujours un chromosome Y", "un X ou un Y", "aucun chromosome sexuel",
 "Ses ovules portent tous un X."),
(3, "La cellule-œuf humaine contient :", "46 chromosomes", "23 chromosomes", "92 chromosomes", "47 chromosomes",
 "23 du spermatozoïde + 23 de l'ovule."),
(2, "L'horizon A du sol est riche en :", "humus", "roche mère", "sable uniquement", "fer pur",
 "C'est la couche sombre de surface."),
(3, "Le sérum antitétanique est utilisé :", "en urgence, pour une protection immédiate", "pour une protection de plusieurs années", "pour soigner la grippe", "à la place d'un antibiotique contre le paludisme",
 "Il apporte des anticorps qui agissent tout de suite."),
(3, "Le cervelet est le centre :", "de l'équilibre et de la coordination", "de la mémoire", "de la respiration", "de la vision",
 "Le tronc cérébral commande la respiration."),
(3, "Les lymphocytes B :", "fabriquent les anticorps", "détruisent les cellules infectées", "transportent le dioxygène", "digèrent les microbes",
 "Les T cytotoxiques détruisent les cellules infectées."),
(4, "Le sol est menacé d'érosion surtout lorsque :", "il est laissé nu après déforestation ou feu de brousse", "il est couvert de végétation", "on y apporte du compost", "on le laisse en jachère",
 "Sans couvert végétal, la pluie emporte la terre."),
(4, "Une personne séropositive au VIH sans aucun signe de maladie :", "peut transmettre le virus", "ne peut pas transmettre le virus", "est vaccinée", "est guérie",
 "Le virus est présent même sans symptôme ; le traitement réduit fortement la transmission."),
(4, "Quand on touche un objet brûlant, l'ordre du trajet du message nerveux est :", "peau, nerf sensitif, moelle épinière, nerf moteur, muscle", "muscle, nerf moteur, cerveau, peau", "cerveau, nerf sensitif, peau, muscle", "peau, nerf moteur, moelle épinière, nerf sensitif, muscle",
 "C'est l'arc réflexe."),
(4, "Pour protéger les sols agricoles, il est conseillé :", "d'apporter du compost et de pratiquer la rotation des cultures", "de brûler les résidus chaque année", "de cultiver la même plante sans arrêt", "de supprimer les arbres",
 "On entretient la matière organique et la fertilité."),
]),
]
