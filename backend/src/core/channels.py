from asgiref.sync import async_to_sync
from channels.auth import login
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import authenticate
from util import websocket

from . import models
from . import serializers


class CoreConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("core", self.channel_name)

        self.send_json({
            "status": "Accepted",
            "code": 202,
            "channel_name": self.channel_name,
            "group": "core"
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

        if model == "Notification":
            response = websocket.make_query(
                models.Notification, content.get("query"), serializers.NotificationSerializer)

        elif model == "Map":
            response = websocket.make_query(
                models.Map, content.get("query"), serializers.MapSerializer)

        elif model == "MapPool":
            response = websocket.make_query(
                models.MapPool, content.get("query"), serializers.MapPoolSerializer)

        elif model == "BombSpot":
            response = websocket.make_query(
                models.BombSpot, content.get("query"), serializers.BombSpotSerializer)

        elif model == "Operator":
            response = websocket.make_query(
                models.Operator, content.get("query"), serializers.OperatorSerializer)

        else:
            self.send_json({"status": "Bad Request", "code": 400})
            return

        self.send_json(websocket.parse_request(model, response))
