"""Génère, à partir des sources de contenu (src/*.py) :
  3eme/quiz.xlsx  -> python manage.py import_questions quiz.xlsx --shared
  3eme/cours.xlsx -> python manage.py import_cours cours.xlsx --fiches fiches
  3eme/fiches/*.pdf
Vérifie chaque question et répartit la bonne réponse entre A, B, C et D."""
import hashlib
import importlib.util
import os
import random
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

rl_config.invariant = 1                                  # PDF identiques d'une génération à l'autre
HERE = os.path.dirname(os.path.abspath(__file__))
# Usage : python contenu/generer.py [3eme|4eme|5eme|6eme|terminale] [dossier de sortie]
NIVEAU_CIBLE = sys.argv[1] if len(sys.argv) > 1 and not os.sep in sys.argv[1] else "3eme"
OUT = sys.argv[2] if len(sys.argv) > 2 else (sys.argv[1] if len(sys.argv) > 1 and os.sep in sys.argv[1]
                                             else os.path.join(HERE, NIVEAU_CIBLE))
SETS = {
    "3eme": ["maths3_a.py", "maths3_b.py", "pc3.py", "svt3.py", "anglais3.py", "hg3.py", "francais3.py"],
    # Un chapitre peut servir à plusieurs classes : NIVEAUX dans le module, ou « niveaux » dans le chapitre.
    "terminale": ["maths_tle_cd.py", "maths_tle_a.py", "pc_tle.py", "svt_tle.py", "hg_tle.py",
                  "philo_tle.py", "anglais_tle.py", "francais_tle.py"],
    "4eme": ["maths4.py", "pc4.py", "edhc4.py", "francais4.py", "anglais4.py", "hg4.py", "svt4.py"],
    "5eme": ["maths5.py", "pc5.py", "edhc5.py", "edhc5b.py", "francais5.py", "anglais5.py", "hg5.py"],
    "6eme": ["pc6.py", "edhc6.py", "francais6.py", "anglais6.py", "hg6.py", "hg6g.py", "svt6.py"],
}
SOURCES = SETS[NIVEAU_CIBLE]
FREE = {"Calcul littéral", "Lentilles minces", "Les micro-organismes et les maladies infectieuses",
        "Simple past et present perfect", "La Seconde Guerre mondiale"}          # 3ème : chapitres ouverts sans abonnement

ORANGE, VERT, ENCRE, IVOIRE, BRUN, SABLE = (HexColor(c) for c in
                                            ("#F2790F", "#0B9A5C", "#221A12", "#FDF6EC", "#6E6152", "#EADFCE"))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DV", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
try:                                                     # schémas SVG : même police que dans l'application
    from svglib.fonts import register_font
    register_font("DejaVu Sans", f"{FONT_DIR}/DejaVuSans.ttf")
    register_font("DejaVu Sans", f"{FONT_DIR}/DejaVuSans-Bold.ttf", weight="bold")
except ImportError:                                      # pip install svglib (seulement pour générer)
    pass


