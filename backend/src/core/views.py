from rest_framework import viewsets
from . import filters
from . import models
from . import serializers


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    filterset_fields = ['show']


class MapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Map.objects.all()
    serializer_class = serializers.MapSerializer
    filterset_fields = ['name']


class MapPoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.MapPool.objects.all()
    serializer_class = serializers.MapPoolSerializer
    filterset_fields = ['name']


class BombSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.BombSpot.objects.all()
    serializer_class = serializers.BombSpotSerializer
    filterset_class = filters.BombSpotFilter


class OperatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Operator.objects.all()
    serializer_class = serializers.OperatorSerializer
    filterset_fields = ['side', 'name', 'identifier']
