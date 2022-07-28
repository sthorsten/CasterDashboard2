import socketio
from asgiref.sync import sync_to_async
from rest_framework.authtoken.models import Token


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.on("connect", namespace="/core")
async def core_connect(sid, environ, auth):
    print("SocketIO connect (core): ", sid)

    # Validate auth token
    try:
        await sync_to_async(Token.objects.get)(key=auth.get("token"))
    except Token.DoesNotExist:
        raise ConnectionRefusedError("Authorization failed")


@sio.on("connect", namespace="/main")
async def main_connect(sid, environ, auth):
    print("SocketIO connect (main): ", sid)

   # Validate auth token
    try:
        await sync_to_async(Token.objects.get)(key=auth.get("token"))
    except Token.DoesNotExist:
        raise ConnectionRefusedError("Authorization failed")


@sio.on("connect", namespace="/match")
async def match_connect(sid, environ, auth):
    print("SocketIO connect (match): ", sid)

   # Validate auth token
    try:
        await sync_to_async(Token.objects.get)(key=auth.get("token"))
    except Token.DoesNotExist:
        raise ConnectionRefusedError("Authorization failed")
