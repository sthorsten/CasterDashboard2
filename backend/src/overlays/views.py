from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member


class UserOverlayViewSet(viewsets.ModelViewSet):
    queryset = models.UserOverlay.objects.all()
    serializer_class = serializers.UserOverlaySerializer


class CustomDesignStyleViewSet(viewsets.ModelViewSet):
    queryset = models.CustomDesignStyle.objects.all()
    serializer_class = serializers.CustomDesignStyleSerializer
