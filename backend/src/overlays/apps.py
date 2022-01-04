from django.apps import AppConfig


class OverlaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'overlays'

    def ready(self):
        import overlays.receivers
