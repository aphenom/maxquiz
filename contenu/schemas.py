"""Schémas MaxQuiz : chaque fonction dessine un SVG dans game/static/game/schemas/.

Usage : python contenu/schemas.py        (régénère tous les schémas)

Même style partout : fond blanc arrondi, encre sombre, orange et vert MaxQuiz,
police DejaVu Sans (identique dans l'application et dans les fiches PDF).
Dans une fiche : une ligne « [[schema:nom|Légende]] ». Dans une question : 8e élément « nom »."""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "game", "static", "game", "schemas")

ENCRE, ORANGE, VERT, BLEU, BRUN, SABLE, ROUGE, JAUNE, GRIS = (
    "#221A12", "#F2790F", "#0B9A5C", "#2F6FB5", "#6E6152", "#EADFCE", "#D23B2F", "#F5C431", "#9A8F84")
FONT = "DejaVu Sans"


class S:
    """Petit dessinateur SVG (coordonnées en pixels, origine en haut à gauche)."""

    def __init__(self, w, h):
        self.w, self.h, self.el = w, h, []

    # -- primitives
    def line(self, x1, y1, x2, y2, c=ENCRE, w=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
                       f'stroke-width="{w}" stroke-linecap="round"{d}/>')

    def poly(self, pts, c=ENCRE, w=2, fill="none", closed=True, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polygon" if closed else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<{tag} points="{p}" stroke="{c}" stroke-width="{w}" fill="{fill}" '
                       f'stroke-linejoin="round"{d}/>')

    def circle(self, x, y, r, c=ENCRE, w=2, fill="none", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" stroke="{c}" stroke-width="{w}" '
                       f'fill="{fill}"{d}/>')

    def ellipse(self, x, y, rx, ry, c=ENCRE, w=2, fill="none", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" stroke="{c}" '
                       f'stroke-width="{w}" fill="{fill}"{d}/>')

    def rect(self, x, y, w, h, c=ENCRE, sw=2, fill="none", r=0):
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
                       f'stroke="{c}" stroke-width="{sw}" fill="{fill}"/>')

    def path(self, d, c=ENCRE, w=2, fill="none", dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" '
                       f'stroke-linecap="round" stroke-linejoin="round"{da}/>')

    def text(self, x, y, t, size=15, c=ENCRE, anchor="middle", bold=False, italic=False):
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        wgt = ' font-weight="bold"' if bold else ""
        sty = ' font-style="italic"' if italic else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{c}" '
                       f'text-anchor="{anchor}"{wgt}{sty}>{t}</text>')

    # -- composés
    def dot(self, x, y, label="", dx=0, dy=-10, c=ENCRE, size=15):
        self.circle(x, y, 3.5, c=c, w=1, fill=c)
        if label:
            self.text(x + dx, y + dy, label, size=size, bold=True, c=c)

    def arrow(self, x1, y1, x2, y2, c=ENCRE, w=2, head=10, dash=None):
        self.line(x1, y1, x2, y2, c, w, dash)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - head * math.cos(a - 0.4), y2 - head * math.sin(a - 0.4))
        p2 = (x2 - head * math.cos(a + 0.4), y2 - head * math.sin(a + 0.4))
        self.poly([(x2, y2), p1, p2], c=c, w=1, fill=c)

    def arc(self, cx, cy, r, a1, a2, c=ORANGE, w=2.5, fill="none"):
        """Arc de a1 à a2 (degrés, sens trigonométrique, y vers le haut)."""
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
        large = 1 if (a2 - a1) % 360 > 180 else 0
        if fill != "none":
            self.path(f"M{cx:.1f},{cy:.1f} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},0 {x2:.1f},{y2:.1f} Z",
                      c=c, w=w, fill=fill)
        else:
            self.path(f"M{x1:.1f},{y1:.1f} A{r},{r} 0 {large},0 {x2:.1f},{y2:.1f}", c=c, w=w)

    def angle_at(self, p, q1, q2, r=22, c=ORANGE, label="", lsize=14, fill="none"):
        """Arc de l'angle de sommet p entre les directions p→q1 et p→q2 (le plus petit)."""
        a1 = math.degrees(math.atan2(p[1] - q1[1], q1[0] - p[0]))
        a2 = math.degrees(math.atan2(p[1] - q2[1], q2[0] - p[0]))
        if (a2 - a1) % 360 > 180:
            a1, a2 = a2, a1
        self.arc(p[0], p[1], r, a1, a1 + (a2 - a1) % 360, c=c, fill=fill)
        if label:
            m = math.radians(a1 + ((a2 - a1) % 360) / 2)
            self.text(p[0] + (r + 13) * math.cos(m), p[1] - (r + 13) * math.sin(m) + 5, label, size=lsize, c=c,
                      bold=True)

    def right_angle(self, p, q1, q2, s=11, c=ENCRE):
        u = _unit(p, q1)
        v = _unit(p, q2)
        a = (p[0] + u[0] * s, p[1] + u[1] * s)
        b = (p[0] + u[0] * s + v[0] * s, p[1] + u[1] * s + v[1] * s)
        d = (p[0] + v[0] * s, p[1] + v[1] * s)
        self.poly([a, b, d], c=c, w=1.6, closed=False)

    def tick(self, p, q, n=1, c=VERT):
        """Codage de longueurs égales : n petits traits au milieu de [pq]."""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        u = _unit(p, q)
        nx, ny = -u[1], u[0]
        for k in range(n):
            off = (k - (n - 1) / 2) * 5
            cx, cy = mx + u[0] * off, my + u[1] * off
            self.line(cx - nx * 7, cy - ny * 7, cx + nx * 7, cy + ny * 7, c=c, w=2)

    def svg(self):
        body = "\n".join(self.el)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" font-family="{FONT}">\n'
                f'<rect x="1" y="1" width="{self.w - 2}" height="{self.h - 2}" rx="14" fill="#FFFFFF" '
                f'stroke="{SABLE}" stroke-width="2"/>\n{body}\n</svg>\n')


def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def _lerp(p, q, t):
    return p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t


SCHEMAS = {}


def schema(fn):
    SCHEMAS[fn.__name__.replace("_", "-")] = fn
    return fn


# ============================================================ MATHÉMATIQUES
@schema
def thales():
    s = S(420, 280)
    A, B, C = (210, 30), (60, 225), (370, 225)
    M, N = _lerp(A, B, 0.45), _lerp(A, C, 0.45)
    s.poly([A, B, C])
    s.line(*M, *N, c=ORANGE, w=3)
    s.line(*B, *C, c=ORANGE, w=3)
    for p, l, dx, dy in [(A, "A", 0, -10), (B, "B", -12, 18), (C, "C", 12, 18), (M, "M", -16, 0), (N, "N", 16, 0)]:
        s.dot(*p, l, dx, dy)
    s.text(210, 266, "(MN) // (BC)   ⇒   AM/AB = AN/AC = MN/BC", 14, c=VERT, bold=True)
    return s


@schema
def trigonometrie():
    s = S(420, 250)
    A, B, C = (40, 200), (330, 200), (330, 45)
    s.poly([A, B, C])
    s.right_angle(B, A, C)
    s.angle_at(A, B, C, r=38, label="α")
    s.text(200, 225, "côté adjacent à α", 14, c=BLEU, bold=True)
    s.text(350, 120, "côté", 14, c=VERT, bold=True, anchor="start")
    s.text(350, 138, "opposé", 14, c=VERT, bold=True, anchor="start")
    s.text(165, 105, "hypoténuse", 14, c=ORANGE, bold=True)
    s.text(210, 30, "cos α = adj/hyp · sin α = opp/hyp · tan α = opp/adj", 13, c=ENCRE)
    return s


@schema
def vecteurs_chasles():
    s = S(420, 230)
    A, B, C = (60, 180), (230, 50), (370, 170)
    s.arrow(*A, *B, c=ORANGE, w=3)
    s.arrow(*B, *C, c=BLEU, w=3)
    s.arrow(*A, *C, c=VERT, w=3)
    s.dot(*A, "A", -12, 8)
    s.dot(*B, "B", 0, -12)
    s.dot(*C, "C", 14, 6)
    s.text(210, 212, "AB⃗ + BC⃗ = AC⃗  (relation de Chasles)", 15, c=ENCRE, bold=True)
    return s


@schema
def angle_inscrit():
    s = S(360, 280)
    O, r = (180, 145), 105
    s.circle(*O, r)

    def pt(deg):
        return O[0] + r * math.cos(math.radians(deg)), O[1] - r * math.sin(math.radians(deg))
    A, B, M = pt(205), pt(335), pt(95)
    s.poly([A, M, B], c=ORANGE, closed=False, w=2.5)
    s.poly([A, O, B], c=BLEU, closed=False, w=2.5)
    s.angle_at(M, A, B, r=24, c=ORANGE)
    s.angle_at(O, A, B, r=22, c=BLEU)
    s.dot(*A, "A", -12, 14)
    s.dot(*B, "B", 12, 14)
    s.dot(*M, "M", 0, -12)
    s.dot(*O, "O", 0, -12)
    s.text(180, 272, "angle au centre AOB = 2 × angle inscrit AMB", 13, c=ENCRE, bold=True)
    return s


@schema
def pyramide_cone():
    s = S(440, 250)
    # pyramide à base carrée (perspective cavalière)
    a, b, c, d = (40, 200), (160, 200), (200, 165), (80, 165)
    S_ = (120, 40)
    H = (120, 182)
    s.poly([a, b, c], closed=False)
    s.poly([c, d, a], closed=False, dash="5,5")
    for p in (a, b, c):
        s.line(*S_, *p)
    s.line(*S_, *d, dash="5,5")
    s.line(*S_, *H, c=ORANGE, dash="4,4")
    s.text(132, 120, "h", 15, c=ORANGE, bold=True, anchor="start")
    s.text(120, 232, "Pyramide : V = (B × h) ÷ 3", 13, c=VERT, bold=True)
    # cône
    cx, cy = 330, 190
    s.ellipse(cx, cy, 70, 18)
    s.line(cx - 70, cy, cx, 45)
    s.line(cx + 70, cy, cx, 45)
    s.line(cx, 45, cx, cy, c=ORANGE, dash="4,4")
    s.line(cx, cy, cx + 70, cy, c=BLEU)
    s.text(cx + 8, 125, "h", 15, c=ORANGE, bold=True, anchor="start")
    s.text(cx + 35, cy - 6, "r", 15, c=BLEU, bold=True)
    s.text(cx, 232, "Cône : V = (π r² × h) ÷ 3", 13, c=VERT, bold=True)
    return s


