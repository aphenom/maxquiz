"""Remontée des incidents par les téléphones et ordinateurs, page d'erreur et contrôle de santé."""
import json

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import incidents
from .stats import _ip

MAX_PAR_HEURE = 30          # par adresse IP


@csrf_exempt
@require_POST
def incident_navigateur(request):
    if len(request.body or b"") > 8000:
        return HttpResponse(status=413)
    key = f"incident-ip-{_ip(request)}"
    n = cache.get(key, 0)
    if n >= MAX_PAR_HEURE:
        return HttpResponse(status=204)
    cache.set(key, n + 1, 3600)
    try:
        data = json.loads(request.body or b"{}")
    except ValueError:
        return HttpResponse(status=400)
    if isinstance(data, dict):
        incidents.depuis_navigateur(request, data)
    return HttpResponse(status=204)


def sante(request):
    """Pour la surveillance externe (UptimeRobot…) : 200 si le site et la base répondent."""
    from django.db import connection
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
            c.fetchone()
    except Exception:
        return JsonResponse({"ok": False, "base": "injoignable"}, status=503)
    return JsonResponse({"ok": True})


PAGE_500 = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Petit souci · MaxQuiz</title>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#FDF6EC;color:#221A12;display:flex;min-height:100vh;
align-items:center;justify-content:center;padding:24px;box-sizing:border-box;text-align:center}
.c{max-width:380px}h1{font-size:24px;margin:12px 0 8px}p{line-height:1.5;color:#6E6152}
a{display:inline-block;margin-top:14px;background:#F2790F;color:#fff;text-decoration:none;font-weight:700;
padding:14px 22px;border-radius:12px}</style></head><body><div class="c"><div style="font-size:56px">🛠️</div>
<h1>Oups, un souci de notre côté</h1><p>Ce n'est pas ta faute. L'équipe MaxQuiz a été prévenue automatiquement
et s'en occupe. Réessaie dans quelques minutes.</p><a href="/">Revenir à l'accueil</a></div></body></html>"""


def erreur_500(request, *args, **kwargs):
    """Page d'erreur sans base de données ni gabarit (elle doit s'afficher même si tout va mal).
    L'incident lui-même est enregistré par le signal got_request_exception."""
    return HttpResponse(PAGE_500, status=500)
