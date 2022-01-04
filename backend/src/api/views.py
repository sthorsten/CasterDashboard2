import logging
import os
from pathlib import Path

from django.conf import settings as django_settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from user.serializers import UserSerializer

logger = logging.getLogger(__name__)


# ViewSets

# region System data view sets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


# endregion


# region Various single api views

@api_view(['GET'])
@permission_classes([AllowAny])
def version(request):
    current_version = Path(os.path.join(
        django_settings.BASE_DIR, "VERSION")).read_text()
    return Response({'version': current_version})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if not django_settings.REGISTRATION_ENABLED:
        return Response({"status": "Registration disabled"}, status=503)

    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Validate input
    if not username or not email or not password or not first_name or not last_name:
        return Response({"status": "invalid data"}, status=400)

    logging.info(f"Creating new user: {username}...")

    # Check if user exists
    try:
        user = get_user_model().objects.get(username=username)
        logger.error(f"User '{username}' already exists!")
        return Response({"status": "duplicate user"}, status=400)
    except get_user_model().DoesNotExist:
        # All ok
        pass

    # Create user
    user = get_user_model().objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name, last_name=last_name)

    if user is not None:
        logging.info(f"User '{username}' registered successfully.")
        profile = Profile.objects.get(user=user)

        return Response({"status": "ok", "registration_token": profile.registration_token})
    else:
        logging.error(f"Registration for user '{username}' failed!")
        return Response({"status": "error", "message": "User could not be created."}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_confirm(request):
    if not django_settings.REGISTRATION_ENABLED:
        return Response({"status": "Registration disabled"}, status=503)

    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    data = request.data
    username = data.get('username')
    token = data.get('token')

    if not username or not token:
        return Response({"status": "invalid data"}, status=400)

    logger.info(f"Validating new user: {username}...")

    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        logger.error(f"User '{username}' does not exist!")
        return Response({"status": "user not found"}, status=400)

    user_profile = Profile.objects.get(user=user)
    if user_profile.registration_token == token:
        user_profile.confirmed = True

    user_profile.save()

    logger.info(f"User '{username}' validated successfully.")

    return Response({"status": "ok"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_user_data(request):
    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    # Check input data
    data = request.data
    if not data.get('user') or not data.get('email') or not data.get('first_name') or \
            not data.get('last_name'):
        return Response({'status': "Invalid Data"}, status=400)

    logger.info(f"Changing data for user: {data['user']}...")

    try:
        user = get_user_model().objects.get(id=data['user'])
    except get_user_model().DoesNotExist:
        logger.error(f"User '{data['user']}' does not exist!")
        return Response({'status': "Not Found"}, status=404)

    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']

    user.save()

    logger.info(f"User data for user {data['user']} updated successfully.")

    return Response({'status': "ok"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if not request.method == 'POST':
        return Response({'status': "Method Not Allowed"}, status=405)

    # Check input data
    data = request.data
    if not data.get('username') or not data.get('current_password') or not data.get('new_password'):
        return Response({'status': "Invalid Data"}, status=400)

    logger.info(f"Changing password for user: {data['username']}...")

    # Check current password
    user = authenticate(
        username=data['username'], password=data['current_password'])
    if not user:
        logger.error(
            f"Current password for user '{data['username']}' is invalid!")
        return Response({'status': "Invalid current password"}, status=400)

    # Set new password
    user.set_password(data['new_password'])
    user.save()

    logger.info(
        f"The password for user '{data['username']}' has been changed successfully.")

    return Response({'status': "ok"}, status=200)


# endregion

# region Other views

@csrf_exempt
def share_match(request, match_id):
    if request.method != 'POST':
        return Response({"detail": "Method not allowed."}, status=405)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({"detail": "Not found."}, status=404)

    data = request.POST.getlist('user')
    for elem in data:
        new_match_user = get_user_model().objects.get(id=elem)
        match.user.add(new_match_user)

    return Response({"detail": "ok"}, status=200)

# endregion
