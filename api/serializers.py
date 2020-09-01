import json

import requests
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from PIL import Image
from django.utils.translation import gettext as _

from dashboard.models import *
from overlays.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']
        read_only_fields = fields


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


###
# Data Serializers / ViewSets
###

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'url', 'name', 'is_restricted', 'league_logo', 'light_logo', 'dark_logo']


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'url', 'name', 'league', 'official_season', 'start_date', 'end_date']


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'url', 'name', 'public', 'sponsor_logo', 'light_logo', 'dark_logo', 'league']


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'url', 'name', 'team_logo']


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_team = serializer.create(validated_data=serializer.validated_data)

                # Download logo from URL if present and no logo upload
                if not request.data['team_logo'] and request.data['team_logo_url']:
                    try:
                        # Download and save file
                        url = request.data['team_logo_url']
                        r = requests.get(url, allow_redirects=True)
                        save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(r.content)

                    except requests.RequestException as e:
                        print(e.messages[0])

                return Response(serializer.validated_data, status=201)

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

                    except requests.RequestException as e:
                        print(e.messages[0])

                return Response({"status": "ok"}, status=200)
            except ValidationError as e:
                return Response({"error": e.messages[0]}, status=400)

        else:
            return Response(data={"error": serializer.errors}, status=400)


'''
     Overlay Serializers
'''


class OverlayStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverlayState
        fields = ['start_state', 'ingame_state', 'maps_state', 'opbans_state', 'rounds_state', 'social_state',
                  'poll_state', 'timer_state', 'ticker_state', 'next_match_state']


class OverlayStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverlayStyle
        fields = ['start_style', 'ingame_style', 'opbans_style', 'maps_style', 'rounds_style', 'timer_style',
                  'next_match_style']


class TimerOverlayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerOverlayData
        fields = ['mode', 'value']


class MatchOverlayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchOverlayData
        fields = ['current_match', 'current_map', 'current_atk_team']


class NextMatchOverlayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextMatchOverlayData
        fields = ['match']


class MapBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapBan
        fields = ['map', 'type', 'order', 'team']


###
# Match Serializers / ViewSets
###

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'url', 'user', 'share_mode', 'season', 'league', 'title', 'subtitle', 'state', 'best_of',
                  'sponsors', 'team_blue', 'team_orange', 'score_blue', 'score_orange']


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MatchState
        fields = ['id', 'url', 'state']


class MatchStateViewSet(viewsets.ModelViewSet):
    queryset = MatchState.objects.all()
    serializer_class = MatchStateSerializer


class MapSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapSettings
        fields = ['atk_team', 'ot_atk_team', 'final_score_blue', 'final_score_orange']


class OperatorBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorBans
        fields = ['operator', 'team', 'order']


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ['round_no', 'bombspot', 'atk_team', 'def_team', 'win_type', 'win_team', 'score_blue', 'score_orange',
                  'notes']
