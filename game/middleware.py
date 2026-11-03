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
