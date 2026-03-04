from django.apps import AppConfig

class BadgesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.badges'

    def ready(self):
        import apps.badges.signals # Active les signaux au démarrage
