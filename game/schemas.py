"""Schémas et images des cours et des quiz.

Les schémas MaxQuiz sont des SVG dans game/static/game/schemas/ (fabriqués par
contenu/schemas.py). Dans une fiche, une ligne « [[schema:thales|Légende]] » les affiche ;
une question les désigne par son champ « illustration » (nom du schéma ou adresse https)."""
import re

from django.templatetags.static import static

NOM = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")
LIGNE = re.compile(r"^\[\[schema:([a-z0-9-]+)(?:\|(.*))?\]\]$")


def url_schema(valeur):
    v = (valeur or "").strip()
    if v.startswith("https://"):
        return v
    if NOM.match(v):
        return static(f"game/schemas/{v}.svg")
    return ""


def ligne_schema(ligne):
    """(nom, légende) si la ligne de fiche est un schéma, sinon None."""
    m = LIGNE.match(ligne.strip())
    return (m.group(1), (m.group(2) or "").strip()) if m else None
