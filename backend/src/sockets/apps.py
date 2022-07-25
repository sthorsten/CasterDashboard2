from django.apps import AppConfig


class SocketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sockets'

    def ready(self):
        import sockets.sio_server
