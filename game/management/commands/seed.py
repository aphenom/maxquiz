from django.core.management.base import BaseCommand
from game.models import Question, AdCampaign, GameConfig

# (catégorie, difficulté 1-4, question, options, index bonne réponse, explication)
QUESTIONS = [
    ("ci",1,"Quelle est la capitale politique de la Côte d'Ivoire ?",["Abidjan","Yamoussoukro","Bouaké","San-Pédro"],1,"Yamoussoukro est la capitale politique depuis 1983."),
    ("ci",2,"Quel fleuve traverse la Côte d'Ivoire du nord au sud ?",["Le Niger","Le Congo","Le Bandama","Le Sénégal"],2,"Le Bandama est le plus long fleuve entièrement ivoirien."),
    ("ci",1,"La basilique Notre-Dame de la Paix se trouve à…",["Abidjan","Grand-Bassam","Korhogo","Yamoussoukro"],3,"L'un des plus grands édifices religieux du monde."),
    ("ci",1,"Qui fut le premier président de la Côte d'Ivoire ?",["Henri Konan Bédié","Félix Houphouët-Boigny","Laurent Gbagbo","Robert Guéï"],1,"Il a dirigé le pays de 1960 à 1993."),
    ("ci",1,"La Côte d'Ivoire est le premier producteur mondial de…",["Café","Coton","Cacao","Hévéa"],2,"Environ 40 % du cacao mondial."),
    ("ci",2,"Combien de pays partagent une frontière avec la Côte d'Ivoire ?",["3","4","5","6"],2,"Liberia, Guinée, Mali, Burkina Faso et Ghana."),
    ("ci",1,"Le garba, plat populaire d'Abidjan, est à base de…",["Riz et poulet","Attiéké et thon","Foutou et sauce graine","Alloco et poisson"],1,"Attiéké + thon frit, le classique des maquis."),
    ("ci",2,"Quel est le plus grand pays d'Afrique par sa superficie ?",["RD Congo","Soudan","Algérie","Libye"],2,"L'Algérie, depuis la partition du Soudan en 2011."),
    ("ci",2,"Le mont Kilimandjaro se situe en…",["Kenya","Tanzanie","Éthiopie","Ouganda"],1,"Point culminant de l'Afrique : 5 895 m."),
    ("ci",3,"L'Abissa est la fête traditionnelle du peuple…",["Baoulé","Sénoufo","N'zima","Bété"],2,"Célébrée chaque année à Grand-Bassam."),
    ("ci",1,"Quel est l'indicatif téléphonique de la Côte d'Ivoire ?",["+221","+225","+228","+229"],1,"+225 !"),
    ("ci",2,"Quelle est la capitale du Ghana ?",["Kumasi","Lagos","Accra","Lomé"],2,"Accra, chez le voisin de l'est."),
    ("ci",3,"Combien de communes compte la ville d'Abidjan ?",["8","10","12","13"],1,"10 communes, d'Abobo à Yopougon."),
    ("ci",3,"Grand-Bassam fut la première capitale. Quelle ville lui a succédé avant Abidjan ?",["Bingerville","Dabou","Bouaké","Assinie"],0,"Bingerville, capitale de 1900 à 1934."),
    ("ci",4,"Quel est le point culminant de la Côte d'Ivoire ?",["Mont Tonkoui","Mont Nimba","Mont Péko","Mont Niénokoué"],1,"Le mont Nimba culmine à environ 1 752 m."),
    ("ci",3,"Quel était l'ancien nom du Ghana ?",["Côte-de-l'Or","Haute-Volta","Dahomey","Soudan français"],0,"La Gold Coast, ou Côte-de-l'Or."),
    ("ci",2,"Quel pays africain n'a jamais été durablement colonisé ?",["Kenya","Éthiopie","Sénégal","Angola"],1,"L'Éthiopie a repoussé l'Italie à Adoua en 1896."),
    ("ci",2,"Quelle est la monnaie du Nigeria ?",["Le cedi","Le naira","Le shilling","Le birr"],1,"Le naira nigérian."),
    ("ci",3,"Le franc CFA de l'UEMOA est émis par quelle institution ?",["BAD","BCEAO","BEAC","FMI"],1,"La Banque Centrale des États de l'Afrique de l'Ouest, basée à Dakar."),
    ("ci",4,"Combien de cordes possède traditionnellement une kora ?",["12","18","21","24"],2,"21 cordes pour la harpe-luth mandingue."),
    ("cg",2,"Quelle planète est la plus proche du Soleil ?",["Vénus","Mars","Mercure","La Terre"],2,"Mercure, à environ 58 millions de km."),
    ("cg",2,"Qui a écrit « Les Soleils des Indépendances » ?",["Bernard Dadié","Ahmadou Kourouma","Véronique Tadjo","Aké Loba"],1,"Chef-d'œuvre de l'Ivoirien Ahmadou Kourouma (1968)."),
    ("cg",3,"Qui a écrit « Une si longue lettre » ?",["Mariama Bâ","Aminata Sow Fall","Fatou Diome","Ken Bugul"],0,"Roman épistolaire de la Sénégalaise Mariama Bâ (1979)."),
    ("cg",1,"À quelle température l'eau bout-elle au niveau de la mer ?",["90 °C","95 °C","100 °C","110 °C"],2,"100 °C à pression atmosphérique normale."),
    ("cg",2,"Quel gaz est produit par la photosynthèse ?",["Le dioxyde de carbone","L'azote","L'oxygène","L'hydrogène"],2,"Les plantes rejettent de l'oxygène."),
    ("cg",1,"Quel organe pompe le sang dans le corps humain ?",["Le foie","Le cœur","Les poumons","Les reins"],1,"Environ 100 000 battements par jour."),
    ("cg",2,"Quelle langue compte le plus de locuteurs natifs au monde ?",["L'anglais","L'espagnol","Le mandarin","L'hindi"],2,"Plus de 900 millions de locuteurs natifs."),
    ("cg",2,"Quel élément chimique a pour symbole Fe ?",["Le fluor","Le fer","Le fermium","Le francium"],1,"Fe vient du latin ferrum."),
    ("cg",3,"Quelle est la capitale de l'Australie ?",["Sydney","Melbourne","Canberra","Perth"],2,"Canberra, et non Sydney !"),
    ("cg",1,"Quel est le plus long fleuve d'Afrique ?",["Le Congo","Le Niger","Le Nil","Le Zambèze"],2,"Le Nil, environ 6 650 km."),
    ("ec",1,"Combien font 12 × 12 ?",["124","144","132","148"],1,"144. Les tables, ça paye !"),
    ("ec",1,"Combien de côtés possède un hexagone ?",["5","6","7","8"],1,"Hexa = six."),
    ("ec",1,"« Nous ___ au marché. » Conjugaison du verbe aller ?",["allons","allez","vont","va"],0,"Avec « nous » : allons."),
    ("ec",2,"Combien font 15 % de 200 ?",["25","30","35","40"],1,"0,15 × 200 = 30."),
    ("ec",1,"Combien y a-t-il de minutes dans 2 h 30 ?",["130","140","150","160"],2,"120 + 30 = 150 minutes."),
    ("ec",2,"Quelle est la racine carrée de 169 ?",["11","12","13","14"],2,"13 × 13 = 169."),
    ("ec",1,"Combien font 7 × 8 ?",["54","56","58","64"],1,"7 × 8 = 56."),
    ("sp",1,"Combien de joueurs par équipe sur un terrain de football ?",["9","10","11","12"],2,"11 joueurs, gardien compris."),
    ("sp",1,"Qui a remporté la CAN 2023, disputée début 2024 ?",["Le Nigeria","Le Sénégal","La Côte d'Ivoire","Le Maroc"],2,"Les Éléphants, 2-1 en finale à domicile !"),
    ("sp",1,"Didier Drogba a marqué l'histoire de quel club européen ?",["Arsenal","Chelsea","Marseille seulement","Liverpool"],1,"Légende de Chelsea, Ligue des champions 2012."),
    ("sp",1,"Au basket, combien de joueurs par équipe sur le terrain ?",["4","5","6","7"],1,"5 joueurs sur le parquet."),
    ("sp",3,"En quelle année a eu lieu la première Coupe du monde de football ?",["1926","1930","1934","1938"],1,"En 1930, en Uruguay."),
    ("sp",4,"Combien de fois Yaya Touré a-t-il remporté le Ballon d'Or africain ?",["2","3","4","5"],2,"4 fois consécutivement, de 2011 à 2014."),
    ("sp",4,"En quelle année la Côte d'Ivoire a-t-elle organisé la CAN pour la première fois ?",["1980","1984","1988","1992"],1,"La CAN 1984, remportée par le Cameroun."),
]

