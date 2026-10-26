from django.conf import settings


class ProductMiddleware:
    """request.product : « pro » sur pro.maxquiz.net (préfixe PRO_HOST_PREFIX),
    « ecole » partout ailleurs (maxquiz.net, l'APK, localhost)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        request.product = "pro" if host.startswith(settings.PRO_HOST_PREFIX) else "ecole"
        return self.get_response(request)
