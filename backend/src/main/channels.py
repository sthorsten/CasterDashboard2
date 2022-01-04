from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from util import websocket

from . import models
from . import serializers


class MainConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("main", self.channel_name)

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

        if model == "League":
            response = websocket.make_query(
                models.League, content.get("query"), serializers.LeagueSerializer)

        elif model == "Season":
            response = websocket.make_query(
                models.Season, content.get("query"), serializers.SeasonSerializer)

        elif model == "Playday":
            response = websocket.make_query(
                models.Playday, content.get("query"), serializers.PlaydaySerializer)

        elif model == "Tournament":
            response = websocket.make_query(
                models.Tournament, content.get("query"), serializers.TournamentSerializer)

        elif model == "Sponsor":
            response = websocket.make_query(
                models.Sponsor, content.get("query"), serializers.SponsorSerializer)

        elif model == "Team":
            response = websocket.make_query(
                models.Team, content.get("query"), serializers.TeamSerializer)                

        else:
            self.send_json({"status": "Bad Request", "code": 400})
            return

        self.send_json(websocket.parse_request(model, response))
