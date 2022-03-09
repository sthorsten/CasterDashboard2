
from rest_framework import serializers
from . import models


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    creatorName = serializers.StringRelatedField(
        source='creator', allow_null=True, read_only=True)
    leagueName = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)
    playdayName = serializers.StringRelatedField(
        source='playday.name', allow_null=True, read_only=True)
    tournamentName = serializers.StringRelatedField(
        source='tournament', allow_null=True, read_only=True)
    teamBlueName = serializers.StringRelatedField(
        source='teamBlue', allow_null=True, read_only=True)
    teamOrangeName = serializers.StringRelatedField(
        source='teamOrange', allow_null=True, read_only=True)
    winTeamName = serializers.StringRelatedField(
        source='winTeam', allow_null=True, read_only=True)
    date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Match
        fields = '__all__'


class MapBanSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    teamName = serializers.StringRelatedField(
        source='team', allow_null=True, read_only=True)
    mapName = serializers.StringRelatedField(
        source='map', allow_null=True, read_only=True)

    class Meta:
        model = models.MapBan
        fields = '__all__'


class MatchMapSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    mapName = serializers.StringRelatedField(source='map', read_only=True)

    atkTeamName = serializers.StringRelatedField(
        source='atkTeam', read_only=True)
    defTeamName = serializers.StringRelatedField(
        source='defTeam', read_only=True)
    otAtkTeamName = serializers.StringRelatedField(
        source='otAtkTeam', read_only=True)
    otDefTeamName = serializers.StringRelatedField(
        source='otDefTeam', read_only=True)
    winTeamName = serializers.StringRelatedField(
        source='winTeam', read_only=True)

    class Meta:
        model = models.MatchMap
        fields = '__all__'


class OperatorBanSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    operatorName = serializers.StringRelatedField(
        source='operator', read_only=True)
    operatorIdentifier = serializers.StringRelatedField(
        source='operator.identifier', read_only=True)
    teamName = serializers.StringRelatedField(
        source='team', read_only=True)

    class Meta:
        model = models.OperatorBan
        fields = '__all__'


class RoundSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    bombSpotName = serializers.StringRelatedField(
        source='bombSpot.name', read_only=True)
    openingFragTeamName = serializers.StringRelatedField(
        source='openingFragTeam', read_only=True)
    winTeamName = serializers.StringRelatedField(
        source='winTeam', read_only=True)

    class Meta:
        model = models.Round
        fields = '__all__'
