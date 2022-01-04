from rest_framework import serializers
from . import models


class LeagueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.League
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    leagueName = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)
    startDate = serializers.DateField(format="%Y-%m-%d")
    endDate = serializers.DateField(format="%Y-%m-%d")
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Season
        fields = '__all__'


class PlaydaySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    seasonName = serializers.StringRelatedField(
        source='season.name', allow_null=True, read_only=True)
    leagueName = serializers.StringRelatedField(
        source='season.league', allow_null=True, read_only=True)
    date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Playday
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    leagueName = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)
    startDate = serializers.DateField(format="%Y-%m-%d")
    endDate = serializers.DateField(format="%Y-%m-%d")
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Tournament
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    leagueName = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Sponsor
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastModified = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Team
        fields = '__all__'
