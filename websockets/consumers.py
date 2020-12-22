import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer
from django.contrib.auth.models import User

from dashboard.models.models import Match
from overlays.models.models import OverlayState, MatchOverlayData
from overlays.models.serializers import OverlayStateSerializer, MatchOverlayDataSerializer
from websockets.helper import send_match_data_to_consumers


class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })


class OverlayStateConsumer(WebsocketConsumer):
    def get_state(self, data):
        if (self.user.id is None):
            if (data['user'] is not None):
                user = User.objects.get(username=data['user'])
                overlay_state = OverlayState.objects.get(user=user)

        else:
            overlay_state = OverlayState.objects.get(user=self.user)

        overlay_serializer = OverlayStateSerializer(overlay_state)
        self.send_state_message(overlay_serializer.data)

    def set_state(self, data):
        print("set_state")
        pass

    commands = {
        'get_state': get_state,
        'set_state': set_state,
    }

    def connect(self):
        self.user = self.scope['user']
        self.room_group_name = str(self.user) + '_overlay_state'
        print("Websocket connecting to room group " + self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("Websocket disconnecting from room group " + self.room_group_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

    # Send message back to the client
    def send_state_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    def send_message(self, event):
        message = event['message']

        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps(message)))


class MatchDataConsumer(WebsocketConsumer):
    def get_state(self, data):
        if (self.user.id is None):
            if (data['user'] is not None):
                user = User.objects.get(username=data['user'])
                match_overlay_data = MatchOverlayData.objects.get(user=user)
        else:
            match_overlay_data = MatchOverlayData.objects.get(user=self.user)

        match_overlay_data = MatchOverlayDataSerializer(match_overlay_data).data

        match = Match.objects.get(id=match_overlay_data['current_match'])
        send_match_data_to_consumers(match)

    commands = {
        'get_state': get_state,
    }

    def connect(self):
        self.user = self.scope['user']
        self.room_group_name = str(self.user) + '_match_data'

        print("Websocket connecting on channel " + self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("Websocket disconnecting from room group " + self.room_group_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

    # Send message back to the client
    def send_match_data_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    def send_message(self, event):
        message = event['message']

        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps(message)))
