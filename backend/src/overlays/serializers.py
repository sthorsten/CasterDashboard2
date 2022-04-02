""" Overlay model serializers

This file contains all serialization for models in the overlays app.
Each serializer may has some extra <field>_name fields to have the name of a field be available in the API.
This improves readability in the API and reduces unnecessary API calls simply to get a name of a field which only
has an ID.

"""

from rest_framework import serializers

from . import models


class CustomDesignStyleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    leagueName = serializers.StringRelatedField(
        source='league', allow_null=True, read_only=True)

    class Meta:
        model = models.CustomDesignStyle
        fields = '__all__'


class UserOverlaySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    userName = serializers.StringRelatedField(source='user', read_only=True)
    overlayLeagueName = serializers.StringRelatedField(
        source='league', read_only=True)

    class Meta:
        model = models.UserOverlay
        fields = '__all__'
