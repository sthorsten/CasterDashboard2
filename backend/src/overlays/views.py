from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member


class OverlayStyleViewSet(viewsets.ModelViewSet):
    queryset = models.OverlayStyle.objects.all()
    serializer_class = serializers.OverlayStyleSerializer
    filterset_fields = ['user']


class OverlayStateViewSet(viewsets.ModelViewSet):
    queryset = models.OverlayState.objects.all()
    serializer_class = serializers.OverlayStateSerializer
    filterset_fields = ['user']


# class MatchOverlayDataViewSet(viewsets.ModelViewSet):
#     queryset = models.MatchOverlayData.objects.all()
#     serializer_class = serializers.MatchOverlayDataSerializer
#     filterset_fields = ['user']


class PollOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = models.PollOverlayData.objects.all()
    serializer_class = serializers.PollOverlayDataSerializer
    filterset_fields = ['user']


class SocialOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = models.SocialOverlayData.objects.all()
    serializer_class = serializers.SocialOverlayDataSerializer
    filterset_fields = ['user']


class TimerOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = models.TimerOverlayData.objects.all()
    serializer_class = serializers.TimerOverlayDataSerializer
    filterset_fields = ['user']


class TickerOverlayDataViewSet(viewsets.ModelViewSet):
    queryset = models.TickerOverlayData.objects.all()
    serializer_class = serializers.TickerOverlayDataSerializer
    filterset_fields = ['user']
