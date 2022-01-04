from rest_framework import viewsets
from . import models
from . import serializers

# pylint: disable=no-member


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.League.objects.all()
    serializer_class = serializers.LeagueSerializer
    filterset_fields = ['name', 'is_restricted', 'has_custom_overlay']


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = serializers.SeasonSerializer


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    filterset_fields = ['league', 'name', 'public']


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filterset_fields = ['name']

    """
    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Creating new team...")

            try:
                new_team = serializer.create(
                    validated_data=serializer.validated_data)

                # Download logo from URL if present and no logo upload
                if not request.data.get('team_logo') and request.data.get('team_logo_url'):
                    try:
                        # Download and save file
                        logger.info("Downloading team logo...")
                        url = request.data['team_logo_url']
                        req = requests.get(url, allow_redirects=True)

                        temp_filename = f"{uuid4().hex}_temp.png"
                        save_path = os.path.join(
                            django_settings.MEDIA_ROOT, 'teams', temp_filename)
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(req.content)

                        logger.info(
                            f"Team logo downloaded from {url} to {temp_filename}")

                        new_team.team_logo = f"teams/{temp_filename}"
                        new_team.save()  # Renaming will be handled by the model receiver

                    except requests.RequestException as ex:
                        logger.error(ex)

                return Response({"status": "ok"}, status=201)

            except ValidationError as ex:
                logger.error({ex.messages[0]})
                return Response({"error": ex.messages[0]}, status=400)

        else:
            if serializer.errors['name'][0].code == "unique":
                logger.error("Team already exists.")
                return Response(data={"error": _('A team with this name already exists!')},
                                status=400)

            logger.error(serializer.errors)
            return Response(data={"error": serializer.errors}, status=400)

    def partial_update(self, request, *args, **kwargs):
        team = Team.objects.get(id=request.data.get("id"))
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                team = serializer.save()

                # Download logo from URL if present and no logo upload
                if not request.data['team_logo'] and request.data['team_logo_url']:
                    try:
                        # Download and save file
                        logger.info("Downloading team logo...")
                        url = request.data['team_logo_url']
                        req = requests.get(url, allow_redirects=True)

                        temp_filename = f"{uuid4().hex}_temp.png"
                        save_path = os.path.join(
                            django_settings.MEDIA_ROOT, 'teams', temp_filename)
                        with open(save_path, 'wb') as logo_file:
                            logo_file.write(req.content)

                        logger.info(
                            f"Team logo downloaded from {url} to {temp_filename}")

                        team.team_logo = f"teams/{temp_filename}"
                        team.save()  # Renaming will be handled by the model receiver

                    except requests.RequestException as ex:
                        logger.error(ex)

                return Response({"status": "ok"}, status=200)
            except ValidationError as ex:
                logger.error({ex.messages[0]})
                return Response({"error": ex.messages[0]}, status=400)

        else:
            logger.error(serializer.errors)
            return Response(data={"error": serializer.errors}, status=400)
    """
