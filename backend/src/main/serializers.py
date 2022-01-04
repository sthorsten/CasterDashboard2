from rest_framework import serializers
from . import models


class LeagueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.League
        fields = '__all__'


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    league_id = serializers.PrimaryKeyRelatedField(
        source='league', read_only=True)
    league_name = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = models.Season
        fields = '__all__'


class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    league_id = serializers.PrimaryKeyRelatedField(
        source='league', read_only=True)
    league_name = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)

    class Meta:
        model = models.Sponsor
        fields = '__all__'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Team
        fields = '__all__'
