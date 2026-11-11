from django.conf import settings


class ProductMiddleware:
    """request.product : « pro » sur pro.maxquiz.net (préfixe PRO_HOST_PREFIX),
    « ecole » partout ailleurs (maxquiz.net, l'APK, localhost)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        request.product = "pro" if host.startswith(settings.PRO_HOST_PREFIX) else "ecole"
        src = request.GET.get("source", "")
        if src in ("app", "play") and hasattr(request, "session"):
            request.session["app_channel"] = src     # ouvert depuis l'APK du site ou la version Play Store
        channel = request.session.get("app_channel", "") if hasattr(request, "session") else ""
        request.in_app = bool(channel)
        request.store_build = False
        if channel == "play":
            from .models import GameConfig
            request.store_build = not GameConfig.get().play_payments_enabled
        if request.product == "ecole":
            from .meta import capture
            capture(request)            # provenance publicitaire (utm_*, fbclid), premier contact
        return self.get_response(request)


class VisiteEleveMiddleware:
    """Note la visite d'un élève (au plus toutes les 10 minutes) : remet à zéro le compteur
    de rappels ignorés et marque la mission du jour comme ouverte après un rappel."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            pid = request.session.get("verified_player_id") if hasattr(request, "session") else None
            if pid and response.status_code < 400 and not request.path.startswith(("/admin/", "/api/", "/static/")):
                import time as _t
                if _t.time() - request.session.get("vu_le", 0) > 600:
                    request.session["vu_le"] = _t.time()
                    from .engagement import noter_visite
                    from .models import Player
                    noter_visite(Player(id=pid))
        except Exception:                                   # la mesure ne doit jamais casser une page
            pass
        return response
