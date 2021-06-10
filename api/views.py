import logging
import os
from pathlib import Path

import requests
from uuid import uuid4
from django.conf import settings as django_settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from pip._vendor import requests
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from api.filter import SeasonFilter
from dashboard.models.models import MatchMap, Profile, Map, MapPool, BombSpot, Operator, League, \
    LeagueGroup, Season, Sponsor, Team, Match, OperatorBans, Round, Notification, MatchGroup
from dashboard.models.serializers import OperatorBanSerializer, RoundSerializer, UserSerializer, \
    ProfileSerializer, MapSerializer, MapPoolSerializer, BombSpotSerializer, OperatorSerializer, \
    LeagueSerializer, LeagueGroupSerializer, SeasonSerializer, SponsorSerializer, TeamSerializer, \
    MatchSerializer, MatchMapSerializer, NotificationSerializer, MatchGroupSerializer
from overlays.models.models import MatchOverlayData, OverlayStyle, OverlayState, PollOverlayData, \
    SocialOverlayData, TimerOverlayData, TickerOverlayData
from overlays.models.serializers import MatchOverlayDataSerializer, OverlayStyleSerializer, \
    OverlayStateSerializer, PollOverlayDataSerializer, SocialOverlayDataSerializer, \
    TimerOverlayDataSerializer, TickerOverlayDataSerializer

logger = logging.getLogger(__name__)


# ViewSets

# region System data view sets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filterset_fields = ['user_id', 'confirmed']


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filterset_fields = ['type', 'show'],

# endregion


# region Core model view sets

class MapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filterset_fields = ['name']


class MapPoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPool.objects.all()
    serializer_class = MapPoolSerializer
    filterset_fields = ['name']


class BombSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BombSpot.objects.all()
    serializer_class = BombSpotSerializer
    filterset_fields = ['map', 'floor']


class OperatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    filterset_fields = ['side', 'name']


# endregion


# region Data model view sets

class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filterset_fields = ['name', 'is_restricted', 'has_custom_overlay']


class LeagueGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeagueGroup.objects.all()
    serializer_class = LeagueGroupSerializer
    filterset_fields = ['user', 'league', 'rank']


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_class = SeasonFilter


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filterset_fields = ['league', 'name', 'public']


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['name']

    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Creating new team...")

            try:
                new_team = serializer.create(
                    validated_data=serializer.validated_data)

                # Download logo from URL if present and no logo upload
                if not request.data.get('team_logo') and request.data.get('team_logo_url'):
                    try:
                        # Download and save file
                        logger.info("Downloading team logo...")
                        url = request.data['team_logo_url']
                        req = requests.get(url, allow_redirects=True)

                        temp_filename = f"{uuid4().hex}_temp.png"
                        save_path = os.path.join(
                            django_settings.MEDIA_ROOT, 'teams', temp_filename)
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(req.content)

                        logger.info(
                            f"Team logo downloaded from {url} to {temp_filename}")

                        new_team.team_logo = f"teams/{temp_filename}"
                        new_team.save()  # Renaming will be handled by the model receiver

                    except requests.RequestException as ex:
                        logger.error(ex)

                return Response({"status": "ok"}, status=201)

            except ValidationError as ex:
                logger.error({ex.messages[0]})
                return Response({"error": ex.messages[0]}, status=400)

        else:
            if serializer.errors['name'][0].code == "unique":
                logger.error("Team already exists.")
                return Response(data={"error": _('A team with this name already exists!')},
                                status=400)

            logger.error(serializer.errors)
            return Response(data={"error": serializer.errors}, status=400)

    def partial_update(self, request, *args, **kwargs):
        team = Team.objects.get(id=request.data.get("id"))
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                team = serializer.save()

                # Download logo from URL if present and no logo upload
                if not request.data['team_logo'] and request.data['team_logo_url']:
                    try:
                        # Download and save file
                        logger.info("Downloading team logo...")
                        url = request.data['team_logo_url']
                        req = requests.get(url, allow_redirects=True)

                        temp_filename = f"{uuid4().hex}_temp.png"
                        save_path = os.path.join(
                            django_settings.MEDIA_ROOT, 'teams', temp_filename)
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(req.content)

                        logger.info(
                            f"Team logo downloaded from {url} to {temp_filename}")

                        team.team_logo = f"teams/{temp_filename}"
                        team.save() # Renaming will be handled by the model receiver

                    except requests.RequestException as ex:
                        logger.error(ex)

                return Response({"status": "ok"}, status=200)
            except ValidationError as ex:
                logger.error({ex.messages[0]})
                return Response({"error": ex.messages[0]}, status=400)

        else:
            logger.error(serializer.errors)
            return Response(data={"error": serializer.errors}, status=400)


