""" Django channels websocket consumers

    Description:
    Manages all websocket connections. All Consumers do not accept incoming messages
    Data is being send (1) when the connection is being opened by a client and (2) when being invoked by a receiver
    from one of the django models

    Custom websocket status codes:
    4000: REJECTED => Connection was closed by the server due to an invalid request - as in HTTP 400 (Bad request)
"""

# pylint: disable=attribute-defined-outside-init

import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from django.contrib.auth import get_user_model

from dashboard.models.models import Match, MatchMap, OperatorBans, Round
from dashboard.models.serializers import MatchSerializer, MatchMapSerializer, \
    OperatorBanSerializer, RoundSerializer, MatchGroupSerializer
from overlays.models.models import MatchOverlayData, OverlayState, TickerOverlayData
from overlays.models.serializers import OverlayStateSerializer, MatchOverlayDataSerializer, \
    TickerOverlayDataSerializer


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
                {"status": "Rejected",
                 "reason": f"Invalid match id: '{self.scope['url_route']['kwargs']['id']}'"})
            self.close(code=4000)
            return

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
        logger.info(
            f"Sending match data to websocket clients: {self.group_name}")
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
                {"status": "Rejected",
                 "reason": f"Invalid match id: '{self.scope['url_route']['kwargs']['id']}'"})
            self.close(code=4000)
            return

        # Get Match maps
        match_maps = MatchMap.objects.filter(match=self.id).order_by('order')

        # Set channels group name
        self.group_name = f"matches_{str(self.id)}_maps"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(MatchMapSerializer(match_maps, many=True).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(
            f"Sending match map all data to websocket clients: {self.group_name}")
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

        # Get Match maps
        match_map = MatchMap.objects.get(match=self.match_id, map=self.map_id)

        # Set channels group name
        self.group_name = f"matches_{str(self.match_id)}_map_{str(self.map_id)}"

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send match maps back to connecting client
        self.send_json(MatchMapSerializer(match_map).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(
            f"Sending match map single data to websocket clients: {self.group_name}")
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

        # Get Match maps
        opbans = OperatorBans.objects.filter(
            match=self.match_id, map=self.map_id)

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
        logger.info(
            f"Sending operator ban data to websocket clients: {self.group_name}")
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
        logger.info(
            f"Sending round data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])


class MatchGroupConsumer(JsonWebsocketConsumer):
    """ Provides the match group data over a websocket connection given a user id

        URL: /ws/match_group/<user_id>/
    """

    def connect(self):
        self.accept()

        # Set id
        try:
            self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        except ValueError:
            # Close connection if the provided match id is not a valid number
            self.send_json(
                {"status": "Rejected",
                 "reason": f"Invalid user id: '{self.scope['url_route']['kwargs']['user_id']}'"})
            self.close(code=4000)
            return

        # Set match
        try:
            user = get_user_model().objects.get(id=self.user_id)
            overlay_data = MatchOverlayData.objects.get(user=user)
            match_group = overlay_data.match_group
        except get_user_model().DoesNotExist:
            # Close connection if the user with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"User not found: {self.user_id}"})
            self.close(code=4000)
            return
        except MatchOverlayData.DoesNotExist:
            # Close connection if the OverlayState with the specified id does not exists
            self.send_json(
                {"status": "Rejected",
                 "reason": f"MatchOverlayData not found for user: {self.user_id}"})
            self.close(code=4000)
            return

        # Set channels group name
        self.group_name = 'match_group_' + str(self.user_id)

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send data back to connecting client
        self.send_json(MatchGroupSerializer(match_group).data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(f"Sending data to websocket clients: {self.group_name}")
        # Relay message from group to client
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
                {"status": "Rejected",
                 "reason": f"Invalid user id: '{self.scope['url_route']['kwargs']['user_id']}'"})
            self.close(code=4000)
            return

        # Set match
        try:
            user = get_user_model().objects.get(id=self.user_id)
            overlay_state = OverlayState.objects.get(user=user)
        except get_user_model().DoesNotExist:
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
        logger.info(
            f"Sending match data to websocket clients: {self.group_name}")
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
                {"status": "Rejected",
                 "reason": f"Invalid user id: '{self.scope['url_route']['kwargs']['user_id']}'"})
            self.close(code=4000)
            return

        # Set match
        try:
            user = get_user_model().objects.get(id=self.user_id)
            match_overlay_data = MatchOverlayData.objects.get(user=user)
            ticker_overlay_data = TickerOverlayData.objects.get(user=user)
        except get_user_model().DoesNotExist:
            # Close connection if the user with the specified id does not exists
            self.send_json(
                {"status": "Rejected", "reason": f"User not found: {self.user_id}"})
            self.close(code=4000)
            return
        except MatchOverlayData.DoesNotExist:
            # Close connection if the OverlayState with the specified id does not exists
            self.send_json(
                {"status": "Rejected",
                 "reason": f"MatchOverlayData not found for user: {self.user_id}"})
            self.close(code=4000)
            return

        # Set channels group name
        self.group_name = 'overlay_data_' + str(self.user_id)

        # Add group django channels
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Send data back to connecting client
        data = {
            "match_overlay_data": MatchOverlayDataSerializer(match_overlay_data).data,
            "ticker_overlay_data": TickerOverlayDataSerializer(ticker_overlay_data).data
        }

        self.send_json(data)

    def disconnect(self, code):
        # Leave channels group
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_to_client(self, event):
        logger.info(
            f"Sending match data to websocket clients: {self.group_name}")
        # Relay message from group to client
        self.send_json(event['data'])
