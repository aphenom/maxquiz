NIVEAU, MATIERE = "3ème", "Anglais"

CHAPITRES = [
dict(
nom="Simple past et present perfect",
fiche="""## Le simple past (prétérit)
Action terminée, à un moment précis du passé.
• Forme : verbe + -ed (worked, played) ou forme irrégulière (go → went, see → saw, eat → ate).
• Négation et question avec did + base verbale : I didn't go. Did you see him?
• Mots repères : yesterday, last week, last year, in 2020, two days ago, when I was young.
   I visited Grand-Bassam last year.

## Le present perfect
Action passée qui a un lien avec le présent.
• Forme : have / has + participe passé (worked, gone, seen, eaten, written, been).
• Il sert pour :
   - une expérience : Have you ever eaten attiéké? I have never been to Ghana.
   - un résultat présent : She has lost her key (elle ne l'a toujours pas).
   - une action qui dure jusqu'à maintenant : We have lived in Abidjan since 2015.
• Mots repères : ever, never, just, already, yet, since, for.

## Since ou for ?
• since + point de départ : since 2015, since Monday, since I was ten.
• for + durée : for ten years, for two hours.

## Comparer
• I saw this film yesterday. (moment précis → simple past)
• I have seen this film. (expérience, sans date → present perfect)
On ne dit jamais « I have seen this film yesterday ».

## Verbes irréguliers à connaître
be – was/were – been · go – went – gone · see – saw – seen · eat – ate – eaten · write – wrote – written · take – took – taken · come – came – come · give – gave – given

## Pièges à éviter
• Après did, la base verbale : I didn't go (et non didn't went).
• Ago va avec le simple past : I arrived two days ago.""",
questions=[
(1, "I ___ to Yamoussoukro last year.", "went", "have gone", "go", "has gone",
 "« Last year » est un moment précis du passé : simple past. Go → went."),
(1, "We ___ in Abidjan since 2015.", "have lived", "lived", "live", "are living",
 "Action qui dure jusqu'à maintenant, avec since : present perfect."),
(1, "Le prétérit (simple past) de « see » est :", "saw", "seen", "seed", "sees",
 "see – saw – seen. « Seen » est le participe passé."),
(2, "My father has worked at the port ___ ten years.", "for", "since", "ago", "during",
 "For + durée (ten years). Since + point de départ."),
(2, "I have known Awa ___ 2020.", "since", "for", "ago", "during",
 "2020 est un point de départ : since."),
(2, "Have you ever ___ attiéké?", "eaten", "ate", "eat", "eating",
 "Present perfect : have + participe passé. eat – ate – eaten."),
(2, "They ___ the match two days ago.", "watched", "have watched", "watch", "has watched",
 "« Ago » indique un moment précis du passé : simple past."),
(2, "___ you ever been to Ghana?", "Have", "Did", "Do", "Has",
 "Expérience avec ever + been : present perfect, « Have you ever been… ? »."),
(3, "Quelle phrase est correcte ?", "I saw this film yesterday.", "I have seen this film yesterday.", "I have saw this film yesterday.", "I seen this film yesterday.",
 "Avec yesterday (moment précis), on utilise le simple past."),
(3, "He ___ to school yesterday because he was sick.", "didn't go", "hasn't gone", "didn't went", "doesn't went",
 "Négation au simple past : didn't + base verbale (go)."),
(3, "She has just ___. (arrive)", "arrived", "arrive", "arriving", "arrives",
 "Has + participe passé : arrived."),
(4, "When ___ you arrive in Abidjan? — Last Monday.", "did", "have", "has", "are",
 "When pose une question sur un moment précis : simple past, « When did you arrive… ? »."),
(4, "Le participe passé de « write » est :", "written", "wrote", "writed", "writing",
 "write – wrote – written."),
]),

dict(
nom="La voix passive",
fiche="""## Principe
À la voix passive, le sujet subit l'action.
• Actif : Aya cleans the classroom.
• Passif : The classroom is cleaned by Aya.
Le complément d'agent est introduit par « by ». On l'omet quand il n'est pas important : Cocoa is grown in Côte d'Ivoire.

## Formation
BE (au temps du verbe actif) + participe passé.
• Présent : is / are + p.p. → English is spoken in Ghana.
• Prétérit : was / were + p.p. → The school was built in 2020.
• Present perfect : has / have been + p.p. → The road has been repaired.
• Futur : will be + p.p. → The results will be announced tomorrow.
• Avec un modal : must / can / should be + p.p. → This exercise must be written in ink.

## Méthode pour transformer
1. Le complément de l'actif devient le sujet du passif.
2. On conjugue BE au temps du verbe actif.
3. On ajoute le participe passé du verbe.
4. Le sujet de l'actif devient complément d'agent (by…), si utile.
They will open a new hospital. → A new hospital will be opened.

## Pièges à éviter
• Toujours le participe passé : is built (et non is build).
• Accorder BE avec le nouveau sujet : The letters were sent (pluriel).""",
questions=[
(1, "Cocoa ___ in Côte d'Ivoire.", "is grown", "is grow", "grown", "are grow",
 "Passif au présent : is + participe passé (grown)."),
(1, "The school ___ in 2020.", "was built", "is build", "was build", "built was",
 "Passif au prétérit : was + participe passé (built)."),
(1, "Le complément d'agent est introduit par :", "by", "of", "from", "with",
 "The classroom is cleaned by Aya."),
(2, "« Aya cleans the classroom. » Au passif :", "The classroom is cleaned by Aya.", "The classroom was cleaned by Aya.", "The classroom is clean by Aya.", "The classroom cleans by Aya.",
 "Le verbe actif est au présent : is + participe passé."),
(2, "The letters ___ yesterday.", "were sent", "was sent", "are sent", "have sent",
 "Sujet pluriel (letters) et moment passé (yesterday) : were + participe passé."),
(2, "The results ___ tomorrow.", "will be announced", "will announce", "are announce", "will been announced",
 "Futur passif : will be + participe passé."),
(2, "English ___ in Ghana.", "is spoken", "speaks", "is speaking", "spoken",
 "La langue ne parle pas : elle est parlée. Passif au présent."),
(3, "The road ___. (repair, present perfect)", "has been repaired", "has repaired", "have been repair", "is been repaired",
 "Present perfect passif : has been + participe passé."),
(3, "« They will open a new hospital. » Au passif :", "A new hospital will be opened.", "A new hospital will open.", "A new hospital is opened.", "A new hospital will been opened.",
 "Will be + participe passé (opened)."),
(3, "This exercise must ___ in ink.", "be written", "written", "be write", "been written",
 "Modal + be + participe passé."),
(4, "« The match was won by our team. » À l'actif :", "Our team won the match.", "Our team wins the match.", "The match won our team.", "Our team was won the match.",
 "Le complément d'agent devient sujet ; le verbe garde le temps (prétérit : won)."),
(4, "Quelle phrase est à la voix passive ?", "The fish was eaten by the cat.", "The cat ate the fish.", "The cat is eating the fish.", "The cat has eaten the fish.",
 "Be + participe passé, avec un complément d'agent introduit par by."),
]),

dict(
nom="Le discours indirect",
fiche="""## Say ou tell ?
• say (that) … : He said that he was late.
• tell + quelqu'un (that) … : He told me that he was late.
On ne dit pas « He said me ».

## La concordance des temps
Quand le verbe introducteur est au passé (said, told, asked), on « recule » les temps :
• présent → prétérit : "I am tired." → He said that he was tired.
• prétérit / present perfect → past perfect : "I saw the film." → She said that she had seen the film.
• will → would ; can → could.
Si le verbe introducteur est au présent (says), les temps ne changent pas : Koffi says that he is tired.

## Les autres changements
• Pronoms : I → he / she ; my → his / her ; you → I / me selon la situation.
• Temps et lieu : today → that day ; tomorrow → the next day ; yesterday → the day before ; now → then ; here → there.

## Les questions
• Question fermée : ask + if : "Are you ready?" → She asked if I was ready.
• Question avec mot interrogatif : on garde le mot, avec l'ordre sujet + verbe : "Where do you live?" → He asked me where I lived.

## Les ordres
tell / ask + quelqu'un + to + verbe ; à la forme négative : not to.
"Close the door." → The teacher told us to close the door.
"Don't talk!" → He told them not to talk.

## Pièges à éviter
• Pas d'inversion dans une question indirecte : where I lived (et non where did I live).
• Pas de « do / did » dans une question indirecte.""",
questions=[
(1, "Koffi says, \"I am tired.\" → Koffi says that ___.", "he is tired", "he was tired", "I am tired", "he tired",
 "Le verbe introducteur est au présent (says) : le temps ne change pas, seul le pronom change."),
(1, "She said, \"I am hungry.\" → ___", "She said that she was hungry.", "She said that I was hungry.", "She said that she were hungry.", "She said me that she was hungry.",
 "Présent → prétérit, I → she. On ne dit pas « said me »."),
(1, "He ___ me that he was late.", "told", "said", "say", "talked",
 "Tell + quelqu'un ; say s'emploie sans complément de personne."),
(2, "\"I will come,\" he said. → He said that ___.", "he would come", "he will came", "he would came", "I would come",
 "will → would, suivi de la base verbale."),
(2, "Au discours indirect, « tomorrow » devient :", "the next day", "yesterday", "today", "the day before",
 "Tomorrow → the next day (ou the following day)."),
(2, "\"Are you ready?\" she asked. → She asked ___.", "if I was ready", "if was I ready", "that I was ready", "if ready I was",
 "Question fermée : if + sujet + verbe, avec concordance des temps."),
(2, "Au discours indirect, « here » devient :", "there", "now", "then", "that",
 "Here → there ; now → then."),
(3, "\"Where do you live?\" he asked me. → He asked me ___.", "where I lived", "where did I live", "where do I live", "where I live did",
 "Ordre sujet + verbe, sans do/did, et concordance des temps."),
(3, "\"Close the door,\" the teacher said to us. → The teacher ___.", "told us to close the door", "told us close the door", "said us to close the door", "told to us close the door",
 "Ordre : tell + quelqu'un + to + verbe."),
(3, "\"Don't talk!\" he said to them. → He told them ___.", "not to talk", "don't talk", "not talk", "didn't talk",
 "Ordre négatif : not to + verbe."),
(3, "\"I can swim,\" Ali said. → Ali said that he ___.", "could swim", "can swam", "could swam", "would can swim",
 "can → could, suivi de la base verbale."),
(4, "\"I saw the film yesterday,\" she said. → She said that ___.", "she had seen the film the day before", "she had saw the film the day before", "she has seen the film yesterday", "she had seen the film tomorrow",
 "Prétérit → past perfect (had seen) ; yesterday → the day before."),
]),

dict(
nom="Les phrases conditionnelles",
fiche="""## Condition 0 : une vérité générale
If + présent, présent.
If you heat ice, it melts.

## Condition 1 : une situation possible, réelle
If + présent, will + base verbale.
If it rains, we will stay at home.
If she studies hard, she will pass her BEPC.
Attention : jamais « will » après if.

## Condition 2 : une situation imaginaire ou peu probable
If + prétérit, would + base verbale.
If I had a car, I would drive you to Bassam.
Avec be, on emploie « were » à toutes les personnes : If I were rich, I would build a school.
Pour donner un conseil : If I were you, I would see a doctor.

## Condition 3 : un regret sur le passé
If + past perfect, would have + participe passé.
If he had worked harder, he would have passed the exam.

## Unless
unless = if … not.
Unless you hurry, you will miss the bus. = If you don't hurry, you will miss the bus.

## Méthode
Repère le temps après « if » : il te donne le type de condition, donc la forme de l'autre partie.
• présent → will
• prétérit → would
• past perfect → would have + p.p.

## Pièges à éviter
• If I would have… est faux.
• La virgule s'emploie quand la phrase commence par if.""",
questions=[
(1, "If it rains, we ___ at home.", "will stay", "would stay", "stayed", "would have stayed",
 "If + présent (rains) → will + base verbale."),
(1, "If you heat ice, it ___.", "melts", "melted", "would melt", "had melted",
 "Vérité générale : if + présent, présent."),
(2, "If I ___ rich, I would build a school.", "were", "am", "will be", "have been",
 "Condition imaginaire : if + prétérit ; avec be, « were » à toutes les personnes."),
(2, "If she studies hard, she ___ her BEPC.", "will pass", "would pass", "passed", "would have passed",
 "If + présent → will + base verbale."),
(2, "If I had a car, I ___ you to Bassam.", "would drive", "will drive", "drive", "drove",
 "If + prétérit (had) → would + base verbale."),
(2, "« Unless you hurry, you will miss the bus » signifie :", "If you don't hurry, you will miss the bus.", "If you hurry, you will miss the bus.", "You hurry because you missed the bus.", "You will hurry if you miss the bus.",
 "Unless = if … not."),
(3, "Quelle phrase est correcte ?", "If I were you, I would see a doctor.", "If I was you, I will see a doctor.", "If I am you, I would see a doctor.", "If I were you, I will see a doctor.",
 "Conseil : If I were you, I would + base verbale."),
(3, "If he had worked harder, he ___ the exam.", "would have passed", "would pass", "will pass", "had passed",
 "If + past perfect → would have + participe passé."),
(3, "What ___ you do if you won the lottery?", "would", "will", "did", "do",
 "If + prétérit (won) → would."),
(3, "If we don't protect the forest, the animals ___.", "will disappear", "would disappear", "disappeared", "had disappeared",
 "If + présent → will + base verbale."),
(4, "Quelle phrase exprime une situation imaginaire ?", "If I were a bird, I would fly.", "If it rains, I will stay.", "If you heat water, it boils.", "If you come, I will help you.",
 "Condition 2 : if + prétérit, would + base verbale."),
(4, "I ___ you if I had your number.", "would call", "will call", "call", "called",
 "If + prétérit (had) → would + base verbale, même quand « if » est en deuxième position."),
]),

dict(
nom="Les modaux",
fiche="""## Règles communes
• Le modal est suivi de la base verbale, sans « to » : She can swim.
• Pas de -s à la 3ᵉ personne : He must go.
• Négation : can't / cannot, mustn't, shouldn't…

## Le sens des principaux modaux
• can : capacité (I can speak English), permission (You can go).
• could : capacité dans le passé (When I was five, I could swim), demande polie.
• may : permission polie (May I open the window?), probabilité.
• might : probabilité faible (Take an umbrella, it might rain).
• must : obligation forte (You must listen), déduction sûre (He has worked all day, he must be tired).
• mustn't : interdiction (You mustn't smoke here).
• should : conseil (You should go to bed early).

## Have to
• have to : obligation venant de l'extérieur, d'une règle : We have to wear a uniform.
• don't have to : absence d'obligation (ce n'est pas nécessaire) : Tomorrow is Sunday, we don't have to get up early.

## mustn't ou don't have to ?
• You mustn't come = tu n'as pas le droit de venir (interdiction).
• You don't have to come = tu n'es pas obligé de venir.

## Pièges à éviter
• « must to » et « can to » n'existent pas.
• Au passé, must devient had to : Yesterday I had to walk.""",
questions=[
(1, "You ___ smoke in the hospital. It's forbidden.", "mustn't", "don't have to", "can", "should",
 "Interdiction : mustn't."),
(1, "She ___ speak three languages.", "can", "cans", "can to", "is can",
 "Modal + base verbale, sans -s et sans to."),
(2, "You look tired. You ___ go to bed early.", "should", "mustn't", "can't", "may not",
 "Conseil : should."),
(2, "Tomorrow is Sunday, we ___ get up early.", "don't have to", "mustn't", "must", "have to",
 "Ce n'est pas nécessaire (absence d'obligation) : don't have to. Mustn't serait une interdiction."),
(2, "Take an umbrella, it ___ rain.", "might", "must not", "can't", "has to",
 "Probabilité : might."),
(2, "He must ___ his homework.", "do", "to do", "does", "doing",
 "Après un modal : base verbale."),
(3, "When I was five, I ___ swim.", "could", "can", "must", "should",
 "Capacité dans le passé : could."),
(3, "___ I open the window, please?", "May", "Am", "Have", "Mustn't",
 "Demande de permission polie : May I… ?"),
(3, "He has worked all day. He ___ be tired.", "must", "mustn't", "doesn't have to", "can to",
 "Déduction quasi certaine : must."),
(3, "« You don't have to come » signifie :", "Tu n'es pas obligé de venir.", "Tu n'as pas le droit de venir.", "Tu dois venir.", "Tu ne peux pas venir.",
 "Don't have to = absence d'obligation."),
(4, "In our school, students ___ wear a uniform; it's the rule.", "have to", "don't have to", "might", "can't",
 "Obligation imposée par une règle : have to."),
(4, "La forme négative de « can » est :", "cannot (can't)", "doesn't can", "don't can", "can to not",
 "Les modaux se mettent à la forme négative sans do."),
]),

dict(
nom="Les pronoms relatifs",
fiche="""## À quoi ils servent
Ils relient deux phrases en évitant une répétition.
I have a friend. He plays football. → I have a friend who plays football.

## Les principaux pronoms relatifs
• who : pour une personne. The man who lives next door is a doctor.
• which : pour une chose ou un animal. This is the book which I bought yesterday.
• that : pour une personne ou une chose (dans une relative qui précise de qui ou de quoi on parle). The car that is parked outside is mine.
• whose : possession (« dont le / la »). The girl whose father is a teacher sits next to me.
• where : un lieu. This is the village where I was born.
• when : un moment. I remember the day when we won the cup.
• whom : personne complément (langue soutenue). The teacher whom we met is very kind.

## Méthode
Regarde le mot qui précède : personne → who ; chose → which ; lieu → where ; moment → when ; possession → whose.

## Pièges à éviter
• « who » ne s'emploie jamais pour une chose : The pen which is on the table (et non who).
• whose est toujours suivi d'un nom : whose father, whose results.""",
questions=[
(1, "The man ___ lives next door is a doctor.", "who", "which", "where", "whose",
 "Une personne, sujet du verbe lives : who."),
(1, "This is the book ___ I bought yesterday.", "which", "who", "where", "whose",
 "Une chose : which."),
(2, "The girl ___ father is a teacher sits next to me.", "whose", "who", "which", "where",
 "Possession (son père) : whose + nom."),
(2, "This is the village ___ I was born.", "where", "which", "who", "whose",
 "Un lieu : where."),
(2, "I remember the day ___ we won the cup.", "when", "where", "who", "whose",
 "Un moment : when."),
(2, "Adjamé market is a place ___ you can find everything.", "where", "who", "whose", "when",
 "Un lieu : where."),
(3, "« I have a friend. He plays football. » En une phrase :", "I have a friend who plays football.", "I have a friend which plays football.", "I have a friend whose plays football.", "I have a friend where plays football.",
 "Une personne, sujet du verbe : who."),
(3, "The car ___ is parked outside is mine.", "which", "who", "whose", "where",
 "Une chose : which (on pourrait aussi dire that)."),
(3, "The teacher ___ we met is very kind.", "whom", "which", "whose", "where",
 "Une personne complément du verbe met : whom (ou who, that, en anglais courant)."),
(3, "« That » peut remplacer :", "who ou which", "where uniquement", "whose uniquement", "when uniquement",
 "That s'emploie pour les personnes comme pour les choses, dans une relative qui précise."),
(4, "The students ___ results were good received a prize.", "whose", "who", "which", "whom",
 "Les résultats des élèves : possession, whose + nom."),
(4, "Quelle phrase est correcte ?", "The pen which is on the table is red.", "The pen who is on the table is red.", "The pen whose is on the table is red.", "The pen where is on the table is red.",
 "Un stylo est une chose : which (ou that), jamais who."),
]),

dict(
nom="Comparatifs et superlatifs",
fiche="""## Adjectifs courts (une syllabe, ou deux syllabes terminées par -y)
• Comparatif : adjectif + -er + than : Abidjan is bigger than Bouaké.
• Superlatif : the + adjectif + -est : the highest mountain.
• Orthographe : big → bigger (consonne doublée), happy → happier (y → i), nice → nicer.

## Adjectifs longs
• Comparatif : more + adjectif + than : more difficult than.
• Superlatif : the most + adjectif : the most interesting book.

## Irréguliers
• good → better → the best
• bad → worse → the worst
• far → farther / further → the farthest / the furthest

## Égalité et infériorité
• as + adjectif + as : Awa is as tall as her brother.
• not as … as : Bouaké is not as big as Abidjan.
• less + adjectif + than : Rice is less expensive than meat.

## Une tournure utile
The more you read, the more you learn. (Plus tu lis, plus tu apprends.)

## Pièges à éviter
• Jamais « more bigger » : on ne cumule pas -er et more.
• Comparatif → than ; égalité → as … as.""",
questions=[
(1, "Abidjan is ___ than Bouaké.", "bigger", "more big", "biggest", "big",
 "Adjectif court : big → bigger (consonne doublée) + than."),
(1, "Le superlatif de « good » est :", "the best", "the goodest", "the better", "the most good",
 "good – better – the best."),
(2, "This exercise is ___ than the last one.", "more difficult", "difficulter", "most difficult", "more difficulter",
 "Adjectif long : more + adjectif + than."),
(2, "Mount Nimba is the ___ mountain in Côte d'Ivoire.", "highest", "higher", "most high", "high",
 "Superlatif d'un adjectif court : the + -est."),
(2, "Le comparatif de « bad » est :", "worse", "badder", "worst", "more bad",
 "bad – worse – the worst."),
(2, "Awa is as tall ___ her brother.", "as", "than", "that", "like",
 "Égalité : as + adjectif + as."),
(3, "Le comparatif de « happy » est :", "happier", "happyer", "more happier", "the happiest",
 "Adjectif en -y : y → i, puis -er."),
(3, "This is ___ book I have ever read.", "the most interesting", "the more interesting", "most interesting", "the interestingest",
 "Adjectif long au superlatif : the most + adjectif."),
(3, "My house is ___ from school than yours.", "farther", "farer", "more far", "farest",
 "far – farther (ou further) – the farthest."),
(3, "Rice is ___ expensive than meat.", "less", "least", "fewer", "lesser",
 "Infériorité : less + adjectif + than."),
(4, "Abidjan is ___ city in Côte d'Ivoire.", "the biggest", "the bigger", "biggest", "the most big",
 "Superlatif d'un adjectif court : the + -est (consonne doublée), sans oublier « the »."),
(4, "The more you read, ___ you learn.", "the more", "more", "the most", "most",
 "Tournure « the more …, the more … » : plus …, plus …"),
]),

dict(
nom="Les question tags",
fiche="""## Principe
Le question tag est une petite question en fin de phrase, comme « n'est-ce pas ? ».
• Phrase affirmative → tag négatif : You are a student, aren't you?
• Phrase négative → tag affirmatif : He didn't come, did he?

## Construction
On reprend l'auxiliaire (ou le modal) de la phrase, puis le pronom sujet.
• She can swim, can't she?
• Your father has finished, hasn't he?
• S'il n'y a pas d'auxiliaire, on utilise do / does / did : They live in Daloa, don't they?

## Cas particuliers
• I am … → aren't I? : I am right, aren't I?
• Let's … → shall we? : Let's go to the beach, shall we?
• Impératif → will you? : Close the door, will you?
• There is … → isn't there? : There is a problem, isn't there?
• Never, nobody, nothing rendent la phrase négative → tag affirmatif : She never eats meat, does she?
• Nobody, everybody, somebody → pronom they : Nobody called me, did they?

## Pièges à éviter
• Le tag reprend le temps de la phrase : He didn't come, did he? (pas does he).
• Le pronom remplace le sujet : Your father … → he.""",
questions=[
(1, "You are a student, ___?", "aren't you", "are you", "don't you", "isn't it",
 "Phrase affirmative avec are → tag négatif aren't you."),
(1, "She can swim, ___?", "can't she", "can she", "doesn't she", "isn't she",
 "On reprend le modal can, à la forme négative."),
(2, "They live in Daloa, ___?", "don't they", "aren't they", "didn't they", "doesn't they",
 "Pas d'auxiliaire, présent, sujet they → don't they."),
(2, "He didn't come, ___?", "did he", "didn't he", "does he", "was he",
 "Phrase négative au prétérit → tag affirmatif did he."),
(2, "Your father has finished, ___?", "hasn't he", "doesn't he", "didn't he", "has he",
 "On reprend l'auxiliaire has à la forme négative."),
(2, "There is a problem, ___?", "isn't there", "isn't it", "is there", "doesn't it",
 "There is → isn't there."),
(3, "I am right, ___?", "aren't I", "amn't I", "am I", "isn't it",
 "Cas particulier : I am → aren't I."),
(3, "Let's go to the beach, ___?", "shall we", "will we", "don't we", "let's we",
 "Après let's, le tag est shall we."),
(3, "Close the door, ___?", "will you", "do you", "don't you", "are you",
 "Après un impératif, on emploie will you."),
(3, "Nobody called me, ___?", "did they", "didn't they", "did he", "does nobody",
 "Nobody rend la phrase négative → tag affirmatif, avec le pronom they."),
(4, "She never eats meat, ___?", "does she", "doesn't she", "did she", "is she",
 "Never rend la phrase négative → tag affirmatif, au présent : does she."),
(4, "You will help me, ___?", "won't you", "don't you", "aren't you", "will not you",
 "On reprend will à la forme négative contractée : won't you."),
]),

dict(
nom="Révision BEPC",
fiche="""## Fiche mémo d'Anglais 3ème

## Les temps
• Simple past : moment précis du passé (yesterday, ago, last…). Did + base verbale pour la négation et la question.
• Present perfect : have / has + participe passé ; expérience (ever, never), durée jusqu'à maintenant (since + point de départ, for + durée).

## La voix passive
BE au temps voulu + participe passé ; agent introduit par by.
is made · was built · has been repaired · will be announced · must be done

## Le discours indirect
say (that) / tell somebody (that). Présent → prétérit ; will → would ; can → could ; prétérit → past perfect.
Questions : ask if… / ask where I lived (sans inversion). Ordres : told us (not) to + verbe.

## Les conditions
• If + présent → will + base verbale (possible).
• If + prétérit → would + base verbale (imaginaire) ; If I were you…
• If + past perfect → would have + participe passé (regret).

## Les modaux
can (capacité), could (passé), may / might (probabilité, permission), must (obligation), mustn't (interdiction), don't have to (pas d'obligation), should (conseil).

## Relatifs, comparaisons, tags
• who (personne), which (chose), whose (possession), where (lieu), when (moment).
• bigger than / more difficult than / the biggest / the most difficult ; good → better → the best ; as … as.
• Tags : on reprend l'auxiliaire, en inversant affirmatif et négatif. I am → aren't I ; Let's → shall we.

## Conseils pour l'épreuve
• Lis le texte deux fois avant de répondre aux questions de compréhension.
• Pour « True or False », justifie avec une phrase exacte du texte.
• Relis tes verbes : temps, -s de la 3ᵉ personne, participes passés irréguliers.""",
questions=[
(2, "We ___ football yesterday.", "played", "have played", "play", "plays",
 "Yesterday : simple past."),
(2, "I have lived here ___ 2018.", "since", "for", "ago", "during",
 "2018 est un point de départ : since."),
(2, "The house ___ in 1990.", "was built", "built", "is build", "has build",
 "Passif au prétérit : was + participe passé."),
(2, "\"I am tired,\" he said. → He said that he ___ tired.", "was", "are", "were", "be",
 "Concordance des temps : présent → prétérit."),
(3, "If I ___ time, I would help you.", "had", "have", "will have", "would have",
 "Would dans la principale → if + prétérit."),
(2, "You ___ cross the road when the light is red.", "mustn't", "don't have to", "should", "can",
 "Interdiction : mustn't."),
(3, "The boy ___ bag was stolen is crying.", "whose", "who", "which", "where",
 "Possession (le sac du garçon) : whose."),
(2, "Lagos is ___ than Abidjan.", "bigger", "more big", "biggest", "the biggest",
 "Adjectif court au comparatif : bigger than."),
(2, "She is a doctor, ___?", "isn't she", "is she", "doesn't she", "isn't it",
 "Phrase affirmative avec is → isn't she."),
(3, "If it is sunny tomorrow, we ___ to the beach.", "will go", "would go", "went", "would have gone",
 "If + présent → will + base verbale."),
(3, "Have you ever ___ to Ghana?", "been", "be", "was", "being",
 "Present perfect : have + participe passé (been)."),
(3, "The teacher told us ___ quiet.", "to be", "be", "being", "that be",
 "Ordre rapporté : told us to + verbe."),
(3, "This is the ___ day of my life.", "best", "better", "goodest", "most good",
 "Superlatif irrégulier de good : the best."),
(4, "Koffi wrote the letter. → The letter ___ by Koffi.", "was written", "is written", "was wrote", "has written",
 "Passif au prétérit : was + participe passé (written)."),
(4, "She asked me, \"Where do you live?\" → She asked me where I ___.", "lived", "live", "did live", "do live",
 "Question indirecte : ordre sujet + verbe, sans do/did, avec concordance des temps."),
]),
]
