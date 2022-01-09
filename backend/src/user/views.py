from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api import views
from . import filters
from . import models
from . import serializers

User = get_user_model()

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filterset_class = filters.ProfileFilter


class LeagueAccessGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.LeagueAccessGroup.objects.all()
    serializer_class = serializers.LeagueAccessGroupSerializer
    filterset_fields = ['user', 'league', 'rank']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ['username']

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


class LoggedInUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.none()
    serializer_class = serializers.UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(serializers.UserSerializer(request.user).data)