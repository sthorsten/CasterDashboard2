from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from util import websocket

from . import models
from . import serializers


class OverlaysConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "overlays", self.channel_name)

        self.send_json({
            "status": "Accepted",
            "code": 202,
            "channel_name": self.channel_name,
            "group": "overlays"
        })

    def server_data(self, event):
        data = event.get("data")
        if data:
            self.send_json(data)

    def receive_json(self, content, **kwargs):
        if content.get("method") != "get":
            self.send_json({"status": "Method Not Allowed", "code": 405})
            return

        if not content.get("model"):
            self.send_json({"status": "Bad Request", "code": 400})
            return

        model = content.get("model")

        if model == "CustomDesignStyle":
            response = websocket.make_query(
                models.CustomDesignStyle, content.get("query"), serializers.CustomDesignStyleSerializer)

        elif model == "UserOverlay":
            response = websocket.make_query(
                models.UserOverlay, content.get("query"), serializers.UserOverlaySerializer)

        else:
            self.send_json({"status": "Bad Request", "code": 400})
            return

        self.send_json(websocket.parse_request(model, response))
