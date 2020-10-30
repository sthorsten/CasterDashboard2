import logging
import os

import requests
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db import DatabaseError
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from pip._vendor import requests
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from api.filter import SeasonFilter
from dashboard.models.models import MatchMap, Profile, Map, MapPool, BombSpot, Operator, League, LeagueGroup, Season, \
    Sponsor, Team, Match, OperatorBans, Round
from dashboard.models.serializers import OperatorBanSerializer, RoundSerializer, UserSerializer, ProfileSerializer, \
    MapSerializer, MapPoolSerializer, BombSpotSerializer, OperatorSerializer, LeagueSerializer, LeagueGroupSerializer, \
    SeasonSerializer, SponsorSerializer, TeamSerializer, MatchSerializer, MatchMapSerializer
from overlays.models import *
from overlays.models.models import MatchOverlayData, OverlayStyle, OverlayState, PollOverlayData, SocialOverlayData, \
    TimerOverlayData, TickerOverlayData
from overlays.models.serializers import MatchOverlayDataSerializer, OverlayStyleSerializer, OverlayStateSerializer, \
    PollOverlayDataSerializer, SocialOverlayDataSerializer, TimerOverlayDataSerializer, TickerOverlayDataSerializer

logger = logging.getLogger(__name__)


# ViewSets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class MapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class MapPoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPool.objects.all()
    serializer_class = MapPoolSerializer
    filterset_fields = ['name']


class BombSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BombSpot.objects.all()
    serializer_class = BombSpotSerializer


class OperatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class LeagueGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeagueGroup.objects.all()
    serializer_class = LeagueGroupSerializer
    filterset_fields = ['user', 'rank']


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_class = SeasonFilter


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_team = serializer.create(validated_data=serializer.validated_data)

                # Download logo from URL if present and no logo upload
                if not request.data.get('team_logo') and request.data.get('team_logo_url'):
                    try:
                        # Download and save file
                        url = request.data['team_logo_url']
                        r = requests.get(url, allow_redirects=True)
                        save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(r.content)

                        new_team.team_logo = "teams/%(id)s.png" % ({'id': new_team.id})
                        new_team.save()

                    except requests.RequestException as e:
                        print(e.messages[0])

                return Response({"status": "ok"}, status=201)

            except ValidationError as e:
                return Response({"error": e.messages[0]}, status=400)

        else:
            if serializer.errors['name'][0].code == "unique":
                return Response(data={"error": _('A team with this name already exists!')}, status=400)
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
                        url = request.data['team_logo_url']
                        r = requests.get(url, allow_redirects=True)
                        save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(team.id) + '.png')
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(r.content)

                        team.team_logo = "teams/%(id)s.png" % ({'id': team.id})
                        team.save()

                    except requests.RequestException as e:
                        print(e.messages[0])

                return Response({"status": "ok"}, status=200)
            except ValidationError as e:
                return Response({"error": e.messages[0]}, status=400)

        else:
            return Response(data={"error": serializer.errors}, status=400)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_fields = ['user']


class MatchMapViewSet(viewsets.ModelViewSet):
    queryset = MatchMap.objects.all()
    serializer_class = MatchMapSerializer
    filterset_fields = ['match', 'map']

    # MapBan elements with a specific match id
    # URL: /api/match/<id>/maps
    @action(methods=['get'], detail=True)
    def match_maps(self, request, *args, **kwargs):
        match_id = int(kwargs['match_id'])
        queryset = MatchMap.objects.filter(match=match_id).all()
        if not queryset:
            return Response({"detail": _("Not found.")}, status=404)
        serializer = MatchMapSerializer(queryset, many=True)
        return Response(serializer.data)


class OperatorBansViewSet(viewsets.ModelViewSet):
    queryset = OperatorBans.objects.all()
    serializer_class = OperatorBanSerializer
    filterset_fields = ['match', 'map']


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


# Overlay Views

class OverlayStyleViewSet(viewsets.ModelViewSet):
    queryset = OverlayStyle.objects.all()
    serializer_class = OverlayStyleSerializer


class OverlayStateViewSet(viewsets.ModelViewSet):
    queryset = OverlayState.objects.all()
    serializer_class = OverlayStateSerializer

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
        serializer = OverlayStateSerializer(queryset, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "Invalid data."}, status=400)


class MatchOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = MatchOverlayData.objects.all()
    serializer_class = MatchOverlayDataSerializer
    filterset_fields = ['user']


class PollOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = PollOverlayData.objects.all()
    serializer_class = PollOverlayDataSerializer


class SocialOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = SocialOverlayData.objects.all()
    serializer_class = SocialOverlayDataSerializer


class TimerOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = TimerOverlayData.objects.all()
    serializer_class = TimerOverlayDataSerializer


class TickerOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = TickerOverlayData.objects.all()
    serializer_class = TickerOverlayDataSerializer


# Other views

