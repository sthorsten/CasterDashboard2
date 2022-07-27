import logging
import os
from pathlib import Path

from django.conf import settings as django_settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from user.serializers import UserSerializer

logger = logging.getLogger(__name__)


# ViewSets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


@api_view((['POST']))
@permission_classes([AllowAny])
def token_auth(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not data:
        return Response({"error": "No credentials provided"}, status=400)
    if not username or not password:
        return Response({"error": "No credentials provided"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    token = Token.objects.get(user=user)
    serialized_user = UserSerializer(user)

    return Response({"token": token.key, "user": serialized_user.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def version(request):
    current_version = Path(os.path.join(
        django_settings.BASE_DIR, "..", "VERSION")).read_text()
    return Response({'version': current_version})
