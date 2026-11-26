NIVEAU, MATIERE = "Tle C", "Physique-Chimie"
NIVEAUX = ["Tle C", "Tle D"]

CHAPITRES = [
dict(
nom="Cinématique du point",
fiche="""## Repérage
Dans un repère (O ; i, j, k), le point M a pour vecteur position OM = x i + y j + z k.
Le mouvement dépend du référentiel choisi (terrestre, géocentrique, héliocentrique).

## Vitesse et accélération
• Vecteur vitesse : v = dOM/dt (tangent à la trajectoire). Composantes vx = dx/dt…
• Vecteur accélération : a = dv/dt. Composantes ax = dvx/dt…
• Valeur : v = √(vx² + vy² + vz²).

## Repère de Frenet (mouvement curviligne)
a = (dv/dt) t + (v²/ρ) n, avec ρ le rayon de courbure.
La composante normale v²/ρ est dirigée vers le centre de courbure.

## Mouvements particuliers
• Rectiligne uniforme : a = 0 ; x = vt + x₀.
• Rectiligne uniformément varié : a constante ; v = at + v₀ ; x = ½at² + v₀t + x₀ ; v² − v₀² = 2a(x − x₀).
• Circulaire uniforme : v constante, a = v²/R dirigée vers le centre ; v = Rω ; période T = 2π/ω.
• Accéléré si a · v > 0 ; retardé si a · v < 0.

## Exemple corrigé
x(t) = 2t² − 4t + 1 (en m, s) : v(t) = 4t − 4, a = 4 m/s². La vitesse s'annule à t = 1 s : le mobile change de sens.
Le mouvement est retardé pour t < 1 s (v < 0 et a > 0), accéléré ensuite.""",
questions=[
(1, "Le vecteur vitesse est toujours :", "tangent à la trajectoire", "perpendiculaire à la trajectoire", "dirigé vers le centre", "nul",
 "C'est la dérivée du vecteur position."),
(1, "Dans un mouvement rectiligne uniforme, l'accélération est :", "nulle", "constante non nulle", "dirigée vers le centre", "égale à la vitesse",
 "La vitesse ne change ni en valeur ni en direction."),
(2, "x(t) = 2t² − 4t + 1. La vitesse à l'instant t est :", "v = 4t − 4", "v = 2t − 4", "v = 4t", "v = 2t² − 4",
 "v = dx/dt."),
(2, "x(t) = 2t² − 4t + 1. L'accélération vaut :", "4 m/s²", "2 m/s²", "−4 m/s²", "0",
 "a = dv/dt = 4."),
(2, "Dans un mouvement circulaire uniforme de rayon R, l'accélération vaut :", "v²/R, dirigée vers le centre", "0", "v/R, tangente", "Rω, tangente",
 "Seule la direction de la vitesse change : accélération centripète."),
(3, "Un mobile démarre sans vitesse avec a = 2 m/s². Sa vitesse après 5 s est :", "10 m/s", "25 m/s", "2,5 m/s", "50 m/s",
 "v = at."),
(3, "Une voiture à 20 m/s freine avec a = −5 m/s². La distance de freinage est :", "40 m", "20 m", "80 m", "4 m",
 "0 − 20² = 2 × (−5) × d, d = 400/10."),
(3, "Un point tourne sur un cercle de rayon 0,5 m à ω = 4 rad/s. Sa vitesse est :", "2 m/s", "8 m/s", "0,125 m/s", "4,5 m/s",
 "v = Rω."),
(3, "Le mouvement est retardé lorsque :", "le produit scalaire a · v est négatif", "a est nulle", "a · v est positif", "v est constante",
 "L'accélération s'oppose alors à la vitesse."),
(4, "Dans le repère de Frenet, la composante normale de l'accélération vaut :", "v²/ρ", "dv/dt", "vρ", "0 en mouvement courbe",
 "aₙ = v²/ρ, toujours dirigée vers le centre de courbure."),
(4, "Un mobile parcourt 100 m d'un mouvement uniformément accéléré sans vitesse initiale en 10 s. Son accélération est :", "2 m/s²", "1 m/s²", "10 m/s²", "0,5 m/s²",
 "100 = ½ a × 10², donc a = 2."),
]),

dict(
nom="Lois de Newton et centre d'inertie",
fiche="""## Les trois lois
1. Principe de l'inertie : dans un référentiel galiléen, si ΣF = 0, le centre d'inertie est au repos ou en mouvement rectiligne uniforme.
2. Théorème du centre d'inertie : ΣF = m a_G.
3. Actions réciproques : A sur B et B sur A sont opposées (même droite, sens contraires, même valeur).

## Méthode de résolution
1. Préciser le système et le référentiel (terrestre supposé galiléen).
2. Faire le bilan des forces et un schéma.
3. Écrire ΣF = m a_G et projeter sur des axes bien choisis.
4. En déduire a, puis la vitesse et la position (cinématique).

## Forces courantes
• Poids P = mg (g ≈ 9,8 m/s², vertical vers le bas).
• Réaction du support R (normale sans frottement).
• Tension d'un fil T ; frottements f opposés au mouvement.

## Plan incliné sans frottement
Projection sur la ligne de plus grande pente : a = g sin α.

## Théorème de l'énergie cinétique
ΔEc = ΣW(F), avec Ec = ½mv² et W(P) = mgh pour une descente h.

## Exemple corrigé
Un solide de 2 kg tiré par F = 10 N sur un sol horizontal sans frottement : a = 10/2 = 5 m/s².""",
questions=[
(1, "Le théorème du centre d'inertie s'écrit :", "ΣF = m a_G", "ΣF = m v_G", "ΣF = 0", "P = mg",
 "C'est la deuxième loi de Newton."),
(1, "Si la somme des forces est nulle, le centre d'inertie est :", "immobile ou en mouvement rectiligne uniforme", "forcément immobile", "en mouvement accéléré", "en mouvement circulaire",
 "Principe de l'inertie."),
(2, "Un solide de 2 kg soumis à une force résultante de 10 N a une accélération de :", "5 m/s²", "20 m/s²", "0,2 m/s²", "12 m/s²",
 "a = F/m."),
(2, "Le poids d'un objet de 5 kg (g = 9,8 m/s²) vaut :", "49 N", "5 N", "0,51 N", "9,8 N",
 "P = mg."),
(2, "Selon la 3ᵉ loi de Newton, la force exercée par A sur B et celle exercée par B sur A :", "ont la même valeur et des sens opposés", "ont des valeurs différentes", "sont dans le même sens", "s'annulent sur B",
 "Elles s'exercent sur deux corps différents, donc ne s'annulent pas."),
(3, "Sur un plan incliné d'angle α sans frottement, l'accélération d'un solide qui glisse est :", "g sin α", "g cos α", "g", "g tan α",
 "Seule la composante du poids le long de la pente accélère le solide."),
(3, "Un plan incliné de 30° sans frottement (g = 10 m/s²) donne une accélération de :", "5 m/s²", "10 m/s²", "8,7 m/s²", "2,5 m/s²",
 "10 × sin 30° = 10 × 0,5."),
(3, "L'énergie cinétique d'une voiture de 1000 kg à 10 m/s est :", "50 000 J", "10 000 J", "100 000 J", "5 000 J",
 "½ × 1000 × 10²."),
(3, "Un référentiel galiléen est un référentiel dans lequel :", "le principe de l'inertie est vérifié", "tous les objets sont immobiles", "il n'y a pas de pesanteur", "la vitesse de la lumière est infinie",
 "C'est sa définition."),
(4, "Un objet tombe sans frottement d'une hauteur de 5 m (g = 10 m/s²), sans vitesse initiale. Il touche le sol à :", "10 m/s", "50 m/s", "5 m/s", "100 m/s",
 "Énergie cinétique : ½mv² = mgh, v = √(2 × 10 × 5)."),
(4, "Un ascenseur monte à vitesse constante. La tension du câble est :", "égale au poids de la cabine", "supérieure au poids", "inférieure au poids", "nulle",
 "Vitesse constante en ligne droite : la somme des forces est nulle."),
]),

dict(
nom="Mouvements dans un champ uniforme",
fiche="""## Projectile dans le champ de pesanteur
Seul le poids agit (frottements négligés) : a = g.
Lancé depuis O avec v₀ faisant l'angle α avec l'horizontale :
• x = v₀ cos α × t   z = −½ g t² + v₀ sin α × t
• Trajectoire parabolique : z = −g x²/(2v₀² cos²α) + x tan α.
• Flèche (hauteur maximale) : v₀² sin²α/(2g) ; portée : v₀² sin 2α/g (maximale pour α = 45°).
Le mouvement horizontal est uniforme, le mouvement vertical uniformément varié.

## Particule chargée dans un champ électrique uniforme
F = qE ; a = qE/m. Entre deux plaques : E = U/d.
• Particule lancée parallèlement à E : mouvement rectiligne accéléré ou freiné.
   Accélération sous la tension U : ½mv² = |q|U (départ sans vitesse).
• Particule lancée perpendiculairement à E : trajectoire parabolique (déviation, oscilloscope).
• Un électron (q = −e) est soumis à une force de sens opposé à E.

## Ordres de grandeur
e = 1,6 × 10⁻¹⁹ C ; masse de l'électron 9,1 × 10⁻³¹ kg : le poids est négligeable devant la force électrique.

## Exemple corrigé
Une balle lancée horizontalement à 10 m/s d'une hauteur de 5 m (g = 10 m/s²) tombe en t = √(2h/g) = 1 s, à 10 m du pied de la table.""",
questions=[
(1, "Pour un projectile sans frottement, l'accélération est :", "égale au vecteur g", "nulle", "horizontale", "dans le sens de la vitesse",
 "Seul le poids agit : ma = mg."),
(2, "La trajectoire d'un projectile lancé obliquement sans frottement est :", "une parabole", "une droite", "un cercle", "une hyperbole",
 "x est proportionnel à t et z est un polynôme de degré 2 en t."),
(2, "Pour un projectile, la composante horizontale de la vitesse :", "reste constante", "augmente", "diminue jusqu'à 0", "est nulle",
 "Aucune force horizontale n'agit."),
(2, "La portée d'un tir (même hauteur de départ et d'arrivée) est maximale pour un angle de :", "45°", "30°", "60°", "90°",
 "Portée v₀² sin 2α/g, maximale quand sin 2α = 1."),
(3, "Une balle lancée horizontalement d'une hauteur de 5 m (g = 10 m/s²) touche le sol après :", "1 s", "0,5 s", "2 s", "5 s",
 "5 = ½ × 10 × t²."),
(3, "Deux plaques distantes de 2 cm sont soumises à 100 V. Le champ électrique vaut :", "5000 V/m", "50 V/m", "200 V/m", "2 V/m",
 "E = U/d = 100/0,02."),
(3, "Un électron placé dans un champ électrique E subit une force :", "de sens opposé à E", "de même sens que E", "perpendiculaire à E", "nulle",
 "F = qE avec q = −e < 0."),
(3, "Un électron accéléré sans vitesse initiale sous 1000 V acquiert une énergie cinétique de :", "1,6 × 10⁻¹⁶ J", "1000 J", "1,6 × 10⁻¹⁹ J", "1,6 × 10⁻²² J",
 "Ec = eU = 1,6 × 10⁻¹⁹ × 1000."),
(4, "Une particule chargée entrant perpendiculairement à un champ électrique uniforme décrit :", "une parabole", "une droite", "un cercle", "une hélice",
 "C'est le même cas que le projectile lancé horizontalement."),
(4, "Pour un électron dans un champ électrique, on néglige le poids car :", "il est très petit devant la force électrique", "l'électron n'a pas de masse", "g est nul dans le vide", "le poids est compensé par la réaction",
 "mg ≈ 10⁻²⁹ N, alors que eE vaut souvent plus de 10⁻¹⁵ N."),
]),

dict(
nom="Gravitation et satellites",
fiche="""## Loi de la gravitation universelle
Deux corps de masses mA et mB, à la distance d, s'attirent avec F = G mA mB/d².
G = 6,67 × 10⁻¹¹ N·m²/kg².

## Champ de gravitation
À la distance r du centre de la Terre (masse M) : g = GM/r².
À la surface : g₀ = GM/R² ≈ 9,8 m/s² ; à l'altitude h : g = g₀ R²/(R + h)².

## Satellite en orbite circulaire
Dans le référentiel géocentrique, seule l'attraction terrestre agit : mouvement circulaire uniforme.
• Vitesse : v = √(GM/r) (indépendante de la masse du satellite).
• Période : T = 2πr/v = 2π √(r³/GM).
• Troisième loi de Kepler : T²/r³ = 4π²/(GM), la même pour tous les satellites d'un même astre.

## Satellite géostationnaire
Il tourne dans le plan de l'équateur, dans le même sens que la Terre, avec T = 24 h (plus précisément 23 h 56 min) : il paraît immobile. Altitude ≈ 36 000 km. Utile pour les télécommunications et la météo.

## Apesanteur
Dans un satellite, les objets et le satellite tombent ensemble vers la Terre : ils semblent flotter.

## Exemple corrigé
Si la distance entre deux corps double, la force est divisée par 4.""",
questions=[
(1, "La force de gravitation entre deux corps est :", "attractive", "répulsive", "nulle si les masses sont petites", "dirigée perpendiculairement à la droite qui les joint",
 "La gravitation attire toujours."),
(2, "Si la distance entre deux corps double, la force de gravitation est :", "divisée par 4", "divisée par 2", "doublée", "inchangée",
 "F est inversement proportionnelle à d²."),
(2, "La vitesse d'un satellite en orbite circulaire de rayon r autour de la Terre est :", "v = √(GM/r)", "v = GM/r", "v = √(gr) quelle que soit l'altitude, avec g = 9,8 m/s²", "v = 2πr",
 "Le théorème du centre d'inertie donne GM/r² = v²/r."),
(2, "La vitesse d'un satellite sur une orbite donnée dépend :", "du rayon de l'orbite et de la masse de l'astre attracteur", "de la masse du satellite", "de sa forme", "de sa couleur",
 "v = √(GM/r) : la masse du satellite se simplifie."),
(2, "Un satellite géostationnaire a une période de révolution d'environ :", "24 h", "12 h", "1 h 30", "27 jours",
 "Il tourne en même temps que la Terre sur elle-même."),
(3, "La troisième loi de Kepler s'écrit :", "T²/r³ = constante", "T/r = constante", "T × r = constante", "T²r³ = constante",
 "T² = 4π² r³/(GM)."),
(3, "Plus un satellite est haut, plus sa vitesse est :", "petite", "grande", "constante", "nulle",
 "v = √(GM/r) diminue quand r augmente."),
(3, "À l'altitude h = R (rayon terrestre), l'intensité de la pesanteur vaut :", "g₀/4", "g₀/2", "2g₀", "g₀",
 "g = g₀ R²/(2R)² = g₀/4."),
(3, "Un satellite géostationnaire tourne :", "dans le plan de l'équateur", "au-dessus des pôles", "dans n'importe quel plan", "en sens inverse de la Terre",
 "Sinon il ne pourrait pas rester au-dessus du même point."),
(4, "Dans la Station spatiale, un astronaute flotte parce que :", "il tombe en même temps que la station", "il n'y a plus de gravitation", "la Terre le repousse", "il est trop loin de la Terre",
 "À 400 km d'altitude, g vaut encore environ 8,7 m/s²."),
(4, "Un satellite A a une orbite de rayon 4 fois plus grand que B. Sa période est :", "8 fois plus grande", "4 fois plus grande", "16 fois plus grande", "2 fois plus grande",
 "T² proportionnel à r³ : T proportionnelle à r^(3/2) = 4^(1,5) = 8."),
]),

dict(
nom="Oscillateurs mécaniques",
fiche="""## Pendule élastique horizontal
Un solide de masse m fixé à un ressort de raideur k, sans frottement.
Équation différentielle : x'' + (k/m) x = 0.
Solution : x(t) = Xm cos(ω₀t + φ), avec ω₀ = √(k/m).
• Période propre T₀ = 2π √(m/k) ; fréquence N₀ = 1/T₀.
• Xm (amplitude) et φ (phase à l'origine) dépendent des conditions initiales.

## Énergie
• Énergie cinétique ½mv² ; énergie potentielle élastique ½kx².
• Sans frottement, l'énergie mécanique E = ½kXm² reste constante.
• La vitesse est maximale au passage par la position d'équilibre : Vm = ω₀ Xm.

## Pendule simple (petites oscillations)
T₀ = 2π √(ℓ/g) : la période ne dépend ni de la masse ni de l'amplitude.

## Amortissement
Avec frottements, l'amplitude diminue : oscillations amorties (régime pseudo-périodique) ou retour sans oscillation (régime apériodique).

## Exemple corrigé
m = 0,1 kg et k = 10 N/m : ω₀ = √100 = 10 rad/s ; T₀ = 2π/10 ≈ 0,63 s.
Lâché à 5 cm sans vitesse : x(t) = 0,05 cos(10t).""",
questions=[
(1, "La période propre d'un pendule élastique est :", "T₀ = 2π √(m/k)", "T₀ = 2π √(k/m)", "T₀ = 2π m/k", "T₀ = √(m/k)",
 "Plus la masse est grande, plus les oscillations sont lentes."),
(2, "L'équation différentielle d'un pendule élastique non amorti est :", "x'' + (k/m) x = 0", "x' + (k/m) x = 0", "x'' − (k/m) x = 0", "x'' = g",
 "Le TCI donne m x'' = −k x."),
(2, "m = 0,1 kg et k = 10 N/m. La pulsation propre vaut :", "10 rad/s", "100 rad/s", "1 rad/s", "0,1 rad/s",
 "√(10/0,1) = √100."),
(2, "Sans frottement, l'énergie mécanique d'un oscillateur :", "reste constante", "diminue", "augmente", "est nulle",
 "Elle passe de la forme cinétique à la forme potentielle sans perte."),
(3, "Si on multiplie la masse par 4, la période d'un pendule élastique est :", "multipliée par 2", "multipliée par 4", "divisée par 2", "inchangée",
 "T₀ est proportionnelle à √m."),
(3, "La vitesse d'un oscillateur élastique est maximale :", "au passage par la position d'équilibre", "aux positions extrêmes", "à t = 0 toujours", "jamais",
 "L'énergie potentielle est alors nulle et l'énergie cinétique maximale."),
(3, "La période d'un pendule simple dépend :", "de sa longueur et de g", "de sa masse", "de l'amplitude, pour de petites oscillations", "de la couleur du fil",
 "Pour de petites oscillations, T₀ = 2π √(ℓ/g)."),
(3, "Un ressort de raideur 20 N/m est étiré de 10 cm. Son énergie potentielle élastique est :", "0,1 J", "1 J", "2 J", "0,2 J",
 "½ × 20 × 0,1²."),
(4, "x(t) = 0,05 cos(10t). La vitesse maximale vaut :", "0,5 m/s", "0,05 m/s", "10 m/s", "5 m/s",
 "Vm = ω₀ Xm = 10 × 0,05."),
(4, "Lorsque l'amplitude d'un oscillateur diminue au cours du temps, on dit que les oscillations sont :", "amorties", "entretenues", "forcées à la résonance", "propres et non amorties",
 "Les frottements dissipent l'énergie."),
]),

dict(
nom="Champ magnétique et force de Lorentz",
fiche="""## Champ magnétique
Créé par un aimant ou un courant ; il se mesure en teslas (T) avec un teslamètre.
• Les lignes de champ sortent du pôle nord et entrent par le pôle sud.
• Solénoïde long : champ uniforme à l'intérieur, B = μ₀ N I/ℓ (μ₀ = 4π × 10⁻⁷ SI).

## Force de Lorentz
Une particule de charge q et de vitesse v dans un champ B subit F = q v ∧ B.
• F est perpendiculaire à v et à B ; valeur |q| v B sin(v, B).
• Elle ne travaille pas : la vitesse garde la même valeur.

## Mouvement dans un champ uniforme (v perpendiculaire à B)
Mouvement circulaire uniforme de rayon R = mv/(|q|B).
Applications : spectrographe de masse (séparer les isotopes), cyclotron, déflexion des faisceaux.

## Force de Laplace
Un conducteur de longueur ℓ parcouru par I dans B : F = I ℓ ∧ B, valeur I ℓ B sin α.
Principe des moteurs électriques et des haut-parleurs.

## Sens de la force
Règle des trois doigts de la main droite (pour q > 0) : pouce = v (ou I), index = B, majeur = F.
Pour un électron, la force est de sens opposé.

## Exemple corrigé
I = 2 A, ℓ = 0,1 m, B = 0,5 T, conducteur perpendiculaire à B : F = 2 × 0,1 × 0,5 = 0,1 N.""",
questions=[
(1, "L'unité du champ magnétique est :", "le tesla", "le volt par mètre", "le weber par seconde", "le newton",
 "Symbole T."),
(1, "À l'extérieur d'un aimant, les lignes de champ vont :", "du pôle nord vers le pôle sud", "du pôle sud vers le pôle nord", "en cercle autour d'un pôle", "dans tous les sens",
 "Elles sortent par le nord."),
(2, "La force de Lorentz est :", "perpendiculaire à la vitesse", "parallèle à la vitesse", "toujours nulle", "parallèle à B",
 "F = q v ∧ B est perpendiculaire à v et à B."),
(2, "Dans un champ magnétique uniforme, une particule lancée perpendiculairement à B a un mouvement :", "circulaire uniforme", "rectiligne uniforme", "parabolique", "rectiligne accéléré",
 "La force, toujours perpendiculaire à v, joue le rôle de force centripète."),
(2, "La force de Lorentz ne modifie pas la valeur de la vitesse car :", "son travail est nul", "elle est trop faible", "elle est parallèle à v", "la charge est nulle",
 "Une force perpendiculaire au déplacement ne travaille pas."),
(3, "Une particule de charge q entre avec une vitesse v perpendiculaire à un champ B uniforme. Le rayon de sa trajectoire circulaire vaut :", "R = mv/(|q|B)", "R = |q|B/(mv)", "R = mvB/|q|", "R = mB/(qv)",
 "|q|vB = mv²/R."),
(3, "Un conducteur de 0,1 m parcouru par 2 A, perpendiculaire à un champ de 0,5 T, subit une force de :", "0,1 N", "1 N", "0,01 N", "10 N",
 "F = IℓB."),
(3, "À l'intérieur d'un solénoïde long parcouru par un courant, le champ magnétique est :", "uniforme", "nul", "radial", "plus intense aux bords",
 "B = μ₀ N I/ℓ, parallèle à l'axe."),
(4, "Dans un spectrographe de masse, deux isotopes de même charge et de même vitesse sont séparés car :", "le plus lourd décrit un cercle plus grand", "le plus léger décrit un cercle plus grand", "ils ont la même trajectoire", "le plus lourd est arrêté",
 "R = mv/(|q|B) est proportionnel à la masse."),
(4, "Si on double la valeur de B, le rayon de la trajectoire d'une particule chargée est :", "divisé par 2", "doublé", "multiplié par 4", "inchangé",
 "R est inversement proportionnel à B."),
]),

dict(
nom="Induction et auto-induction",
fiche="""## Flux magnétique
Φ = N B S cos θ (en webers, Wb), θ angle entre B et la normale à la surface.

## Induction
Une variation de flux à travers un circuit y crée une force électromotrice induite e = −dΦ/dt (loi de Faraday).
Loi de Lenz : le courant induit s'oppose, par ses effets, à la cause qui lui donne naissance.
Applications : alternateur, dynamo, transformateur, plaques à induction.

## Auto-induction
Une bobine parcourue par un courant variable crée elle-même une f.é.m. : e = −L di/dt.
L est l'inductance (en henrys, H). Tension aux bornes d'une bobine : u = r i + L di/dt.
La bobine s'oppose aux variations du courant : elle retarde son établissement et sa rupture (étincelle à l'ouverture).

## Circuit RL
Établissement du courant : i(t) = (E/R)(1 − e^(−t/τ)), avec la constante de temps τ = L/R.
À t = τ, le courant atteint 63 % de sa valeur finale ; à 5τ, le régime permanent est atteint.

## Énergie stockée dans une bobine
E = ½ L i².

## Exemple corrigé
L = 0,2 H et R = 100 Ω : τ = 0,2/100 = 2 ms. Avec i = 0,5 A, la bobine stocke ½ × 0,2 × 0,25 = 0,025 J.""",
questions=[
(1, "L'unité de l'inductance d'une bobine est :", "le henry", "le farad", "le tesla", "l'ohm",
 "Symbole H."),
(2, "Une f.é.m. induite apparaît dans un circuit lorsque :", "le flux magnétique qui le traverse varie", "le flux est constant", "le circuit est ouvert seulement", "il n'y a pas de champ",
 "Loi de Faraday : e = −dΦ/dt."),
(2, "Selon la loi de Lenz, le courant induit :", "s'oppose à la cause qui le produit", "renforce toujours le champ", "est toujours nul", "dépend de la couleur du fil",
 "C'est le sens du signe moins dans e = −dΦ/dt."),
(2, "La tension aux bornes d'une bobine de résistance r et d'inductance L est :", "u = ri + L di/dt", "u = ri", "u = L i", "u = q/C",
 "Terme résistif plus terme d'auto-induction."),
(3, "La constante de temps d'un circuit RL est :", "τ = L/R", "τ = RL", "τ = R/L", "τ = √(LR)",
 "τ = L/R s'exprime en secondes."),
(3, "L = 0,2 H et R = 100 Ω. La constante de temps vaut :", "2 ms", "20 s", "500 s", "0,5 ms",
 "0,2/100 = 0,002 s."),
(3, "Une bobine d'inductance 0,2 H parcourue par 0,5 A stocke une énergie de :", "0,025 J", "0,05 J", "0,1 J", "0,25 J",
 "½ × 0,2 × 0,5²."),
(3, "Dans un circuit RL, à t = τ, le courant atteint environ :", "63 % de sa valeur finale", "37 %", "100 %", "50 %",
 "1 − e⁻¹ ≈ 0,63."),
(4, "Une étincelle peut apparaître à l'ouverture d'un circuit contenant une bobine car :", "la bobine s'oppose à la chute brutale du courant", "la bobine est un condensateur", "le courant devient nul instantanément sans conséquence", "la résistance devient infinie sans effet",
 "e = −L di/dt est très grande quand i chute brusquement."),
(4, "Un alternateur produit du courant grâce :", "à la rotation d'un aimant devant des bobines", "à une réaction chimique", "à l'effet photoélectrique", "à la chaleur",
 "Le flux varie dans les bobines : il y a induction."),
]),

dict(
nom="Solutions aqueuses et pH",
fiche="""## Le pH
pH = −log[H₃O⁺] et [H₃O⁺] = 10^(−pH) (en mol/L).
À 25 °C : solution neutre pH = 7 ; acide pH < 7 ; basique pH > 7.

## Autoprotolyse de l'eau
2 H₂O ⇌ H₃O⁺ + HO⁻. Produit ionique Ke = [H₃O⁺][HO⁻] = 10⁻¹⁴ à 25 °C (pKe = 14).
Dans l'eau pure : [H₃O⁺] = [HO⁻] = 10⁻⁷ mol/L.

## Concentrations
• Concentration molaire C = n/V (mol/L) ; massique Cm = m/V = C × M.
• Dilution : la quantité de soluté se conserve, C₁V₁ = C₂V₂.
• Diluer 10 fois un acide fort augmente son pH d'une unité.

## Électroneutralité
Dans une solution, la somme des concentrations des charges positives égale celle des charges négatives.

## Mesure du pH
pH-mètre (précis, étalonné avec des solutions tampons) ou papier pH (approximatif).
Le pH se donne avec une précision de 0,1 unité.

## Exemple corrigé
[H₃O⁺] = 10⁻³ mol/L : pH = 3. Alors [HO⁻] = 10⁻¹⁴/10⁻³ = 10⁻¹¹ mol/L.""",
questions=[
(1, "À 25 °C, une solution de pH = 7 est :", "neutre", "acide", "basique", "concentrée",
 "[H₃O⁺] = [HO⁻] = 10⁻⁷ mol/L."),
(1, "Une solution de pH = 3 est :", "acide", "basique", "neutre", "saturée",
 "pH < 7 à 25 °C."),
(2, "Si [H₃O⁺] = 10⁻⁴ mol/L, le pH vaut :", "4", "−4", "10", "0,0001",
 "pH = −log(10⁻⁴)."),
(2, "À 25 °C, le produit ionique de l'eau vaut :", "10⁻¹⁴", "10⁻⁷", "14", "1",
 "Ke = [H₃O⁺][HO⁻]."),
(2, "Si pH = 3, [HO⁻] est égale à :", "10⁻¹¹ mol/L", "10⁻³ mol/L", "10⁻⁷ mol/L", "10³ mol/L",
 "10⁻¹⁴/10⁻³."),
(2, "On dissout 0,2 mol de soluté dans 500 mL. La concentration est :", "0,4 mol/L", "0,1 mol/L", "100 mol/L", "0,2 mol/L",
 "C = 0,2/0,5."),
(3, "On dilue 10 mL d'une solution à 1 mol/L pour obtenir 100 mL. La nouvelle concentration est :", "0,1 mol/L", "10 mol/L", "1 mol/L", "0,01 mol/L",
 "C₂ = C₁V₁/V₂ = 1 × 10/100."),
(3, "Quand on dilue 10 fois une solution d'acide fort, son pH :", "augmente d'une unité", "diminue d'une unité", "ne change pas", "est multiplié par 10",
 "[H₃O⁺] est divisée par 10."),
(3, "Une solution a pour pH 2,5. [H₃O⁺] vaut environ :", "3,2 × 10⁻³ mol/L", "2,5 mol/L", "3,2 × 10⁻² mol/L", "0,25 mol/L",
 "10^(−2,5) ≈ 3,16 × 10⁻³."),
(4, "Dans une solution de chlorure de sodium, l'électroneutralité s'écrit :", "[Na⁺] + [H₃O⁺] = [Cl⁻] + [HO⁻]", "[Na⁺] = [H₃O⁺]", "[Na⁺] + [Cl⁻] = 0", "[H₃O⁺] = 0",
 "Charges positives = charges négatives."),
(4, "La masse molaire du NaOH est 40 g/mol. Une solution à 0,1 mol/L a une concentration massique de :", "4 g/L", "40 g/L", "0,4 g/L", "400 g/L",
 "Cm = C × M = 0,1 × 40."),
]),

dict(
nom="Acides forts et bases fortes",
fiche="""## Définitions (Brønsted)
• Un acide est une espèce capable de céder un proton H⁺ ; une base peut en capter un.
• Acide fort : réaction totale avec l'eau. HCl + H₂O → H₃O⁺ + Cl⁻.
• Base forte : réaction totale avec l'eau. Exemples : l'hydroxyde de sodium (NaOH → Na⁺ + HO⁻) ; l'ion éthanolate (C₂H₅O⁻ + H₂O → C₂H₅OH + HO⁻).

## pH
• Acide fort de concentration C (10⁻⁶ < C < 10⁻¹ mol/L) : pH = −log C.
• Base forte de concentration C (10⁻⁶ < C < 10⁻¹ mol/L) : pH = 14 + log C.

## Réaction acide fort / base forte
H₃O⁺ + HO⁻ → 2 H₂O : réaction totale, rapide et exothermique.
À l'équivalence, les réactifs sont dans les proportions stœchiométriques : Ca Va = Cb Vb, et le pH vaut 7 à 25 °C.

## Sécurité
Les acides et bases concentrés sont corrosifs : blouse, gants, lunettes. Verser l'acide dans l'eau, jamais l'inverse.

## Exemple corrigé
Acide chlorhydrique à 10⁻² mol/L : pH = 2.
Soude à 10⁻² mol/L : pH = 14 + log 10⁻² = 12.
10 mL d'acide à 0,1 mol/L sont neutralisés par 20 mL de soude à 0,05 mol/L : 0,1 × 10 = 0,05 × 20.""",
questions=[
(1, "Selon Brønsted, un acide est une espèce capable de :", "céder un proton", "capter un proton", "céder un électron", "capter un électron",
 "Il libère H⁺."),
(2, "Le pH d'une solution d'acide chlorhydrique à 10⁻² mol/L est :", "2", "12", "−2", "0,01",
 "Acide fort : pH = −log C."),
(2, "Le pH d'une solution de soude à 10⁻² mol/L est :", "12", "2", "14", "10",
 "Base forte : pH = 14 + log C = 14 − 2."),
(2, "La réaction entre un acide fort et une base forte a pour équation :", "H₃O⁺ + HO⁻ → 2 H₂O", "H₂O → H⁺ + HO⁻", "H₃O⁺ + Cl⁻ → HCl", "Na⁺ + HO⁻ → NaOH",
 "Les ions spectateurs (Na⁺, Cl⁻) n'apparaissent pas."),
(2, "La réaction d'un acide fort avec l'eau est :", "totale", "limitée", "impossible", "très lente",
 "C'est la définition d'un acide fort."),
(3, "À l'équivalence du dosage d'un acide fort par une base forte, le pH à 25 °C vaut :", "7", "0", "14", "4",
 "Il ne reste que de l'eau et des ions spectateurs."),
(3, "10 mL d'acide à 0,1 mol/L sont dosés par de la soude à 0,05 mol/L. Le volume équivalent est :", "20 mL", "10 mL", "5 mL", "50 mL",
 "Vb = CaVa/Cb = 0,1 × 10/0,05."),
(3, "Pour préparer une solution diluée d'acide, il faut :", "verser l'acide dans l'eau", "verser l'eau dans l'acide", "chauffer l'acide", "agiter sans lunettes",
 "La réaction est exothermique : verser l'eau sur l'acide peut provoquer des projections."),
(4, "Une solution d'acide fort a pH = 3. On la dilue 100 fois. Le nouveau pH est :", "5", "3", "1", "300",
 "[H₃O⁺] passe de 10⁻³ à 10⁻⁵ mol/L."),
(4, "On mélange 10 mL d'acide fort à 0,1 mol/L et 5 mL de base forte à 0,1 mol/L. Le mélange est :", "acide", "neutre", "basique", "saturé",
 "1 mmol de H₃O⁺ pour 0,5 mmol de HO⁻ : l'acide est en excès."),
]),

dict(
nom="Acides faibles, bases faibles et pKa",
fiche="""## Acide faible
Sa réaction avec l'eau est limitée : AH + H₂O ⇌ A⁻ + H₃O⁺.
Pour un acide faible de concentration C : pH > −log C. Exemple : l'acide éthanoïque CH₃COOH.

## Couple acide/base et Ka
AH/A⁻ est un couple. Constante d'acidité : Ka = [A⁻][H₃O⁺]/[AH] ; pKa = −log Ka.
Relation d'Henderson : pH = pKa + log([A⁻]/[AH]).

## Domaines de prédominance
• pH < pKa : la forme acide AH prédomine.
• pH > pKa : la forme basique A⁻ prédomine.
• pH = pKa : [AH] = [A⁻].

## Force des acides
Plus le pKa est petit, plus l'acide est fort (et sa base conjuguée faible).
Couples de référence : H₃O⁺/H₂O (pKa = 0) et H₂O/HO⁻ (pKa = 14).
Exemples : CH₃COOH/CH₃COO⁻ (pKa = 4,8) ; NH₄⁺/NH₃ (pKa = 9,2).

## Solution tampon
Mélange en quantités voisines d'un acide faible et de sa base conjuguée : pH ≈ pKa.
Son pH varie peu par dilution modérée ou par ajout de petites quantités d'acide ou de base. Le sang est tamponné vers 7,4.

## Indicateurs colorés
Ce sont des couples acide/base dont les deux formes ont des couleurs différentes ; zone de virage autour du pKa.""",
questions=[
(1, "La réaction d'un acide faible avec l'eau est :", "limitée", "totale", "impossible", "explosive",
 "Seule une partie des molécules réagit."),
(2, "Pour le couple AH/A⁻, si pH < pKa, l'espèce prédominante est :", "AH", "A⁻", "H₂O", "aucune",
 "En milieu plus acide que le pKa, la forme acide domine."),
(2, "Lorsque pH = pKa :", "[AH] = [A⁻]", "[AH] = 0", "[A⁻] = 0", "[H₃O⁺] = 1 mol/L",
 "log([A⁻]/[AH]) = 0."),
(2, "Le pKa du couple CH₃COOH/CH₃COO⁻ est 4,8. À pH = 7, l'espèce prédominante est :", "CH₃COO⁻", "CH₃COOH", "les deux à égalité", "H₃O⁺",
 "pH > pKa : forme basique."),
(2, "Plus le pKa d'un couple est petit :", "plus l'acide est fort", "plus l'acide est faible", "plus la base est forte", "plus la solution est diluée",
 "Ka est alors plus grand : l'acide cède plus facilement son proton."),
(3, "Une solution d'acide faible à 10⁻² mol/L a un pH :", "supérieur à 2", "égal à 2", "inférieur à 2", "égal à 12",
 "La réaction étant limitée, [H₃O⁺] < C."),
(3, "pH = pKa + log([A⁻]/[AH]). Si [A⁻] = 10 [AH] et pKa = 4,8, le pH vaut :", "5,8", "3,8", "4,8", "48",
 "4,8 + log 10."),
(3, "Une solution tampon est une solution dont le pH :", "varie peu par ajout modéré d'acide, de base ou par dilution", "est toujours 7", "varie beaucoup par dilution", "est toujours acide",
 "Elle contient un couple acide/base en quantités voisines."),
(3, "Le pKa du couple NH₄⁺/NH₃ est 9,2. NH₃ est :", "une base faible", "un acide fort", "une base forte", "un acide faible",
 "Il capte un proton dans une réaction limitée."),
(4, "Ka = 10⁻⁵. Le pKa vaut :", "5", "−5", "10⁵", "0,00001",
 "pKa = −log Ka."),
(4, "On choisit un indicateur coloré pour un dosage de sorte que :", "sa zone de virage contienne le pH à l'équivalence", "son pKa soit 0", "il soit incolore", "son pKa soit 14",
 "Le changement de couleur doit avoir lieu au moment de l'équivalence."),
]),

dict(
nom="Dosages acido-basiques",
fiche="""## Principe
On fait réagir une solution de concentration inconnue (dans le bécher) avec une solution titrante de concentration connue (dans la burette). La réaction doit être totale et rapide.

## Équivalence
Les réactifs ont été mélangés dans les proportions stœchiométriques : Ca Va = Cb VbE.
On repère l'équivalence par un saut de pH (méthode des tangentes) ou par le virage d'un indicateur coloré.

## Courbes pH = f(Vb)
• Acide fort par base forte : pH à l'équivalence = 7 ; saut de pH important ; BBT adapté.
• Acide faible par base forte : pH à l'équivalence > 7 (la base conjuguée est présente) ; phénolphtaléine adaptée.
   À la demi-équivalence (Vb = VbE/2), pH = pKa : on lit le pKa du couple.
• Base faible par acide fort : pH à l'équivalence < 7 ; rouge de méthyle adapté.

[[schema:courbe-dosage|Allure de la courbe pH = f(Vb) (acide fort et base forte)]]
## Méthode des tangentes
On trace deux tangentes parallèles de part et d'autre du saut, puis la parallèle équidistante : elle coupe la courbe au point d'équivalence.

## Exemple corrigé
20 mL d'acide éthanoïque dosés par de la soude à 0,1 mol/L : VbE = 10 mL.
Ca = 0,1 × 10/20 = 0,05 mol/L. Le pH lu pour Vb = 5 mL donne le pKa (≈ 4,8).""",
questions=[
(3, 'Sur la courbe du schéma, le point E correspond :', "à l'équivalence", 'au début du dosage', 'à la demi-équivalence', 'à la fin de la burette',
 "Le saut de pH est maximal à l'équivalence ; ici pH = 7 (acide fort et base forte).", 'courbe-dosage'),
(1, "Dans un dosage, la solution titrante est placée :", "dans la burette", "dans le bécher", "dans l'éprouvette seulement", "dans le pH-mètre",
 "On connaît sa concentration et on mesure le volume versé."),
(2, "À l'équivalence d'un dosage acide/base :", "les réactifs sont dans les proportions stœchiométriques", "le pH vaut toujours 7", "l'acide est en excès", "le volume versé est nul",
 "Ca Va = Cb VbE pour une réaction mole à mole."),
(2, "20 mL d'acide sont dosés par une base à 0,1 mol/L ; VbE = 10 mL. La concentration de l'acide est :", "0,05 mol/L", "0,2 mol/L", "0,1 mol/L", "2 mol/L",
 "Ca = 0,1 × 10/20."),
(2, "Pour repérer l'équivalence sur une courbe pH = f(V), on utilise :", "la méthode des tangentes", "la loi d'Ohm", "la règle des trois doigts", "la loi de Kepler",
 "Elle permet de trouver le point d'inflexion du saut de pH."),
(3, "Lors du dosage d'un acide faible par une base forte, le pH à l'équivalence est :", "supérieur à 7", "égal à 7", "inférieur à 7", "égal au pKa",
 "La solution contient la base conjuguée de l'acide faible."),
(3, "À la demi-équivalence du dosage d'un acide faible par une base forte :", "pH = pKa", "pH = 7", "pH = 14", "pH = 0",
 "La moitié de l'acide a été transformée : [AH] = [A⁻]."),
(3, "Pour doser un acide faible par une base forte, l'indicateur le plus adapté est :", "la phénolphtaléine (zone de virage 8,2 à 10)", "le rouge de méthyle (4,2 à 6,2)", "l'hélianthine (3,1 à 4,4)", "aucun",
 "Le pH à l'équivalence est basique."),
(3, "Lors du dosage d'une base faible par un acide fort, le pH à l'équivalence est :", "inférieur à 7", "supérieur à 7", "égal à 7", "égal à 14",
 "La solution contient l'acide conjugué de la base faible."),
(4, "On dose 10 mL d'ammoniac par HCl à 0,02 mol/L ; VE = 15 mL. La concentration de l'ammoniac est :", "0,03 mol/L", "0,013 mol/L", "0,3 mol/L", "0,02 mol/L",
 "C = 0,02 × 15/10."),
(4, "Si on ajoute de l'eau distillée dans le bécher avant le dosage, le volume équivalent :", "ne change pas", "augmente", "diminue", "devient nul",
 "La quantité d'acide à doser est la même."),
]),

dict(
nom="Les alcools",
fiche="""## Structure
Un alcool contient un groupe hydroxyle —OH porté par un carbone tétragonal. Formule générale (alcool saturé) : CₙH₂ₙ₊₁OH.
Nom : celui de l'alcane avec la terminaison « -ol » et le numéro du carbone porteur : propan-2-ol.

## Trois classes
• Primaire : le carbone fonctionnel est lié à au plus un autre carbone (éthanol, propan-1-ol).
• Secondaire : lié à deux carbones (propan-2-ol, butan-2-ol).
• Tertiaire : lié à trois carbones (2-méthylpropan-2-ol).

## Oxydation ménagée (par exemple par le dichromate de potassium acidifié, orange qui devient vert)
• Alcool primaire → aldéhyde → acide carboxylique.
• Alcool secondaire → cétone.
• Alcool tertiaire : pas d'oxydation ménagée.

## Tests des produits
• DNPH (2,4-dinitrophénylhydrazine) : précipité jaune avec aldéhydes et cétones (groupe carbonyle).
• Liqueur de Fehling (précipité rouge brique) et réactif de Tollens (miroir d'argent) : seulement avec les aldéhydes.

## Autres réactions
• Déshydratation (acide sulfurique, chaleur) : alcène ou éther-oxyde.
• Estérification avec un acide carboxylique (voir chapitre suivant).

## Usages
Éthanol : boissons, antiseptique, carburant ; méthanol : très toxique.""",
questions=[
(1, "Le groupe caractéristique des alcools est :", "—OH", "—COOH", "—CHO", "—NH₂",
 "Groupe hydroxyle."),
(1, "Le nom de CH₃—CH₂—OH est :", "l'éthanol", "le méthanol", "l'éthanal", "l'acide éthanoïque",
 "Deux carbones et la terminaison -ol."),
(2, "Le propan-2-ol est un alcool :", "secondaire", "primaire", "tertiaire", "aromatique",
 "Le carbone fonctionnel est lié à deux autres carbones."),
(2, "L'oxydation ménagée d'un alcool secondaire donne :", "une cétone", "un aldéhyde", "un acide carboxylique", "rien",
 "Le carbone fonctionnel ne porte qu'un hydrogène."),
(2, "Un alcool tertiaire soumis à une oxydation ménagée :", "ne réagit pas", "donne une cétone", "donne un aldéhyde", "donne un ester",
 "Son carbone fonctionnel ne porte aucun hydrogène."),
(3, "L'oxydation ménagée de l'éthanol en excès d'oxydant conduit finalement à :", "l'acide éthanoïque", "la propanone", "l'éthanal seulement", "l'éthène",
 "Alcool primaire → aldéhyde → acide carboxylique."),
(3, "Un composé donne un précipité jaune avec la DNPH mais ne réagit pas avec la liqueur de Fehling. C'est :", "une cétone", "un aldéhyde", "un alcool", "un acide",
 "DNPH : groupe carbonyle ; Fehling négatif : pas un aldéhyde."),
(3, "Lors de l'oxydation par le dichromate acidifié, la solution passe :", "de l'orange au vert", "du vert à l'orange", "du bleu au rouge", "de l'incolore au violet",
 "Cr₂O₇²⁻ (orange) est réduit en Cr³⁺ (vert)."),
(3, "La formule brute d'un alcool saturé à 3 carbones est :", "C₃H₈O", "C₃H₆O", "C₃H₆O₂", "C₃H₈",
 "CₙH₂ₙ₊₁OH avec n = 3."),
(4, "La déshydratation intramoléculaire de l'éthanol donne :", "l'éthène", "l'éthanal", "l'éthane", "l'acide éthanoïque",
 "Une molécule d'eau est retirée : CH₂=CH₂."),
(4, "Le 2-méthylpropan-2-ol est :", "un alcool tertiaire", "un alcool primaire", "un alcool secondaire", "une cétone",
 "Le carbone porteur du —OH est lié à trois carbones."),
]),

dict(
nom="Acides carboxyliques et dérivés",
fiche="""## Acides carboxyliques
Groupe carboxyle —COOH. Nom : « acide » + nom de l'alcane en « -oïque » (acide éthanoïque CH₃COOH, dans le vinaigre).
Ce sont des acides faibles (pKa ≈ 4 à 5).

## Dérivés
• Chlorure d'acyle R—COCl ; anhydride d'acide R—CO—O—CO—R.
• Ester R—COO—R' (odeurs fruitées, arômes, parfums).
• Amide R—CONH₂.

## Estérification (acide + alcool ⇌ ester + eau)
Réaction lente, limitée (environ 67 % avec un alcool primaire, mélange équimolaire) et athermique.
L'acide sulfurique (catalyseur) et la chaleur accélèrent la réaction sans changer le rendement.
Pour améliorer le rendement : un réactif en excès ou l'élimination de l'eau ou de l'ester.

## Hydrolyse
Ester + eau ⇌ acide + alcool : réaction inverse, lente et limitée.

## Réactions totales
• Avec un chlorure d'acyle ou un anhydride à la place de l'acide : estérification rapide et totale.
• Saponification : ester + ion hydroxyde → ion carboxylate + alcool. Totale ; avec les corps gras, elle donne le savon.

## Nommer un ester
R—COO—R' : « R-oate de R'-yle ». CH₃COOC₂H₅ : éthanoate d'éthyle.""",
questions=[
(1, "Le groupe caractéristique d'un acide carboxylique est :", "—COOH", "—OH", "—CO—", "—NH₂",
 "Groupe carboxyle."),
(1, "Le vinaigre contient principalement :", "de l'acide éthanoïque", "de l'éthanol", "de l'acide chlorhydrique", "de l'éthanoate d'éthyle",
 "CH₃COOH."),
(2, "L'estérification entre un acide carboxylique et un alcool est :", "lente et limitée", "rapide et totale", "lente et totale", "impossible",
 "Elle aboutit à un équilibre."),
(2, "Le rôle de l'acide sulfurique dans l'estérification est de :", "accélérer la réaction", "augmenter le rendement", "neutraliser l'ester", "colorer le mélange",
 "C'est un catalyseur : il ne modifie pas l'état final."),
(2, "Le nom de CH₃COOC₂H₅ est :", "éthanoate d'éthyle", "propanoate de méthyle", "acide butanoïque", "éthanoate de méthyle",
 "Partie acide à 2 carbones, partie alcool éthyle."),
(3, "Avec un mélange équimolaire d'acide et d'alcool primaire, le rendement de l'estérification est d'environ :", "67 %", "100 %", "33 %", "10 %",
 "Il reste un tiers des réactifs à l'équilibre."),
(3, "Pour augmenter le rendement de l'estérification, on peut :", "mettre un réactif en excès", "ajouter de l'eau", "refroidir le mélange", "retirer le catalyseur",
 "On déplace l'équilibre dans le sens de la formation de l'ester."),
(3, "Pour obtenir un ester de façon rapide et totale, on remplace l'acide par :", "un anhydride d'acide ou un chlorure d'acyle", "un alcool tertiaire", "de l'eau", "une amine",
 "Ces dérivés sont beaucoup plus réactifs."),
(3, "La saponification d'un ester par la soude donne :", "un ion carboxylate et un alcool", "un acide et un alcool", "un aldéhyde", "un alcène",
 "Réaction totale ; avec les corps gras, on obtient le savon."),
(4, "L'hydrolyse d'un ester est :", "la réaction inverse de l'estérification", "une réaction totale", "une oxydation", "une saponification",
 "Ester + eau ⇌ acide + alcool."),
(4, "Les esters sont souvent utilisés pour :", "leurs odeurs fruitées (arômes, parfums)", "leur grande acidité", "leur toxicité", "leur couleur bleue",
 "Exemple : l'arôme de banane."),
]),

dict(
nom="Amines et acides α-aminés",
fiche="""## Amines
Dérivés de l'ammoniac NH₃ où des H sont remplacés par des groupes carbonés.
• Primaire R—NH₂ ; secondaire R—NH—R' ; tertiaire R—N(R')—R''.
• Nom : méthylamine CH₃NH₂, ou méthanamine.
Le doublet libre de l'azote leur donne :
• un caractère basique (bases faibles) : R—NH₂ + H₂O ⇌ R—NH₃⁺ + HO⁻ ;
• un caractère nucléophile : elles réagissent avec les chlorures d'acyle pour donner des amides.

## Acides α-aminés
Formule R—CH(NH₂)—COOH : le groupe amine est porté par le carbone voisin du groupe carboxyle (carbone α).
• Glycine : R = H (seul acide α-aminé non chiral) ; alanine : R = CH₃.
• Le carbone α (sauf glycine) est asymétrique : deux énantiomères, notés D et L ; les protéines naturelles sont formées d'acides L.

## Amphion
En solution, l'acide α-aminé existe surtout sous forme d'amphion : R—CH(NH₃⁺)—COO⁻. Il est amphotère (acide et base).

## Liaison peptidique
—CO—NH— : elle se forme entre le —COOH d'un acide aminé et le —NH₂ d'un autre, avec élimination d'eau.
Deux acides aminés différents peuvent donner deux dipeptides différents (Gly-Ala et Ala-Gly).
Les protéines sont de longues chaînes d'acides α-aminés.""",
questions=[
(1, "Une amine dérive de :", "l'ammoniac", "l'eau", "l'éthanol", "l'acide éthanoïque",
 "On remplace des H de NH₃ par des groupes carbonés."),
(2, "CH₃—NH—CH₃ est une amine :", "secondaire", "primaire", "tertiaire", "aromatique",
 "L'azote est lié à deux carbones."),
(2, "Les amines ont un caractère basique grâce :", "au doublet libre de l'azote", "à leur groupe —OH", "à leur odeur", "à l'oxygène",
 "Le doublet libre peut capter un proton."),
(2, "Un acide α-aminé possède :", "un groupe —NH₂ et un groupe —COOH liés au même atome de carbone", "deux groupes —OH", "un groupe —CHO", "seulement un groupe —COOH",
 "Le groupe amine est porté par le carbone α, celui qui est lié au groupe carboxyle."),
(2, "L'acide α-aminé le plus simple, non chiral, est :", "la glycine", "l'alanine", "la valine", "la leucine",
 "R = H : le carbone α porte deux H."),
(3, "En solution aqueuse, un acide α-aminé existe principalement sous forme :", "d'amphion", "d'ester", "de cétone", "d'alcène",
 "R—CH(NH₃⁺)—COO⁻."),
(3, "La liaison peptidique a pour formule :", "—CO—NH—", "—COO—", "—O—", "—NH₂",
 "C'est une fonction amide."),
(3, "L'alanine possède un carbone asymétrique. Elle existe donc sous :", "deux formes énantiomères", "une seule forme", "trois formes", "quatre formes",
 "Deux images l'une de l'autre dans un miroir, non superposables."),
(3, "La formation d'une liaison peptidique s'accompagne de l'élimination :", "d'une molécule d'eau", "d'une molécule de dioxyde de carbone", "d'un ion chlorure toujours", "de dihydrogène",
 "C'est une condensation."),
(4, "Avec la glycine et l'alanine, le nombre de dipeptides différents possibles (Gly-Gly compris) est :", "4", "2", "1", "3",
 "Gly-Gly, Gly-Ala, Ala-Gly et Ala-Ala."),
(4, "Une amine réagit avec un chlorure d'acyle pour donner :", "un amide", "un ester", "un alcool", "une cétone",
 "Le doublet de l'azote attaque le carbone du groupe —COCl."),
]),

dict(
nom="Révision BAC",
fiche="""## Physique : les formules clés
• Cinématique : v = at + v₀ ; x = ½at² + v₀t + x₀ ; v² − v₀² = 2aΔx.
• Newton : ΣF = ma ; plan incliné a = g sin α ; Ec = ½mv².
• Projectile : x = v₀cos α t ; z = −½gt² + v₀sin α t ; portée v₀² sin 2α/g.
• Champ électrique : F = qE ; E = U/d ; Ec = |q|U.
• Satellite : v = √(GM/r) ; T²/r³ = 4π²/(GM).
• Oscillateur : T₀ = 2π√(m/k) ; pendule simple T₀ = 2π√(ℓ/g).
• Magnétisme : F = |q|vB ; R = mv/(|q|B) ; Laplace F = IℓB.
• Bobine : u = ri + L di/dt ; τ = L/R ; E = ½Li².

## Chimie : les essentiels
• pH = −log[H₃O⁺] ; Ke = 10⁻¹⁴ ; acide fort pH = −log C ; base forte pH = 14 + log C.
• pH = pKa + log([A⁻]/[AH]) ; demi-équivalence : pH = pKa ; dosage : CaVa = CbVbE.
• Alcool I → aldéhyde → acide ; II → cétone ; III → rien.
• Estérification lente, limitée (67 %), athermique ; saponification totale.
• Liaison peptidique —CO—NH—.

## Conseils
• Fais un schéma avec les forces et le repère.
• Écris la formule littérale avant l'application numérique, puis l'unité.
• Vérifie l'ordre de grandeur et le nombre de chiffres significatifs.""",
questions=[
(2, "Une voiture passe de 0 à 20 m/s en 10 s. Son accélération moyenne est :", "2 m/s²", "200 m/s²", "0,5 m/s²", "10 m/s²",
 "a = Δv/Δt."),
(2, "Le pH d'une solution d'acide fort à 10⁻³ mol/L est :", "3", "11", "−3", "7",
 "pH = −log C."),
(2, "L'oxydation ménagée d'un aldéhyde donne :", "un acide carboxylique", "une cétone", "un alcool", "un ester",
 "Dernière étape de l'oxydation d'un alcool primaire."),
(2, "Si on quadruple la longueur d'un pendule simple, sa période :", "double", "quadruple", "est divisée par 2", "ne change pas",
 "T₀ proportionnelle à √ℓ."),
(3, "Un proton (charge e) entre perpendiculairement dans un champ B uniforme. Si sa vitesse double, le rayon :", "double", "est divisé par 2", "quadruple", "ne change pas",
 "R = mv/(eB)."),
(3, "Pendant le dosage d'un acide faible, à la demi-équivalence on lit pH = 4,2. Le pKa du couple est :", "4,2", "8,4", "2,1", "7",
 "À la demi-équivalence, pH = pKa."),
(3, "Un satellite décrit une orbite circulaire. Son mouvement est :", "circulaire uniforme", "rectiligne uniforme", "circulaire accéléré tangentiellement", "parabolique",
 "La force de gravitation est centripète, perpendiculaire à la vitesse."),
(3, "Un solide de 0,5 kg suspendu à un ressort de raideur 50 N/m oscille. Sa pulsation propre est :", "10 rad/s", "100 rad/s", "25 rad/s", "0,1 rad/s",
 "√(50/0,5) = √100."),
(4, "Pour fabriquer du savon, on réalise :", "la saponification d'un corps gras par une base forte", "l'estérification d'un alcool", "l'oxydation d'un alcool", "un dosage acido-basique",
 "Corps gras (ester) + soude → savon (carboxylate) + glycérol."),
(4, "Dans un circuit RL, la constante de temps est 5 ms et R = 20 Ω. L'inductance est :", "0,1 H", "4 H", "100 H", "0,25 H",
 "L = τR = 0,005 × 20."),
(4, "Un électron (e = 1,6 × 10⁻¹⁹ C) dans un champ de 10⁴ V/m subit une force de :", "1,6 × 10⁻¹⁵ N", "1,6 × 10⁻²³ N", "10⁴ N", "1,6 × 10⁻¹⁹ N",
 "F = eE."),
]),
]