ADS = [
    ("SoliPay","Mobile money nouvelle génération","Envoyez et recevez de l'argent partout en Côte d'Ivoire, sans frais cachés.","📲","#0B9A5C",False),
    ("Choco Lagune","Le chocolat 100 % ivoirien","Du cacao de chez nous, transformé chez nous.","🍫","#7A4A21",False),
    ("KpataMarket","Vos courses livrées à Abidjan","Commandez avant midi, livré avant le dîner.","🛵","#F2790F",False),
    ("SoliPay TV","Le spot vidéo SoliPay","15 secondes pour découvrir le mobile money sans frais cachés.","🎬","#0B9A5C",True),
]


class Command(BaseCommand):
    help = "Charge la configuration, les questions et les campagnes de démonstration"

    def handle(self, *args, **options):
        GameConfig.get()
        for cat, diff, text, opts, correct, expl in QUESTIONS:
            Question.objects.get_or_create(
                text=text,
                defaults=dict(category=cat, difficulty=diff,
                              option_a=opts[0], option_b=opts[1],
                              option_c=opts[2], option_d=opts[3],
                              correct=correct, explanation=expl))
        for brand, tag, pitch, emoji, color, video in ADS:
            AdCampaign.objects.get_or_create(
                brand=brand, defaults=dict(tagline=tag, pitch=pitch, emoji=emoji,
                                           color=color, is_video=video))
        self.stdout.write(self.style.SUCCESS(
            f"Config OK · {Question.objects.count()} questions · {AdCampaign.objects.count()} campagnes."))
