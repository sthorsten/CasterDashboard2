from rest_framework import serializers
from . import models


class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    typeName = serializers.StringRelatedField(
        source='get_type_display', read_only=True)

    class Meta:
        model = models.Notification
        fields = '__all__'


class MapPoolSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    mapsName = serializers.StringRelatedField(
        source='maps', many=True, read_only=True)

    class Meta:
        model = models.MapPool
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Map
        fields = '__all__'


class BombSpotSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    mapMame = serializers.StringRelatedField(source='map', read_only=True)
    mapId = serializers.PrimaryKeyRelatedField(source='map', read_only=True)
    floorName = serializers.StringRelatedField(
        source='get_floor_display', read_only=True)

    class Meta:
        model = models.BombSpot
        fields = '__all__'


class OperatorSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Operator
        fields = '__all__'
