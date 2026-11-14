NIVEAU, MATIERE = "Tle A", "Mathématiques"

CHAPITRES = [
dict(
nom="Fonctions polynômes et rationnelles",
fiche="""## Dérivées à connaître
• (k)' = 0 ; (x)' = 1 ; (x²)' = 2x ; (x³)' = 3x² ; (1/x)' = −1/x².
• (u + v)' = u' + v' ; (ku)' = ku' ; (u/v)' = (u'v − uv')/v².

## Limites en +∞ et −∞
• Un polynôme a la limite de son terme de plus haut degré : −2x³ + x tend vers −∞ en +∞.
• Une fonction rationnelle a la limite du quotient de ses termes de plus haut degré.
• En une valeur interdite a, on étudie le signe du dénominateur pour savoir si f tend vers +∞ ou −∞.

## Sens de variation
• f'(x) > 0 sur un intervalle : f y est croissante. f'(x) < 0 : f y est décroissante.
• On étudie le signe de f' (souvent un polynôme du second degré) et on dresse le tableau de variations.

## Second degré : ax² + bx + c
Δ = b² − 4ac.
• Δ > 0 : deux racines (−b ± √Δ)/(2a) ; le trinôme est du signe de a à l'extérieur des racines.
• Δ = 0 : une racine double −b/(2a).
• Δ < 0 : pas de racine ; le trinôme est toujours du signe de a.

## Tangente
Au point d'abscisse a : y = f'(a)(x − a) + f(a).

## Exemple corrigé
f(x) = x² − 4x + 3 : f'(x) = 2x − 4, nulle en 2. f décroît sur ]−∞ ; 2], croît sur [2 ; +∞[ ; minimum f(2) = −1.
Racines : Δ = 16 − 12 = 4, x = 1 ou x = 3.""",
questions=[
(1, "La dérivée de f(x) = x² + 3x est :", "2x + 3", "x + 3", "2x", "2x + 3x",
 "(x²)' = 2x et (3x)' = 3."),
(1, "La dérivée d'une fonction constante est :", "0", "1", "la constante elle-même", "x",
 "Une constante ne varie pas."),
(2, "Les racines de x² − 4x + 3 sont :", "1 et 3", "−1 et −3", "2 et 4", "il n'y en a pas",
 "Δ = 16 − 12 = 4 : (4 ± 2)/2 donne 1 et 3."),
(2, "f(x) = x² − 4x + 3 atteint son minimum en x = :", "2", "4", "3", "−2",
 "f'(x) = 2x − 4 s'annule en 2 et passe de − à +."),
(2, "lim (x→+∞) (−2x³ + x) est égale à :", "−∞", "+∞", "0", "−2",
 "Terme de plus haut degré : −2x³, qui tend vers −∞."),
(2, "lim (x→+∞) (4x + 1)/(2x − 3) est égale à :", "2", "4", "0", "+∞",
 "Quotient des termes de plus haut degré : 4x/2x = 2."),
(3, "Si Δ < 0 et a > 0, le trinôme ax² + bx + c est :", "toujours strictement positif", "toujours négatif", "nul en un point", "de signe variable",
 "Sans racine, le trinôme garde le signe de a."),
(3, "La tangente à la courbe de f(x) = x² au point d'abscisse 2 a pour équation :", "y = 4x − 4", "y = 4x + 4", "y = 2x", "y = 4x",
 "f'(2) = 4 et f(2) = 4 : y = 4(x − 2) + 4."),
(3, "La dérivée de f(x) = 1/x est :", "−1/x²", "1/x²", "ln x", "−1/x",
 "Dérivée usuelle à connaître."),
(4, "f(x) = x³ − 3x² est décroissante sur :", "[0 ; 2]", "[2 ; +∞[", "]−∞ ; 0]", "ℝ",
 "f'(x) = 3x² − 6x = 3x(x − 2), négative entre 0 et 2."),
(4, "L'inéquation x² − 5x + 6 < 0 a pour solutions :", "les x de ]2 ; 3[", "x < 2 ou x > 3", "aucun réel", "tous les réels",
 "Racines 2 et 3, a = 1 > 0 : le trinôme est négatif entre les racines."),
]),

dict(
nom="Probabilités et dénombrement",
fiche="""## Dénombrer
• Principe multiplicatif : 3 chemises et 4 pantalons donnent 3 × 4 = 12 tenues.
• Arrangements (ordre compte, sans répétition) : A(n, p) = n × (n − 1) × … (p facteurs).
• Permutations : n! = 1 × 2 × … × n.
• Combinaisons (ordre ne compte pas) : C(n, p) = A(n, p)/p!. C(4, 2) = 6.
• Tirages avec remise de p éléments parmi n : nᵖ.

## Probabilité
• Équiprobabilité : P(A) = cas favorables / cas possibles.
• 0 ≤ P(A) ≤ 1 ; P(Ā) = 1 − P(A).
• P(A ∪ B) = P(A) + P(B) − P(A ∩ B).

## Variable aléatoire
X associe un nombre à chaque issue. Sa loi donne P(X = xᵢ) ; la somme des probabilités vaut 1.
Espérance E(X) = Σ xᵢ P(X = xᵢ) : c'est le gain moyen. Un jeu est équitable si E(X) = 0.

## Exemple corrigé
Une classe de 10 élèves élit un délégué et un suppléant : A(10, 2) = 10 × 9 = 90 possibilités.
Elle choisit 2 élèves pour une sortie : C(10, 2) = 45.

## Piège
Demande-toi toujours si l'ordre compte (bureau : président, trésorier) ou non (comité, groupe).""",
questions=[
(1, "On a 3 chemises et 4 pantalons. Le nombre de tenues différentes est :", "12", "7", "34", "81",
 "Principe multiplicatif : 3 × 4."),
(1, "4! est égal à :", "24", "16", "10", "4",
 "1 × 2 × 3 × 4."),
(2, "C(4, 2) est égal à :", "6", "12", "8", "2",
 "A(4, 2)/2! = 12/2 = 6."),
(2, "Dans une classe de 10 élèves, on élit un délégué et un suppléant. Le nombre de possibilités est :", "90", "45", "100", "20",
 "L'ordre compte : 10 × 9."),
(2, "On lance un dé équilibré. La probabilité d'obtenir un 6 est :", "1/6", "1/2", "6", "5/6",
 "1 cas favorable sur 6."),
(2, "Si P(A) = 0,25, alors P(Ā) est :", "0,75", "0,25", "1,25", "0",
 "1 − 0,25."),
(3, "Un code de 3 chiffres (de 0 à 9, répétitions permises) peut prendre combien de valeurs ?", "1000", "720", "30", "27",
 "10 × 10 × 10 = 10³."),
(3, "On choisit 2 élèves parmi 10 pour une sortie. Le nombre de choix est :", "45", "90", "20", "100",
 "L'ordre ne compte pas : C(10, 2) = 90/2."),
(3, "X prend les valeurs 0 et 10 avec P(X = 0) = 0,7 et P(X = 10) = 0,3. E(X) est égale à :", "3", "5", "7", "10",
 "0 × 0,7 + 10 × 0,3 = 3."),
(4, "P(A) = 0,4, P(B) = 0,5 et P(A ∩ B) = 0,2. P(A ∪ B) est égale à :", "0,7", "0,9", "0,2", "0,1",
 "0,4 + 0,5 − 0,2."),
(4, "Un jeu est équitable lorsque l'espérance du gain est :", "nulle", "positive", "égale à 1", "négative",
 "En moyenne, le joueur ne gagne ni ne perd."),
]),

dict(
nom="Fonction logarithme népérien",
fiche="""## L'essentiel
ln est définie sur ]0 ; +∞[ ; ln 1 = 0 ; ln e = 1 (e ≈ 2,718).
(ln x)' = 1/x > 0 : ln est strictement croissante.
ln x < 0 sur ]0 ; 1[ et ln x > 0 sur ]1 ; +∞[.

## Propriétés (a > 0, b > 0)
• ln(ab) = ln a + ln b
• ln(a/b) = ln a − ln b
• ln(aⁿ) = n ln a
• ln(1/a) = −ln a

## Résoudre
• ln x = k ⇔ x = eᵏ.
• ln a = ln b ⇔ a = b (avec a et b > 0).
• Toujours vérifier que les expressions dans ln sont strictement positives.

## Limites
ln x → +∞ en +∞ ; ln x → −∞ en 0 (par valeurs positives).

## Utilité
Le logarithme sert à trouver un exposant inconnu : 2ⁿ = 100 donne n ln 2 = ln 100, donc n = ln 100/ln 2 ≈ 6,64.

## Exemple corrigé
ln(x − 1) = ln 3 : il faut x > 1, puis x − 1 = 3, donc x = 4.""",
questions=[
(1, "ln 1 est égal à :", "0", "1", "e", "−1",
 "Valeur à connaître."),
(1, "ln e est égal à :", "1", "0", "e", "2,718",
 "e est le nombre dont le logarithme vaut 1."),
(2, "ln 2 + ln 5 est égal à :", "ln 10", "ln 7", "ln 2,5", "10",
 "ln a + ln b = ln(ab)."),
(2, "ln 9 est égal à :", "2 ln 3", "3 ln 2", "ln 3 + 2", "9 ln 1",
 "9 = 3² et ln(aⁿ) = n ln a."),
(2, "La fonction ln est définie pour :", "x > 0", "x ≥ 0", "tout réel x", "x < 0",
 "On ne peut calculer ln que d'un nombre strictement positif."),
(2, "La dérivée de ln x est :", "1/x", "x", "eˣ", "−1/x²",
 "Dérivée à connaître."),
(3, "La solution de ln x = 3 est :", "e³", "3e", "ln 3", "1/3",
 "ln x = k ⇔ x = eᵏ."),
(3, "La solution de ln(x − 1) = ln 3 est :", "4", "2", "3", "e³ + 1",
 "x − 1 = 3, et 4 > 1 convient."),
(3, "ln(1/2) est :", "négatif", "positif", "nul", "non défini",
 "1/2 est entre 0 et 1, donc ln(1/2) = −ln 2 < 0."),
(4, "Le plus petit entier n tel que 2ⁿ > 1000 est :", "10", "9", "100", "500",
 "n > ln 1000/ln 2 ≈ 9,97 : n = 10 (2¹⁰ = 1024)."),
(4, "ln(x²) est égal à 2 ln x pour :", "x > 0", "tout réel x", "x < 0", "x ≠ 0",
 "La formule ln(aⁿ) = n ln a suppose a > 0 ; pour x < 0, ln x n'existe pas."),
]),

dict(
nom="Fonction exponentielle",
fiche="""## L'essentiel
exp(x) = eˣ est définie sur ℝ ; eˣ > 0 pour tout x ; e⁰ = 1 ; e¹ = e.
(eˣ)' = eˣ : la fonction est strictement croissante.
eˣ et ln x sont réciproques : ln(eˣ) = x et e^(ln x) = x pour x > 0.

## Propriétés
• e^(a + b) = eᵃ × eᵇ
• e^(a − b) = eᵃ / eᵇ
• e^(−a) = 1/eᵃ
• (eᵃ)ⁿ = e^(na)

## Résoudre
• eˣ = k avec k > 0 ⇔ x = ln k ; si k ≤ 0, pas de solution.
• eᵃ < eᵇ ⇔ a < b.

## Limites
eˣ → +∞ en +∞ ; eˣ → 0 en −∞ (l'axe des abscisses est asymptote).

## Applications
Les phénomènes à croissance (ou décroissance) proportionnelle : population, intérêts composés en continu, refroidissement.
Une population P(t) = 1000 e^(0,05t) double quand e^(0,05t) = 2, soit t = ln 2/0,05 ≈ 13,9 ans.

## Exemple corrigé
e^(2x) = e⁶ ⇔ 2x = 6 ⇔ x = 3.""",
questions=[
(1, "e⁰ est égal à :", "1", "0", "e", "non défini",
 "Valeur à connaître."),
(1, "La dérivée de eˣ est :", "eˣ", "x eˣ⁻¹", "1/x", "e",
 "La fonction exponentielle est égale à sa dérivée."),
(2, "e² × e³ est égal à :", "e⁵", "e⁶", "e", "2e³",
 "e^(a + b) = eᵃ × eᵇ."),
(2, "e^(ln 7) est égal à :", "7", "ln 7", "e⁷", "1/7",
 "ln et exp sont réciproques."),
(2, "Pour tout réel x, eˣ est :", "strictement positif", "négatif", "nul pour x = 0", "inférieur à 1",
 "e⁰ = 1 et la fonction ne s'annule jamais."),
(2, "La solution de eˣ = 5 est :", "ln 5", "e⁵", "5/e", "5",
 "eˣ = k ⇔ x = ln k."),
(3, "La solution de e^(2x) = e⁶ est :", "3", "6", "12", "4",
 "2x = 6."),
(3, "L'équation eˣ = −2 :", "n'a pas de solution", "a pour solution ln 2", "a pour solution −ln 2", "a pour solution e⁻²",
 "eˣ est toujours strictement positif."),
(3, "lim (x→−∞) eˣ est égale à :", "0", "−∞", "+∞", "1",
 "La courbe se rapproche de l'axe des abscisses."),
(4, "P(t) = 1000 e^(0,05t). La population double au bout de :", "ln 2/0,05 ans, soit environ 13,9 ans", "20 ans", "0,05 × ln 2 ans", "2 ans",
 "e^(0,05t) = 2 donne 0,05t = ln 2."),
(4, "Les solutions de e^(x − 1) > 1 sont :", "x > 1", "x < 1", "x > 0", "x > e",
 "e^(x − 1) > e⁰ ⇔ x − 1 > 0."),
]),

dict(
nom="Suites numériques",
fiche="""## Suites arithmétiques
On ajoute toujours le même nombre r (la raison) : uₙ₊₁ = uₙ + r.
Terme général : uₙ = u₀ + nr (ou uₙ = u₁ + (n − 1)r).
Somme de termes consécutifs : nombre de termes × (premier + dernier)/2.

## Suites géométriques
On multiplie toujours par le même nombre q (la raison) : uₙ₊₁ = q × uₙ.
Terme général : uₙ = u₀ × qⁿ.
Somme : premier terme × (1 − q^(nombre de termes))/(1 − q)   (q ≠ 1).

## Reconnaître
• uₙ₊₁ − uₙ constant : arithmétique.
• uₙ₊₁ / uₙ constant : géométrique.

## Applications à la vie courante
• Intérêts simples (même somme ajoutée chaque année) : suite arithmétique.
• Intérêts composés, hausse de x % par an : suite géométrique de raison 1 + x/100.
   Une baisse de 10 % correspond à la raison 0,9.

## Exemple corrigé
Un salaire de 150 000 F augmente de 5 % par an : uₙ = 150 000 × 1,05ⁿ.
Après 2 ans : 150 000 × 1,1025 = 165 375 F.""",
questions=[
(1, "La suite 2 ; 5 ; 8 ; 11 ; … est arithmétique de raison :", "3", "2", "5", "1,5",
 "On ajoute 3 à chaque fois."),
(1, "La suite 3 ; 6 ; 12 ; 24 ; … est géométrique de raison :", "2", "3", "6", "1/2",
 "On multiplie par 2 à chaque fois."),
(2, "(uₙ) arithmétique avec u₀ = 5 et r = 4. u₁₀ est égal à :", "45", "40", "54", "14",
 "u₁₀ = 5 + 10 × 4."),
(2, "(uₙ) géométrique avec u₀ = 1 et q = 2. u₅ est égal à :", "32", "10", "16", "64",
 "u₅ = 2⁵."),
(2, "Une hausse de 5 % par an correspond à une suite géométrique de raison :", "1,05", "0,05", "5", "0,95",
 "Augmenter de 5 %, c'est multiplier par 1 + 5/100."),
(2, "Une baisse de 10 % par an correspond à une raison de :", "0,9", "1,1", "0,1", "−10",
 "Baisser de 10 %, c'est multiplier par 1 − 10/100."),
(3, "1 + 2 + 3 + … + 20 est égal à :", "210", "200", "420", "190",
 "20 × (1 + 20)/2 = 210."),
(3, "Un salaire de 150 000 F augmente de 5 % par an. Après 2 ans, il vaut :", "165 375 F", "165 000 F", "157 500 F", "180 000 F",
 "150 000 × 1,05² = 150 000 × 1,1025."),
(3, "1 + 3 + 9 + 27 + 81 est égal à :", "121", "81", "243", "120",
 "5 termes de raison 3 : (1 − 3⁵)/(1 − 3) = 242/2."),
(4, "uₙ = 7 − 2n définit une suite :", "arithmétique de raison −2", "arithmétique de raison 7", "géométrique de raison −2", "ni arithmétique ni géométrique",
 "uₙ₊₁ − uₙ = −2 pour tout n."),
(4, "Un capital de 100 000 F placé à 10 % d'intérêts composés devient au bout de 3 ans :", "133 100 F", "130 000 F", "110 000 F", "300 000 F",
 "100 000 × 1,1³ = 133 100. 130 000 correspond à des intérêts simples."),
]),

dict(
nom="Systèmes linéaires et programmation linéaire",
fiche="""## Système de deux équations à deux inconnues
• Substitution : on exprime une inconnue en fonction de l'autre et on remplace.
• Combinaison : on multiplie les équations pour éliminer une inconnue en les ajoutant.
• Déterminant : pour ax + by = c et a'x + b'y = c', D = ab' − a'b. Si D ≠ 0, une solution unique.

## Système de trois équations
On élimine une inconnue pour revenir à deux équations (méthode du pivot de Gauss), puis on remonte.

## Inéquations à deux inconnues
L'inéquation ax + by ≤ c représente un demi-plan limité par la droite ax + by = c.
On teste un point (souvent l'origine) pour savoir quel côté garder.

## Programmation linéaire
1. Choisir les inconnues (quantités à produire).
2. Traduire les contraintes en inéquations ; elles délimitent le polygone des contraintes.
3. Écrire la fonction à optimiser (bénéfice, coût).
4. L'optimum est atteint en un sommet du polygone : on compare les valeurs aux sommets.

## Exemple corrigé
x + y = 10 et x − y = 2 : en ajoutant, 2x = 12, x = 6, puis y = 4.

## Mettre en équation
« Des cahiers à 300 F et des stylos à 100 F, 8 articles pour 1 600 F » : x + y = 8 et 300x + 100y = 1 600, d'où x = 4 et y = 4.""",
questions=[
(1, "La solution de x + y = 10 et x − y = 2 est :", "x = 6 et y = 4", "x = 4 et y = 6", "x = 5 et y = 5", "x = 8 et y = 2",
 "En ajoutant : 2x = 12."),
(2, "La solution de 2x + y = 7 et x − y = 2 est :", "x = 3 et y = 1", "x = 1 et y = 5", "x = 2 et y = 3", "x = 4 et y = −1",
 "En ajoutant : 3x = 9, x = 3, puis y = 7 − 6 = 1."),
(2, "Le déterminant du système 2x + 3y = 5 ; x + 4y = 6 est :", "5", "11", "−5", "8",
 "D = 2 × 4 − 1 × 3."),
(2, "Si le déterminant d'un système de deux équations est non nul, le système a :", "une solution unique", "aucune solution", "une infinité de solutions", "deux solutions",
 "C'est la règle de Cramer."),
(2, "Le point (0 ; 0) vérifie-t-il l'inéquation x + y ≤ 4 ?", "oui", "non", "seulement si x = y", "on ne peut pas savoir",
 "0 + 0 = 0 ≤ 4 : le demi-plan contenant l'origine est solution."),
(3, "8 articles (cahiers à 300 F, stylos à 100 F) coûtent 1 600 F. Le nombre de cahiers est :", "4", "3", "5", "6",
 "x + y = 8 et 300x + 100y = 1 600 : 200x = 800."),
(3, "Le système x + y = 3 ; 2x + 2y = 6 a :", "une infinité de solutions", "une solution unique", "aucune solution", "deux solutions",
 "La 2ᵉ équation est la 1ʳᵉ multipliée par 2 : même droite."),
(3, "Le système x + y = 3 ; x + y = 5 a :", "aucune solution", "une solution unique", "une infinité de solutions", "la solution (1 ; 2)",
 "Deux droites parallèles distinctes."),
(4, "En programmation linéaire, le bénéfice maximal est atteint :", "en un sommet du polygone des contraintes", "au centre du polygone", "toujours à l'origine", "en dehors du polygone",
 "On compare la fonction aux sommets du polygone."),
(4, "Un artisan fait x tables (bénéfice 5 000 F) et y chaises (2 000 F). Aux sommets (0 ; 10), (4 ; 6) et (6 ; 0), le bénéfice maximal est :", "32 000 F", "30 000 F", "20 000 F", "26 000 F",
 "20 000 en (0 ; 10), 20 000 + 12 000 = 32 000 en (4 ; 6), 30 000 en (6 ; 0)."),
]),

dict(
nom="Statistiques",
fiche="""## Paramètres de position
• Moyenne : x̄ = (Σ nᵢ xᵢ)/N.
• Médiane : valeur qui partage la série ordonnée en deux moitiés.
• Mode : valeur (ou classe) de plus grand effectif.
• Quartiles Q1 et Q3 : au moins 25 % et 75 % des valeurs sont inférieures ou égales.

## Paramètres de dispersion
• Étendue = plus grande valeur − plus petite.
• Variance V = (Σ nᵢ xᵢ²)/N − x̄² ; écart type σ = √V.
• Écart interquartile = Q3 − Q1.

## Séries groupées en classes
On prend le centre de chaque classe pour calculer la moyenne. [10 ; 20[ a pour centre 15.
Fréquence = effectif/N ; les fréquences cumulées aident à trouver la médiane.

## Série à deux variables
Point moyen G(x̄ ; ȳ). Une droite d'ajustement passe par G ; elle permet des prévisions.
Méthode de Mayer : on coupe le nuage en deux groupes, on calcule leurs points moyens G1 et G2, la droite (G1G2) passe par G.

## Exemple corrigé
Notes : 8, 10, 12, 14, 16. Moyenne 12 ; médiane 12 ; étendue 8.
Variance : (64 + 100 + 144 + 196 + 256)/5 − 144 = 152 − 144 = 8.""",
questions=[
(1, "La moyenne de 8, 10, 12, 14 et 16 est :", "12", "10", "14", "60",
 "60/5 = 12."),
(1, "L'étendue de la série 3 ; 7 ; 12 ; 20 est :", "17", "20", "10,5", "3",
 "20 − 3."),
(2, "La médiane de 2 ; 5 ; 7 ; 9 ; 30 est :", "7", "10,6", "5", "9",
 "Valeur du milieu de la série ordonnée. 10,6 est la moyenne."),
(2, "La médiane de 4 ; 6 ; 8 ; 10 est :", "7", "6", "8", "28",
 "Nombre pair de valeurs : moyenne des deux du milieu (6 + 8)/2."),
(2, "Le centre de la classe [10 ; 20[ est :", "15", "10", "20", "30",
 "(10 + 20)/2."),
(2, "Le mode d'une série est :", "la valeur de plus grand effectif", "la valeur du milieu", "la moyenne", "la plus grande valeur",
 "C'est la valeur la plus fréquente."),
(3, "La variance de 8, 10, 12, 14 et 16 est :", "8", "√8", "12", "40",
 "Moyenne des carrés 152 − 144."),
(3, "Dans une classe de 40 élèves, 10 ont 12. La fréquence de la note 12 est :", "25 %", "10 %", "40 %", "12 %",
 "10/40 = 0,25."),
(3, "Une droite d'ajustement par la méthode de Mayer passe toujours par :", "le point moyen G du nuage", "l'origine", "le premier point", "le point le plus haut",
 "La droite (G1G2) passe par G."),
(4, "L'écart type d'une série de variance 16 est :", "4", "16", "256", "8",
 "σ = √V."),
(4, "Si on ajoute 2 points à toutes les notes, l'écart type :", "ne change pas", "augmente de 2", "double", "diminue de 2",
 "La moyenne augmente de 2, mais les écarts à la moyenne restent les mêmes."),
]),

dict(
nom="Révision BAC",
fiche="""## Formulaire de Terminale A

## Fonctions
• Dérivées : (xⁿ)' = nxⁿ⁻¹ ; (1/x)' = −1/x² ; (ln x)' = 1/x ; (eˣ)' = eˣ ; (u/v)' = (u'v − uv')/v².
• Tangente : y = f'(a)(x − a) + f(a).
• Second degré : Δ = b² − 4ac ; racines (−b ± √Δ)/(2a).

## Logarithme et exponentielle
• ln(ab) = ln a + ln b ; ln(aⁿ) = n ln a ; ln x = k ⇔ x = eᵏ.
• e^(a + b) = eᵃeᵇ ; eˣ = k ⇔ x = ln k (k > 0).

## Suites
• Arithmétique : uₙ = u₀ + nr ; somme = nombre de termes × (premier + dernier)/2.
• Géométrique : uₙ = u₀qⁿ ; somme = premier × (1 − q^N)/(1 − q) (q ≠ 1, N = nombre de termes). Hausse de t % : q = 1 + t/100.

## Dénombrement et probabilités
• n! ; A(n, p) (ordre compte) ; C(n, p) (ordre ne compte pas).
• P(Ā) = 1 − P(A) ; E(X) = Σ xᵢ pᵢ.

## Statistiques
• Moyenne, médiane, variance V = moyenne des carrés − carré de la moyenne, σ = √V.

## Conseils
• Lis tout le sujet et commence par l'exercice que tu maîtrises le mieux.
• Rédige chaque calcul : une réponse juste sans justification rapporte peu.
• Contrôle tes résultats : une probabilité est entre 0 et 1, un prix est positif.""",
questions=[
(2, "La dérivée de f(x) = 3x² − 5x + 1 est :", "6x − 5", "3x − 5", "6x + 1", "6x² − 5",
 "(3x²)' = 6x et (−5x)' = −5."),
(2, "ln 3 + ln 4 est égal à :", "ln 12", "ln 7", "12", "ln 3 × ln 4",
 "ln a + ln b = ln(ab)."),
(2, "La solution de eˣ = 1 est :", "0", "1", "e", "il n'y en a pas",
 "e⁰ = 1."),
(2, "5! est égal à :", "120", "25", "60", "15",
 "1 × 2 × 3 × 4 × 5."),
(3, "(uₙ) arithmétique : u₀ = 100 et r = −15. u₄ est égal à :", "40", "160", "55", "85",
 "100 − 4 × 15."),
(3, "Un prix de 20 000 F baisse de 20 %. Il devient :", "16 000 F", "18 000 F", "4 000 F", "19 800 F",
 "20 000 × 0,8."),
(3, "On tire une carte dans un jeu de 32. La probabilité d'obtenir un as est :", "1/8", "1/32", "1/4", "4/52",
 "4 as sur 32 cartes."),
(3, "C(5, 3) est égal à :", "10", "60", "15", "20",
 "A(5, 3)/3! = 60/6."),
(4, "Le nombre de solutions de x² + x + 1 = 0 dans ℝ est :", "0", "1", "2", "3",
 "Δ = 1 − 4 = −3 < 0."),
(4, "Pour quel entier n a-t-on pour la première fois 1,1ⁿ > 2 ?", "8", "7", "10", "20",
 "n > ln 2/ln 1,1 ≈ 7,27 ; 1,1⁷ ≈ 1,95 et 1,1⁸ ≈ 2,14."),
(4, "Le gain X d'un jeu vaut −100 F avec la probabilité 0,9 et 900 F avec la probabilité 0,1. E(X) est égale à :", "0", "800", "−90", "90",
 "−90 + 90 = 0 : le jeu est équitable."),
]),
]
