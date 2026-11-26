NIVEAU, MATIERE = "Tle C", "Mathématiques"
NIVEAUX = ["Tle C", "Tle D"]

CHAPITRES = [
dict(
nom="Limites et continuité",
fiche="""## Limites à connaître
• En +∞ : x, x², √x, eˣ, ln x tendent vers +∞ ; 1/x, 1/x² tendent vers 0.
• En 0⁺ : 1/x tend vers +∞ ; ln x tend vers −∞.
• lim (x→0) sin x / x = 1.

## Formes indéterminées
∞ − ∞ ; 0 × ∞ ; ∞/∞ ; 0/0. On lève l'indétermination en factorisant, en simplifiant ou avec la quantité conjuguée.
• Polynôme ou fonction rationnelle en ±∞ : on garde les termes de plus haut degré.
   (3x² − x + 1)/(x² + 2) a pour limite 3x²/x² = 3.
• √(x + 1) − √x = 1/(√(x + 1) + √x), qui tend vers 0 en +∞.

## Théorèmes de comparaison
• Si f(x) ≥ g(x) et g(x) → +∞, alors f(x) → +∞.
• Gendarmes : si g ≤ f ≤ h et g, h ont la même limite ℓ, alors f tend vers ℓ.
   −1/x ≤ sin x / x ≤ 1/x, donc sin x / x → 0 en +∞.

## Asymptotes
• Verticale x = a : f(x) → ±∞ quand x → a.
• Horizontale y = b : f(x) → b en ±∞.
• Oblique y = ax + b : f(x) − (ax + b) → 0 en ±∞.

## Continuité et valeurs intermédiaires
• Les fonctions usuelles sont continues sur leur ensemble de définition.
• TVI : si f est continue sur [a ; b], f prend toute valeur entre f(a) et f(b).
• Si de plus f est strictement monotone, l'équation f(x) = k a une unique solution dans [a ; b].
• On encadre la solution par dichotomie ou avec la calculatrice.

## Au BAC
Justifie toujours : « f est continue et strictement croissante sur [a ; b], et 0 est compris entre f(a) et f(b), donc… »""",
questions=[
(1, "lim (x→+∞) (3x² − x + 1)/(x² + 2) est égale à :", "3", "0", "+∞", "1/2",
 "On garde les termes de plus haut degré : 3x²/x² = 3."),
(1, "lim (x→0, x>0) 1/x est égale à :", "+∞", "−∞", "0", "1",
 "Quand x tend vers 0 par valeurs positives, 1/x devient très grand et positif."),
(2, "lim (x→+∞) (x³ − 2x)/(5x² + 1) est égale à :", "+∞", "1/5", "0", "−∞",
 "Termes de plus haut degré : x³/(5x²) = x/5, qui tend vers +∞."),
(2, "Laquelle de ces formes est indéterminée ?", "∞ − ∞", "∞ + ∞", "0 × 5", "1/∞",
 "∞ + ∞ = ∞, 0 × 5 = 0 et 1/∞ = 0. Seule ∞ − ∞ ne permet pas de conclure directement."),
(2, "La courbe de f(x) = (2x + 1)/(x − 3) admet pour asymptotes les droites :", "x = 3 et y = 2", "x = −3 et y = 2", "x = 3 et y = 1/2", "x = 2 et y = 3",
 "f tend vers ±∞ en 3 (verticale x = 3) et vers 2x/x = 2 en ±∞ (horizontale y = 2)."),
(2, "lim (x→+∞) (√(x + 1) − √x) est égale à :", "0", "+∞", "1", "1/2",
 "Quantité conjuguée : 1/(√(x + 1) + √x), dont le dénominateur tend vers +∞."),
(3, "lim (x→0) sin x / x est égale à :", "1", "0", "+∞", "elle n'existe pas",
 "C'est une limite de référence (le nombre dérivé de sin en 0, qui vaut cos 0 = 1)."),
(3, "f est continue sur [1 ; 2], f(1) = −1 et f(2) = 3. On peut affirmer que l'équation f(x) = 0 :", "a au moins une solution dans ]1 ; 2[", "a exactement une solution dans ]1 ; 2[", "n'a pas de solution", "a deux solutions",
 "TVI : 0 est entre −1 et 3. Sans savoir si f est monotone, on ne peut pas dire « exactement une »."),
(3, "lim (x→+∞) sin x / x est égale à :", "0", "1", "+∞", "elle n'existe pas",
 "Gendarmes : −1/x ≤ sin x / x ≤ 1/x et ±1/x tendent vers 0."),
(4, "f(x) = x + 2 + 1/x. Sa courbe admet en +∞ l'asymptote oblique :", "y = x + 2", "y = x", "y = 2", "x = 0",
 "f(x) − (x + 2) = 1/x tend vers 0. La droite x = 0 est une asymptote verticale."),
(4, "L'équation x³ + x − 1 = 0 :", "a une unique solution, comprise entre 0 et 1", "n'a aucune solution réelle", "a trois solutions réelles", "a une unique solution, comprise entre 1 et 2",
 "x³ + x − 1 est continue et strictement croissante, vaut −1 en 0 et 1 en 1 : une seule solution, dans ]0 ; 1[."),
]),

dict(
nom="Dérivation et étude de fonctions",
fiche="""## Nombre dérivé et tangente
f'(a) = lim (h→0) [f(a + h) − f(a)]/h.
Tangente au point d'abscisse a : y = f'(a)(x − a) + f(a).

## Dérivées usuelles
• (xⁿ)' = n xⁿ⁻¹   (√x)' = 1/(2√x)   (1/x)' = −1/x²
• (sin x)' = cos x   (cos x)' = −sin x   (eˣ)' = eˣ   (ln x)' = 1/x

## Opérations
• (u + v)' = u' + v'   (ku)' = ku'
• (uv)' = u'v + uv'   (u/v)' = (u'v − uv')/v²
• (uⁿ)' = n u' uⁿ⁻¹   (√u)' = u'/(2√u)
• (f(ax + b))' = a f'(ax + b) ; plus généralement (v ∘ u)' = u' × (v' ∘ u)

## Étude d'une fonction
1. Ensemble de définition, limites aux bornes, asymptotes.
2. Dérivée et son signe : f' > 0 ⇒ f croissante ; f' < 0 ⇒ f décroissante.
3. Tableau de variations, extremums (f' s'annule en changeant de signe).
4. Points particuliers, tangentes, courbe.

## Pour aller plus loin
• Point d'inflexion : la dérivée seconde s'annule en changeant de signe ; la courbe traverse sa tangente.
• Dérivabilité en un point : f peut être continue sans être dérivable (|x| en 0 : pente −1 à gauche, 1 à droite).

## Exemple corrigé
f(x) = x³ − 3x : f'(x) = 3x² − 3 = 3(x − 1)(x + 1).
f croît sur ]−∞ ; −1], décroît sur [−1 ; 1], croît sur [1 ; +∞[.
Maximum local f(−1) = 2, minimum local f(1) = −2.""",
questions=[
(1, "La dérivée de x³ est :", "3x²", "x²", "3x³", "3x",
 "(xⁿ)' = n xⁿ⁻¹."),
(1, "La dérivée de √x (x > 0) est :", "1/(2√x)", "2√x", "1/√x", "√x/2",
 "Dérivée usuelle à connaître."),
(2, "La dérivée de f(x) = (2x + 1)⁵ est :", "10(2x + 1)⁴", "5(2x + 1)⁴", "10(2x + 1)⁵", "2(2x + 1)⁴",
 "(uⁿ)' = n u' uⁿ⁻¹ avec u = 2x + 1, u' = 2 : 5 × 2 × (2x + 1)⁴."),
(2, "La dérivée de f(x) = x/(x + 1) est :", "1/(x + 1)²", "−1/(x + 1)²", "x/(x + 1)²", "1",
 "(u/v)' = (1 × (x + 1) − x × 1)/(x + 1)² = 1/(x + 1)²."),
(2, "La tangente à la courbe de f(x) = x² au point d'abscisse 1 a pour équation :", "y = 2x − 1", "y = 2x + 1", "y = x", "y = 2x",
 "f'(1) = 2 et f(1) = 1 : y = 2(x − 1) + 1 = 2x − 1."),
(2, "Si f'(x) > 0 pour tout x d'un intervalle I, alors f est sur I :", "strictement croissante", "strictement décroissante", "constante", "positive",
 "Le signe de la dérivée donne le sens de variation, pas le signe de f."),
(3, "f(x) = x³ − 3x admet un maximum local :", "en x = −1, égal à 2", "en x = 1, égal à −2", "en x = 0, égal à 0", "en x = −1, égal à −2",
 "f'(x) = 3(x − 1)(x + 1) passe de + à − en −1 ; f(−1) = −1 + 3 = 2."),
(3, "La dérivée de sin(3x) est :", "3 cos(3x)", "cos(3x)", "−3 cos(3x)", "3 sin(3x)",
 "(f(ax + b))' = a f'(ax + b)."),
(3, "La dérivée de f(x) = √(x² + 1) est :", "x/√(x² + 1)", "1/(2√(x² + 1))", "2x/√(x² + 1)", "x√(x² + 1)",
 "(√u)' = u'/(2√u) = 2x/(2√(x² + 1))."),
(4, "La courbe de f(x) = x³ − 3x² a un point d'inflexion d'abscisse :", "1", "0", "2", "3",
 "f''(x) = 6x − 6 s'annule en 1 en changeant de signe."),
(4, "La fonction x ↦ |x| en 0 est :", "continue mais pas dérivable", "dérivable, de nombre dérivé 0", "dérivable, de nombre dérivé 1", "non continue",
 "Le taux d'accroissement vaut −1 à gauche et 1 à droite : pas de nombre dérivé unique."),
]),

dict(
nom="Primitives",
fiche="""## Définition
F est une primitive de f sur I si F' = f sur I.
Deux primitives d'une même fonction diffèrent d'une constante. Il en existe une seule qui prend une valeur donnée en un point.

## Primitives usuelles
• a (constante) → ax
• xⁿ → xⁿ⁺¹/(n + 1)   (n ≠ −1)
• 1/x² → −1/x   1/√x → 2√x   1/x → ln|x|
• cos x → sin x   sin x → −cos x   eˣ → eˣ
• cos(ax + b) → sin(ax + b)/a   sin(ax + b) → −cos(ax + b)/a

## Formes composées (u dérivable)
• u' uⁿ → uⁿ⁺¹/(n + 1)
• u'/u² → −1/u   u'/√u → 2√u
• u'/u → ln|u|   u' eᵘ → eᵘ

## Méthode
1. Reconnais la forme (souvent u' × quelque chose de u).
2. Ajuste la constante multiplicative : 2x(x² + 1)³ = u' u³ avec u = x² + 1.
3. Vérifie en dérivant ton résultat.

## Exemple corrigé
Primitive F de f(x) = 2x telle que F(1) = 3 : F(x) = x² + c, et 1 + c = 3, donc F(x) = x² + 2.

## Piège
La primitive de sin x est −cos x (et non cos x).""",
questions=[
(1, "Une primitive de 2x est :", "x²", "2", "x²/2", "2x²",
 "La dérivée de x² est 2x."),
(1, "Une primitive de cos x est :", "sin x", "−sin x", "cos x", "−cos x",
 "(sin x)' = cos x."),
(2, "Une primitive de 3x² + 4x est :", "x³ + 2x²", "6x + 4", "x³ + 4x²", "3x³ + 2x²",
 "x³ a pour dérivée 3x² et 2x² a pour dérivée 4x."),
(2, "Sur ]0 ; +∞[, une primitive de 1/x² est :", "−1/x", "1/x", "ln x", "−2/x³",
 "(−1/x)' = 1/x². −2/x³ est la dérivée de 1/x²."),
(2, "Une primitive de 2x(x² + 1)³ est :", "(x² + 1)⁴/4", "(x² + 1)⁴", "2(x² + 1)⁴", "(x² + 1)³/3",
 "Forme u' u³ avec u = x² + 1 : primitive u⁴/4."),
(3, "La primitive F de f(x) = 2x telle que F(1) = 3 est :", "F(x) = x² + 2", "F(x) = x² + 3", "F(x) = x²", "F(x) = x² − 2",
 "F(x) = x² + c et F(1) = 1 + c = 3, donc c = 2."),
(3, "Une primitive de sin(2x) est :", "−cos(2x)/2", "cos(2x)/2", "−2 cos(2x)", "−cos(2x)",
 "La dérivée de −cos(2x)/2 est 2 sin(2x)/2 = sin(2x)."),
(3, "Sur ]0 ; +∞[, une primitive de 1/√x est :", "2√x", "√x/2", "1/(2√x)", "−1/(2x√x)",
 "(2√x)' = 2 × 1/(2√x) = 1/√x."),
(4, "Une primitive de x/(x² + 1)² est :", "−1/(2(x² + 1))", "−1/(x² + 1)", "1/(2(x² + 1))", "ln(x² + 1)/2",
 "x/(x² + 1)² = ½ × u'/u² avec u = x² + 1 : primitive −1/(2u)."),
(4, "Deux primitives d'une même fonction sur un intervalle :", "diffèrent d'une constante", "sont toujours égales", "diffèrent d'un facteur multiplicatif", "sont de signes opposés",
 "Leur différence a une dérivée nulle sur l'intervalle : elle est constante."),
]),

dict(
nom="Fonction logarithme népérien",
fiche="""## Définition
ln est la primitive de 1/x sur ]0 ; +∞[ qui s'annule en 1.
ln 1 = 0 ; ln e = 1 (e ≈ 2,718) ; (ln x)' = 1/x : ln est strictement croissante.

[[schema:courbes-ln-exp|Courbes de ln et de exp]]
## Propriétés algébriques (a > 0, b > 0, n entier)
• ln(ab) = ln a + ln b   ln(a/b) = ln a − ln b
• ln(1/a) = −ln a   ln(aⁿ) = n ln a   ln √a = ½ ln a

## Équations et inéquations
• ln a = ln b ⇔ a = b ; ln a < ln b ⇔ a < b (a, b > 0).
• ln x = k ⇔ x = eᵏ ; ln x < 0 ⇔ 0 < x < 1.
• Toujours commencer par l'ensemble de validité (ce qui est dans ln doit être > 0).

## Limites
• ln x → +∞ en +∞ ; ln x → −∞ en 0⁺.
• Croissances comparées : (ln x)/x → 0 en +∞ ; x ln x → 0 en 0⁺.
• ln(1 + x)/x → 1 en 0.

## Dérivée et primitive
• (ln u)' = u'/u (u > 0).
• Une primitive de u'/u est ln|u|.

## Exemple corrigé
ln x + ln(x − 2) = ln 3, avec x > 2 : ln[x(x − 2)] = ln 3, donc x² − 2x − 3 = 0, x = 3 ou x = −1.
Seul x = 3 vérifie x > 2.""",
questions=[
(2, 'Sur le schéma, les courbes de ln et de exp sont symétriques par rapport à :', "la droite d'équation y = x", "l'axe des abscisses", "l'origine du repère", "l'axe des ordonnées",
 'ln et exp sont des fonctions réciproques.', 'courbes-ln-exp'),
(1, "ln 1 est égal à :", "0", "1", "e", "−1",
 "Par définition, ln s'annule en 1."),
(1, "La fonction ln est définie sur :", "]0 ; +∞[", "ℝ", "[0 ; +∞[", "]−∞ ; 0[",
 "Le logarithme n'existe que pour les nombres strictement positifs."),
(2, "ln 8 est égal à :", "3 ln 2", "4 ln 2", "ln 2 + 3", "2 ln 3",
 "8 = 2³ et ln(aⁿ) = n ln a."),
(2, "La dérivée de ln(x² + 1) est :", "2x/(x² + 1)", "1/(x² + 1)", "2x/(x² + 1)²", "ln(2x)",
 "(ln u)' = u'/u avec u = x² + 1."),
(2, "La solution de l'équation ln x = 2 est :", "e²", "2e", "√e", "ln 2",
 "ln x = k ⇔ x = eᵏ."),
(2, "lim (x→+∞) (ln x)/x est égale à :", "0", "+∞", "1", "−∞",
 "Croissance comparée : x l'emporte sur ln x."),
(3, "ln x < 0 équivaut à :", "0 < x < 1", "x < 0", "x > 1", "x < 1",
 "ln x < ln 1 ⇔ x < 1, avec x > 0 pour que ln x existe."),
(3, "La solution de ln(2x − 1) = ln(x + 3) est :", "x = 4", "x = −4", "x = 2", "Il n'y en a pas",
 "2x − 1 = x + 3 donne x = 4, et 2 × 4 − 1 = 7 > 0, 4 + 3 = 7 > 0 : valable."),
(3, "lim (x→0, x>0) x ln x est égale à :", "0", "−∞", "+∞", "1",
 "Croissance comparée à connaître."),
(4, "Les solutions de ln x + ln(x − 2) = ln 3 sont :", "x = 3", "x = 3 ou x = −1", "x = −1", "x = 1",
 "x(x − 2) = 3 donne 3 ou −1, mais il faut x > 2 : seul 3 convient."),
(4, "Sur ]−1 ; +∞[, une primitive de 1/(x + 1) est :", "ln(x + 1)", "−1/(x + 1)²", "ln x + 1", "e^(x + 1)",
 "Forme u'/u avec u = x + 1 > 0."),
]),

dict(
nom="Fonction exponentielle",
fiche="""## Définition
exp est la fonction réciproque de ln : pour tout réel x, eˣ > 0, et ln(eˣ) = x ; pour x > 0, e^(ln x) = x.
e⁰ = 1 ; e¹ = e ; (eˣ)' = eˣ : exp est strictement croissante.

[[schema:courbes-ln-exp|Courbes de exp et de ln]]
## Propriétés algébriques
• e^(a + b) = eᵃ × eᵇ   e^(a − b) = eᵃ/eᵇ   e^(−a) = 1/eᵃ   (eᵃ)ⁿ = e^(na)

## Équations et inéquations
• eᵃ = eᵇ ⇔ a = b ; eᵃ < eᵇ ⇔ a < b.
• eˣ = k (k > 0) ⇔ x = ln k. eˣ = k n'a pas de solution si k ≤ 0.
• Astuce : poser X = eˣ (X > 0) pour se ramener au second degré.

## Limites
• eˣ → +∞ en +∞ ; eˣ → 0 en −∞.
• Croissances comparées : eˣ/xⁿ → +∞ en +∞ ; xⁿ eˣ → 0 en −∞.
• (eˣ − 1)/x → 1 en 0.

## Dérivée et primitive
(eᵘ)' = u' eᵘ ; une primitive de u' eᵘ est eᵘ.

## Exemple corrigé
e^(2x) − 3eˣ + 2 = 0 : avec X = eˣ, X² − 3X + 2 = 0, donc X = 1 ou X = 2, soit x = 0 ou x = ln 2.""",
questions=[
(1, "e⁰ est égal à :", "1", "0", "e", "+∞",
 "Comme a⁰ = 1 pour tout nombre a non nul."),
(1, "Pour tout réel x, eˣ est :", "strictement positif", "positif ou nul", "négatif", "compris entre 0 et 1",
 "La fonction exponentielle ne prend que des valeurs strictement positives."),
(2, "La dérivée de e^(2x + 1) est :", "2e^(2x + 1)", "e^(2x + 1)", "(2x + 1)e^(2x)", "2e^(2x)",
 "(eᵘ)' = u' eᵘ avec u' = 2."),
(2, "e^(ln 5) est égal à :", "5", "ln 5", "e⁵", "1/5",
 "exp et ln sont réciproques."),
(2, "La solution de eˣ = 3 est :", "ln 3", "e³", "3/e", "1/3",
 "eˣ = k ⇔ x = ln k."),
(2, "lim (x→−∞) eˣ est égale à :", "0", "−∞", "+∞", "1",
 "L'axe des abscisses est asymptote en −∞."),
(3, "Les solutions de e^(2x) − 3eˣ + 2 = 0 sont :", "0 et ln 2", "1 et 2", "0 seulement", "ln 2 seulement",
 "Avec X = eˣ : X = 1 ou 2, d'où x = ln 1 = 0 ou x = ln 2."),
(3, "lim (x→+∞) eˣ/x² est égale à :", "+∞", "0", "1", "e",
 "Croissance comparée : l'exponentielle l'emporte sur toute puissance."),
(3, "eˣ × e^(−x) est égal à :", "1", "0", "e^(x²)", "e^(2x)",
 "e^(x − x) = e⁰ = 1."),
(4, "Les solutions de e^(2x − 1) > 1 sont :", "x > 1/2", "x < 1/2", "x > 1", "x > 0",
 "e^(2x − 1) > e⁰ ⇔ 2x − 1 > 0."),
(4, "lim (x→0) (eˣ − 1)/x est égale à :", "1", "0", "e", "+∞",
 "C'est le nombre dérivé de exp en 0, qui vaut e⁰ = 1."),
]),

dict(
nom="Suites numériques",
fiche="""## Suites arithmétiques
uₙ₊₁ = uₙ + r ; uₙ = u₀ + nr.
Somme de termes consécutifs = nombre de termes × (premier + dernier)/2.

## Suites géométriques
uₙ₊₁ = q uₙ ; uₙ = u₀ qⁿ.
Somme = premier terme × (1 − q^(nombre de termes))/(1 − q)   (q ≠ 1).

## Limites
• qⁿ → 0 si −1 < q < 1 ; qⁿ → +∞ si q > 1.
• Une suite croissante et majorée converge ; décroissante et minorée, elle converge aussi.
• Si uₙ₊₁ = f(uₙ), f continue et uₙ → ℓ, alors ℓ = f(ℓ) (point fixe).

## Raisonnement par récurrence
1. Initialisation : la propriété est vraie au premier rang.
2. Hérédité : si elle est vraie au rang n, elle l'est au rang n + 1.
Conclusion : elle est vraie pour tout n.

## Méthode classique au BAC
uₙ₊₁ = 0,5 uₙ + 3. On pose vₙ = uₙ − 6 (6 est le point fixe : ℓ = 0,5ℓ + 3).
vₙ₊₁ = 0,5 uₙ + 3 − 6 = 0,5(uₙ − 6) = 0,5 vₙ : suite géométrique de raison 0,5.
Donc vₙ = v₀ × 0,5ⁿ → 0 et uₙ = 6 + vₙ → 6.

## Pièges
• Bien compter le nombre de termes (de u₀ à uₙ : n + 1 termes).
• Ne pas confondre la raison et le premier terme.""",
questions=[
(1, "(uₙ) est arithmétique avec u₀ = 3 et r = 2. u₁₀ est égal à :", "23", "20", "13", "25",
 "u₁₀ = u₀ + 10r = 3 + 20 = 23."),
(1, "(uₙ) est géométrique avec u₀ = 2 et q = 3. u₃ est égal à :", "54", "18", "162", "11",
 "u₃ = 2 × 3³ = 54."),
(2, "1 + 2 + 3 + … + 100 est égal à :", "5050", "5000", "10100", "4950",
 "100 termes × (1 + 100)/2 = 5050."),
(2, "1 + 2 + 4 + … + 2⁹ est égal à :", "1023", "1024", "512", "2047",
 "10 termes de raison 2 : (1 − 2¹⁰)/(1 − 2) = 1023."),
(2, "lim (n→+∞) (1/2)ⁿ est égale à :", "0", "1/2", "1", "+∞",
 "qⁿ → 0 quand −1 < q < 1."),
(2, "Si uₙ₊₁ = uₙ + 5 pour tout n, la suite est :", "arithmétique de raison 5", "géométrique de raison 5", "ni arithmétique ni géométrique", "arithmétique de raison −5",
 "On ajoute 5 à chaque étape."),
(3, "Une suite croissante et majorée :", "converge", "diverge vers +∞", "est décroissante", "est constante",
 "C'est le théorème de convergence monotone."),
(3, "La limite de uₙ = (n + 1)/(2n + 3) est :", "1/2", "1", "0", "1/3",
 "Termes de plus haut degré : n/(2n) = 1/2."),
(3, "uₙ₊₁ = 0,5 uₙ + 3. Si (uₙ) converge, sa limite est :", "6", "3", "1,5", "0",
 "ℓ = 0,5ℓ + 3 donne 0,5ℓ = 3, soit ℓ = 6."),
(4, "uₙ₊₁ = 0,5 uₙ + 3 et vₙ = uₙ − 6. La suite (vₙ) est :", "géométrique de raison 0,5", "arithmétique de raison −3", "géométrique de raison 2", "géométrique de raison 3",
 "vₙ₊₁ = 0,5uₙ + 3 − 6 = 0,5(uₙ − 6) = 0,5 vₙ."),
(4, "Un raisonnement par récurrence comporte :", "une initialisation puis une hérédité", "une hérédité seulement", "le calcul des premiers termes seulement", "le calcul de la limite",
 "Les deux étapes sont indispensables."),
]),

dict(
nom="Calcul intégral",
fiche="""## Définition
Si F est une primitive de f sur [a ; b] : ∫ₐᵇ f(x) dx = F(b) − F(a), noté [F(x)]ₐᵇ.

## Propriétés
• ∫ₐᵃ f = 0 ; l'intégrale de b à a est l'opposée de ∫ₐᵇ f.
• Linéarité : ∫(αf + βg) = α∫f + β∫g.
• Chasles : ∫ₐᶜ f = ∫ₐᵇ f + (intégrale de b à c de f).
• Positivité : si a ≤ b et f ≥ 0 sur [a ; b], alors ∫ₐᵇ f ≥ 0. Si a ≤ b et f ≤ g sur [a ; b], ∫ₐᵇ f ≤ ∫ₐᵇ g.

## Aire et valeur moyenne
• Si f ≥ 0, ∫ₐᵇ f est l'aire (en unités d'aire) sous la courbe, entre x = a et x = b.
• Aire entre deux courbes (f ≥ g) : ∫ₐᵇ (f − g).
• Valeur moyenne de f sur [a ; b] : (1/(b − a)) ∫ₐᵇ f.

## Intégration par parties
∫ₐᵇ u v' = [uv]ₐᵇ − ∫ₐᵇ u' v.
Choisis u qui se simplifie en dérivant (x, ln x…).

## Exemple corrigé
∫₀¹ x eˣ dx : u = x, v' = eˣ ; = [x eˣ]₀¹ − ∫₀¹ eˣ dx = e − (e − 1) = 1.

## Au BAC
Exprime l'aire en cm² si l'unité est donnée : 1 u.a. = (unité en x) × (unité en y).""",
questions=[
(1, "∫₀¹ 2x dx est égal à :", "1", "2", "1/2", "0",
 "[x²]₀¹ = 1 − 0 = 1."),
(1, "∫ₐᵃ f(x) dx est égal à :", "0", "f(a)", "1", "2f(a)",
 "Les bornes sont égales : F(a) − F(a) = 0."),
(2, "∫₁ᵉ (1/x) dx est égal à :", "1", "e", "0", "e − 1",
 "[ln x]₁ᵉ = ln e − ln 1 = 1."),
(2, "∫₀^π sin x dx est égal à :", "2", "0", "1", "π",
 "[−cos x]₀^π = −cos π + cos 0 = 1 + 1 = 2."),
(2, "∫₀² f + ∫₂⁵ f est égal à :", "∫₀⁵ f", "∫₂⁵ f", "∫₀² f", "0",
 "Relation de Chasles."),
(3, "La valeur moyenne de f(x) = x² sur [0 ; 3] est :", "3", "9", "4,5", "1",
 "(1/3) × [x³/3]₀³ = (1/3) × 9 = 3."),
(3, "∫₀¹ eˣ dx est égal à :", "e − 1", "e", "1", "e + 1",
 "[eˣ]₀¹ = e¹ − e⁰."),
(3, "Si f ≥ 0 sur [a ; b] avec a < b, alors ∫ₐᵇ f(x) dx est :", "positive ou nulle", "négative", "toujours nulle", "égale à f(b) − f(a)",
 "Positivité de l'intégrale (c'est une aire)."),
(4, "∫₀¹ x eˣ dx est égal à :", "1", "e", "e − 1", "0",
 "Par parties : [x eˣ]₀¹ − ∫₀¹ eˣ dx = e − (e − 1) = 1."),
(4, "L'aire comprise entre les courbes y = x et y = x² sur [0 ; 1] est :", "1/6 u.a.", "1/2 u.a.", "1/3 u.a.", "1/12 u.a.",
 "Sur [0 ; 1], x ≥ x² : ∫₀¹ (x − x²) dx = 1/2 − 1/3 = 1/6."),
]),

dict(
nom="Équations différentielles",
fiche="""## y' = ay (a réel)
Les solutions sont y = C e^(ax), C réel.
Avec une condition y(x₀) = y₀, il y a une seule solution.

## y' = ay + b (a ≠ 0)
Solution constante : y = −b/a.
Solutions générales : y = C e^(ax) − b/a.

## y'' + ω²y = 0 (ω > 0)
Les solutions sont y = A cos(ωx) + B sin(ωx), A et B réels.
Deux conditions (souvent y(0) et y'(0)) déterminent A et B.
Elles décrivent les oscillations (ressort, circuit LC).

## Méthode
1. Écris l'équation sous la forme y' = ay + b ou y'' + ω²y = 0.
2. Donne la forme générale.
3. Utilise la condition initiale pour trouver la constante.
4. Vérifie en remplaçant dans l'équation.

## Exemple corrigé
y' = −0,5 y et y(0) = 4 : y = 4 e^(−0,5x).
En x = 2 ln 2 : y = 4 e^(−ln 2) = 4 × 1/2 = 2 (la valeur a été divisée par deux).

## Applications
Décroissance radioactive, refroidissement, charge et décharge d'un condensateur, oscillations.""",
questions=[
(1, "Les solutions de y' = 2y sont les fonctions :", "y = C e^(2x)", "y = C e^(x/2)", "y = 2eˣ + C", "y = Cx²",
 "y' = ay a pour solutions C e^(ax)."),
(2, "La solution de y' = −y telle que y(0) = 3 est :", "y = 3e^(−x)", "y = 3eˣ", "y = −3e^(−x)", "y = e^(−3x)",
 "y = C e^(−x) et y(0) = C = 3."),
(2, "Les solutions de y' = 2y + 4 sont :", "y = C e^(2x) − 2", "y = C e^(2x) + 2", "y = C e^(2x) − 4", "y = C e^(4x) − 2",
 "Solution constante −b/a = −4/2 = −2."),
(2, "La solution constante de y' = −3y + 6 est :", "y = 2", "y = 6", "y = −2", "y = 3",
 "0 = −3y + 6 donne y = 2."),
(3, "Les solutions de y'' + 4y = 0 sont :", "A cos 2x + B sin 2x", "A cos 4x + B sin 4x", "A e^(2x) + B e^(−2x)", "A cos x + B sin 2x",
 "ω² = 4, donc ω = 2."),
(3, "La solution de y'' + 9y = 0 avec y(0) = 1 et y'(0) = 0 est :", "y = cos 3x", "y = sin 3x", "y = cos 9x", "y = 3 cos x",
 "y = A cos 3x + B sin 3x ; y(0) = A = 1 ; y'(0) = 3B = 0."),
(3, "Laquelle de ces fonctions est solution de y' = y ?", "eˣ", "x eˣ", "x²", "ln x",
 "(eˣ)' = eˣ. La dérivée de x eˣ est eˣ + x eˣ."),
(4, "y' = −0,5 y et y(0) = 4. Alors y(2 ln 2) est égal à :", "2", "1", "4", "8",
 "y = 4e^(−0,5x) ; 4e^(−ln 2) = 4/2 = 2."),
(4, "Toutes les solutions de y' = ay + b (a ≠ 0) tendent vers −b/a en +∞ lorsque :", "a < 0", "a > 0", "a = 1", "b = 0",
 "y = C e^(ax) − b/a et C e^(ax) → 0 en +∞ pour tout C si et seulement si a < 0."),
(2, "Pour trouver la constante C d'une solution, on utilise :", "une condition initiale", "la dérivée seconde", "la limite en −∞", "le discriminant",
 "Par exemple y(0) = 3."),
]),

dict(
nom="Nombres complexes",
fiche="""## Forme algébrique
z = a + ib (a, b réels, i² = −1). a = Re(z), b = Im(z).
Conjugué : z̄ = a − ib ; z z̄ = a² + b².
Pour diviser, multiplie par le conjugué du dénominateur : 1/i = −i.

## Module et argument
|z| = √(a² + b²) ; un argument θ vérifie cos θ = a/|z| et sin θ = b/|z|.
Forme trigonométrique : z = r(cos θ + i sin θ) ; forme exponentielle : z = r e^(iθ).
• |zz'| = |z||z'| ; arg(zz') = arg z + arg z' (à 2π près).
• Moivre : (e^(iθ))ⁿ = e^(inθ).
1 + i = √2 e^(iπ/4) ; i = e^(iπ/2) ; −1 = e^(iπ).

## Équation du second degré à coefficients réels
az² + bz + c = 0 avec Δ < 0 : z = (−b ± i√(−Δ))/(2a), deux solutions conjuguées.

## Géométrie
• Le point M d'affixe z ; le vecteur AB a pour affixe z_B − z_A ; AB = |z_B − z_A|.
• Translation : z' = z + b ; homothétie de centre O : z' = kz ; rotation de centre O et d'angle θ : z' = e^(iθ) z.

## Exemple corrigé
z² + 2z + 5 = 0 : Δ = 4 − 20 = −16, z = (−2 ± 4i)/2 = −1 ± 2i.""",
questions=[
(1, "i² est égal à :", "−1", "1", "i", "−i",
 "C'est la définition du nombre i."),
(1, "Le conjugué de 3 − 4i est :", "3 + 4i", "−3 + 4i", "4 − 3i", "−3 − 4i",
 "On change le signe de la partie imaginaire."),
(2, "Le module de 3 + 4i est :", "5", "7", "25", "√7",
 "√(9 + 16) = 5."),
(2, "(1 + i)² est égal à :", "2i", "2", "0", "2 + 2i",
 "1 + 2i + i² = 1 + 2i − 1 = 2i."),
(2, "Un argument de i est :", "π/2", "0", "π", "−π/2",
 "i est sur l'axe des imaginaires, du côté positif."),
(2, "1/i est égal à :", "−i", "i", "1", "−1",
 "1/i = i/(i × i) = i/(−1) = −i."),
(3, "Les solutions de z² + 2z + 5 = 0 sont :", "−1 + 2i et −1 − 2i", "1 + 2i et 1 − 2i", "−1 + 4i et −1 − 4i", "−2 + 2i et −2 − 2i",
 "Δ = −16, z = (−2 ± 4i)/2."),
(3, "La forme exponentielle de 1 + i est :", "√2 e^(iπ/4)", "2 e^(iπ/4)", "√2 e^(iπ/2)", "e^(iπ/4)",
 "|1 + i| = √2 et cos θ = sin θ = √2/2, donc θ = π/4."),
(3, "A et B ont pour affixes 1 + i et 4 + 5i. La distance AB est :", "5", "7", "25", "√7",
 "|z_B − z_A| = |3 + 4i| = 5."),
(4, "(1 + i)⁸ est égal à :", "16", "16i", "−16", "256",
 "(√2 e^(iπ/4))⁸ = (√2)⁸ e^(2iπ) = 16 × 1."),
(4, "La rotation de centre O et d'angle π/2 a pour écriture complexe :", "z' = iz", "z' = −z", "z' = z̄", "z' = z + i",
 "z' = e^(iπ/2) z = iz."),
]),

dict(
nom="Probabilités",
fiche="""## Vocabulaire et règles
• Équiprobabilité : P(A) = nombre de cas favorables / nombre de cas possibles.
• P(Ā) = 1 − P(A) ; P(A ∪ B) = P(A) + P(B) − P(A ∩ B).
• A et B incompatibles : P(A ∩ B) = 0.

## Dénombrement
• n! = 1 × 2 × … × n (nombre de façons de ranger n objets).
• Combinaisons : C(n, p) = n!/(p!(n − p)!) (tirages simultanés).
   C(5, 2) = 10.

## Probabilités conditionnelles
P_B(A) = P(A ∩ B)/P(B). Arbre : on multiplie le long des branches.
Probabilités totales : P(A) = P(A ∩ B) + P(A ∩ B̄).
A et B indépendants ⇔ P(A ∩ B) = P(A) × P(B).

## Variable aléatoire
Espérance E(X) = Σ xᵢ pᵢ ; variance V(X) = Σ xᵢ² pᵢ − E(X)² ; écart type σ = √V.

## Loi binomiale B(n ; p)
n épreuves identiques et indépendantes, chacune avec probabilité de succès p.
P(X = k) = C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ ; E(X) = np ; V(X) = np(1 − p).
« Au moins un succès » : P(X ≥ 1) = 1 − P(X = 0).

## Exemple corrigé
Urne : 3 boules rouges et 2 blanches, on en tire 2 à la fois.
P(2 rouges) = C(3, 2)/C(5, 2) = 3/10.""",
questions=[
(1, "On lance un dé équilibré. La probabilité d'obtenir un nombre pair est :", "1/2", "1/3", "1/6", "2/3",
 "3 cas favorables (2, 4, 6) sur 6."),
(1, "Si P(A) = 0,3, alors P(Ā) est égale à :", "0,7", "0,3", "1,3", "0",
 "P(Ā) = 1 − P(A)."),
(2, "C(5, 2) est égal à :", "10", "20", "25", "5",
 "5!/(2! × 3!) = 120/(2 × 6) = 10."),
(2, "A et B sont indépendants, P(A) = 0,5 et P(B) = 0,4. P(A ∩ B) est égale à :", "0,2", "0,9", "0,45", "0,1",
 "Indépendance : P(A ∩ B) = 0,5 × 0,4."),
(2, "P(A) = 0,5, P(B) = 0,4 et P(A ∩ B) = 0,2. P(A ∪ B) est égale à :", "0,7", "0,9", "0,2", "0,5",
 "0,5 + 0,4 − 0,2 = 0,7."),
(3, "P(A ∩ B) = 0,12 et P(B) = 0,3. P_B(A) est égale à :", "0,4", "0,036", "0,12", "2,5",
 "0,12/0,3 = 0,4."),
(3, "X suit la loi binomiale B(10 ; 0,3). Son espérance est :", "3", "0,3", "7", "2,1",
 "E(X) = np = 10 × 0,3. 2,1 est la variance np(1 − p)."),
(3, "X suit la loi B(3 ; 1/2). P(X = 2) est égale à :", "3/8", "1/8", "1/2", "1/4",
 "C(3, 2) × (1/2)² × (1/2) = 3/8."),
(3, "Le nombre de façons de ranger 4 livres différents sur une étagère est :", "24", "16", "4", "12",
 "4! = 24."),
(4, "Une urne contient 3 boules rouges et 2 blanches. On tire 2 boules simultanément. P(2 rouges) est égale à :", "3/10", "9/25", "3/5", "1/10",
 "C(3, 2)/C(5, 2) = 3/10."),
(4, "X suit la loi B(4 ; 0,5). P(X ≥ 1) est égale à :", "15/16", "1/16", "1/2", "3/4",
 "1 − P(X = 0) = 1 − 0,5⁴ = 1 − 1/16."),
]),

dict(
nom="Arithmétique",
niveaux=["Tle C"],
fiche="""## Division euclidienne
Pour a entier et b entier > 0, il existe un unique couple (q ; r) tel que a = bq + r et 0 ≤ r < b.

## Congruences
a ≡ b (mod n) ⇔ n divise a − b ⇔ a et b ont le même reste dans la division par n.
On peut additionner, multiplier et élever à une puissance des congruences de même modulo.
Exemple : 2³ = 8 ≡ 1 (mod 7), donc 2¹⁰ = (2³)³ × 2 ≡ 2 (mod 7).

## PGCD et PPCM
• Algorithme d'Euclide : PGCD(a, b) = PGCD(b, r).
• a et b sont premiers entre eux si PGCD(a, b) = 1.
• PGCD(a, b) × PPCM(a, b) = a × b (a, b > 0).

## Les grands théorèmes
• Bézout : a et b premiers entre eux ⇔ il existe u, v entiers tels que au + bv = 1.
• Gauss : si a divise bc et a est premier avec b, alors a divise c.

## Équation ax + by = c
1. Trouve une solution particulière (x₀ ; y₀).
2. Soustrais : a(x − x₀) = −b(y − y₀), puis applique Gauss.
3. Avec PGCD(a, b) = 1 : x = x₀ + bk et y = y₀ − ak, k entier.

## Nombres premiers
Tout entier ≥ 2 se décompose de façon unique en produit de facteurs premiers.
360 = 2³ × 3² × 5 a (3 + 1)(2 + 1)(1 + 1) = 24 diviseurs positifs.""",
questions=[
(1, "Le reste de la division euclidienne de 47 par 5 est :", "2", "9", "4", "7",
 "47 = 5 × 9 + 2."),
(1, "PGCD(24, 36) est égal à :", "12", "6", "72", "4",
 "24 = 2 × 12 et 36 = 3 × 12, avec 2 et 3 premiers entre eux."),
(2, "17 est congru modulo 5 à :", "2", "3", "4", "1",
 "17 = 5 × 3 + 2."),
(2, "Lequel de ces nombres est premier ?", "97", "91", "87", "99",
 "91 = 7 × 13, 87 = 3 × 29, 99 = 9 × 11."),
(2, "Un couple (u ; v) tel que 7u + 5v = 1 est :", "(3 ; −4)", "(2 ; −3)", "(1 ; −1)", "(−1 ; 2)",
 "21 − 20 = 1. Les autres donnent −1, 2 et 3."),
(3, "Si a divise bc et si PGCD(a, b) = 1, alors :", "a divise c", "a divise b", "b divise c", "a = c",
 "C'est le théorème de Gauss."),
(3, "Le reste de la division de 2¹⁰ par 7 est :", "2", "1", "4", "3",
 "2³ ≡ 1 (mod 7), donc 2⁹ ≡ 1 et 2¹⁰ ≡ 2."),
(3, "PPCM(12, 18) est égal à :", "36", "6", "216", "72",
 "PGCD = 6 et 12 × 18/6 = 36."),
(4, "Une solution de 3x + 5y = 1 est (2 ; −1). Les solutions entières sont :", "(2 + 5k ; −1 − 3k), k entier", "(2 + 3k ; −1 − 5k), k entier", "(2 + 5k ; −1 + 3k), k entier", "(5k ; −3k), k entier",
 "3(x − 2) = −5(y + 1) ; Gauss : x − 2 = 5k, puis y + 1 = −3k."),
(4, "Le nombre de diviseurs positifs de 360 est :", "24", "12", "36", "18",
 "360 = 2³ × 3² × 5 : (3 + 1)(2 + 1)(1 + 1) = 24."),
]),

dict(
nom="Similitudes directes",
niveaux=["Tle C"],
fiche="""## Écriture complexe
Une similitude directe s'écrit z' = az + b, avec a complexe non nul et b complexe.
• Rapport : k = |a| ; angle : θ = arg a.
• Si a ≠ 1, elle a un unique point fixe, son centre Ω d'affixe ω = b/(1 − a).
• Si a = 1 : translation de vecteur d'affixe b.

## Cas particuliers
• a réel, a ≠ 0 et a ≠ 1 : homothétie (z' = kz : centre O, rapport k).
• |a| = 1 et a ≠ 1 : rotation (z' = e^(iθ) z : centre O, angle θ).
• z' = −z + 2ω : symétrie de centre Ω d'affixe ω (rotation d'angle π).

## Propriétés
Une similitude directe de rapport k :
• multiplie les distances par k et les aires par k² ;
• conserve les angles orientés, l'alignement, le parallélisme, les milieux.
La composée de deux similitudes directes est une similitude directe : les rapports se multiplient, les angles s'additionnent.

## Forme réduite
De centre Ω, de rapport k et d'angle θ : z' − ω = k e^(iθ)(z − ω).

## Exemple corrigé
z' = 2z − 3 : rapport 2, angle 0, centre ω = −3/(1 − 2) = 3. C'est l'homothétie de centre le point d'affixe 3 et de rapport 2.""",
questions=[
(1, "La transformation z' = z + 3 − i est :", "la translation de vecteur d'affixe 3 − i", "une rotation de centre O", "une homothétie de rapport 3", "la symétrie de centre O",
 "a = 1 : c'est une translation."),
(2, "La transformation z' = 2z est :", "l'homothétie de centre O et de rapport 2", "la rotation de centre O et d'angle 2", "la translation de vecteur d'affixe 2", "une symétrie",
 "a = 2 est réel."),
(2, "La transformation z' = iz est :", "la rotation de centre O et d'angle π/2", "l'homothétie de rapport i", "la symétrie d'axe (Ox)", "la translation de vecteur i",
 "|i| = 1 et arg i = π/2."),
(2, "La similitude z' = (1 + i)z a pour rapport et angle :", "√2 et π/4", "2 et π/4", "√2 et π/2", "1 et π/4",
 "|1 + i| = √2 et arg(1 + i) = π/4."),
(3, "Le centre de la similitude z' = 2z − 3 a pour affixe :", "3", "−3", "1", "0",
 "ω = b/(1 − a) = −3/(1 − 2) = 3."),
(3, "Une similitude de rapport 3 multiplie les aires par :", "9", "3", "6", "1/3",
 "Les aires sont multipliées par k²."),
(3, "On compose la rotation de centre Ω et d'angle π/3 et l'homothétie de centre Ω et de rapport 2. On obtient une similitude de :", "rapport 2 et d'angle π/3", "rapport 2 et d'angle 2π/3", "rapport 1/2 et d'angle π/3", "rapport 3 et d'angle π/3",
 "Les rapports se multiplient (1 × 2), les angles s'additionnent (π/3 + 0)."),
(4, "La similitude directe de centre O qui transforme le point d'affixe 1 en le point d'affixe 1 + i a pour écriture :", "z' = (1 + i)z", "z' = z + i", "z' = iz", "z' = (1 − i)z",
 "Centre O : z' = az, et a × 1 = 1 + i."),
(4, "La transformation z' = −z + 2 est :", "la symétrie de centre le point d'affixe 1", "une translation", "la rotation de centre O et d'angle π/2", "la symétrie de centre O",
 "a = −1 (rotation d'angle π), centre ω = 2/(1 + 1) = 1."),
(2, "Une similitude directe conserve toujours :", "les angles orientés", "les distances", "les aires", "les coordonnées des points",
 "Elle multiplie les distances par son rapport k, qui n'est pas forcément 1."),
]),

dict(
nom="Statistiques à deux variables",
niveaux=["Tle D"],
fiche="""## Série double
On étudie deux caractères x et y sur une même population : n couples (xᵢ ; yᵢ), représentés par un nuage de points.
Point moyen G(x̄ ; ȳ).

## Indicateurs
• Variance : V(x) = (1/n) Σ xᵢ² − x̄².
• Covariance : cov(x, y) = (1/n) Σ xᵢyᵢ − x̄ȳ.
• Coefficient de corrélation linéaire : r = cov(x, y)/(σ(x) σ(y)), toujours compris entre −1 et 1.
   |r| proche de 1 : forte corrélation linéaire ; r > 0 : y augmente avec x ; r < 0 : y diminue quand x augmente.

## Droite de régression de y en x (moindres carrés)
y = ax + b avec a = cov(x, y)/V(x) ; elle passe par G, donc b = ȳ − a x̄.

## Prévision
On remplace x par la valeur voulue dans l'équation de la droite. La prévision n'a de sens que si |r| est proche de 1.

## Exemple corrigé
x̄ = 3, ȳ = 5, cov = 6, V(x) = 4 : a = 1,5 et b = 5 − 1,5 × 3 = 0,5.
Droite : y = 1,5x + 0,5. Pour x = 10 : y = 15,5.""",
questions=[
(1, "Le point moyen des points (1 ; 2), (3 ; 4) et (5 ; 9) est :", "(3 ; 5)", "(9 ; 15)", "(3 ; 4)", "(5 ; 9)",
 "x̄ = 9/3 = 3 et ȳ = 15/3 = 5."),
(2, "cov(x, y) = 6 et V(x) = 4. Le coefficient directeur de la droite de régression de y en x est :", "1,5", "24", "0,67", "10",
 "a = cov/V(x) = 6/4."),
(2, "La droite de régression de y en x passe toujours par :", "le point moyen G", "l'origine", "le premier point du nuage", "le point le plus haut",
 "b est choisi pour que G soit sur la droite."),
(2, "r = 0,98 signifie :", "une forte corrélation linéaire positive", "une absence de corrélation", "une forte corrélation négative", "que les points sont tous confondus",
 "|r| proche de 1 et r > 0."),
(3, "r = −0,95 signifie que :", "il y a une forte corrélation linéaire négative : y tend à diminuer quand x augmente", "y augmente quand x augmente", "x et y sont indépendants", "le calcul est faux",
 "Corrélation forte et négative."),
(3, "G(3 ; 5) et a = 1,5. La droite de régression de y en x est :", "y = 1,5x + 0,5", "y = 1,5x + 5", "y = 1,5x − 0,5", "y = 3x + 5",
 "b = 5 − 1,5 × 3 = 0,5."),
(3, "(1/n) Σ xᵢyᵢ = 20, x̄ = 3 et ȳ = 5. La covariance est :", "5", "15", "20", "35",
 "20 − 3 × 5 = 5."),
(3, "Le coefficient de corrélation r est toujours :", "compris entre −1 et 1", "positif", "supérieur à 1", "égal à la covariance",
 "C'est une propriété du coefficient de corrélation."),
(4, "V(x) = 4, V(y) = 9 et cov(x, y) = 5,4. Le coefficient de corrélation vaut :", "0,9", "0,15", "1,35", "0,6",
 "r = 5,4/(2 × 3) = 0,9."),
(4, "Un ajustement affine est justifié quand :", "|r| est proche de 1", "r est proche de 0", "la covariance est négative", "la variance de x est grande",
 "La corrélation linéaire doit être forte."),
]),

dict(
nom="Révision BAC",
fiche="""## Formulaire de mathématiques de Terminale

## Analyse
• Limites : croissances comparées (ln x)/x → 0, eˣ/x → +∞, x ln x → 0 (0⁺), x eˣ → 0 (−∞).
• Dérivées : (uv)' = u'v + uv' ; (u/v)' = (u'v − uv')/v² ; (ln u)' = u'/u ; (eᵘ)' = u'eᵘ ; (uⁿ)' = nu'uⁿ⁻¹.
• Primitives : u'uⁿ → uⁿ⁺¹/(n + 1) ; u'/u → ln|u| ; u'eᵘ → eᵘ ; u'/√u → 2√u.
• Intégrale : ∫ₐᵇ f = F(b) − F(a) ; par parties ∫uv' = [uv] − ∫u'v ; valeur moyenne (1/(b − a))∫f.
• Équations différentielles : y' = ay + b → y = Ce^(ax) − b/a ; y'' + ω²y = 0 → A cos ωx + B sin ωx.
• Suites : arithmétique uₙ = u₀ + nr ; géométrique uₙ = u₀qⁿ ; somme géométrique u₀(1 − qⁿ⁺¹)/(1 − q).

## Complexes et géométrie
• |a + ib| = √(a² + b²) ; z = re^(iθ) ; Δ < 0 : z = (−b ± i√(−Δ))/(2a).
• z' = az + b : rapport |a|, angle arg a, centre b/(1 − a).

## Probabilités
• P_B(A) = P(A ∩ B)/P(B) ; indépendance P(A ∩ B) = P(A)P(B).
• Loi binomiale : P(X = k) = C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ ; E = np ; V = np(1 − p).

## Conseils pour l'épreuve
• Lis tout le sujet, repère les questions indépendantes et commence par ce que tu maîtrises.
• Une question non résolue peut être admise pour faire la suite : utilise le résultat donné.
• Justifie chaque étape (théorème utilisé, conditions vérifiées) et encadre les résultats.""",
questions=[
(2, "lim (x→+∞) x e^(−x) est égale à :", "0", "+∞", "1", "−∞",
 "x e^(−x) = x/eˣ et l'exponentielle l'emporte."),
(2, "La dérivée de x ln x est :", "ln x + 1", "1/x", "ln x", "x/ln x",
 "(uv)' = 1 × ln x + x × 1/x."),
(2, "∫₀² 3x² dx est égal à :", "8", "12", "6", "4",
 "[x³]₀² = 8."),
(2, "Le module de 1 − i√3 est :", "2", "4", "1 + √3", "√2",
 "√(1 + 3) = 2."),
(3, "L'équation ln(x − 1) = 0 a pour solution :", "x = 2", "x = 1", "x = e", "x = 0",
 "x − 1 = 1."),
(3, "(uₙ) géométrique de raison 3 et de premier terme u₀ = 1. u₀ + u₁ + … + u₄ est égal à :", "121", "81", "243", "40",
 "(1 − 3⁵)/(1 − 3) = 242/2 = 121."),
(3, "La solution de y' = 3y telle que y(0) = 2 est :", "y = 2e^(3x)", "y = 3e^(2x)", "y = e^(3x) + 1", "y = 2e^(x/3)",
 "y = Ce^(3x) avec C = y(0) = 2."),
(3, "On lance deux fois une pièce équilibrée. La probabilité d'obtenir au moins un pile est :", "3/4", "1/2", "1/4", "1",
 "1 − P(aucun pile) = 1 − 1/4."),
(4, "La fonction f(x) = e^(−x²) atteint son maximum en x = 0. Ce maximum vaut :", "1", "0", "e", "1/e",
 "f(0) = e⁰ = 1, et e^(−x²) ≤ 1 car −x² ≤ 0."),
(4, "Une primitive de ln x sur ]0 ; +∞[ est :", "x ln x − x", "1/x", "x ln x", "ln x − x",
 "La dérivée de x ln x − x est ln x + 1 − 1 = ln x."),
(4, "∫₀^(π/2) cos x dx est égal à :", "1", "0", "π/2", "−1",
 "[sin x]₀^(π/2) = 1 − 0."),
(4, "z = 2e^(iπ/3). z³ est égal à :", "−8", "8", "8i", "6e^(iπ)",
 "z³ = 8e^(iπ) = −8."),
]),
]
