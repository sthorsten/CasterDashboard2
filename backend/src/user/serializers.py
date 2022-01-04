from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'user_permissions']


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    user_name = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = models.Profile
        exclude = ['registration_token']


class LeagueAccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeagueAccessGroup
        fields = '__all__'
