from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from util import websocket

from . import models
from . import serializers


class MatchConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("match", self.channel_name)

        self.send_json({
            "status": "Accepted",
            "code": 202,
            "channel_name": self.channel_name,
            "group": "match"
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

        if model == "Match":
            response = websocket.make_query(
                models.Match, content.get("query"), serializers.MatchSerializer)

        elif model == "MapBan":
            response = websocket.make_query(
                models.MapBan, content.get("query"), serializers.MapBanSerializer)

        elif model == "MatchMap":
            response = websocket.make_query(
                models.MatchMap, content.get("query"), serializers.MatchMapSerializer)

        elif model == "OperatorBan":
            response = websocket.make_query(
                models.OperatorBan, content.get("query"), serializers.OperatorBanSerializer)

        elif model == "Round":
            response = websocket.make_query(
                models.Round, content.get("query"), serializers.RoundSerializer)

        else:
            self.send_json({"status": "Bad Request", "code": 400})
            return

        self.send_json(websocket.parse_request(model, response))
