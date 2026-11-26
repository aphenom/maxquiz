NIVEAU, MATIERE = "6ème", "EDHC"

CHAPITRES = [
dict(
nom="L'école et le règlement intérieur",
fiche="""## L'école, un lieu de vie
Au collège, l'élève apprend, mais il vit aussi avec d'autres : camarades, professeurs, éducateurs, surveillants, personnel administratif, chef d'établissement (principal ou proviseur).

## Le règlement intérieur
C'est l'ensemble des règles qui organisent la vie dans l'établissement. Il est remis et expliqué en début d'année.
Il fixe notamment :
• les horaires et l'obligation d'assiduité (être présent) et de ponctualité (être à l'heure) ;
• la tenue scolaire (uniforme) ;
• le respect des personnes et du matériel ;
• les interdits : violence, tricherie, téléphone en classe (selon l'établissement), drogue, alcool, tabac, armes ;
• les sanctions : avertissement, blâme, exclusion temporaire ou définitive (décidée par le conseil de discipline).

## Les droits de l'élève
Recevoir un enseignement, être respecté, être protégé, s'exprimer (par les délégués), être informé de ses résultats.

## Les devoirs de l'élève
Travailler, faire ses devoirs, respecter les adultes et les camarades, prendre soin des locaux et du matériel, respecter le règlement.

## Pourquoi des règles ?
Sans règles, c'est le désordre et la loi du plus fort. Les règles protègent chacun et permettent d'apprendre dans de bonnes conditions.""",
questions=[
(1, "Être présent à tous les cours, c'est :", "être assidu", "être ponctuel", "être exclu", "être en retard",
 "La ponctualité, c'est être à l'heure."),
(1, "Arriver à l'heure en classe, c'est être :", "ponctuel", "assidu", "absent", "puni",
 "L'assiduité, c'est être présent."),
(2, "Le document qui fixe les règles de vie dans un collège est :", "le règlement intérieur", "le bulletin de notes", "le cahier de textes", "l'emploi du temps",
 "Il est expliqué en début d'année."),
(2, "Un droit de l'élève est :", "être respecté", "frapper ses camarades", "tricher aux devoirs", "sortir quand il veut",
 "Les droits vont avec des devoirs."),
(2, "Un devoir de l'élève est :", "prendre soin du matériel de l'école", "abîmer les tables", "insulter les surveillants", "manquer les cours",
 "Le matériel appartient à tous."),
(2, "La personne qui dirige un collège est :", "le principal (ou proviseur)", "le délégué de classe", "le surveillant", "le gardien",
 "C'est le chef d'établissement."),
(3, "Les règles à l'école servent surtout à :", "protéger chacun et permettre d'apprendre", "punir les élèves", "faire peur", "remplacer les cours",
 "Sans règles, c'est la loi du plus fort."),
(3, "Copier sur son voisin pendant un devoir est :", "de la tricherie, interdite", "un droit", "de l'entraide", "conseillé",
 "Elle est sanctionnée."),
(3, "Laquelle est une sanction prévue par le règlement intérieur ?", "l'avertissement", "la récompense", "la bourse", "le tableau d'honneur",
 "Il y a aussi le blâme et l'exclusion."),
(4, "Un élève est souvent en retard. Il manque surtout :", "de ponctualité", "d'assiduité", "de tolérance", "de solidarité",
 "Il vient, mais pas à l'heure."),
]),

dict(
nom="La vie de classe et les délégués",
fiche="""## La classe, une petite communauté
Chaque classe a un professeur principal, qui suit les élèves et fait le lien avec les parents et l'administration.

## Les délégués de classe
• Ils sont élus par les élèves de la classe en début d'année, au vote secret.
• En général, la classe élit un délégué et un délégué adjoint (suppléant).
• Rôle : représenter la classe, transmettre les demandes et les difficultés des élèves aux professeurs et à l'administration, participer aux conseils de classe, aider à maintenir l'ordre et la propreté.
• Le délégué n'est pas un chef : il est un porte-parole.

## L'élection : un apprentissage de la démocratie
Candidatures, campagne (présenter ses idées), vote secret, dépouillement, proclamation des résultats.
Comme pour les élections nationales : chacun vote librement, une voix par électeur, on accepte le résultat.

## Les qualités d'un bon délégué
Honnête, à l'écoute, disponible, respectueux, bon exemple pour la classe.

## Les responsabilités de chacun
Respecter le délégué élu, participer à la vie de classe (propreté, coopérative, clubs), aider les camarades en difficulté.""",
questions=[
(1, "Les délégués de classe sont :", "élus par les élèves", "nommés par le principal", "choisis par les parents", "tirés au sort par le gardien",
 "L'élection se fait au vote secret."),
(2, "Le rôle principal du délégué est de :", "représenter la classe et transmettre ses demandes", "punir les élèves", "donner les notes", "remplacer le professeur",
 "C'est un porte-parole."),
(2, "Le professeur qui suit particulièrement une classe est :", "le professeur principal", "le délégué", "le surveillant général", "le gardien",
 "Il fait le lien avec les parents."),
(2, "Lors de l'élection des délégués, le vote est :", "secret", "à main levée obligatoirement", "fait par le principal", "payant",
 "Chacun vote librement."),
(2, "Une qualité d'un bon délégué est :", "l'honnêteté", "la violence", "le mensonge", "l'absentéisme",
 "Il doit être un bon exemple."),
(3, "Le délégué participe :", "aux conseils de classe", "à la correction des devoirs", "au recrutement des professeurs", "aux élections présidentielles",
 "Il y donne l'avis de la classe."),
(3, "Compter les bulletins après un vote s'appelle :", "le dépouillement", "la campagne", "la candidature", "le boycott",
 "Puis on proclame les résultats."),
(3, "Après l'élection, les élèves qui ont voté pour un autre candidat doivent :", "respecter le délégué élu", "refuser de lui parler", "recommencer le vote", "se plaindre aux parents",
 "Accepter le résultat est un principe démocratique."),
(3, "L'élection des délégués permet d'apprendre :", "la démocratie", "la tricherie", "la violence", "l'impôt",
 "Voter, débattre, accepter le résultat."),
(4, "Le délégué de classe est avant tout :", "un porte-parole", "un chef qui donne des ordres", "un professeur adjoint", "un surveillant payé",
 "Il représente ses camarades."),
]),

dict(
nom="Les symboles de la République",
fiche="""## La Côte d'Ivoire
Devenue indépendante le 7 août 1960, la Côte d'Ivoire est une République. Le 7 août est la fête de l'Indépendance.
Premier Président : Félix Houphouët-Boigny.

## Les symboles
• Le drapeau : trois bandes verticales de même largeur, orange (côté hampe), blanc et vert.
  – orange : la savane du nord et la terre fertile ;
  – blanc : la paix et l'unité ;
  – vert : la forêt et l'espérance.
• L'hymne national : l'Abidjanaise, qui commence par « Salut ô terre d'espérance ».
• La devise : Union – Discipline – Travail.
• Les armoiries : une tête d'éléphant, animal emblème du pays.

## Les attributs
• Capitale politique : Yamoussoukro ; capitale économique : Abidjan.
• Langue officielle : le français.
• Monnaie : le franc CFA (FCFA), utilisé dans l'UEMOA.

## Respecter les symboles
Se lever et se tenir droit pendant l'hymne, ne pas déchirer ni salir le drapeau, participer à la montée des couleurs.""",
questions=[
(1, "La Côte d'Ivoire est devenue indépendante le :", "7 août 1960", "1er janvier 1960", "8 novembre 2016", "20 novembre 1989",
 "Le 7 août est la fête de l'Indépendance."),
(1, "La devise de la Côte d'Ivoire est :", "Union – Discipline – Travail", "Liberté – Égalité – Fraternité", "Paix – Unité – Progrès", "Travail – Famille – Patrie",
 "Elle figure dans la Constitution."),
(2, "L'hymne national s'appelle :", "l'Abidjanaise", "l'Ivoirienne", "la Lagunaire", "le Chant de la paix",
 "Il commence par « Salut ô terre d'espérance »."),
(2, "Sur le drapeau, la bande placée du côté de la hampe est :", "orange", "verte", "blanche", "rouge",
 "Orange, blanc, vert."),
(2, "Dans le drapeau, le blanc symbolise :", "la paix et l'unité", "la savane", "la forêt", "le sang",
 "L'orange évoque la savane, le vert la forêt."),
(2, "L'animal emblème de la Côte d'Ivoire est :", "l'éléphant", "le lion", "l'aigle", "le crocodile",
 "Il figure sur les armoiries."),
(3, "Le premier Président de la Côte d'Ivoire est :", "Félix Houphouët-Boigny", "Henri Konan Bédié", "Laurent Gbagbo", "Alassane Ouattara",
 "Président de 1960 à 1993."),
(3, "La capitale politique de la Côte d'Ivoire est :", "Yamoussoukro", "Abidjan", "Bouaké", "Korhogo",
 "Abidjan est la capitale économique."),
(3, "Pendant l'exécution de l'hymne national, on doit :", "se lever et se tenir droit", "continuer à parler", "rester assis en mangeant", "quitter la cour",
 "C'est une marque de respect."),
(4, "La monnaie utilisée en Côte d'Ivoire est :", "le franc CFA", "le naira", "le cedi", "l'euro",
 "Elle est commune aux pays de l'UEMOA."),
]),

dict(
nom="La politesse et le savoir-vivre",
fiche="""## Définitions
• La politesse : ensemble des règles de comportement qui montrent le respect des autres.
• Le savoir-vivre : savoir se conduire en société, à la maison, à l'école, dans la rue.

## Les mots magiques
Bonjour, bonsoir, s'il vous plaît, merci, pardon, excusez-moi, au revoir.

## Les gestes de politesse
• Saluer en arrivant, céder sa place à une personne âgée, une femme enceinte ou une personne handicapée dans le bus ou le gbaka.
• Frapper avant d'entrer, attendre son tour, ne pas couper la parole.
• Respecter les aînés : en Côte d'Ivoire, on salue les « tontons » et les « tanties », on les aide à porter leurs charges.
• À table : se laver les mains, ne pas parler la bouche pleine, attendre que les aînés commencent.

## La politesse au téléphone et sur Internet
Se présenter, parler poliment, ne pas insulter ni se moquer dans les messages ou sur les réseaux sociaux.

## Les impolitesses
Insultes, moqueries, cris, crachats par terre, bousculades, gestes vulgaires.

## Pourquoi être poli ?
La politesse facilite la vie en groupe, évite les conflits et donne une bonne image de soi.""",
questions=[
(1, "Quand on reçoit un cadeau, on dit :", "merci", "pardon", "au revoir", "rien",
 "C'est un des mots de politesse."),
(1, "Avant d'entrer dans le bureau du principal, on doit :", "frapper à la porte", "entrer en courant", "crier son nom", "pousser la porte du pied",
 "Puis attendre qu'on nous invite à entrer."),
(2, "Dans un bus plein, un élève poli :", "cède sa place à une personne âgée", "garde sa place et fait semblant de dormir", "pousse les autres", "met son sac sur le siège voisin",
 "On cède aussi sa place aux femmes enceintes."),
(2, "Couper la parole à quelqu'un est :", "impoli", "poli", "obligatoire", "un signe de respect",
 "On attend que l'autre ait fini."),
(2, "Le savoir-vivre, c'est :", "savoir se conduire en société", "savoir conduire une voiture", "savoir nager", "savoir compter",
 "À la maison, à l'école, dans la rue."),
(2, "À table, il est poli de :", "ne pas parler la bouche pleine", "manger dans l'assiette des autres", "jeter les restes par terre", "commencer avant tout le monde",
 "Et de se laver les mains avant."),
(3, "Se moquer d'un camarade sur un réseau social est :", "une forme d'impolitesse et de harcèlement", "une simple plaisanterie sans conséquence", "conseillé", "un droit",
 "La politesse s'applique aussi en ligne."),
(3, "Cracher par terre dans la cour est :", "impoli et mauvais pour l'hygiène", "poli", "obligatoire", "un signe de respect",
 "Cela peut transmettre des microbes."),
(3, "La politesse facilite :", "la vie en groupe", "les conflits", "les bagarres", "l'exclusion",
 "Elle montre le respect des autres."),
(4, "Un élève bouscule une personne sans le vouloir. Il doit :", "s'excuser", "partir en courant", "rire", "l'insulter",
 "« Pardon » ou « Excusez-moi »."),
]),

dict(
nom="L'hygiène corporelle et la propreté de l'école",
fiche="""## L'hygiène corporelle
• Se laver le corps chaque jour avec du savon.
• Se brosser les dents matin et soir et après les repas.
• Se laver les mains au savon avant de manger et après être allé aux toilettes.
• Couper ses ongles, se coiffer, porter des vêtements propres (uniforme lavé et repassé).

## La propreté de la classe et de l'école
• Jeter les papiers et les sachets dans les poubelles.
• Participer au balayage et aux journées de salubrité.
• Utiliser correctement les toilettes et tirer la chasse ou verser de l'eau.
• Ne pas écrire sur les murs ni sur les tables.

## Les conséquences du manque d'hygiène
Maladies de la peau (gale, teigne), caries, diarrhées, choléra, poux, mauvaises odeurs, mise à l'écart par les autres.

## L'eau potable
Boire de l'eau propre (robinet, eau traitée, eau bouillie) ; ne pas boire l'eau des puits non protégés sans la traiter ; garder les récipients d'eau couverts.

## Vente aux abords de l'école
Choisir des aliments protégés des mouches et de la poussière, vendus dans des conditions propres.""",
questions=[
(1, "On doit se laver les mains :", "avant de manger et après les toilettes", "une fois par semaine", "seulement le dimanche", "jamais avec du savon",
 "C'est le geste le plus simple contre les maladies."),
(1, "Les papiers et sachets doivent être jetés :", "dans la poubelle", "dans la cour", "sous la table", "dans le caniveau",
 "Pour garder l'école propre."),
(2, "Se brosser les dents permet d'éviter :", "les caries", "le paludisme", "les poux", "la rougeole",
 "Matin, soir et après les repas."),
(2, "Écrire sur les tables de la classe est :", "une dégradation du bien commun", "une décoration autorisée", "un exercice d'écriture", "obligatoire",
 "Les tables servent à tous les élèves."),
(2, "Les journées de salubrité à l'école servent à :", "nettoyer les locaux et la cour", "faire des examens", "élire les délégués", "chanter l'hymne",
 "Chacun participe à la propreté."),
(2, "La gale et la teigne sont des maladies :", "de la peau", "des dents", "des yeux uniquement", "du cœur",
 "Elles sont favorisées par le manque d'hygiène."),
(3, "L'eau d'un puits non protégé doit être :", "traitée ou bouillie avant d'être bue", "bue directement", "laissée au soleil seulement", "mélangée avec du sucre",
 "Elle peut contenir des microbes."),
(3, "Acheter un beignet exposé aux mouches est :", "risqué pour la santé", "sans risque", "conseillé", "obligatoire",
 "Les mouches transportent des microbes."),
(3, "Une conséquence du manque d'hygiène corporelle est :", "les maladies de la peau et les mauvaises odeurs", "de meilleures notes", "une bonne santé", "plus d'amis",
 "Et parfois la mise à l'écart."),
(4, "Pourquoi garder les récipients d'eau couverts ?", "pour éviter la poussière, les insectes et les microbes", "pour que l'eau soit plus froide", "pour économiser du savon", "pour que l'eau s'évapore",
 "L'eau reste propre à la consommation."),
]),

dict(
nom="La solidarité et l'entraide",
fiche="""## Définitions
• La solidarité : le lien qui unit les membres d'un groupe et les pousse à s'aider les uns les autres.
• L'entraide : l'aide que l'on s'apporte mutuellement.

## Les formes de solidarité
• Dans la famille : prendre soin des grands-parents, aider les petits frères et sœurs.
• À l'école : expliquer une leçon à un camarade en difficulté, partager son goûter, prêter un livre, rendre visite à un camarade malade.
• Dans le quartier ou le village : cotisations lors d'un décès, d'un mariage ou d'une naissance, travaux collectifs, tontines.
• Au niveau national : aide aux sinistrés (inondations), dons de sang, couverture maladie universelle (CMU).
• Au niveau international : aide humanitaire (Croix-Rouge, UNICEF).

## Les personnes vulnérables
Personnes âgées, personnes handicapées, orphelins, malades, sinistrés. Elles ont droit au respect et à l'aide.

## Les contraires de la solidarité
L'égoïsme, l'indifférence, l'exclusion, la moquerie envers les plus faibles.

## Un proverbe
« Un seul doigt ne peut pas ramasser la farine » : on réussit mieux ensemble.""",
questions=[
(1, "S'aider les uns les autres, c'est :", "l'entraide", "l'égoïsme", "l'exclusion", "l'indifférence",
 "C'est une forme de solidarité."),
(2, "Expliquer une leçon à un camarade en difficulté est un acte de :", "solidarité", "tricherie", "égoïsme", "moquerie",
 "On l'aide à progresser."),
(2, "Le contraire de la solidarité est :", "l'égoïsme", "l'entraide", "le partage", "la générosité",
 "Penser seulement à soi."),
(2, "Une cotisation des habitants pour aider une famille en deuil est :", "une forme de solidarité", "un impôt", "une amende", "un jeu",
 "Une pratique courante dans les quartiers et villages."),
(2, "Donner son sang est un geste de solidarité :", "envers les malades", "envers les commerçants", "sans utilité", "interdit",
 "Il peut sauver des vies."),
(3, "Une personne vulnérable est par exemple :", "une personne âgée ou handicapée", "un champion de football", "un ministre", "un commerçant prospère",
 "Elle a besoin d'attention et d'aide."),
(3, "L'aide apportée aux victimes d'une inondation s'appelle :", "l'aide aux sinistrés", "la contrebande", "la fraude", "l'arbitrage",
 "C'est une solidarité nationale."),
(3, "Se moquer d'un camarade handicapé est :", "un manque de respect et de solidarité", "une plaisanterie acceptable", "un droit", "de l'entraide",
 "Il a droit au respect."),
(3, "« Un seul doigt ne peut pas ramasser la farine » signifie :", "on réussit mieux ensemble", "il faut manger seul", "la farine est rare", "il faut travailler sans aide",
 "C'est un proverbe sur la solidarité."),
(4, "Une organisation internationale d'aide humanitaire est :", "la Croix-Rouge", "la CIE", "la SODECI", "la DGI",
 "Elle secourt les victimes de catastrophes et de conflits."),
]),

dict(
nom="La sécurité sur le chemin de l'école",
fiche="""## Le piéton
• Marcher sur le trottoir ; s'il n'y en a pas, sur le bord gauche de la route, face aux véhicules.
• Traverser au passage pour piétons (« zébras ») ou aux feux, quand le petit bonhomme est vert.
• Avant de traverser : s'arrêter, regarder à gauche, à droite, puis encore à gauche ; traverser en marchant, sans courir.
• Ne pas jouer au ballon au bord de la route ; ne pas traverser entre deux véhicules garés.

## Dans les transports
• Attendre que le véhicule (bus, gbaka, taxi, wôrô-wôrô) soit arrêté pour monter ou descendre.
• Ne pas se pencher par la fenêtre, ne pas s'accrocher à l'arrière des véhicules.
• Sur une moto, porter un casque.

## Les dangers sur le chemin
• Les inconnus : ne pas accepter de cadeau, de nourriture ou de transport d'un inconnu ; ne pas suivre quelqu'un qu'on ne connaît pas.
• Les lieux isolés : préférer marcher en groupe, sur le chemin habituel.
• Les fils électriques tombés, les caniveaux ouverts, les chantiers.

## En cas de problème
Aller vers un lieu fréquenté (boutique, école), prévenir un adulte de confiance, un agent de police ou appeler les secours (police 111 ou 110, pompiers 180).""",
questions=[
(1, "Pour traverser la route, on utilise :", "le passage pour piétons", "le milieu du carrefour", "l'espace entre deux voitures garées", "un virage",
 "On l'appelle aussi « zébra »."),
(1, "Avant de traverser, on regarde :", "à gauche, à droite, puis encore à gauche", "seulement devant soi", "seulement en l'air", "son téléphone",
 "Et on traverse en marchant."),
(2, "Sur une route sans trottoir, le piéton marche :", "sur le bord gauche, face aux véhicules", "au milieu de la route", "sur le bord droit, dos aux véhicules", "en zigzag",
 "Pour voir venir les véhicules."),
(2, "On monte dans un gbaka :", "quand il est complètement arrêté", "pendant qu'il roule", "par la fenêtre", "en s'accrochant à l'arrière",
 "Pour éviter de tomber."),
(2, "Un inconnu propose de te ramener à la maison en voiture. Tu dois :", "refuser et prévenir un adulte de confiance", "accepter tout de suite", "lui donner ton adresse", "le suivre s'il a l'air gentil",
 "On ne suit jamais un inconnu."),
(2, "Au feu pour piétons, on traverse quand le petit bonhomme est :", "vert", "rouge", "orange", "éteint",
 "Rouge : on attend."),
(3, "Il vaut mieux faire le chemin de l'école :", "en groupe, sur le chemin habituel", "seul, par des raccourcis isolés", "en courant sur la route", "en jouant au ballon",
 "Le groupe protège."),
(3, "Un fil électrique tombé sur le chemin :", "ne doit pas être touché", "peut être ramassé", "sert de corde à sauter", "est sans danger",
 "Il peut être sous tension."),
(3, "S'accrocher à l'arrière d'un véhicule est :", "très dangereux", "un jeu sans risque", "autorisé", "conseillé pour aller plus vite",
 "On peut tomber et être écrasé."),
(4, "Si tu te sens suivi sur le chemin de l'école, le mieux est de :", "aller vers un lieu fréquenté et prévenir un adulte", "aller dans un lieu isolé", "te cacher seul dans un buisson", "ne jamais en parler",
 "Une boutique, l'école, un agent de police."),
]),

dict(
nom="Révision de l'année",
fiche="""## L'école
• Assiduité (être présent) et ponctualité (être à l'heure) ; règlement intérieur : droits, devoirs, sanctions.
• Délégués élus au vote secret ; ils sont porte-parole de la classe.

## La Nation
• Indépendance : 7 août 1960 ; premier Président : Félix Houphouët-Boigny.
• Drapeau orange-blanc-vert ; hymne : l'Abidjanaise ; devise : Union – Discipline – Travail ; emblème : l'éléphant.
• Capitale politique : Yamoussoukro ; monnaie : le franc CFA.

## Vivre avec les autres
• Politesse : bonjour, merci, pardon ; céder sa place ; ne pas couper la parole.
• Solidarité et entraide ; contraire : égoïsme.

## Santé et sécurité
• Hygiène : mains, dents, vêtements ; propreté de l'école ; eau potable.
• Route : passage pour piétons ; regarder à gauche, à droite, à gauche ; ne pas suivre un inconnu.""",
questions=[
(2, "Le 7 août, on célèbre en Côte d'Ivoire :", "la fête de l'Indépendance", "la fête du Travail", "la Journée de l'enfant", "le Nouvel An",
 "Indépendance en 1960."),
(2, "Être ponctuel, c'est :", "arriver à l'heure", "être présent", "être poli", "être solidaire",
 "L'assiduité, c'est la présence."),
(2, "Les délégués de classe sont élus :", "au vote secret par les élèves", "par le gardien", "par tirage au sort des parents", "par le délégué de l'année précédente",
 "C'est un exercice de démocratie."),
(3, "L'éléphant est :", "l'animal emblème de la Côte d'Ivoire", "l'animal emblème du Ghana", "un symbole du drapeau", "l'hymne national",
 "Il figure sur les armoiries."),
(3, "Céder sa place à une femme enceinte dans le bus est un acte de :", "politesse", "tricherie", "égoïsme", "désordre",
 "C'est le savoir-vivre."),
(3, "Partager son goûter avec un camarade qui n'a rien est un acte de :", "solidarité", "fraude", "moquerie", "désobéissance",
 "C'est de l'entraide."),
(3, "Le vert du drapeau ivoirien symbolise :", "la forêt et l'espérance", "la savane", "la paix", "le sang des héros",
 "L'orange évoque la savane, le blanc la paix."),
(3, "Pour éviter les diarrhées, il faut :", "boire de l'eau potable et se laver les mains", "boire l'eau des caniveaux", "manger des aliments exposés aux mouches", "ne jamais se laver",
 "Ce sont des règles d'hygiène."),
(4, "Un camarade frappe un autre élève dans la cour. Il viole surtout :", "le règlement intérieur et le respect d'autrui", "le Code de la route", "la devise nationale seulement", "le droit de vote",
 "La violence est interdite à l'école."),
(4, "Tu dois traverser une route sans passage pour piétons. La bonne conduite est :", "t'arrêter, regarder à gauche, à droite, à gauche, puis traverser en marchant", "courir sans regarder", "traverser entre deux voitures garées", "traverser en regardant ton téléphone",
 "Toujours vérifier avant de traverser."),
]),
]
