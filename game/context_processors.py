from .models import GameConfig, Player


def nav(request):
    """Détermine si l'onglet Portefeuille a un sens à afficher : récompenses
    activées côté jeu public, ou un joueur qui a déjà un solde réel."""
    pid = request.session.get("player_id")
    player = Player.objects.filter(id=pid).first() if pid else None
    cfg = GameConfig.get()
    return {"nav_show_wallet": bool(cfg.rewards_enabled or (player and player.balance))}
