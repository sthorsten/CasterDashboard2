"""
ASGI config for caster_dashboard_2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
import socketio
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caster_dashboard_2.settings')
django.setup()


def setup_app():
    django.setup()
    from sockets.sio_server import sio
    return socketio.ASGIApp(sio, get_asgi_application())


application = setup_app()

# def get_sio_application():
#     return socketio.ASGIApp(sio, get_asgi_application())

# def get_app():
#     from sockets.sio_server import get_sio_application
#     return get_sio_application()


# application = get_app()
