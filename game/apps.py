from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'

    def ready(self):
        from django.core.signals import got_request_exception

        from .incidents import erreur_serveur
        got_request_exception.connect(erreur_serveur, dispatch_uid="maxquiz-incidents")