def _repere(s, ox, oy, u, xmin, xmax, ymin, ymax, grid=True):
    if grid:
        for i in range(xmin, xmax + 1):
            s.line(ox + i * u, oy - ymin * u, ox + i * u, oy - ymax * u, c=SABLE, w=1)
        for j in range(ymin, ymax + 1):
            s.line(ox + xmin * u, oy - j * u, ox + xmax * u, oy - j * u, c=SABLE, w=1)
    s.arrow(ox + xmin * u - 8, oy, ox + xmax * u + 14, oy, w=1.6, head=8)
    s.arrow(ox, oy - ymin * u + 8, ox, oy - ymax * u - 14, w=1.6, head=8)
    s.text(ox - 9, oy + 16, "O", 12, c=BRUN)
    s.text(ox + u, oy + 16, "1", 11, c=BRUN)
    s.text(ox - 10, oy - u + 4, "1", 11, c=BRUN)


@schema
def droite_repere():
    s = S(360, 290)
    ox, oy, u = 150, 150, 34
    _repere(s, ox, oy, u, -3, 5, -3, 3)
    f = lambda x: 2 * x - 1  # noqa: E731
    x1, x2 = -0.9, 1.95
    s.line(ox + x1 * u, oy - f(x1) * u, ox + x2 * u, oy - f(x2) * u, c=ORANGE, w=3)
    s.dot(ox, oy + u, "", c=VERT)
    s.text(ox + 10, oy + u + 5, "(0 ; −1)", 12, c=VERT, anchor="start", bold=True)
    s.dot(ox + u, oy - u, "", c=VERT)
    s.text(ox + u + 10, oy - u + 5, "(1 ; 1)", 12, c=VERT, anchor="start", bold=True)
    s.text(ox + 2.0 * u + 4, oy - 2.6 * u, "y = 2x − 1", 15, c=ORANGE, anchor="start", bold=True)
    return s


@schema
def angles_paralleles():
    s = S(420, 260)
    s.line(30, 80, 390, 80, w=2.5)
    s.line(30, 190, 390, 190, w=2.5)
    s.text(398, 84, "d", 15, anchor="start", bold=True)
    s.text(398, 194, "d′", 15, anchor="start", bold=True)
    P, Q = (250, 80), (165, 190)
    t1, t2 = _lerp(Q, P, 1.4), _lerp(P, Q, 1.3)
    s.line(*t2, *t1, c=BLEU, w=2.5)
    s.angle_at(P, (30, 80), Q, r=26, c=ORANGE, label="a", fill="#FDE3CC")
    s.angle_at(Q, (390, 190), P, r=26, c=ORANGE, label="b", fill="#FDE3CC")
    s.text(210, 244, "a et b alternes-internes : égaux si d // d′", 14, c=ENCRE, bold=True)
    return s


@schema
def bissectrice():
    s = S(400, 260)
    O = (50, 210)
    A, B = (370, 210), (290, 30)
    s.line(*O, *A)
    s.line(*O, *B)
    a1 = math.degrees(math.atan2(O[1] - B[1], B[0] - O[0]))
    m = math.radians(a1 / 2)
    D = (O[0] + 330 * math.cos(m), O[1] - 330 * math.sin(m))
    s.line(*O, *D, c=ORANGE, w=2.5, dash="7,5")
    s.text(D[0] - 6, D[1] - 8, "bissectrice", 13, c=ORANGE, bold=True, anchor="end")
    M = (O[0] + 210 * math.cos(m), O[1] - 210 * math.sin(m))
    H1 = (M[0], O[1])
    u = _unit(O, B)
    t = (M[0] - O[0]) * u[0] + (M[1] - O[1]) * u[1]
    H2 = (O[0] + u[0] * t, O[1] + u[1] * t)
    s.line(*M, *H1, c=BLEU, dash="4,4")
    s.line(*M, *H2, c=BLEU, dash="4,4")
    s.right_angle(H1, O, M, c=BLEU)
    s.right_angle(H2, O, M, c=BLEU)
    s.tick(M, H1, 1)
    s.tick(M, H2, 1)
    s.dot(*M, "M", 14, 4)
    s.angle_at(O, A, D, r=40, c=VERT)
    s.angle_at(O, D, B, r=46, c=VERT)
    s.dot(*O, "O", -10, 10)
    s.text(200, 248, "Un point de la bissectrice est à égale distance des deux côtés", 12, c=ENCRE)
    return s


@schema
def pythagore():
    s = S(380, 260)
    A, B, C = (70, 200), (300, 200), (70, 50)
    s.poly([A, B, C], w=2.5)
    s.right_angle(A, B, C)
    s.text(185, 222, "b", 17, c=BLEU, bold=True)
    s.text(50, 130, "a", 17, c=BLEU, bold=True)
    s.text(200, 115, "c (hypoténuse)", 15, c=ORANGE, bold=True, anchor="start")
    s.text(190, 250, "c² = a² + b²", 17, c=VERT, bold=True)
    return s


@schema
def cercle_triangle_rectangle():
    s = S(340, 280)
    O, r = (170, 140), 105
    s.circle(*O, r)
    A, B = (O[0] - r, O[1]), (O[0] + r, O[1])
    C = (O[0] + r * math.cos(math.radians(60)), O[1] - r * math.sin(math.radians(60)))
    s.poly([A, B, C], c=ORANGE, w=2.5)
    s.right_angle(C, A, B)
    s.dot(*O, "O", 0, 20)
    s.dot(*A, "A", -12, 6)
    s.dot(*B, "B", 14, 6)
    s.dot(*C, "C", 6, -10)
    s.tick(A, O, 2)
    s.tick(O, B, 2)
    s.text(170, 270, "[AB] diamètre ⇔ ABC rectangle en C", 14, c=VERT, bold=True)
    return s


@schema
def perspective_cube():
    s = S(320, 260)
    a = 130
    x0, y0 = 60, 210
    k = a * 0.5 * math.cos(math.radians(45))
    A, B, C, D = (x0, y0), (x0 + a, y0), (x0 + a, y0 - a), (x0, y0 - a)
    E, F, G, H = [(p[0] + k, p[1] - k) for p in (A, B, C, D)]
    s.poly([A, B, C, D], w=2.5)
    s.line(*B, *F)
    s.line(*C, *G)
    s.line(*D, *H)
    s.line(*F, *G)
    s.line(*G, *H)
    s.line(*A, *E, dash="6,5", c=BRUN)
    s.line(*E, *F, dash="6,5", c=BRUN)
    s.line(*E, *H, dash="6,5", c=BRUN)
    s.angle_at(B, (B[0] + 40, B[1]), F, r=26, c=ORANGE, label="45°", lsize=12)
    s.text(160, 246, "Arêtes cachées en pointillés", 12, c=ENCRE)
    return s


@schema
def symetrie_centrale():
    s = S(420, 260)
    O = (210, 130)
    pts = {"A": (90, 70), "B": (60, 160), "C": (140, 190)}
    sym = {k + "′": (2 * O[0] - p[0], 2 * O[1] - p[1]) for k, p in pts.items()}
    s.poly(list(pts.values()), c=BLEU, fill="#DCE8F6")
    s.poly(list(sym.values()), c=ORANGE, fill="#FDE3CC")
    for k, p in pts.items():
        q = sym[k + "′"]
        s.line(*p, *q, c=GRIS, w=1.2, dash="4,4")
        u = _unit(O, q)
        s.dot(*p, k, -u[0] * 16, -u[1] * 16 + 5, c=BLEU)
        s.dot(*q, k + "′", u[0] * 18, u[1] * 18 + 5, c=ORANGE)
    s.dot(*O, "O", 0, -12)
    s.text(210, 248, "O est le milieu de [AA′], [BB′] et [CC′]", 14, c=ENCRE, bold=True)
    return s


@schema
def angles_opposes():
    s = S(420, 240)
    O = (210, 110)
    p1, p2 = (70, 40), (350, 180)
    q1, q2 = (70, 180), (350, 40)
    s.line(*p1, *p2, w=2.5)
    s.line(*q1, *q2, w=2.5)
    s.angle_at(O, p2, q2, r=34, c=ORANGE, label="53°", fill="#FDE3CC")
    s.angle_at(O, p1, q1, r=34, c=ORANGE, label="53°", fill="#FDE3CC")
    s.angle_at(O, q2, p1, r=24, c=BLEU, label="127°", lsize=12)
    s.text(210, 226, "Angles opposés par le sommet : même mesure", 14, c=ENCRE, bold=True)
    return s


@schema
def parallelogramme():
    s = S(420, 250)
    A, B, C, D = (60, 190), (290, 190), (360, 60), (130, 60)
    O = _lerp(A, C, 0.5)
    s.poly([A, B, C, D], w=2.5)
    s.line(*A, *C, c=ORANGE, dash="6,4")
    s.line(*B, *D, c=ORANGE, dash="6,4")
    s.tick(A, O, 1, c=ORANGE)
    s.tick(O, C, 1, c=ORANGE)
    s.tick(B, O, 2, c=BLEU)
    s.tick(O, D, 2, c=BLEU)
    s.tick(A, B, 1)
    s.tick(D, C, 1)
    s.tick(A, D, 3)
    s.tick(B, C, 3)
    for p, l, dx, dy in [(A, "A", -12, 12), (B, "B", 12, 12), (C, "C", 12, -6), (D, "D", -12, -6)]:
        s.dot(*p, l, dx, dy)
    s.dot(*O, "O", 0, 22)
    s.text(210, 236, "Diagonales qui se coupent en leur milieu O", 14, c=ENCRE, bold=True)
    return s


