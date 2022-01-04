from rest_framework import viewsets
from . import filters
from . import models
from . import serializers


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filterset_class = filters.ProfileFilter


class LeagueAccessGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.LeagueAccessGroup.objects.all()
    serializer_class = serializers.LeagueAccessGroupSerializer
    filterset_fields = ['user', 'league', 'rank']
