from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member


class CustomDesignStyleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserOverlay.objects.all()
    serializer_class = serializers.UserOverlaySerializer


class UserOverlayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CustomDesignStyle.objects.all()
    serializer_class = serializers.CustomDesignStyleSerializer
