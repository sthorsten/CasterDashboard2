""" Overlay model serializers

This file contains all serialization for models in the overlays app.
Each serializer may has some extra <field>_name fields to have the name of a field be available in the API.
This improves readability in the API and reduces unnecessary API calls simply to get a name of a field which only
has an ID.

"""

from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from overlays.models.models import OverlayStyle, OverlayState, MatchOverlayData, PollOverlayData, SocialOverlayData, \
    TimerOverlayData, TickerOverlayData


class OverlayStyleSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = OverlayStyle
        fields = '__all__'


class OverlayStateSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = OverlayState
        fields = '__all__'


class MatchOverlayDataSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = MatchOverlayData
        fields = '__all__'


class PollOverlayDataSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = PollOverlayData
        fields = '__all__'


class SocialOverlayDataSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)
    type_name = StringRelatedField(source='get_type_display', read_only=True)

    class Meta:
        model = SocialOverlayData
        fields = '__all__'


class TimerOverlayDataSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)
    mode_name = StringRelatedField(source='get_mode_display', read_only=True)

    class Meta:
        model = TimerOverlayData
        fields = '__all__'


class TickerOverlayDataSerializer(serializers.ModelSerializer):
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = TickerOverlayData
        fields = '__all__'