def load(name):
    spec = importlib.util.spec_from_file_location(name[:-3], os.path.join(HERE, "sources", name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def slug(text):
    import unicodedata
    t = unicodedata.normalize("NFKD", text.replace("œ", "oe").replace("Œ", "Oe")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


# --- Vérifications -------------------------------------------------------------
SCHEMAS = os.path.join(os.path.dirname(HERE), "game", "static", "game", "schemas")
LIGNE_SCHEMA = re.compile(r"^\[\[schema:([a-z0-9-]+)(?:\|(.*))?\]\]$")


def schema_path(nom):
    return os.path.join(SCHEMAS, f"{nom}.svg")


def parts(q):
    """(d, texte, bonne, 3 fausses, explication), schéma : un 8e élément facultatif nomme le schéma."""
    return (q[:7], q[7]) if len(q) == 8 else (q, "")


def check(chap, errors):
    names = set()
    for line in chap["fiche"].splitlines():
        m = LIGNE_SCHEMA.match(line.strip())
        if m and not os.path.exists(schema_path(m.group(1))):
            errors.append(f"{chap['nom']} : schéma introuvable « {m.group(1)} » (lance contenu/schemas.py)")
    for i, q in enumerate(chap["questions"], 1):
        where = f"{chap['nom']} · Q{i}"
        if len(q) not in (7, 8):
            errors.append(f"{where} : {len(q)} éléments au lieu de 7 (ou 8 avec un schéma)")
            continue
        q, sch = parts(q)
        if sch and not os.path.exists(schema_path(sch)):
            errors.append(f"{where} : schéma introuvable « {sch} »")
        d, text, good, *wrong, expl = q
        opts = [good] + wrong
        if d not in (1, 2, 3, 4):
            errors.append(f"{where} : difficulté {d}")
        if len(set(o.strip().lower() for o in opts)) != 4:
            errors.append(f"{where} : réponses en double")
        if any(len(o) > 200 for o in opts):
            errors.append(f"{where} : réponse de plus de 200 caractères")
        if not expl.strip():
            errors.append(f"{where} : explication vide")
        if text in names:
            errors.append(f"{where} : question en double")
        names.add(text)
    if len(chap["questions"]) < 10:
        errors.append(f"{chap['nom']} : seulement {len(chap['questions'])} questions")


def shuffled(q):
    """Ordre des réponses stable d'une génération à l'autre (graine = la question)."""
    q, sch = parts(q)
    d, text, good, *wrong, expl = q
    opts = [good] + wrong
    rnd = random.Random(hashlib.sha1(text.encode()).hexdigest())
    rnd.shuffle(opts)
    return d, text, opts, "ABCD"[opts.index(good)], expl, sch


def figure(nom, legende, largeur_max, hauteur_max=62 * mm):
    """Schéma SVG mis à l'échelle pour la fiche PDF, centré, avec sa légende."""
    from svglib.svglib import svg2rlg
    dessin = svg2rlg(schema_path(nom))
    k = min(largeur_max, 105 * mm) / dessin.width            # au plus 10,5 cm de large…
    k = min(k, hauteur_max / dessin.height)                   # … et 6,2 cm de haut
    dessin.width, dessin.height = dessin.width * k, dessin.height * k
    dessin.scale(k, k)
    dessin.hAlign = "CENTER"
    bloc = [Spacer(1, 4), dessin]
    if legende:
        bloc.append(Paragraph(esc(legende), ParagraphStyle("leg", parent=ST["c"], alignment=1, leftIndent=0)))
    bloc.append(Spacer(1, 4))
    return bloc


# --- Fiche (texte affiché dans l'application) ------------------------------------
def app_summary(fiche):
    lines = []
    for line in fiche.strip().splitlines():
        if line.startswith("## "):
            if lines and lines[-1] != "":
                lines.append("")
            lines.append("■ " + line[3:].strip())
        else:
            lines.append(line)
    return "\n".join(lines)


# --- Fiche PDF -------------------------------------------------------------------
ST = {
    "h": ParagraphStyle("h", fontName="DVB", fontSize=12.5, textColor=VERT, spaceBefore=9, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="DV", fontSize=10.2, leading=14.2, textColor=ENCRE, alignment=TA_LEFT),
    "b": ParagraphStyle("b", fontName="DV", fontSize=10.2, leading=14.2, textColor=ENCRE, leftIndent=12,
                        bulletIndent=2),
    "q": ParagraphStyle("q", fontName="DVB", fontSize=10.2, leading=14, textColor=ENCRE, spaceBefore=6),
    "o": ParagraphStyle("o", fontName="DV", fontSize=10, leading=13.5, textColor=ENCRE, leftIndent=12),
    "c": ParagraphStyle("c", fontName="DV", fontSize=9.6, leading=13, textColor=BRUN, leftIndent=12),
}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(t):
    """Petites mises en forme : ✔ en vert, PIÈGES en gras déjà en majuscules."""
    t = esc(t)
    return t.replace("✔", '<font color="#0B9A5C">✔</font>')


def pdf(chap, niveau, matiere, path):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=f"{chap['nom']} – {matiere} {niveau}", author="MaxQuiz")
    story = []
    head = Table([[Paragraph(f'<font name="DVB" size="9" color="#FFFFFF">MAXQUIZ · {esc(matiere.upper())} · '
                             f'{esc(niveau.upper())}</font>', ST["p"])],
                  [Paragraph(f'<font name="DVB" size="19" color="#FFFFFF">{esc(chap["nom"])}</font>', ST["p"])]],
                 colWidths=[doc.width])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ORANGE),
                              ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, 0), 10),
                              ("TOPPADDING", (0, 1), (-1, 1), 4), ("BOTTOMPADDING", (0, 1), (-1, 1), 12)]))
    story += [head, Spacer(1, 6)]
    for line in chap["fiche"].strip().splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        m = LIGNE_SCHEMA.match(s.strip())
        if m:
            story.append(KeepTogether(figure(m.group(1), (m.group(2) or "").strip(), doc.width)))
        elif s.startswith("## "):
            story.append(Paragraph(esc(s[3:]), ST["h"]))
        elif s.lstrip().startswith("• "):
            story.append(Paragraph(fmt(s.lstrip()[2:]), ST["b"], bulletText="•"))
        elif re.match(r"^\s*\d+\. ", s):
            n, rest = s.strip().split(" ", 1)
            story.append(Paragraph(fmt(rest), ST["b"], bulletText=n))
        elif s.startswith("   "):
            story.append(Paragraph(fmt(s.strip()), ParagraphStyle("i", parent=ST["p"], leftIndent=22)))
        else:
            story.append(Paragraph(fmt(s), ST["p"]))
    # Teste-toi : quatre questions du quiz, corrigé en bas
    picks = ([q for q in chap["questions"] if q[0] >= 2 and len(q) == 8][:1]
             + [q for q in chap["questions"] if q[0] >= 2 and len(q) == 7])[:4]
    story.append(Spacer(1, 8))
    titre = Paragraph("Teste-toi", ParagraphStyle("t", parent=ST["h"], textColor=ORANGE))
    corr = []
    for i, q in enumerate(picks, 1):
        d, text, opts, letter, expl, sch = shuffled(q)
        block = [Paragraph(f"{i}. {fmt(text)}", ST["q"])]
        if sch:
            block += figure(sch, "", doc.width * 0.6, 42 * mm)
        block += [Paragraph(f"{'ABCD'[k]}. {fmt(o)}", ST["o"]) for k, o in enumerate(opts)]
        story.append(KeepTogether(([titre] if i == 1 else []) + block))
        corr.append(Paragraph(f"<b>{i}. {letter}</b> : {fmt(expl)}", ST["c"]))
    story.append(Spacer(1, 6))
    story.append(KeepTogether([Paragraph("Corrigé", ParagraphStyle("t2", parent=ST["h"], textColor=BRUN,
                                                                    fontSize=10.5))] + corr))

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("DV", 8)
        canvas.setFillColor(BRUN)
        canvas.drawString(18 * mm, 9 * mm, f"MaxQuiz · {matiere} {niveau} · {chap['nom']}")
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"maxquiz.net · page {d.page}")
        canvas.setStrokeColor(SABLE)
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


