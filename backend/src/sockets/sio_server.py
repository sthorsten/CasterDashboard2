import socketio
from asgiref.sync import sync_to_async
from rest_framework.authtoken.models import Token


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event(namespace="/core")
async def connect(sid, environ, auth):
    print("SocketIO connect (core): ", sid)

    # Validate auth token
    try:
        await sync_to_async(Token.objects.get)(key=auth.get("token"))
    except Token.DoesNotExist:
        raise ConnectionRefusedError("Authorization failed")
