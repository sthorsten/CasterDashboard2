import logging
from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member

logger = logging.getLogger(__name__)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer


class MapBanViewSet(viewsets.ModelViewSet):
    queryset = models.MapBan.objects.all()
    serializer_class = serializers.MapBanSerializer


class MatchMapViewSet(viewsets.ModelViewSet):
    queryset = models.MatchMap.objects.all()
    serializer_class = serializers.MatchMapSerializer


class OperatorBansViewSet(viewsets.ModelViewSet):
    queryset = models.OperatorBan.objects.all()
    serializer_class = serializers.OperatorBanSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = models.Round.objects.all()
    serializer_class = serializers.RoundSerializer
