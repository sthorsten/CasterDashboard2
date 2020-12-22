""" Main model serializers

This file contains all serialization for models in the dashboard app.
Each serializer may has some extra <field>_name fields to have the name of a field be available in the API.
This improves readability in the API and reduces unnecessary API calls simply to get a name of a field which only
has an ID.

"""

from rest_framework import serializers

from dashboard.models.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class MapPoolSerializer(serializers.ModelSerializer):
    maps_name = serializers.StringRelatedField(source='maps', many=True, read_only=True)

    class Meta:
        model = MapPool
        fields = '__all__'


class BombSpotSerializer(serializers.ModelSerializer):
    map_name = serializers.StringRelatedField(source='map', read_only=True)
    floor_name = serializers.StringRelatedField(source='get_floor_display', read_only=True)

    class Meta:
        model = BombSpot
        fields = '__all__'


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class LeagueGroupSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user', read_only=True)
    league_name = serializers.StringRelatedField(source='league', read_only=True)
    rank_name = serializers.StringRelatedField(source='get_rank_display', read_only=True)

    class Meta:
        model = LeagueGroup
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    league_name = serializers.StringRelatedField(source='league', allow_null=True, read_only=True)
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Season
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    league_name = serializers.StringRelatedField(source='league', allow_null=True, read_only=True)

    class Meta:
        model = Sponsor
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user', many=True, read_only=True)
    share_mode_name = serializers.StringRelatedField(source='get_share_mode_display', read_only=True)
    season_name = serializers.StringRelatedField(source='season.name', read_only=True)
    league_name = serializers.StringRelatedField(source='league.name', read_only=True)
    sponsors_name = serializers.StringRelatedField(source='sponsors', many=True, read_only=True)
    state_name = serializers.StringRelatedField(source='get_state_display', read_only=True)
    team_blue_name = serializers.StringRelatedField(source='team_blue.name', read_only=True)
    team_orange_name = serializers.StringRelatedField(source='team_orange.name', read_only=True)
    win_team_name = serializers.StringRelatedField(source='win_team.name', allow_null=True, read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Match
        fields = '__all__'


class MatchMapSerializer(serializers.ModelSerializer):
    map_name = serializers.StringRelatedField(source='map', read_only=True)
    type_name = serializers.StringRelatedField(source='get_type_display', read_only=True)
    choose_team_name = serializers.StringRelatedField(source='choose_team', read_only=True)
    atk_team_name = serializers.StringRelatedField(source='atk_team', read_only=True)
    ot_atk_team_name = serializers.StringRelatedField(source='ot_atk_team', read_only=True)
    win_team_name = serializers.StringRelatedField(source='win_team', read_only=True)
    win_type_name = serializers.StringRelatedField(source='get_win_type_display', read_only=True)
    status_name = serializers.StringRelatedField(source='get_status_display', read_only=True)

    class Meta:
        model = MatchMap
        fields = '__all__'


class OperatorBanSerializer(serializers.ModelSerializer):
    map_name = serializers.StringRelatedField(source='map', read_only=True)
    operator_name = serializers.StringRelatedField(source='operator', read_only=True)
    operator_side = serializers.StringRelatedField(source='operator.side', read_only=True)
    team_name = serializers.StringRelatedField(source='team', read_only=True)

    class Meta:
        model = OperatorBans
        fields = '__all__'


class RoundSerializer(serializers.ModelSerializer):
    map_name = serializers.StringRelatedField(source='map', read_only=True)
    bombspot_name = serializers.StringRelatedField(source='bombspot', read_only=True)
    atk_team_name = serializers.StringRelatedField(source='atk_team', read_only=True)
    def_team_name = serializers.StringRelatedField(source='def_team', read_only=True)
    of_team_name = serializers.StringRelatedField(source='of_team', read_only=True)
    win_team_name = serializers.StringRelatedField(source='win_team', read_only=True)
    win_type_name = serializers.StringRelatedField(source='get_win_type_display', read_only=True)

    class Meta:
        model = Round
        fields = '__all__'