# endregion


# region Match model view sets

class MatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_fields = ['user']


class MatchMapViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = MatchMap.objects.all()
    serializer_class = MatchMapSerializer
    filterset_fields = ['match', 'map', 'status']

    # MapBan elements with a specific match id
    # URL: /api/match/<id>/maps
    @action(methods=['get'], detail=True)
    def match_maps(self, request, *args, **kwargs):
        match_id = int(kwargs['match_id'])
        queryset = MatchMap.objects.filter(match=match_id).all()
        if not queryset:
            return Response({"detail": _("Not found.")}, status=404)
        serializer = MatchMapSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class OperatorBansViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = OperatorBans.objects.all()
    serializer_class = OperatorBanSerializer
    filterset_fields = ['match', 'map']


class RoundViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    filterset_fields = ['match', 'map']

    def create(self, request, *args, **kwargs):
        data = request.data
        # Validate data
        if not data.get('match') or not data.get('map') or not data.get('win_type') or not data.get(
                'bomb_spot') or not data.get('win_team'):
            logger.error("Invalid round data!")    
            return Response({"required_fields":
                            ["match", "map", "bomb_spot", "win_type", "win_team"]},
                            status=400)

        # Get Match related data
        filtered_rounds = Round.objects.filter(match=data.get(
            'match'), map=data.get('map')).order_by('-round_no').all()
        match_map = MatchMap.objects.get(
            match=data.get('match'), map=data.get('map'))
        match_data = Match.objects.get(id=data.get('match'))

        # Round ID and Score
        if filtered_rounds and len(filtered_rounds) > 0:
            last_round = filtered_rounds[0]
            next_round_no = len(filtered_rounds) + 1
            score_blue = last_round.score_blue
            score_orange = last_round.score_orange
        else:
            next_round_no = 1
            score_blue = 0
            score_orange = 0

        if data.get('win_team') == match_data.team_blue.id:
            score_blue += 1
        else:
            score_orange += 1

        # Team constellation
        atk_team = match_map.atk_team
        if match_map.atk_team == match_data.team_blue:
            def_team = match_data.team_orange
        else:
            def_team = match_data.team_blue

        if next_round_no > 6:
            tmp = atk_team
            atk_team = def_team
            def_team = tmp

        serializer = RoundSerializer(
            data={'match': data.get('match'), 'map': data.get('map'), 'round_no': next_round_no,
                  'bomb_spot': data.get('bomb_spot'), 'atk_team': atk_team.id,
                  'def_team': def_team.id, 'of_team': data.get('of_team'),
                  'win_type': data.get('win_type'), 'win_team': data.get('win_team'),
                  'score_blue': score_blue, 'score_orange': score_orange,
                  'notes': data.get('notes')})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        logger.error("Invalid round data!")   
        return Response({"detail": "Invalid Data"}, status=400)


class MatchGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = MatchGroup.objects.all()
    serializer_class = MatchGroupSerializer
    filterset_fields = ['users', 'matches']


# endregion


# region overlay view sets

class OverlayStyleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = OverlayStyle.objects.all()
    serializer_class = OverlayStyleSerializer
    filterset_fields = ['user']


class OverlayStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = OverlayState.objects.all()
    serializer_class = OverlayStateSerializer
    filterset_fields = ['user']

    # // Deprecated
    # OverlayState elements with a specific user id
    # URL: /api/overlay/state/by_user/<id>/
    @action(methods=['get'], detail=True)
    def get_by_user(self, request, *args, **kwargs):
        user_id = int(kwargs['user_id'])
        queryset = OverlayState.objects.get(user=user_id)
        if not queryset:
            return Response({"detail": _("Not found.")}, status=404)
        serializer = OverlayStateSerializer(queryset)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def post_by_user(self, request, *args, **kwargs):
        user_id = int(kwargs['user_id'])
        queryset = OverlayState.objects.get(user=user_id)
        if not queryset:
            return Response({"detail": _("Not found.")}, status=404)
        serializer = OverlayStateSerializer(
            queryset, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "Invalid data."}, status=400)


class MatchOverlayDataViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MatchOverlayData.objects.all()
    serializer_class = MatchOverlayDataSerializer
    filterset_fields = ['user']


class PollOverlayDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PollOverlayData.objects.all()
    serializer_class = PollOverlayDataSerializer
    filterset_fields = ['user']


class SocialOverlayDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SocialOverlayData.objects.all()
    serializer_class = SocialOverlayDataSerializer
    filterset_fields = ['user']


class TimerOverlayDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = TimerOverlayData.objects.all()
    serializer_class = TimerOverlayDataSerializer
    filterset_fields = ['user']


class TickerOverlayDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = TickerOverlayData.objects.all()
    serializer_class = TickerOverlayDataSerializer
    filterset_fields = ['user']


# endregion


# region Various single api views

@api_view(['GET'])
@permission_classes([AllowAny])
def version(request):
    current_version = Path(os.path.join(
        django_settings.BASE_DIR, "VERSION")).read_text()
    return Response({'version': current_version})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if not django_settings.REGISTRATION_ENABLED:
        return Response({"status": "Registration disabled"}, status=503)

    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Validate input
    if not username or not email or not password or not first_name or not last_name:
        return Response({"status": "invalid data"}, status=400)

    logging.info(f"Creating new user: {username}...")

    # Check if user exists
    try:
        user = get_user_model().objects.get(username=username)
        logger.error(f"User '{username}' already exists!")
        return Response({"status": "duplicate user"}, status=400)
    except get_user_model().DoesNotExist:
        # All ok
        pass

    # Create user
    user = get_user_model().objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name, last_name=last_name)

    if user is not None:
        logging.info(f"User '{username}' registered successfully.")
        profile = Profile.objects.get(user=user)

        return Response({"status": "ok", "registration_token": profile.registration_token})
    else:
        logging.error(f"Registration for user '{username}' failed!")
        return Response({"status": "error", "message": "User could not be created."}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_confirm(request):
    if not django_settings.REGISTRATION_ENABLED:
        return Response({"status": "Registration disabled"}, status=503)

    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    data = request.data
    username = data.get('username')
    token = data.get('token')

    if not username or not token:
        return Response({"status": "invalid data"}, status=400)

    logger.info(f"Validating new user: {username}...")

    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        logger.error(f"User '{username}' does not exist!")
        return Response({"status": "user not found"}, status=400)

    user_profile = Profile.objects.get(user=user)
    if user_profile.registration_token == token:
        user_profile.confirmed = True

    user_profile.save()

    logger.info(f"User '{username}' validated successfully.")

    return Response({"status": "ok"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_user_data(request):
    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    # Check input data
    data = request.data
    if not data.get('user') or not data.get('email') or not data.get('first_name') or \
            not data.get('last_name'):
        return Response({'status': "Invalid Data"}, status=400)

    logger.info(f"Changing data for user: {data['user']}...")

    try:
        user = get_user_model().objects.get(id=data['user'])
    except get_user_model().DoesNotExist:
        logger.error(f"User '{data['user']}' does not exist!")
        return Response({'status': "Not Found"}, status=404)

    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']

    user.save()

    logger.info(f"User data for user {data['user']} updated successfully.")

    return Response({'status': "ok"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    # Check input data
    data = request.data
    if not data.get('username') or not data.get('current_password') or not data.get('new_password'):
        return Response({'status': "Invalid Data"}, status=400)

    logger.info(f"Changing password for user: {data['username']}...")

    # Check current password
    user = authenticate(
        username=data['username'], password=data['current_password'])
    if not user:
        logger.error(f"Current password for user '{data['username']}' is invalid!")
        return Response({'status': "Invalid current password"}, status=400)

    # Set new password
    user.set_password(data['new_password'])
    user.save()

    logger.info(f"The password for user '{data['username']}' has been changed successfully.")

    return Response({'status': "ok"}, status=200)


# endregion

# region Other views

@csrf_exempt
def share_match(request, match_id):
    if request.method != 'POST':
        return Response({"detail": "Method not allowed."}, status=405)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"detail": "Not found."}, status=404)
    
    data = request.POST.getlist('user')
    for elem in data:
        new_match_user = get_user_model().objects.get(id=elem)
        match.user.add(new_match_user)

    return Response({"detail": "ok"}, status=200)

# endregion
