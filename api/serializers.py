from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from overlays.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''
     Overlay Serializers
'''


class OverlayStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverlayState
        fields = ['start_state', 'ingame_state', 'maps_state', 'opbans_state', 'rounds_state', 'social_state',
                  'poll_state', 'timer_state', 'ticker_state', 'next_match_state']


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

