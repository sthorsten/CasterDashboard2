from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import websockets.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),

    'websocket': AuthMiddlewareStack(
        URLRouter(
            websockets.routing.websocket_urlpatterns
        )
    ),
})
