"""Mise en forme d'un résumé de cours écrit en texte simple :
  ■ TITRE        -> intertitre
  • élément      -> puce
  1. étape       -> étape numérotée
  autre ligne    -> paragraphe (les lignes vides sont ignorées)
Le texte est échappé ligne par ligne : aucun HTML saisi n'est interprété."""
import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def fiche(text):
    out = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("■") or line.startswith("## "):
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
