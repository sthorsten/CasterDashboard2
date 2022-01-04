import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from . import models
from . import serializers

# pylint: disable=no-member

logger = logging.getLogger(__name__)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_fields = ['user']


class MatchMapViewSet(viewsets.ModelViewSet):
    queryset = models.MatchMap.objects.all()
    serializer_class = serializers.MatchMapSerializer
    filterset_fields = ['match', 'map', 'status']

    # MapBan elements with a specific match id
    # URL: /api/match/<id>/maps
    @action(methods=['get'], detail=True)
    def match_maps(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        match_id = int(kwargs['match_id'])
        queryset = models.MatchMap.objects.filter(match=match_id).all()
        if not queryset:
            return Response({"detail": "Not found."}, status=404)
        serializer = serializers.MatchMapSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class OperatorBansViewSet(viewsets.ModelViewSet):
    queryset = models.OperatorBan.objects.all()
    serializer_class = serializers.OperatorBanSerializer
    filterset_fields = ['match', 'map']


class RoundViewSet(viewsets.ModelViewSet):
    queryset = models.Round.objects.all()
    serializer_class = serializers.RoundSerializer
    filterset_fields = ['match', 'map']

    def create(self, request, *args, **kwargs):
        data = request.data
        # Validate data
        if not data.get('match') or not data.get('map') or not data.get('win_type') or not data.get(
                'bomb_spot') or not data.get('win_team'):
            logger.error("Invalid round data!")
            return Response({"required_fields":
                            ["match", "map", "bomb_spot", "win_type", "win_team"]},
                            status=400)

        # Get Match related data
        filtered_rounds = models.Round.objects.filter(match=data.get(
            'match'), map=data.get('map')).order_by('-round_no').all()
        match_map = models.MatchMap.objects.get(
            match=data.get('match'), map=data.get('map'))
        match_data = models.Match.objects.get(id=data.get('match'))

        # Round ID and Score
        if filtered_rounds and len(filtered_rounds) > 0:
            last_round = filtered_rounds[0]
            next_round_no = len(filtered_rounds) + 1
            score_blue = last_round.score_blue
            score_orange = last_round.score_orange
        else:
            next_round_no = 1
            score_blue = 0
            score_orange = 0

        if data.get('win_team') == match_data.team_blue.id:
            score_blue += 1
        else:
            score_orange += 1

        # Team constellation
        atk_team = match_map.atk_team
        if match_map.atk_team == match_data.team_blue:
            def_team = match_data.team_orange
        else:
            def_team = match_data.team_blue

        if next_round_no > 6:
            tmp = atk_team
            atk_team = def_team
            def_team = tmp

        serializer = serializers.RoundSerializer(
            data={'match': data.get('match'), 'map': data.get('map'), 'round_no': next_round_no,
                  'bomb_spot': data.get('bomb_spot'), 'atk_team': atk_team.id,
                  'def_team': def_team.id, 'of_team': data.get('of_team'),
                  'win_type': data.get('win_type'), 'win_team': data.get('win_team'),
                  'score_blue': score_blue, 'score_orange': score_orange,
                  'notes': data.get('notes')})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        logger.error("Invalid round data!")
        return Response({"detail": "Invalid Data"}, status=400)

