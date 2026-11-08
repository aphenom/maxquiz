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
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "3eme")
SOURCES = ["maths3_a.py", "maths3_b.py", "pc3.py"]
FREE = {"Calcul littéral", "Lentilles minces"}          # chapitres ouverts sans abonnement

ORANGE, VERT, ENCRE, IVOIRE, BRUN, SABLE = (HexColor(c) for c in
                                            ("#F2790F", "#0B9A5C", "#221A12", "#FDF6EC", "#6E6152", "#EADFCE"))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DV", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))


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
def check(chap, errors):
    names = set()
    for i, q in enumerate(chap["questions"], 1):
        where = f"{chap['nom']} · Q{i}"
        if len(q) != 7:
            errors.append(f"{where} : {len(q)} éléments au lieu de 7")
            continue
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
    d, text, good, *wrong, expl = q
    opts = [good] + wrong
    rnd = random.Random(hashlib.sha1(text.encode()).hexdigest())
    rnd.shuffle(opts)
    return d, text, opts, "ABCD"[opts.index(good)], expl


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
        if s.startswith("## "):
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
    picks = [q for q in chap["questions"] if q[0] >= 2][:4]
    story.append(Spacer(1, 8))
    story.append(Paragraph("Teste-toi", ParagraphStyle("t", parent=ST["h"], textColor=ORANGE)))
    corr = []
    for i, q in enumerate(picks, 1):
        d, text, opts, letter, expl = shuffled(q)
        block = [Paragraph(f"{i}. {fmt(text)}", ST["q"])]
        block += [Paragraph(f"{'ABCD'[k]}. {fmt(o)}", ST["o"]) for k, o in enumerate(opts)]
        story.append(KeepTogether(block))
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
    for col, w in zip("ABCDEFGHIJK", widths):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    wb.save(path)


def main():
    os.makedirs(os.path.join(OUT, "fiches"), exist_ok=True)
    errors, qrows, crows, stats = [], [], [], []
    letters = {k: 0 for k in "ABCD"}
    for src in SOURCES:
        mod = load(src)
        for order, chap in enumerate(mod.CHAPITRES, 1):
            check(chap, errors)
            if errors:
                continue
            for q in chap["questions"]:
                d, text, opts, letter, expl = shuffled(q)
                letters[letter] += 1
                qrows.append([mod.NIVEAU, mod.MATIERE, chap["nom"], d, text, *opts, letter, expl])
            base = order if src != "maths3_b.py" else order + 7
            fname = f"{slug(mod.NIVEAU)}-{slug(mod.MATIERE)}-{base:02d}-{slug(chap['nom'])}.pdf"
            pdf(chap, mod.NIVEAU, mod.MATIERE, os.path.join(OUT, "fiches", fname))
            crows.append([mod.NIVEAU, mod.MATIERE, chap["nom"], chap["nom"], app_summary(chap["fiche"]),
                          "", fname, base, "oui" if chap["nom"] in FREE else "non"])
            stats.append((mod.MATIERE, chap["nom"], len(chap["questions"])))
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    sheet(os.path.join(OUT, "quiz.xlsx"),
          ["niveau", "matiere", "thematique", "difficulte", "question", "a", "b", "c", "d", "bonne", "explication"],
          qrows, [8, 16, 30, 6, 60, 28, 28, 28, 28, 6, 70])
    sheet(os.path.join(OUT, "cours.xlsx"),
          ["niveau", "matiere", "chapitre", "titre", "resume", "youtube", "fiche_pdf", "ordre", "gratuit"],
          crows, [8, 16, 30, 30, 90, 30, 45, 6, 8])
    for s in stats:
        print(f"{s[0]:16} {s[1]:45} {s[2]} questions")
    print(f"Total : {len(qrows)} questions, {len(crows)} chapitres. Bonnes réponses : {letters}")


if __name__ == "__main__":
    main()