def get_current_match(request, user_id):
    try:
        match_overlay_data = MatchOverlayData.objects.get(user=user_id)
    except MatchOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = MatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    else:
        return JsonResponse(data={"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def set_current_match(request, user_id):
    try:
        match_overlay_data = MatchOverlayData.objects.get(user=user_id)
    except MatchOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = MatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MatchOverlayDataSerializer(match_overlay_data, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def update_match_score(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if data.get("score_blue") is not None:
            match.score_blue = data.get("score_blue")
        elif data.get("score_orange") is not None:
            match.score_orange = data.get("score_orange")
        else:
            return JsonResponse({"error": "Bad Request"}, status=400)

        try:
            match.save()
        except ValidationError:
            return JsonResponse({"error": "Internal Server Error"}, status=500)

        return JsonResponse({"status": "OK"})


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
        new_match_user = User.objects.get(id=elem)
        match.user.add(new_match_user)

    return Response({"detail": "ok"}, status=200)


@csrf_exempt
def swap_teams(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"team_blue": match.team_blue.id, "team_orange": match.team_orange.id})

    if request.method == 'POST':
        team_blue = match.team_blue
        match.team_blue = match.team_orange
        match.team_orange = team_blue
        match.save()

        return JsonResponse({"team_blue": match.team_blue.id, "team_orange": match.team_orange.id})


@csrf_exempt
def rounds(request, match_id, map_id):
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)
    map_settings = MapSettings.objects.get(match=match, map=map)

    rounds = Round.objects.filter(match=match, map=map).all()

    if request.method == 'GET':
        if len(rounds) == 0:
            return JsonResponse({"status": "Not Found"}, status=404)

        data = []
        for round in rounds:
            serializer = RoundSerializer(round)
            data.append(serializer.data)

        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        # Reset Round(s)
        if data.get('reset'):
            if data['reset'] == "single":
                last_round = rounds.last()
                last_round.delete()
            elif data['reset'] == "all":
                for round in rounds:
                    round.delete()

            return JsonResponse({"status": "ok"})

        # Check data
        if not data['bombspot'] or not data['win_type'] or not data['win_team'] or not data['of_team']:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            bombspot = BombSpot.objects.get(id=data['bombspot'])
        except BombSpot.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_type = WinType.objects.get(id=data['win_type'])
        except WinType.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_team = Team.objects.get(id=data['win_team'])
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            of_team = Team.objects.get(id=data['of_team'])
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        if not data.get('notes'):
            notes = None
        else:
            notes = data['notes']

        # Format data
        round_no = len(rounds) + 1

        # Set ATK / DEF team for round
        if round_no <= 6:
            atk_team = map_settings.atk_team
            if atk_team == match.team_blue:
                def_team = match.team_orange
            else:
                def_team = match.team_blue

        elif 6 < round_no <= 12:
            def_team = map_settings.atk_team
            if def_team == match.team_blue:
                atk_team = match.team_orange
            else:
                atk_team = match.team_blue

        # Odd OT Rounds (13, 15, ...)
        elif round_no > 12 and (round_no % 2 != 0):
            atk_team = map_settings.ot_atk_team
            if atk_team == match.team_blue:
                def_team = match.team_orange
            else:
                def_team = match.team_blue

        # Even OT Rounds (14, 16, ...)
        else:
            def_team = map_settings.ot_atk_team
            if def_team == match.team_blue:
                atk_team = match.team_orange
            else:
                atk_team = match.team_blue

        # Set Score
        if round_no <= 1:
            score_blue = 0
            score_orange = 0
        else:
            score_blue = rounds.last().score_blue
            score_orange = rounds.last().score_orange

        if win_team == match.team_blue:
            score_blue += 1
        else:
            score_orange += 1

        new_round = Round(match=match, map=map, round_no=round_no, bombspot=bombspot, atk_team=atk_team,
                          def_team=def_team, of_team=of_team, win_type=win_type, win_team=win_team,
                          score_blue=score_blue, score_orange=score_orange, notes=notes)

        try:
            new_round.save()
        except DatabaseError:
            return JsonResponse({"error": "Database Error"}, status=500)

        messages.success(request, _('The round has been added successfully'))
        return JsonResponse({"status": "ok"})


@csrf_exempt
def finish_map(request, match_id, map_id):
    if request.method == 'GET':
        return JsonResponse({"status": "Method Not Allowed"}, status=405)

    data = JSONParser().parse(request)

    if data.get('finish_map'):
        match = Match.objects.get(id=match_id)
        map = Map.objects.get(id=map_id)
        last_round = Round.objects.filter(match=match, map=map).last()

        if last_round.score_blue > last_round.score_orange:
            win_team = match.team_blue
            match.score_blue += 1
        elif last_round.score_orange > last_round.score_blue:
            win_team = match.team_orange
            match.score_orange += 1
        else:
            win_team = None

        map_win = MapWins(match=match, map=map, win_team=win_team)
        current_map_ban = MatchMap.objects.get(match=match, map=map)
        current_map_ban.status = 3  # Set map status to Finished (3)
        map_win.save()
        match.save()
        current_map_ban.save()

        # Set Next URL
        map_win_len = len(MapWins.objects.filter(match=match).all())
        if match.best_of == 1:
            match.state = MatchState.objects.get(id=8)
            match.save()
            next_url = "/dashboard/matches/%s" % match.id

        else:
            if map_win_len >= match.best_of:
                match.state = MatchState.objects.get(id=8)
                match.save()
                next_url = "/dashboard/matches/%s" % match.id
            else:
                next_map = MatchMap.objects.get(match=match, play_order=(map_win_len + 1))
                match.state = MatchState.objects.get(id=(2 + next_map.order))
                match.save()
                next_url = "/dashboard/matches/%s/map/%s/opbans" % (match.id, next_map.map.id)

        messages.info(request, _('Match Finished!'))
        return JsonResponse({"status": "ok", "next_url": next_url})

    else:
        return JsonResponse({"status": "Bad Request"}, status=400)