# --- Excel -------------------------------------------------------------------------
def sheet(path, headers, rows, widths):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="F2790F")
    for col, w in zip("ABCDEFGHIJKL", widths):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    wb.save(path)


def _progression():
    spec = importlib.util.spec_from_file_location("progression", os.path.join(HERE, "progression.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PROGRESSION


def _par_matiere(errors):
    """{(matière, niveaux): [(chapitre, niveaux du chapitre)]}, chapitres rangés selon
    contenu/progression.py (ordre de l'année et mois de chaque chapitre)."""
    groups = {}
    for src in SOURCES:
        mod = load(src)
        default_levels = list(getattr(mod, "NIVEAUX", None) or [mod.NIVEAU])
        key = (mod.MATIERE, tuple(default_levels))       # Maths Tle A et Maths Tle C/D numérotées à part
        for chap in mod.CHAPITRES:
            check(chap, errors)
            groups.setdefault(key, []).append((chap, list(chap.get("niveaux") or default_levels)))
    prog = _progression()
    for (matiere, levels), chaps in groups.items():
        plan = prog.get(("+".join(levels), matiere))
        if not plan:
            errors.append(f"{matiere} {'+'.join(levels)} : absent de contenu/progression.py")
            continue
        mois = dict(plan)
        names = [c["nom"] for c, _ in chaps]
        missing = [n for n in names if n not in mois]
        extra = [n for n in mois if n not in names]
        if missing or extra:
            errors.append(f"{matiere} {'+'.join(levels)} : progression à revoir "
                          f"(absents : {missing}, en trop : {extra})")
            continue
        rang = {n: i for i, (n, _) in enumerate(plan)}
        chaps.sort(key=lambda c: rang[c[0]["nom"]])
        for c, _ in chaps:
            c["mois"] = mois[c["nom"]]
    return groups


def main():
    os.makedirs(os.path.join(OUT, "fiches"), exist_ok=True)
    errors, qrows, crows, stats = [], [], [], []
    letters = {k: 0 for k in "ABCD"}
    groups = _par_matiere(errors)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    for (matiere, _default), chaps in groups.items():
        for base, (chap, levels) in enumerate(chaps, 1):
            label = levels[0] if len(levels) == 1 else ", ".join(levels[:-1]) + " et " + levels[-1]
            fname = f"{slug('-'.join(levels))}-{slug(matiere)}-{base:02d}-{slug(chap['nom'])}.pdf"
            pdf(chap, label, matiere, os.path.join(OUT, "fiches", fname))
            free = chap.get("gratuit") or (NIVEAU_CIBLE == "3eme" and chap["nom"] in FREE) or base == 1
            shuffled_qs = [shuffled(q) for q in chap["questions"]]
            for niveau in levels:
                for d, text, opts, letter, expl, sch in shuffled_qs:
                    letters[letter] += 1
                    qrows.append([niveau, matiere, chap["nom"], d, text, *opts, letter, expl, sch])
                crows.append([niveau, matiere, chap["nom"], chap["nom"], app_summary(chap["fiche"]),
                              "", fname, base, "oui" if free else "non", chap["mois"]])
            stats.append((matiere, f"{base:02d}. {chap['nom']} [{', '.join(levels)}] · mois {chap['mois']}",
                          len(chap["questions"])))
    sheet(os.path.join(OUT, "quiz.xlsx"),
          ["niveau", "matiere", "thematique", "difficulte", "question", "a", "b", "c", "d", "bonne", "explication",
           "schema"],
          qrows, [8, 16, 30, 6, 60, 28, 28, 28, 28, 6, 70, 16])
    sheet(os.path.join(OUT, "cours.xlsx"),
          ["niveau", "matiere", "chapitre", "titre", "resume", "youtube", "fiche_pdf", "ordre", "gratuit", "mois"],
          crows, [8, 16, 30, 30, 90, 30, 45, 6, 8, 6])
    for s in stats:
        print(f"{s[0]:16} {s[1]:60} {s[2]} questions")
    print(f"Total : {len(qrows)} questions, {len(crows)} chapitres. Bonnes réponses : {letters}")


if __name__ == "__main__":
    main()
