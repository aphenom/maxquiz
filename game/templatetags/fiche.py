"""Mise en forme d'un résumé de cours écrit en texte simple :
  ■ TITRE        -> intertitre
  • élément      -> puce
  1. étape       -> étape numérotée
  [[schema:nom|Légende]] -> schéma MaxQuiz (game/static/game/schemas/nom.svg)
  autre ligne    -> paragraphe (les lignes vides sont ignorées)
Le texte est échappé ligne par ligne : aucun HTML saisi n'est interprété."""
import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from game.schemas import ligne_schema, url_schema

register = template.Library()


@register.filter
def fiche(text):
    out = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        sch = ligne_schema(line)
        if sch:
            nom, legende = sch
            alt = escape(legende or "Schéma")
            cap = f"<figcaption>{escape(legende)}</figcaption>" if legende else ""
            out.append(f'<figure class="fiche-fig"><img src="{escape(url_schema(nom))}" alt="{alt}" '
                       f'loading="lazy" decoding="async">{cap}</figure>')
        elif line.startswith("■") or line.startswith("## "):
            title = line.lstrip("■#").strip()
            out.append(f'<h3 class="fiche-h">{escape(title)}</h3>')
        elif line.startswith("• "):
            out.append(f'<p class="fiche-li"><span>•</span>{escape(line[2:])}</p>')
        elif re.match(r"^\d+\. ", line):
            n, rest = line.split(" ", 1)
            out.append(f'<p class="fiche-li"><span>{escape(n)}</span>{escape(rest)}</p>')
        else:
            indent = " fiche-in" if raw.startswith("   ") else ""
            out.append(f'<p class="fiche-p{indent}">{escape(line)}</p>')
    return mark_safe("\n".join(out))


@register.filter
def cherchable(text, limit=4000):
    """Texte normalisé pour la recherche instantanée : minuscules, sans accents,
    sans puces, espaces simplifiés (comparé au texte saisi, normalisé pareil)."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(text or ""))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"\[\[schema:[^\]]*\]\]", " ", t)
    t = re.sub(r"[■•#→⇔]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:int(limit)]