@schema
def triangle_hauteur():
    s = S(400, 250)
    A, B, C = (150, 40), (40, 200), (360, 200)
    H = (A[0], B[1])
    s.poly([A, B, C], w=2.5)
    s.line(*A, *H, c=ORANGE, w=2.5, dash="6,4")
    s.right_angle(H, C, A, c=ORANGE)
    s.dot(*A, "A", 0, -10)
    s.dot(*B, "B", -12, 14)
    s.dot(*C, "C", 12, 14)
    s.dot(*H, "H", 0, 18, c=ORANGE)
    s.text(162, 130, "hauteur", 13, c=ORANGE, bold=True, anchor="start")
    s.text(200, 240, "Aire = (base × hauteur) ÷ 2 = (BC × AH) ÷ 2", 13, c=VERT, bold=True)
    return s


@schema
def repere_points():
    s = S(360, 290)
    ox, oy, u = 140, 140, 32
    _repere(s, ox, oy, u, -4, 6, -3, 3)
    for (x, y), l, c in [((3, -2), "A(3 ; −2)", ORANGE), ((4, 0), "B(4 ; 0)", VERT), ((0, -1), "C(0 ; −1)", BLEU),
                         ((-2, 2), "D(−2 ; 2)", ROUGE)]:
        px, py = ox + x * u, oy - y * u
        s.dot(px, py, "", c=c)
        if x == 0:
            s.text(px - 8, py + 5, l, 12, c=c, anchor="end", bold=True)
        else:
            s.text(px + 8, py - 8, l, 12, c=c, anchor="start", bold=True)
    s.line(ox + 3 * u, oy, ox + 3 * u, oy + 2 * u, c=ORANGE, w=1.2, dash="3,3")
    s.line(ox, oy + 2 * u, ox + 3 * u, oy + 2 * u, c=ORANGE, w=1.2, dash="3,3")
    s.text(ox + 6 * u + 6, oy + 18, "abscisses", 11, c=BRUN, anchor="end")
    s.text(ox + 8, oy - 3 * u - 4, "ordonnées", 11, c=BRUN, anchor="start")
    return s


@schema
def prisme_cylindre():
    s = S(440, 250)
    # prisme droit à base triangulaire
    a, b, c = (40, 200), (150, 200), (80, 160)
    h = 120
    a2, b2, c2 = [(p[0], p[1] - h) for p in (a, b, c)]
    s.poly([a, b, b2, a2])
    s.poly([a2, b2, c2], fill="#FDE3CC", c=ORANGE)
    s.line(*b, *c, dash="5,4", c=BRUN)
    s.line(*a, *c, dash="5,4", c=BRUN)
    s.line(*c, *c2, dash="5,4", c=BRUN)
    s.line(*b2, *c2, c=ORANGE)
    s.text(100, 236, "Prisme droit", 14, c=VERT, bold=True)
    # cylindre
    cx, top, bot, r = 320, 60, 190, 60
    s.ellipse(cx, top, r, 16, c=ORANGE, fill="#FDE3CC")
    s.line(cx - r, top, cx - r, bot)
    s.line(cx + r, top, cx + r, bot)
    s.path(f"M{cx - r},{bot} A{r},16 0 0,0 {cx + r},{bot}")
    s.path(f"M{cx - r},{bot} A{r},16 0 0,1 {cx + r},{bot}", dash="5,4", c=BRUN)
    s.line(cx, bot, cx + r, bot, c=BLEU)
    s.text(cx + 30, bot - 6, "r", 14, c=BLEU, bold=True)
    s.text(cx, 236, "Cylindre", 14, c=VERT, bold=True)
    s.text(220, 24, "V = aire de la base × hauteur", 14, c=ENCRE, bold=True)
    return s


@schema
def diagramme_circulaire():
    s = S(460, 250)
    cx, cy, r = 120, 120, 95
    parts = [(30, "Football", ORANGE), (45, "Basket", VERT), (25, "Handball", BLEU)]
    a = 90
    for pct, lab, col in parts:
        span = pct * 3.6
        s.arc(cx, cy, r, a - span, a, c="#FFFFFF", w=2, fill=col)
        a -= span
    y = 85
    for pct, lab, col in parts:
        s.rect(250, y - 12, 16, 16, c=col, fill=col, r=3)
        s.text(274, y + 1, f"{lab} : {pct} % → {pct * 3.6:.0f}°", 13, anchor="start")
        y += 30
    s.text(230, 238, "angle = fréquence × 360°", 14, c=ENCRE, bold=True)
    return s


@schema
def courbes_ln_exp():
    s = S(360, 340)
    ox, oy, u = 120, 190, 40
    _repere(s, ox, oy, u, -2, 5, -3, 2, grid=True)
    pts_e = [(x / 10, math.exp(x / 10)) for x in range(-20, 10)]
    pts_l = [(x / 100, math.log(x / 100)) for x in range(6, 500, 4)]
    s.poly([(ox + x * u, oy - y * u) for x, y in pts_e if y < 2.6], c=ORANGE, w=3, closed=False)
    s.poly([(ox + x * u, oy - y * u) for x, y in pts_l if y > -3], c=BLEU, w=3, closed=False)
    s.line(ox - 2 * u, oy + 2 * u, ox + 2.5 * u, oy - 2.5 * u, c=GRIS, w=1.2, dash="5,4")
    s.text(ox + 0.95 * u, oy - 2.4 * u, "exp", 15, c=ORANGE, bold=True, anchor="start")
    s.text(ox + 4.2 * u, oy - 1.75 * u, "ln", 15, c=BLEU, bold=True)
    s.text(ox + 2.6 * u, oy - 2.55 * u, "y = x", 11, c=GRIS, anchor="start")
    s.dot(ox, oy - u, "", c=ORANGE)
    s.dot(ox + u, oy, "", c=BLEU)
    s.text(180, 330, "Courbes symétriques par rapport à y = x", 13, c=ENCRE, bold=True)
    return s


# ============================================================ PHYSIQUE-CHIMIE
def _pile(s, x, y, vertical=False):
    """Symbole de pile centré en (x, y) : grand trait fin (+), petit trait épais (−)."""
    if vertical:
        s.line(x - 16, y - 4, x + 16, y - 4, w=2)
        s.line(x - 8, y + 4, x + 8, y + 4, w=5)
        s.text(x + 24, y - 2, "+", 14, c=ROUGE, bold=True)
    else:
        s.line(x - 4, y - 16, x - 4, y + 16, w=2)
        s.line(x + 4, y - 8, x + 4, y + 8, w=5)
        s.text(x - 12, y - 18, "+", 14, c=ROUGE, bold=True)


def _lampe(s, x, y, r=13):
    s.circle(x, y, r, w=2, fill="#FFFFFF")
    d = r * 0.7
    s.line(x - d, y - d, x + d, y + d, w=2)
    s.line(x - d, y + d, x + d, y - d, w=2)


def _appareil(s, x, y, lettre, c=BLEU, r=14):
    s.circle(x, y, r, c=c, w=2, fill="#FFFFFF")
    s.text(x, y + 5, lettre, 14, c=c, bold=True)


def _interrupteur(s, x1, x2, y, ferme=True):
    s.dot(x1, y, "", size=1)
    s.dot(x2, y, "", size=1)
    if ferme:
        s.line(x1, y, x2, y, w=2)
    else:
        s.line(x1, y, x2 - 4, y - 16, w=2)


