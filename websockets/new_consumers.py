import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

""" Django channels websocket consumers
    
    Description:
    Manages all websocket connections. All Consumers do not accept incoming messages
    Data is being send (1) when the connection is being opened by a client and (2) when being invoked by a receiver
    from one of the django models 

    Custom websocket status codes:
    4000: REJECTED => Connection was closed by the server due to an invalid request - as in HTTP 400 (Bad request)
"""

logger = logging.getLogger(__name__)


class MatchConsumer(JsonWebsocketConsumer):
    """ Provides match data over a websocket connection given a match id

        URL: /ws/match/<id>/
    """

    def connect(self):
        self.accept()

        # Set id
        try:
            self.id = int(self.scope['url_route']['kwargs']['id'])
        except ValueError:
            # Close connection if the provided match id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": f"Invalid match id: '{self.scope['url_route']['kwargs']['id']}'"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from dashboard.models.models import Match
        from dashboard.models.serializers import MatchSerializer

        # Set match
        try:
            match = Match.objects.get(id=self.id)
        except Match.DoesNotExist:
            # Close connection if the match with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"Match not found: {self.id}"})
            self.close(code=4000)
            return

        # Set channels group name
        self.group_name = 'match_' + str(self.id)

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match data back to connecting client
        self.send_json(MatchSerializer(match).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending match data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class MatchMapAllConsumer(JsonWebsocketConsumer):
    """ Provides all match maps data over a websocket connection given a match id

        URL: /ws/matches/<id>/maps/
    """

    def connect(self):
        self.accept()

        # Set id
        try:
            self.id = int(self.scope['url_route']['kwargs']['id'])
        except ValueError:
            # Close connection if the provided match id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": f"Invalid match id: '{self.scope['url_route']['kwargs']['id']}'"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from dashboard.models.models import MatchMap
        from dashboard.models.serializers import MatchMapSerializer

        # Get Match maps
        matchMaps = MatchMap.objects.filter(match=self.id)

        # Set channels group name
        self.group_name = f"matches_{str(self.id)}_maps"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(MatchMapSerializer(matchMaps, many=True).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending match map all data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class MatchMapSingleConsumer(JsonWebsocketConsumer):
    """ Provides match map data for a single map over a websocket connection given a match and a map id
        URL: /ws/matches/<id>/map/<id>/
    """

    def connect(self):
        self.accept()

        # Set match and map id
        try:
            self.match_id = int(self.scope['url_route']['kwargs']['match_id'])
            self.map_id = int(self.scope['url_route']['kwargs']['map_id'])
        except ValueError:
            # Close connection if the provided match or map id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": "Invalid match or map id!"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from dashboard.models.models import MatchMap
        from dashboard.models.serializers import MatchMapSerializer

        # Get Match maps
        matchMap = MatchMap.objects.get(match=self.match_id, map=self.map_id)

        # Set channels group name
        self.group_name = f"matches_{str(self.match_id)}_map_{str(self.map_id)}"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(MatchMapSerializer(matchMap).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending match map single data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class OpBansConsumer(JsonWebsocketConsumer):
    """ Provides round data for a specific match and map over a websocket connection
            URL: /ws/matches/<id>/map/<id>/opbans/
    """

    # Connect new client
    def connect(self):
        self.accept()

        # Set match and map id
        try:
            self.match_id = int(self.scope['url_route']['kwargs']['match_id'])
            self.map_id = int(self.scope['url_route']['kwargs']['map_id'])
        except ValueError:
            # Close connection if the provided match or map id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": "Invalid match or map id!"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from dashboard.models.models import OperatorBans
        from dashboard.models.serializers import OperatorBanSerializer

        # Get Match maps
        opbans = OperatorBans.objects.filter(match=self.match_id, map=self.map_id)

        # Set channels group name
        self.group_name = f"matches_{str(self.match_id)}_map_{str(self.map_id)}_opbans"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(OperatorBanSerializer(opbans, many=True).data)

    # Disconnect client
    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    # Send from group to client
    def send_to_client(self, event):
        logger.info(f"Sending operator ban data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class RoundConsumer(JsonWebsocketConsumer):
    """ Provides round data for a specific match and map over a websocket connection
        URL: /ws/matches/<id>/map/<id>/rounds/
    """

    # Connect new client
    def connect(self):
        self.accept()

        # Set match and map id
        try:
            self.match_id = int(self.scope['url_route']['kwargs']['match_id'])
            self.map_id = int(self.scope['url_route']['kwargs']['map_id'])
        except ValueError:
            # Close connection if the provided match or map id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": "Invalid match or map id!"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from dashboard.models.models import Round
        from dashboard.models.serializers import RoundSerializer

        # Get Match maps
        rounds = Round.objects.filter(match=self.match_id, map=self.map_id)

        # Set channels group name
        self.group_name = f"matches_{str(self.match_id)}_map_{str(self.map_id)}_rounds"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(RoundSerializer(rounds, many=True).data)

    # Disconnect client
    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    # Send from group to client
    def send_to_client(self, event):
        logger.info(f"Sending round data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


"""
    OLD

"""


class MatchDataConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'match_data_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from dashboard.models.serializers import MatchSerializer

        # Send data on request
        if content.get('command') == 'get_match_data':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            match = MatchOverlayData.objects.get(user=user_id).current_match

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchSerializer(match).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class MapDataConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'map_data_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from dashboard.models.serializers import MatchMapSerializer
        from dashboard.models.models import MatchMap

        # Send data on request
        if content.get('command') == 'get_map_data':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            match = MatchOverlayData.objects.get(user=user_id).current_match
            match_maps = MatchMap.objects.filter(match=match.id).all()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchMapSerializer(match_maps, many=True).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class MatchMapConsumer2(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'match_map_' + self.scope['url_route']['kwargs']['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from dashboard.models.models import MatchMap
        from dashboard.models.serializers import MatchMapSerializer

        # Send data on request
        if content.get('command') == 'get_match_map':
            user_id = User.objects.get(username=self.scope['url_route']['kwargs']['user']).id
            match = MatchOverlayData.objects.get(user=user_id).current_match
            try:
                match_map = MatchMap.objects.get(match=match, status=2)
            except MatchMap.DoesNotExist:
                return

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchMapSerializer(match_map).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class MatchMapConsumer3(JsonWebsocketConsumer):

    # Connect new client
    def connect(self):
        # Get room group
        self.group_name = 'match_map_' + self.scope['url_route']['kwargs']['match_map_id']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    # Disconnect client
    def disconnect(self, code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive from client and send to group
    def receive_json(self, content, **kwargs):
        from dashboard.models.models import MatchMap
        from dashboard.models.serializers import MatchMapSerializer

        # Send data on request
        if content.get('command') == 'get_match_map':
            match_map = MatchMap.objects.get(id=self.scope['url_route']['kwargs']['match_map_id'])

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_to_client',
                    'data': MatchMapSerializer(match_map).data
                }
            )

    # Send from group to client
    def send_to_client(self, event):
        self.send_json(event['data'])


class OverlayStateConsumer(JsonWebsocketConsumer):
    """ Provides match data over a websocket connection given a match id

        URL: /ws/overlays/state/<user_id>/
    """

    def connect(self):
        self.accept()

        # Set id
        try:
            self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        except ValueError:
            # Close connection if the provided match id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": f"Invalid user id: '{self.scope['url_route']['kwargs']['user_id']}'"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from django.contrib.auth.models import User
        from overlays.models.models import OverlayState
        from overlays.models.serializers import OverlayStateSerializer

        # Set match
        try:
            user = User.objects.get(id=self.user_id)
            overlay_state = OverlayState.objects.get(user=user)
        except User.DoesNotExist:
            # Close connection if the user with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"User not found: {self.user_id}"})
            self.close(code=4000)
            return
        except OverlayState.DoesNotExist:
            # Close connection if the OverlayState with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"OverlayState not found: {self.user_id}"})
            self.close(code=4000)
            return

        # Set channels group name
        self.group_name = 'overlay_state_' + str(self.user_id)

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match data back to connecting client
        self.send_json(OverlayStateSerializer(overlay_state).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending match data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class OverlayDataConsumer(JsonWebsocketConsumer):
    """ Provides the overlay data over a websocket connection given a user id

        URL: /ws/overlays/data/<user_id>/
    """

    def connect(self):
        self.accept()

        # Set id
        try:
            self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        except ValueError:
            # Close connection if the provided match id is not a valid number
            self.send_json(
                {"status": "Rejected", "reason": f"Invalid user id: '{self.scope['url_route']['kwargs']['user_id']}'"})
            self.close(code=4000)
            return

        # Local import to prevent circular imports
        from django.contrib.auth.models import User
        from overlays.models.models import MatchOverlayData
        from overlays.models.serializers import MatchOverlayDataSerializer

        # Set match
        try:
            user = User.objects.get(id=self.user_id)
            overlay_state = MatchOverlayData.objects.get(user=user)
        except User.DoesNotExist:
            # Close connection if the user with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"User not found: {self.user_id}"})
            self.close(code=4000)
            return
        except MatchOverlayData.DoesNotExist:
            # Close connection if the OverlayState with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"MatchOverlayData not found for user: {self.user_id}"})
            self.close(code=4000)
            return

        # Set channels group name
        self.group_name = 'overlay_data_' + str(self.user_id)

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match data back to connecting client
        self.send_json(MatchOverlayDataSerializer(overlay_state).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending match data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])
