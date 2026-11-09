from .models import GameConfig, Player


def nav(request):
    """Détermine si l'onglet Portefeuille a un sens à afficher : récompenses
    activées côté jeu public, ou un joueur qui a déjà un solde réel."""
    pid = request.session.get("player_id")
    player = Player.objects.filter(id=pid).first() if pid else None
    cfg = GameConfig.get()
    return {"nav_show_wallet": bool(cfg.rewards_enabled or (player and player.balance))}



def navigation(request):
    """nav_space : l'école dont on affiche la barre de navigation élève.
    L'école de l'adresse (/e/<slug>/…), sinon, sur les pages du compte,
    l'école réservée aux élèves dont le joueur connecté est membre."""
    from .models import Membership, Space
    space = None
    match = getattr(request, "resolver_match", None)
    slug = match.kwargs.get("slug") if match else None
    if slug:
        space = Space.objects.filter(slug=slug, active=True).first()
    elif request.path.startswith(("/compte/", "/notifications/", "/moi/", "/aide/")):
        pid = request.session.get("player_id")
        if pid:
            ms = list(Membership.objects.filter(player_id=pid, space__members_only=True, space__active=True)
                      .select_related("space").order_by("-created_at"))
            # L'espace MaxQuiz École d'abord : l'école rejointe s'ajoute, elle ne remplace pas.
            m = next((x for x in ms if x.space.kind == "catalog"), ms[0] if ms else None)
            space = m.space if m else None
    return {"nav_space": space}


def notifications(request):
    """Nombre de notifications non lues (cloche), pour un joueur ou un enseignant."""
    from .models import Notification
    pid, tid = request.session.get("player_id"), request.session.get("teacher_id")
    if not (pid or tid):
        return {"unread_notifs": None}
    qs = Notification.objects.filter(read_at__isnull=True)
    qs = qs.filter(player_id=pid) if pid else qs.filter(teacher_id=tid)
    return {"unread_notifs": qs.count()}


def product(request):
    """Produit servi (École ou Pro) et réglages utiles aux gabarits."""
    from django.conf import settings
    return {"product": getattr(request, "product", "ecole"),
            "pro_actif": settings.PRO_ACTIF,
            "jeu_public_actif": settings.JEU_PUBLIC_ACTIF,
            "catalog_slug": settings.CATALOG_SPACE_SLUG,
            "in_app": getattr(request, "in_app", False),
            "contact_email": getattr(settings, "CONTACT_EMAIL", ""),
            "store_build": getattr(request, "store_build", False)}


def ads(request):
    """Pixel Meta : identifiant, consentement et événements en attente (MaxQuiz École)."""
    from django.conf import settings
    staff_page = "/tableau-de-bord" in request.path or "/ressources/" in request.path or request.path.startswith("/admin/")
    in_app = getattr(request, "in_app", False)       # rien vers Meta depuis l'application installée
    if not settings.META_PIXEL_ID or getattr(request, "product", "ecole") != "ecole" or staff_page or in_app:
        return {"meta_pixel_id": ""}
    consent = request.COOKIES.get("mq_consent", "")
    events = []
    if consent == "1" and hasattr(request, "session") and request.session.get("pixel_events"):
        events = request.session.pop("pixel_events")
    return {"meta_pixel_id": settings.META_PIXEL_ID, "ad_consent": consent, "pixel_events": events}


def app_handoff(request):
    """Ouvrir l'application Android quand elle est installée (MaxQuiz École, pages élèves)."""
    from django.conf import settings
    staff_page = "/tableau-de-bord" in request.path or "/ressources/" in request.path or request.path.startswith("/admin/")
    pkg = getattr(settings, "ANDROID_PACKAGE_NAME", "")
    if staff_page or getattr(request, "product", "ecole") != "ecole" or not (pkg or settings.APK_URL):
        return {"android_package": ""}
    return {"android_package": pkg, "apk_url": settings.APK_URL}