@schema
def circuit_serie():
    s = S(380, 240)
    L, R, T, B = 50, 330, 50, 190
    s.line(L, T, R, T)
    s.line(R, T, R, B)
    s.line(L, B, L, T)
    s.line(L, B, 150, B)
    s.line(200, B, R, B)
    _pile(s, L, 120, vertical=True)
    s.rect(L - 18, 110, 36, 20, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _pile(s, L, 120, vertical=True)
    _interrupteur(s, 150, 200, B, ferme=True)
    s.rect(127, T - 15, 30, 30, c="#FFFFFF", sw=0, fill="#FFFFFF")
    s.rect(227, T - 15, 30, 30, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _lampe(s, 142, T)
    _lampe(s, 242, T)
    s.text(142, T - 22, "L1", 13, bold=True)
    s.text(242, T - 22, "L2", 13, bold=True)
    s.text(175, B + 20, "interrupteur fermé", 12, c=BRUN)
    s.arrow(R, 95, R, 140, c=ORANGE, w=2.5)
    s.text(R + 10, 122, "I", 15, c=ORANGE, bold=True, anchor="start")
    s.text(190, 228, "Série : une seule boucle, même intensité partout", 13, c=VERT, bold=True)
    return s


@schema
def circuit_derivation():
    s = S(400, 260)
    L, M, R, T, B = 50, 200, 330, 50, 200
    s.line(L, T, R, T)
    s.line(L, B, R, B)
    s.line(L, T, L, B)
    s.line(M, T, M, B)
    s.line(R, T, R, B)
    s.rect(L - 18, 115, 36, 20, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _pile(s, L, 125, vertical=True)
    s.rect(M - 15, 110, 30, 30, c="#FFFFFF", sw=0, fill="#FFFFFF")
    s.rect(R - 15, 110, 30, 30, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _lampe(s, M, 125)
    _lampe(s, R, 125)
    s.text(M + 22, 130, "L1", 13, bold=True, anchor="start")
    s.text(R + 22, 130, "L2", 13, bold=True, anchor="start")
    s.dot(M, T, "N", 0, -10, c=ORANGE)
    s.dot(M, B, "N′", 0, 22, c=ORANGE)
    s.text(200, 246, "Dérivation : deux boucles, I = I1 + I2 (loi des nœuds)", 13, c=VERT, bold=True)
    return s


@schema
def symboles_electriques():
    s = S(440, 260)
    cells = [(70, 70), (180, 70), (290, 70), (390, 70), (70, 170), (180, 170), (290, 170), (390, 170)]
    noms = ["Pile", "Lampe", "Interrupteur|ouvert", "Interrupteur|fermé", "Moteur", "Diode", "Ampèremètre",
            "Voltmètre"]
    for (x, y), nom in zip(cells, noms):
        s.line(x - 40, y, x - 18, y)
        s.line(x + 18, y, x + 40, y)
        for k, morceau in enumerate(nom.split("|")):
            s.text(x, y + 38 + k * 14, morceau, 11.5, c=BRUN)
    x, y = cells[0]
    s.line(x - 18, y, x - 4, y)
    s.line(x + 4, y, x + 18, y)
    _pile(s, x, y)
    x, y = cells[1]
    s.line(x - 18, y, x - 13, y)
    s.line(x + 13, y, x + 18, y)
    _lampe(s, x, y)
    x, y = cells[2]
    s.dot(x - 18, y)
    s.dot(x + 18, y)
    s.line(x - 18, y, x + 14, y - 16)
    x, y = cells[3]
    s.dot(x - 18, y)
    s.dot(x + 18, y)
    s.line(x - 18, y, x + 18, y)
    x, y = cells[4]
    _appareil(s, x, y, "M", c=ENCRE, r=16)
    x, y = cells[5]
    s.line(x - 18, y, x - 10, y)
    s.poly([(x - 10, y - 12), (x - 10, y + 12), (x + 10, y)], fill=ENCRE)
    s.line(x + 10, y - 12, x + 10, y + 12, w=3)
    s.line(x + 10, y, x + 18, y)
    x, y = cells[6]
    _appareil(s, x, y, "A", r=16)
    x, y = cells[7]
    _appareil(s, x, y, "V", c=VERT, r=16)
    return s


@schema
def amperemetre_voltmetre():
    s = S(400, 270)
    L, R, T, B = 50, 330, 60, 200
    s.line(L, T, R, T)
    s.line(R, T, R, B)
    s.line(R, B, L, B)
    s.line(L, B, L, T)
    s.rect(L - 18, 120, 36, 20, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _pile(s, L, 130, vertical=True)
    s.rect(110, T - 16, 32, 32, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _appareil(s, 126, T, "A")
    s.rect(R - 15, 115, 30, 30, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _lampe(s, R, 130)
    s.line(R, 100, 260, 100, c=VERT)
    s.line(R, 160, 260, 160, c=VERT)
    s.line(260, 100, 260, 160, c=VERT)
    s.rect(244, 114, 32, 32, c="#FFFFFF", sw=0, fill="#FFFFFF")
    _appareil(s, 260, 130, "V", c=VERT)
    s.text(126, T - 24, "en série", 13, c=BLEU, bold=True)
    s.text(260, 182, "en dérivation", 12, c=VERT, bold=True)
    s.text(200, 236, "Ampèremètre en série", 13, c=BLEU, bold=True)
    s.text(200, 254, "Voltmètre aux bornes du dipôle", 13, c=VERT, bold=True)
    return s


@schema
def loi_ohm():
    s = S(380, 280)
    ox, oy = 60, 220
    s.arrow(ox, oy, 350, oy, w=1.8)
    s.arrow(ox, oy, ox, 30, w=1.8)
    for i in range(1, 6):
        s.line(ox + i * 50, oy - 4, ox + i * 50, oy + 4)
        s.text(ox + i * 50, oy + 18, f"{i * 0.1:.1f}".replace(".", ","), 11, c=BRUN)
        s.line(ox - 4, oy - i * 34, ox + 4, oy - i * 34)
        s.text(ox - 10, oy - i * 34 + 4, str(i * 2), 11, c=BRUN, anchor="end")
    s.line(ox, oy, ox + 250, oy - 170, c=ORANGE, w=3)
    for i in range(1, 6):
        s.dot(ox + i * 50, oy - i * 34, "", c=ORANGE)
    s.text(350, oy - 8, "I (A)", 12, anchor="end", bold=True)
    s.text(ox + 8, 40, "U (V)", 12, anchor="start", bold=True)
    s.text(140, 70, "U = R × I", 16, c=VERT, bold=True)
    s.text(140, 90, "ici R = 20 Ω", 12, c=BRUN)
    return s


@schema
def tension_alternative():
    s = S(420, 260)
    ox, oy, A = 40, 130, 80
    s.arrow(ox, oy, 400, oy, w=1.6, head=8)
    s.arrow(ox, 225, ox, 25, w=1.6, head=8)
    per = 150
    pts = [(ox + t, oy - A * math.sin(2 * math.pi * t / per)) for t in range(0, 341, 4)]
    s.poly(pts, c=ORANGE, w=3, closed=False)
    s.line(ox, oy - A, ox + per / 4, oy - A, c=BLEU, w=1.2, dash="4,4")
    s.text(ox + 6, oy - A - 6, "Umax", 12, c=BLEU, bold=True, anchor="start")
    s.line(ox, oy + A + 22, ox + per, oy + A + 22, c=VERT, w=1.5)
    s.line(ox, oy + A + 16, ox, oy + A + 28, c=VERT)
    s.line(ox + per, oy + A + 16, ox + per, oy + A + 28, c=VERT)
    s.text(ox + per / 2, oy + A + 40, "période T", 12, c=VERT, bold=True)
    s.text(398, oy + 18, "temps", 11, c=BRUN, anchor="end")
    s.text(ox + 70, 34, "tension", 11, c=BRUN, anchor="start")
    s.text(300, 245, "f = 1 / T", 15, c=ENCRE, bold=True)
    return s


@schema
def ombres():
    s = S(440, 240)
    src = (50, 110)
    s.circle(*src, 14, c=JAUNE, fill=JAUNE)
    s.text(50, 150, "source", 12, c=BRUN)
    bx, by, r = 190, 110, 32
    top, bot = (bx, by - r), (bx, by + r)
    ex = 400
    k1 = (ex, src[1] + (top[1] - src[1]) * (ex - src[0]) / (bx - src[0]))
    k2 = (ex, src[1] + (bot[1] - src[1]) * (ex - src[0]) / (bx - src[0]))
    s.poly([top, k1, k2, bot], c="none", w=0, fill="#E9E4DD")
    s.line(*src, *k1, c=JAUNE, w=1.5)
    s.line(*src, *k2, c=JAUNE, w=1.5)
    s.arc(bx, by, r, 270, 90 + 360, c=ENCRE, w=2, fill="#FFFFFF")
    s.arc(bx, by, r, 90, 270, c=ENCRE, w=2, fill="#FFFFFF")
    s.arc(bx, by, r, 270, 450, c=ENCRE, w=2, fill="#6E6152")
    s.line(ex, 20, ex, 210, w=4, c=BRUN)
    s.line(ex, k1[1], ex, k2[1], w=6, c=ENCRE)
    s.text(bx, by + r + 22, "objet opaque", 12, c=BRUN)
    s.text(bx + 48, by - r - 6, "ombre propre", 11, c=ENCRE, anchor="start")
    s.text(300, 118, "cône d'ombre", 12, c=BRUN)
    s.text(ex - 6, 225, "ombre portée sur l'écran", 11, c=ENCRE, anchor="end")
    return s


@schema
def eclipses():
    s = S(440, 250)
    for row, (titre, ordre) in enumerate([("Éclipse de Soleil (nouvelle lune)", ("Soleil", "Lune", "Terre")),
                                         ("Éclipse de Lune (pleine lune)", ("Soleil", "Terre", "Lune"))]):
        y = 70 + row * 115
        s.text(220, y - 40, titre, 13, c=VERT, bold=True)
        xs = {"Soleil": 50, ordre[1]: 230, ordre[2]: 370}
        s.circle(50, y, 30, c=ORANGE, fill=JAUNE)
        for nom in ordre[1:]:
            rr = 20 if nom == "Terre" else 9
            fill = BLEU if nom == "Terre" else GRIS
            s.circle(xs[nom], y, rr, c=ENCRE, w=1.2, fill=fill)
            s.text(xs[nom], y + rr + 16, nom, 12, c=BRUN)
        s.text(50, y + 46, "Soleil", 12, c=BRUN)
        mid = xs[ordre[1]]
        rr = 20 if ordre[1] == "Terre" else 9
        s.poly([(mid, y - rr), (mid + 120, y - 3), (mid + 120, y + 3), (mid, y + rr)], c="none", w=0,
               fill="#55504A")
    return s


@schema
def lentille_rayons():
    s = S(460, 260)
    ox, oy, f = 230, 130, 80
    s.line(20, oy, 440, oy, c=BRUN, w=1.2)
    s.path(f"M{ox},{oy - 95} Q{ox + 18},{oy} {ox},{oy + 95} Q{ox - 18},{oy} {ox},{oy - 95}", c=BLEU, w=2,
           fill="#DCE8F6")
    s.dot(ox - f, oy, "F", 0, 20, c=VERT)
    s.dot(ox + f, oy, "F′", 0, 20, c=VERT)
    s.dot(ox, oy, "O", 10, 20)
    xa, ha = ox - 2.2 * f, 50
    xi = ox + f * 2.2 / 1.2
    hi = ha * (xi - ox) / (ox - xa)
    s.arrow(xa, oy, xa, oy - ha, c=ORANGE, w=3)
    s.text(xa, oy + 18, "objet", 11, c=ORANGE)
    s.arrow(xi, oy, xi, oy + hi, c=ROUGE, w=3)
    s.text(xi, oy - 10, "image", 11, c=ROUGE)
    B = (xa, oy - ha)
    s.line(*B, ox, oy - ha, c=ENCRE, w=1.4)
    s.line(ox, oy - ha, xi, oy + hi, c=ENCRE, w=1.4)
    s.line(*B, xi, oy + hi, c=ORANGE, w=1.4)
    yF = oy + ha * (0 - f) / (ox - f - xa) * 0 + ha * f / (ox - f - xa)
    s.line(*B, ox, yF, c=VERT, w=1.4)
    s.line(ox, yF, xi, yF, c=VERT, w=1.4)
    s.text(230, 248, "Lentille convergente : image réelle et renversée", 13, c=ENCRE, bold=True)
    return s


@schema
def etats_matiere():
    import random
    rnd = random.Random(7)
    s = S(450, 220)
    titres = ["Solide", "Liquide", "Gaz"]
    for i, t in enumerate(titres):
        x0 = 20 + i * 145
        s.rect(x0, 40, 120, 120, c=BRUN, sw=2, r=6)
        s.text(x0 + 60, 28, t, 14, c=VERT, bold=True)
        if i == 0:
            for a in range(5):
                for b in range(5):
                    s.circle(x0 + 20 + a * 20, 60 + b * 20, 8, c=BLEU, w=1, fill="#9CC0EA")
        elif i == 1:
            for a in range(5):
                for b in range(3):
                    x = x0 + 18 + a * 21 + rnd.uniform(-3, 3) + (b % 2) * 6
                    y = 108 + b * 19 + rnd.uniform(-3, 3)
                    s.circle(x, y, 8, c=BLEU, w=1, fill="#9CC0EA")
        else:
            for x_, y_ in [(25, 25), (85, 20), (55, 60), (20, 95), (95, 85), (60, 105), (35, 60)]:
                x = x0 + x_ + rnd.uniform(-4, 4)
                y = 40 + y_ + rnd.uniform(-4, 4)
                s.circle(x, y, 8, c=BLEU, w=1, fill="#9CC0EA")
                s.arrow(x + 9, y, x + 24, y - 8 + rnd.random() * 16, c=GRIS, w=1, head=5)
    legendes = ["serrées, ordonnées", "serrées, en désordre", "éloignées, rapides"]
    for i, l in enumerate(legendes):
        s.text(80 + i * 145, 184, l, 12, c=BRUN)
    s.text(225, 208, "Modèle des particules", 12, c=ENCRE, bold=True)
    return s


@schema
def changements_etat():
    s = S(440, 280)
    P = {"SOLIDE": (90, 220), "LIQUIDE": (350, 220), "GAZ": (220, 50)}
    for nom, (x, y) in P.items():
        s.rect(x - 52, y - 18, 104, 36, c=VERT, sw=2, fill="#E2F4EB", r=10)
        s.text(x, y + 5, nom, 14, c=VERT, bold=True)
    s.arrow(145, 212, 295, 212, c=ROUGE, w=2.5)
    s.text(220, 204, "fusion", 13, c=ROUGE, bold=True)
    s.arrow(295, 232, 145, 232, c=BLEU, w=2.5)
    s.text(220, 252, "solidification", 13, c=BLEU, bold=True)
    s.arrow(342, 198, 258, 72, c=ROUGE, w=2.5)
    s.text(320, 130, "vaporisation", 13, c=ROUGE, bold=True, anchor="start")
    s.arrow(240, 74, 322, 198, c=BLEU, w=2.5)
    s.text(262, 160, "liquéfaction", 12, c=BLEU, bold=True, anchor="start")
    s.arrow(98, 198, 184, 72, c=ROUGE, w=2, dash="6,4")
    s.text(118, 118, "sublimation", 12, c=ROUGE, anchor="end")
    s.text(220, 274, "rouge : on chauffe · bleu : on refroidit", 12, c=BRUN)
    return s


@schema
def filtration():
    s = S(300, 290)
    s.poly([(80, 40), (220, 40), (160, 130), (160, 170), (140, 170), (140, 130)], c=ENCRE, w=2, fill="#FFFFFF")
    s.poly([(92, 46), (208, 46), (150, 125)], c=BRUN, w=1.5, fill="#F3EBDD")
    s.poly([(110, 62), (190, 62), (150, 112)], c="none", w=0, fill="#B58A5A")
    s.text(225, 70, "papier filtre", 12, c=BRUN, anchor="start")
    s.text(225, 86, "+ résidu", 12, c=BRUN, anchor="start")
    s.path("M95,200 L95,270 L205,270 L205,200", c=ENCRE, w=2)
    s.rect(97, 235, 106, 33, c="none", sw=0, fill="#BFDDF5")
    for y in (180, 196, 212):
        s.circle(150, y, 3, c=BLEU, w=0, fill=BLEU)
    s.text(150, 255, "filtrat", 13, c=BLEU, bold=True)
    s.text(150, 25, "Filtration", 14, c=VERT, bold=True)
    return s


@schema
def distillation():
    s = S(460, 290)
    s.circle(90, 160, 42, fill="#FFFFFF")
    s.path("M52,178 A42,42 0 0,0 128,178 Z", c="none", w=0, fill="#BFDDF5")
    s.line(90, 118, 90, 80)
    s.line(90, 80, 300, 150, w=10, c="#DCE8F6")
    s.line(90, 80, 300, 150, w=2)
    s.text(250, 100, "réfrigérant (eau froide)", 12, c=BLEU, bold=True, anchor="start")
    s.arrow(250, 150, 270, 128, c=BLEU, w=1.5, head=6)
    s.path("M300,150 L310,170")
    s.path("M285,190 L285,250 L345,250 L345,190")
    s.rect(287, 225, 56, 23, c="none", sw=0, fill="#BFDDF5")
    s.text(315, 274, "distillat", 12, c=BLEU, bold=True)
    for k in range(3):
        s.path(f"M{70 + k * 20},230 q5,-12 0,-22 q-5,-10 0,-20", c=ORANGE, w=2.5)
    s.text(90, 252, "chauffage", 12, c=ORANGE, bold=True)
    s.text(90, 138, "mélange", 11, c=BRUN)
    s.text(360, 40, "La vapeur se liquéfie", 12, c=ENCRE, anchor="middle")
    s.text(360, 56, "dans le réfrigérant", 12, c=ENCRE, anchor="middle")
    return s


@schema
def ampoule_decanter():
    s = S(300, 300)
    s.path("M150,30 C90,60 80,150 120,200 L140,225 L160,225 L180,200 C220,150 210,60 150,30 Z", fill="#FFFFFF")
    s.path("M96,95 C92,120 95,150 110,175 L190,175 C205,150 208,120 204,95 Z", c="none", w=0, fill="#F6D776")
    s.path("M110,175 L120,200 L140,225 L160,225 L180,200 L190,175 Z", c="none", w=0, fill="#BFDDF5")
    s.path("M150,30 C90,60 80,150 120,200 L140,225 L160,225 L180,200 C220,150 210,60 150,30 Z")
    s.line(150, 225, 150, 270, w=3)
    s.rect(138, 240, 24, 10, c=ENCRE, sw=1.5, fill=ORANGE, r=2)
    s.text(230, 130, "huile", 13, c="#A67C00", bold=True, anchor="start")
    s.text(230, 198, "eau", 13, c=BLEU, bold=True, anchor="start")
    s.text(175, 250, "robinet", 12, c=BRUN, anchor="start")
    s.text(150, 292, "Le liquide le plus dense est en bas", 12, c=ENCRE)
    return s


@schema
def triangle_feu():
    s = S(380, 280)
    A, B, C = (190, 40), (85, 220), (295, 220)
    s.poly([A, B, C], c=ORANGE, w=4, fill="#FFF3E6")
    s.text(190, 30, "CHALEUR", 14, c=ROUGE, bold=True)
    s.text(85, 248, "COMBUSTIBLE", 13, c=BRUN, bold=True)
    s.text(295, 248, "COMBURANT", 13, c=BLEU, bold=True)
    s.text(295, 265, "(dioxygène)", 11, c=BLEU)
    s.text(85, 265, "(bois, gaz…)", 11, c=BRUN)
    s.path("M190,185 c-30,-20 -10,-60 0,-80 c5,25 30,30 20,60 c10,-5 12,-15 10,-22 c18,25 0,50 -30,42 z",
           c=ROUGE, w=2, fill=ORANGE)
    s.text(190, 210, "Retirer un côté éteint le feu", 12, c=ENCRE)
    return s


@schema
def eprouvette_menisque():
    s = S(320, 300)
    x0, x1, top, bot = 110, 170, 30, 260
    s.line(x0, top, x0, bot)
    s.line(x1, top, x1, bot)
    s.line(x0 - 20, bot, x1 + 20, bot, w=4)
    lvl = 138
    s.path(f"M{x0 + 1},{lvl - 6} Q{(x0 + x1) / 2},{lvl + 10} {x1 - 1},{lvl - 6} L{x1 - 1},{bot - 1} L{x0 + 1},{bot - 1} Z",
           c="none", w=0, fill="#BFDDF5")
    s.path(f"M{x0 + 1},{lvl - 6} Q{(x0 + x1) / 2},{lvl + 10} {x1 - 1},{lvl - 6}", c=BLEU, w=2)
    for i, y in enumerate(range(60, 251, 10)):
        long = i % 5 == 0
        s.line(x1, y, x1 - (14 if long else 7), y, w=1.3)
        if long:
            s.text(x1 + 6, y + 4, str(100 - (y - 50) // 2 * 1 if False else 100 - (y - 60) // 2), 11, c=BRUN,
                   anchor="start")
    s.line(30, lvl + 2, x0 - 4, lvl + 2, c=ORANGE, w=1.5, dash="4,3")
    s.ellipse(30, lvl + 2, 12, 7, c=ORANGE, w=2)
    s.circle(30, lvl + 2, 3, c=ORANGE, fill=ORANGE)
    s.text(230, 132, "lire au bas", 12, c=ORANGE, bold=True, anchor="start")
    s.text(230, 148, "du ménisque", 12, c=ORANGE, bold=True, anchor="start")
    s.text(230, 166, "→ 60 mL", 13, c=VERT, bold=True, anchor="start")
    s.text(160, 290, "L'œil à la hauteur du liquide", 12, c=ENCRE)
    return s


@schema
def regle_mesure():
    s = S(460, 170)
    x0, y0, u = 40, 100, 45
    s.rect(x0 - 10, y0, 9 * u + 20, 46, c=BRUN, sw=2, fill="#FBF3E3", r=4)
    for mm in range(0, 91):
        x = x0 + mm * u / 10
        h = 18 if mm % 10 == 0 else (12 if mm % 5 == 0 else 7)
        s.line(x, y0, x, y0 + h, w=1 if h < 18 else 1.6)
        if mm % 10 == 0:
            s.text(x, y0 + 34, str(mm // 10), 12, c=ENCRE)
    s.rect(x0, y0 - 34, 7.5 * u, 26, c=ORANGE, sw=2, fill="#FDE3CC", r=6)
    s.line(x0, y0 - 40, x0, y0, c=VERT, w=1.5, dash="3,3")
    s.line(x0 + 7.5 * u, y0 - 40, x0 + 7.5 * u, y0, c=VERT, w=1.5, dash="3,3")
    s.text(x0 + 3.75 * u, y0 - 16, "objet : 7,5 cm", 13, c=ENCRE, bold=True)
    s.text(230, 162, "Le zéro de la règle à une extrémité de l'objet", 12, c=BRUN)
    return s


@schema
def thermometre():
    s = S(260, 320)
    x, top, bot = 110, 30, 260
    s.rect(x - 10, top, 20, bot - top, c=ENCRE, sw=2, fill="#FFFFFF", r=10)
    s.circle(x, bot + 14, 20, c=ENCRE, w=2, fill=ROUGE)
    t = 37
    yt = bot - 10 - (t + 10) * (bot - top - 30) / 60
    s.rect(x - 5, yt, 10, bot - yt + 4, c="none", sw=0, fill=ROUGE)
    for deg in range(-10, 51, 2):
        y = bot - 10 - (deg + 10) * (bot - top - 30) / 60
        long = deg % 10 == 0
        s.line(x + 12, y, x + (26 if long else 18), y, w=1.2)
        if long:
            s.text(x + 32, y + 4, f"{deg} °C", 11, c=BRUN, anchor="start")
    s.line(x - 30, yt, x - 12, yt, c=ORANGE, w=2)
    s.text(x - 34, yt + 5, "37 °C", 13, c=ORANGE, bold=True, anchor="end")
    s.text(130, 312, "Lire en face du haut de la colonne", 12, c=ENCRE)
    return s


@schema
def balance_roberval():
    s = S(420, 250)
    s.poly([(150, 210), (270, 210), (245, 170), (175, 170)], fill="#EADFCE", c=BRUN)
    s.line(210, 170, 210, 110, w=4)
    s.line(90, 110, 330, 110, w=5)
    s.poly([(204, 104), (216, 104), (210, 60)], fill=ORANGE, c=ORANGE)
    for x in (90, 330):
        s.line(x, 110, x, 130, w=3)
        s.ellipse(x, 135, 58, 9, fill="#D9D9D9")
    s.rect(60, 95, 60, 32, c=VERT, sw=2, fill="#E2F4EB", r=6)
    s.text(90, 116, "objet", 12, c=VERT, bold=True)
    for i, (w_, lab) in enumerate([(26, "200 g"), (18, "50 g"), (14, "20 g")]):
        xx = 300 + i * 26
        s.rect(xx - w_ / 2 - 6, 127 - w_ - 4, w_, w_ + 4, c=BRUN, sw=1.5, fill="#C9A86A", r=3)
        s.text(xx - 6, 127 - w_ - 10 - i * 0, lab, 10, c=BRUN) if i != 1 else s.text(xx - 6, 160, lab, 10, c=BRUN)
    s.text(210, 238, "Équilibre : masse de l'objet = 200 + 50 + 20 = 270 g", 12.5, c=ENCRE, bold=True)
    return s


@schema
def neurone():
    s = S(460, 220)
    cx, cy = 90, 110
    s.circle(cx, cy, 34, c=VERT, w=2.5, fill="#E2F4EB")
    s.circle(cx, cy, 11, c=VERT, w=1.5, fill="#9AD7B8")
    for a in range(0, 360, 45):
        if 315 > a > 45 or True:
            if a in (0,):
                continue
            r1 = math.radians(a)
            x1, y1 = cx + 34 * math.cos(r1), cy - 34 * math.sin(r1)
            x2, y2 = cx + 66 * math.cos(r1), cy - 66 * math.sin(r1)
            s.line(x1, y1, x2, y2, c=VERT, w=2)
            s.line(x2, y2, x2 + 12 * math.cos(r1 + 0.6), y2 - 12 * math.sin(r1 + 0.6), c=VERT, w=1.5)
            s.line(x2, y2, x2 + 12 * math.cos(r1 - 0.6), y2 - 12 * math.sin(r1 - 0.6), c=VERT, w=1.5)
    s.line(cx + 34, cy, 380, cy, c=VERT, w=3)
    for k in range(5):
        s.rect(160 + k * 42, cy - 8, 32, 16, c=ORANGE, sw=1.5, fill="#FDE3CC", r=7)
    for a in (-30, 0, 30):
        r1 = math.radians(a)
        x2, y2 = 380 + 40 * math.cos(r1), cy - 40 * math.sin(r1)
        s.line(380, cy, x2, y2, c=VERT, w=2)
        s.circle(x2, y2, 5, c=VERT, fill=VERT)
    s.arrow(160, cy + 32, 330, cy + 32, c=ROUGE, w=2)
    s.text(245, cy + 50, "sens du message nerveux", 12, c=ROUGE, bold=True)
    s.text(90, 30, "dendrites", 12, c=BRUN)
    s.text(90, 196, "corps cellulaire (noyau)", 12, c=BRUN)
    s.text(270, 80, "axone (gaine de myéline)", 12, c=ORANGE, bold=True)
    s.text(420, 180, "terminaisons", 12, c=BRUN, anchor="end")
    return s


@schema
def courbe_dosage():
    s = S(400, 290)
    ox, oy, W, H = 55, 240, 320, 210
    s.arrow(ox, oy, ox + W + 10, oy, w=1.6, head=8)
    s.arrow(ox, oy, ox, oy - H - 10, w=1.6, head=8)
    for ph in range(0, 15, 2):
        y = oy - ph * H / 14
        s.line(ox - 4, y, ox + 4, y)
        s.text(ox - 8, y + 4, str(ph), 10, c=BRUN, anchor="end")
    Ve = 12.0
    pts = []
    for i in range(0, 241):
        v = i / 10
        pH = 7 + 6 * math.tanh((v - Ve) * 1.1) if abs(v - Ve) > 0.02 else 7
        pH = 2 + (pH - 1) * 0.92 if pH < 7 else pH
        pts.append((ox + v * W / 24, oy - min(pH, 13) * H / 14))
    s.poly(pts, c=ORANGE, w=3, closed=False)
    xe, ye = ox + Ve * W / 24, oy - 7 * H / 14
    s.line(xe, ye, xe, oy, c=BLEU, w=1.2, dash="4,4")
    s.line(ox, ye, xe, ye, c=BLEU, w=1.2, dash="4,4")
    s.dot(xe, ye, "E", 14, -4, c=BLEU)
    s.text(xe, oy + 16, "VbE", 12, c=BLEU, bold=True)
    s.text(ox + 4, oy - H - 4, "pH", 12, bold=True, anchor="start")
    s.text(ox + W, oy + 16, "Vb (mL)", 11, c=BRUN, anchor="end")
    s.text(210, 280, "Acide fort + base forte : pH = 7 à l'équivalence", 12, c=ENCRE, bold=True)
    return s


@schema
def fleur():
    s = S(460, 300)
    cx, base = 230, 250
    s.line(cx, base + 40, cx, base, c=VERT, w=5)
    # réceptacle et sépales
    s.path(f"M{cx - 30},{base} Q{cx},{base + 22} {cx + 30},{base} Z", c=VERT, w=2, fill="#9AD7B8")
    s.path(f"M{cx - 28},{base - 2} Q{cx - 70},{base - 10} {cx - 60},{base - 40} Q{cx - 35},{base - 20} {cx - 18},{base - 8}",
           c=VERT, w=2, fill="#BFE6CF")
    s.path(f"M{cx + 28},{base - 2} Q{cx + 70},{base - 10} {cx + 60},{base - 40} Q{cx + 35},{base - 20} {cx + 18},{base - 8}",
           c=VERT, w=2, fill="#BFE6CF")
    # pétales
    s.path(f"M{cx - 20},{base - 10} C{cx - 120},{base - 60} {cx - 110},{base - 170} {cx - 40},{base - 120} Z",
           c=ORANGE, w=2, fill="#FDE3CC")
    s.path(f"M{cx + 20},{base - 10} C{cx + 120},{base - 60} {cx + 110},{base - 170} {cx + 40},{base - 120} Z",
           c=ORANGE, w=2, fill="#FDE3CC")
    # pistil : ovaire, style, stigmate
    s.ellipse(cx, base - 25, 18, 22, c=VERT, w=2, fill="#E2F4EB")
    s.circle(cx - 6, base - 28, 4, c=VERT, w=1, fill="#FFFFFF")
    s.circle(cx + 6, base - 22, 4, c=VERT, w=1, fill="#FFFFFF")
    s.line(cx, base - 47, cx, base - 140, c=VERT, w=4)
    s.ellipse(cx, base - 146, 12, 7, c=VERT, w=2, fill="#9AD7B8")
    # étamines
    for dx in (-38, 38):
        s.line(cx + dx * 0.4, base - 30, cx + dx, base - 120, c=BRUN, w=2)
        s.ellipse(cx + dx, base - 127, 9, 13, c=BRUN, w=2, fill=JAUNE)
    labels = [(cx + 60, 95, "anthère", cx + 40, base - 128, BRUN), (cx + 95, 150, "filet", cx + 28, base - 90, BRUN),
              (cx - 85, 95, "stigmate", cx - 12, base - 146, VERT), (cx - 105, 150, "style", cx - 3, base - 100, VERT),
              (cx - 115, 222, "ovaire (ovules)", cx - 18, base - 25, VERT), (cx + 120, 205, "pétale", cx + 75, base - 85, ORANGE),
              (cx + 115, 262, "sépale", cx + 55, base - 30, VERT)]
    for tx, ty, t, px, py, col in labels:
        s.line(tx + (-4 if tx > cx else 4), ty - 4, px, py, c=GRIS, w=1)
        s.text(tx, ty, t, 12, c=col, bold=True, anchor="start" if tx > cx else "end")
    s.text(cx, 26, "étamines = organes mâles · pistil = organe femelle", 12, c=ENCRE, bold=True)
    return s


# ============================================================ HISTOIRE
@schema
def frise_cote_divoire():
    s = S(480, 175)
    y = 100
    xs = {"−1500": 30, "1470": 160, "1893": 265, "1960": 360}
    s.arrow(20, y, 465, y, w=3)
    blocs = [(30, 160, "#EADFCE", "Période ancienne"), (160, 265, "#FDE3CC", "Précoloniale"),
             (265, 360, "#F6C9A0", "Coloniale"), (360, 458, "#CDEBDB", "Indépendance")]
    for x1, x2, col, nom in blocs:
        s.rect(x1, y - 28, x2 - x1, 28, c="none", sw=0, fill=col)
        s.text((x1 + x2) / 2, y - 10, nom, 11.5, c=ENCRE, bold=True)
    for lab, x in xs.items():
        s.line(x, y - 6, x, y + 8, w=2)
        s.text(x, y + 26, lab, 13, c=ORANGE if lab != "−1500" else BRUN, bold=True)
    s.text(360, y + 44, "7 août 1960", 11, c=VERT)
    s.text(265, y + 44, "colonie", 11, c=BRUN)
    s.text(160, y + 44, "Portugais", 11, c=BRUN)
    s.text(240, 34, "Les périodes de l'histoire de la Côte d'Ivoire", 13, c=ENCRE, bold=True)
    s.text(240, 52, "(frise simplifiée, pas à l'échelle)", 10.5, c=BRUN)
    return s


# --- Carte simplifiée de la Côte d'Ivoire (longitude, latitude approximatives)
CI = [(-7.53, 4.36), (-6.9, 4.65), (-6.08, 4.95), (-5.57, 5.08), (-5.0, 5.13), (-4.0, 5.24), (-3.74, 5.2),
      (-3.25, 5.12), (-2.93, 5.1), (-3.05, 5.6), (-3.2, 6.25), (-3.0, 7.0), (-2.78, 7.9), (-2.6, 8.2),
      (-2.5, 8.9), (-2.7, 9.6), (-3.2, 9.9), (-3.65, 9.95), (-4.3, 9.65), (-4.75, 9.75), (-5.5, 10.4),
      (-6.2, 10.6), (-6.75, 10.3), (-7.3, 10.4), (-7.65, 10.45), (-8.05, 10.2), (-8.2, 9.5), (-7.9, 8.8),
      (-8.2, 8.2), (-8.45, 7.6), (-8.3, 7.1), (-7.75, 6.5), (-7.45, 5.85), (-7.6, 4.9)]
VILLES = {"Abidjan": (-4.02, 5.33), "Yamoussoukro": (-5.28, 6.82), "Bouaké": (-5.03, 7.69),
          "Korhogo": (-5.63, 9.46), "Man": (-7.55, 7.41), "San-Pédro": (-6.64, 4.75), "Odienné": (-7.56, 9.51),
          "Bondoukou": (-2.8, 8.04)}


def _ci(s, x0=40, y0=30, k=42, fill="#F7F1E6", villes=("Abidjan", "Yamoussoukro", "Bouaké", "Korhogo", "Man")):
    def P(lon, lat):
        return x0 + (lon + 8.6) * k, y0 + (10.8 - lat) * k
    s.poly([P(*c) for c in CI], c=BRUN, w=2, fill=fill)
    return P


def _villes(s, P, noms):
    for v in noms:
        x, y = P(*VILLES[v])
        s.circle(x, y, 3.5, c=ENCRE, w=1, fill=ENCRE)
        s.text(x + 6, y - 5, v, 11, c=ENCRE, anchor="start")


def _ocean(s, P):
    x, y = P(-5.4, 4.3)
    s.text(x, y + 14, "Océan Atlantique", 12, c=BLEU, italic=True)


@schema
def carte_climats_ci():
    s = S(360, 340)
    P = _ci(s)
    zones = [((-5.6, 9.5), 95, 40, "#F6D776", "soudanien"), ((-5.2, 7.7), 100, 30, "#BFE6CF", "baouléen"),
             ((-5.2, 5.9), 105, 32, "#9AD7B8", "attiéen"), ((-7.9, 7.5), 26, 48, "#BFDDF5", "montagne")]
    for (lon, lat), rx, ry, col, nom in zones:
        x, y = P(lon, lat)
        s.ellipse(x, y, rx, ry, c="none", w=0, fill=col)
    _ci(s, fill="none")
    for (lon, lat), rx, ry, col, nom in zones:
        x, y = P(lon, lat)
        s.text(x, y + 5, nom, 13, c=ENCRE, bold=True)
    _ocean(s, P)
    s.text(180, 24, "Les climats de la Côte d'Ivoire (schéma simplifié)", 12, c=ENCRE, bold=True)
    return s


@schema
def carte_groupes_ethniques():
    s = S(360, 340)
    P = _ci(s)
    zones = [((-7.0, 9.6), 50, 34, "#F6D776", "Mandé Nord"), ((-4.3, 9.3), 85, 32, "#F6C9A0", "Gour"),
             ((-7.3, 7.6), 34, 46, "#BFDDF5", "Mandé Sud"), ((-6.4, 5.9), 58, 40, "#E2C8F0", "Krou"),
             ((-4.2, 6.6), 72, 62, "#BFE6CF", "Akan")]
    for (lon, lat), rx, ry, col, nom in zones:
        x, y = P(lon, lat)
        s.ellipse(x, y, rx, ry, c="none", w=0, fill=col)
    _ci(s, fill="none")
    for (lon, lat), rx, ry, col, nom in zones:
        x, y = P(lon, lat)
        s.text(x, y + 5, nom, 13, c=ENCRE, bold=True)
    _ocean(s, P)
    s.text(180, 24, "Les grands groupes ethniques (schéma simplifié)", 12, c=ENCRE, bold=True)
    return s


@schema
def carte_migrations():
    s = S(420, 400)
    P = _ci(s, x0=80, y0=70)
    fleches = [((-5.5, 11.6), (-5.4, 9.6), ORANGE, "Sénoufo (dès le Xᵉ s.)", (-5.0, 11.75), "start"),
               ((-9.3, 10.5), (-7.4, 9.4), ROUGE, "Mandé (XIᵉ-XVᵉ s.)", (-9.3, 10.85), "start"),
               ((-9.4, 6.0), (-7.0, 6.0), BLEU, "Krou (XIVᵉ-XVᵉ s.)", (-9.5, 5.55), "start"),
               ((-1.2, 6.9), (-3.9, 6.9), VERT, "Akan (XVIIᵉ-XVIIIᵉ s.)", (-1.0, 6.35), "end")]
    for (a, b, col, lab, t, anc) in fleches:
        s.arrow(*P(*a), *P(*b), c=col, w=4, head=14)
        x, y = P(*t)
        s.text(x, y, lab, 11.5, c=col, bold=True, anchor=anc)
    _villes(s, P, ("Abidjan", "Korhogo", "Man"))
    _ocean(s, P)
    s.text(210, 390, "Les grandes migrations (schéma simplifié)", 12, c=ENCRE, bold=True)
    return s


@schema
def commerce_triangulaire():
    s = S(480, 300)
    E, Af, Am = (330, 60), (360, 220), (90, 150)
    for (x, y), nom, col in [(E, "EUROPE", BLEU), (Af, "AFRIQUE", ORANGE), (Am, "AMÉRIQUE", VERT)]:
        s.ellipse(x, y, 62, 28, c=col, w=2, fill="#FFFFFF")
        s.text(x, y + 5, nom, 13, c=col, bold=True)
    s.arrow(E[0] + 10, E[1] + 28, Af[0] - 2, Af[1] - 30, c=BLEU, w=3, head=12)
    s.text(360, 128, "1. tissus, armes,", 11.5, c=BLEU, anchor="start")
    s.text(360, 143, "alcool, pacotille", 11.5, c=BLEU, anchor="start")
    s.arrow(Af[0] - 60, Af[1] - 4, Am[0] + 50, Am[1] + 22, c=ROUGE, w=3, head=12)
    s.text(205, 238, "2. captifs africains", 12, c=ROUGE, bold=True)
    s.text(205, 254, "(« passage du milieu »)", 11, c=ROUGE)
    s.arrow(Am[0] + 46, Am[1] - 20, E[0] - 60, E[1] + 4, c=VERT, w=3, head=12)
    s.text(150, 72, "3. sucre, café,", 11.5, c=VERT, anchor="middle")
    s.text(150, 87, "coton, tabac", 11.5, c=VERT, anchor="middle")
    s.text(240, 288, "Le commerce triangulaire (XVIᵉ-XIXᵉ siècle)", 12.5, c=ENCRE, bold=True)
    return s


# ============================================================ GÉOGRAPHIE
@schema
def formes_relief():
    s = S(480, 250)
    sea = 190
    s.rect(2, sea, 96, 32, c="none", sw=0, fill="#BFDDF5")
    s.text(50, sea + 22, "mer (0 m)", 11, c=BLEU, bold=True)
    pts = [(98, sea), (150, sea - 4), (200, sea - 8), (230, sea - 60), (330, sea - 66), (345, sea - 70),
           (380, sea - 150), (405, sea - 115), (430, sea - 165), (478, sea - 90)]
    s.poly(pts + [(478, 222), (98, 222)], c=BRUN, w=2.5, fill="#EADFCE")
    s.text(150, sea - 16, "plaine", 13, c=VERT, bold=True)
    s.text(280, sea - 80, "plateau", 13, c=ORANGE, bold=True)
    s.text(410, 16 + 4, "montagne", 13, c=ROUGE, bold=True)
    s.line(20, sea, 470, sea, c=BLEU, w=1, dash="4,4")
    s.line(430, sea - 165, 430, sea, c=GRIS, w=1, dash="3,3")
    s.text(424, sea - 60, "altitude", 10.5, c=BRUN, anchor="end")
    s.text(240, 244, "Altitude mesurée à partir du niveau de la mer", 12, c=ENCRE)
    return s


@schema
def globe_reperes():
    s = S(470, 340)
    cx, cy, r = 170, 175, 125
    s.circle(cx, cy, r, c=BLEU, w=2.5, fill="#E8F1FB")
    for lat, nom, col in [(0, "équateur (0°)", ROUGE), (23.4, "tropique du Cancer", ORANGE),
                          (-23.4, "tropique du Capricorne", ORANGE), (66.6, "cercle polaire arctique", BLEU),
                          (-66.6, "cercle polaire antarctique", BLEU)]:
        y = cy - r * math.sin(math.radians(lat))
        half = r * math.cos(math.radians(lat))
        s.ellipse(cx, y, half, max(3, half * 0.12), c=col, w=2 if lat == 0 else 1.5)
        s.line(cx + half, y, 305, y, c=col, w=1, dash="2,3")
        s.text(310, y + 4, nom, 11.5, c=col, bold=(lat == 0), anchor="start")
    s.ellipse(cx, cy, 40, r, c=VERT, w=2)
    s.line(cx - 40, cy - 40, 60, 40, c=VERT, w=1, dash="2,3")
    s.text(20, 34, "méridien de Greenwich (0°)", 11.5, c=VERT, anchor="start", bold=True)
    s.dot(cx, cy - r, "")
    s.text(cx + 10, cy - r - 6, "pôle Nord", 12, anchor="start", bold=True)
    s.dot(cx, cy + r, "")
    s.text(cx + 10, cy + r + 14, "pôle Sud", 12, anchor="start", bold=True)
    return s


@schema
def cycle_eau():
    s = S(480, 300)
    s.rect(2, 220, 200, 76, c="none", sw=0, fill="#BFDDF5")
    s.text(100, 270, "océan", 13, c=BLEU, bold=True)
    s.poly([(202, 296), (202, 220), (300, 180), (380, 120), (440, 170), (478, 150), (478, 296)], c=BRUN, w=2,
           fill="#EADFCE")
    s.circle(50, 50, 24, c=ORANGE, fill=JAUNE)
    for x in (110, 250):
        s.ellipse(x + 40, 60, 60, 22, c=GRIS, w=1.5, fill="#F2F2F2")
    for x in (70, 110, 150):
        s.arrow(x, 210, x + 10, 110, c=ORANGE, w=2, dash="5,4")
    s.text(110, 242, "évaporation", 12, c=ORANGE, bold=True)
    s.arrow(205, 60, 245, 60, c=GRIS, w=2)
    s.text(225, 48, "condensation", 11, c=BRUN)
    for x in (270, 300, 330):
        s.arrow(x, 88, x - 8, 150, c=BLEU, w=2)
    s.text(345, 110, "précipitations", 12, c=BLEU, bold=True, anchor="start")
    s.arrow(330, 176, 215, 222, c=VERT, w=2.5)
    s.text(300, 216, "ruissellement", 12, c=VERT, bold=True)
    s.arrow(380, 200, 380, 262, c=BRUN, w=2, dash="4,3")
    s.text(390, 250, "infiltration", 12, c=BRUN, bold=True, anchor="start")
    s.text(470, 285, "nappe souterraine", 10.5, c=BRUN, anchor="end")
    return s


@schema
def roches_magma():
    s = S(460, 300)
    s.rect(2, 60, 456, 236, c="none", sw=0, fill="#EADFCE")
    s.poly([(170, 60), (230, 10), (290, 60)], c=BRUN, w=2, fill="#B89C7A")
    s.path("M230,14 C235,40 222,60 230,90 C240,130 220,170 230,210", c=ROUGE, w=6)
    s.ellipse(230, 250, 90, 32, c=ROUGE, w=2, fill="#F6A37A")
    s.text(230, 256, "magma", 13, c=ENCRE, bold=True)
    s.ellipse(230, 140, 30, 14, c=ORANGE, w=2, fill="#FCD3B6")
    s.ellipse(310, 52, 40, 8, c=ENCRE, w=1.5, fill="#55504A")
    s.text(165, 26, "basalte : refroidissement", 11.5, c=ENCRE, anchor="end", bold=True)
    s.text(165, 41, "rapide en surface (lave)", 11.5, c=ENCRE, anchor="end")
    s.text(268, 136, "microgranite :", 11.5, c=ENCRE, anchor="start", bold=True)
    s.text(268, 151, "à mi-profondeur", 11.5, c=ENCRE, anchor="start")
    s.ellipse(110, 225, 60, 26, c=GRIS, w=2, fill="#D8D3CC")
    s.text(110, 222, "granite :", 11.5, c=ENCRE, bold=True)
    s.text(110, 237, "lent, en profondeur", 11, c=ENCRE)
    s.arrow(20, 70, 20, 280, c=BLEU, w=1.5, head=8)
    s.text(28, 84, "profondeur", 10.5, c=BLEU, anchor="start")
    s.text(230, 294, "Plus le refroidissement est lent, plus les cristaux sont gros", 11.5, c=VERT, bold=True)
    return s


@schema
def profil_sol():
    s = S(470, 340)
    x0, w = 30, 150
    couches = [(20, 18, "#6B4E2E", "litière"), (38, 70, "#5A4632", "horizon A : humus + minéraux"),
               (108, 80, "#C26A3D", "horizon B : argile, sable, fer"), (188, 62, "#D9C3A0", "horizon C : roche altérée (arène)"),
               (250, 68, "#9A9086", "roche mère")]
    for y, h, col, lab in couches:
        s.rect(x0, y, w, h, c="#FFFFFF", sw=1, fill=col)
        s.line(x0 + w, y + h / 2, x0 + w + 14, y + h / 2, c=GRIS, w=1)
        s.text(x0 + w + 18, y + h / 2 + 4, lab, 11.5, c=ENCRE, anchor="start", bold=True)
    for k in range(6):
        s.line(x0 + 15 + k * 22, 20, x0 + 10 + k * 22, 14, c=VERT, w=2)
    for cx, cy in [(70, 280), (120, 300), (160, 270), (95, 260)]:
        s.poly([(cx - 14, cy - 6), (cx + 10, cy - 10), (cx + 16, cy + 6), (cx - 8, cy + 10)], c="#6E6152", w=1,
               fill="#B5ACA2")
    s.path(f"M{x0 + 60},{40} q8,25 -4,50 q-10,20 6,45", c="#E8D7B5", w=2)
    s.text(235, 334, "Profil d'un sol (coupe verticale)", 12, c=VERT, bold=True)
    return s


# ============================================================ EDHC
@schema
def drapeau_ci():
    s = S(360, 250)
    x0, y0, w, h = 40, 40, 280, 180
    s.rect(x0, y0, w / 3, h, c="none", sw=0, fill="#F77F00")
    s.rect(x0 + w / 3, y0, w / 3, h, c="none", sw=0, fill="#FFFFFF")
    s.rect(x0 + 2 * w / 3, y0, w / 3, h, c="none", sw=0, fill="#009E60")
    s.rect(x0, y0, w, h, c=GRIS, sw=1.5)
    s.line(x0 - 6, y0 - 10, x0 - 6, y0 + h + 10, c=BRUN, w=5)
    s.text(x0 + w / 6, y0 + h + 20, "orange", 12, c=BRUN, bold=True)
    s.text(x0 + w / 2, y0 + h + 20, "blanc", 12, c=BRUN, bold=True)
    s.text(x0 + 5 * w / 6, y0 + h + 20, "vert", 12, c=BRUN, bold=True)
    s.text(180, 26, "Drapeau de la Côte d'Ivoire (hampe à gauche)", 12, c=ENCRE, bold=True)
    return s


@schema
def panneaux_routiers():
    s = S(500, 210)
    # interdiction
    s.circle(60, 80, 38, c=ROUGE, w=9, fill="#FFFFFF")
    s.text(60, 89, "50", 24, bold=True)
    # obligation
    s.circle(160, 80, 40, c=BLEU, w=0, fill=BLEU)
    s.arrow(140, 80, 182, 80, c="#FFFFFF", w=6, head=16)
    # danger
    s.poly([(260, 38), (305, 118), (215, 118)], c=ROUGE, w=8, fill="#FFFFFF")
    s.text(260, 108, "!", 34, bold=True)
    # stop
    pts = [(355 + 40 * math.cos(math.radians(22.5 + 45 * k)), 80 + 40 * math.sin(math.radians(22.5 + 45 * k)))
           for k in range(8)]
    s.poly(pts, c="#FFFFFF", w=3, fill=ROUGE)
    s.text(355, 88, "STOP", 17, c="#FFFFFF", bold=True)
    # indication
    s.rect(433, 42, 46, 76, c="none", sw=0, fill=BLEU, r=6)
    s.text(456, 96, "P", 34, c="#FFFFFF", bold=True)
    for x, t in [(60, "interdiction"), (160, "obligation"), (260, "danger"), (355, "arrêt absolu"),
                 (456, "indication")]:
        s.text(x, 150, t, 12, c=BRUN, bold=True)
    s.text(250, 190, "Rond rouge : interdit · rond bleu : obligatoire · triangle : danger", 12, c=ENCRE)
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    for nom, fn in SCHEMAS.items():
        with open(os.path.join(OUT, f"{nom}.svg"), "w", encoding="utf-8") as f:
            f.write(fn().svg())
    print(f"{len(SCHEMAS)} schémas dans {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
