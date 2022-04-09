from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.League.objects.all()
    serializer_class = serializers.LeagueSerializer


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = serializers.SeasonSerializer


class PlaydayViewSet(viewsets.ModelViewSet):
    queryset = models.Playday.objects.all()
    serializer_class = serializers.PlaydaySerializer


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    filterset_fields = ['league', 'name', 'public']


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filterset_fields = ['name']
