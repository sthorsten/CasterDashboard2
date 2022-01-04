""" Overlay model serializers

This file contains all serialization for models in the overlays app.
Each serializer may has some extra <field>_name fields to have the name of a field be available in the API.
This improves readability in the API and reduces unnecessary API calls simply to get a name of a field which only
has an ID.

"""

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from . import models


class OverlayStyleSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.OverlayStyle
        fields = '__all__'


class OverlayStateSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.OverlayState
        fields = '__all__'


class MatchOverlayDataSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.MatchOverlayData
        fields = '__all__'


class PollOverlayDataSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.PollOverlayData
        fields = '__all__'


class SocialOverlayDataSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)
    type_name = StringRelatedField(source='get_type_display', read_only=True)

    class Meta:
        model = models.SocialOverlayData
        fields = '__all__'


class TimerOverlayDataSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)
    mode_name = StringRelatedField(source='get_mode_display', read_only=True)

    class Meta:
        model = models.TimerOverlayData
        fields = '__all__'


class TickerOverlayDataSerializer(serializers.HyperlinkedModelSerializer):
    id = PrimaryKeyRelatedField(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.TickerOverlayData
        fields = '__all__'
