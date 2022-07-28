from django.apps import AppConfig


class MatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'match'

    def ready(self):
        import match.socket
        import match.receivers
