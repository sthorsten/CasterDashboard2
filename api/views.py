import logging
import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import DatabaseError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pip._vendor import requests
from rest_framework.parsers import JSONParser

from api.serializers import *
from caster_dashboard_2 import settings
from dashboard.models import MapBan
from overlays.models import *

logger = logging.getLogger(__name__)


@csrf_exempt
def overlay_state(request, user_id):
    try:
        overlay_state = OverlayState.objects.get(user=user_id)
    except OverlayState.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = OverlayStateSerializer(overlay_state)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OverlayStateSerializer(overlay_state, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def timer_overlay_data(request, user_id):
    try:
        timer_overlay_data = TimerOverlayData.objects.get(user=user_id)
    except TimerOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = TimerOverlayDataSerializer(timer_overlay_data)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TimerOverlayDataSerializer(timer_overlay_data, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


def get_current_match(request, user_id):
    try:
        match_overlay_data = MatchOverlayData.objects.get(user=user_id)
    except MatchOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = MatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    else:
        return JsonResponse(data={"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def set_current_match(request, user_id):
    try:
        match_overlay_data = MatchOverlayData.objects.get(user=user_id)
    except MatchOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = MatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MatchOverlayDataSerializer(match_overlay_data, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def set_next_match(request, user_id):
    try:
        match_overlay_data = NextMatchOverlayData.objects.get(user=user_id)
    except NextMatchOverlayData.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = NextMatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NextMatchOverlayDataSerializer(match_overlay_data, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def map_ban(request, match_id):
    match = Match.objects.filter(id=match_id).first()

    if request.method == 'GET':
        map_ban = MapBan.objects.filter(match=match).all().order_by("order")
        if not map_ban or len(map_ban) == 0:
            return JsonResponse({"status": "Not Found"}, status=404)

        data = []
        for map in map_ban:
            data.append({
                "map": map.map.name,
                "map_id": map.map.id,
                "type": map.type,
                "order": map.order,
                "team": map.team.name
            })
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        map = Map.objects.filter(id=data['map']).first()

        if data['type']:
            if data['type'] == "delete":
                map_ban = MapBan.objects.filter(match=match, map=map).first()
                map_ban.delete()
                map_play_order = MapPlayOrder.objects.filter(match=match, map=map).first()
                if map_play_order:
                    map_play_order.delete()

        team = Team.objects.filter(id=data['team']).first()
        if not map or not team or not data['type'] or not data['order']:
            return JsonResponse({"status": "Bad Request"}, status=400)

        # Check if map is already in map_ban
        map_ban = MapBan.objects.filter(match=match, map=map)
        if map_ban:
            return JsonResponse({"status": "Duplicate"}, status=400)

        if data['type'] == "pick" or data['type'] == "decider":
            next_order = len(MapPlayOrder.objects.filter(match=match).all()) + 1
            map_play_order = MapPlayOrder(match=match, map=map, order=next_order)
            try:
                map_play_order.save()
            except DatabaseError:
                return JsonResponse({"status": "Database Error"}, status=500)

        map_ban = MapBan(match=match, map=map, type=data['type'], order=data['order'], team=team)
        try:
            map_ban.save()
            return JsonResponse({"status": "ok"})
        except DatabaseError:
            return JsonResponse({"status": "Database Error"}, status=500)


@csrf_exempt
def map_settings(request, match_id, map_id):
    match = Match.objects.filter(id=match_id).first()
    map = Map.objects.filter(id=map_id).first()

    try:
        map_settings = MapSettings.objects.filter(match=match, map=map).first()
    except MapSettings.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = MapSettingsSerializer(map_settings)
        return JsonResponse(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MapSettingsSerializer(map_settings, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def swap_teams(request, match_id):
    try:
        match = Match.objects.filter(id=match_id).first()
    except Match.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"team_blue": match.team_blue.id, "team_orange": match.team_orange.id})

    if request.method == 'POST':
        team_blue = match.team_blue
        match.team_blue = match.team_orange
        match.team_orange = team_blue
        match.save()

        return JsonResponse({"team_blue": match.team_blue.id, "team_orange": match.team_orange.id})


@csrf_exempt
def operator_bans(request, match_id, map_id):
    match = Match.objects.filter(id=match_id).first()
    map = Map.objects.filter(id=map_id).first()

    operator_bans = OperatorBans.objects.filter(match=match, map=map).all()

    if request.method == 'GET':
        if len(operator_bans) == 0:
            return JsonResponse({"status": "Not Found"}, status=404)

        data = []
        for op_ban in operator_bans:
            serializer = OperatorBanSerializer(op_ban)
            data.append(serializer.data)

        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        # Reset Last Ban
        if data.get('reset'):
            if data['reset'] == "single":
                last_op_ban = operator_bans.last()
                last_op_ban.delete()
            elif data['reset'] == "all":
                for op_ban in operator_bans:
                    op_ban.delete()

            return JsonResponse({"status": "ok"})

        # Abort if there are already 4 Operator Bans
        if len(operator_bans) >= 4:
            return JsonResponse({"status": "Bad Request"}, status=400)

        if not data['operator'] or not data['team']:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            operator = Operator.objects.filter(id=data['operator']).first()
        except Operator.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            team = Team.objects.filter(id=data['team']).first()
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

            # Check if team is in current match
        if not (team == match.team_blue or team == match.team_orange):
            return JsonResponse({"status": "Bad Request"}, status=400)

        next_order = len(operator_bans) + 1
        op_ban = OperatorBans(match=match, map=map, operator=operator, team=team, order=next_order)
        op_ban.save()

        return JsonResponse({"status": "ok"})


@csrf_exempt
def rounds(request, match_id, map_id):
    match = Match.objects.filter(id=match_id).first()
    map = Map.objects.filter(id=map_id).first()
    map_settings = MapSettings.objects.filter(match=match, map=map).first()

    rounds = Round.objects.filter(match=match, map=map).all()

    if request.method == 'GET':
        if len(rounds) == 0:
            return JsonResponse({"status": "Not Found"}, status=404)

        data = []
        for round in rounds:
            serializer = RoundSerializer(round)
            data.append(serializer.data)

        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        # Reset Round(s)
        if data.get('reset'):
            if data['reset'] == "single":
                last_round = rounds.last()
                last_round.delete()
            elif data['reset'] == "all":
                for round in rounds:
                    round.delete()

            return JsonResponse({"status": "ok"})

        # Check data
        if not data['bombspot'] or not data['win_type'] or not data['win_team'] or not data['of_team']:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            bombspot = BombSpot.objects.filter(id=data['bombspot']).first()
        except BombSpot.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_type = WinType.objects.filter(id=data['win_type']).first()
        except WinType.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_team = Team.objects.filter(id=data['win_team']).first()
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            of_team = Team.objects.filter(id=data['of_team']).first()
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        if not data.get('notes'):
            notes = None
        else:
            notes = data['notes']

        # Format data
        round_no = len(rounds) + 1

        # Set ATK / DEF team for round
        if round_no <= 6:
            atk_team = map_settings.atk_team
            if atk_team == match.team_blue:
                def_team = match.team_orange
            else:
                def_team = match.team_blue

        elif 6 < round_no <= 12:
            def_team = map_settings.atk_team
            if def_team == match.team_blue:
                atk_team = match.team_orange
            else:
                atk_team = match.team_blue

        # Odd OT Rounds (13, 15, ...)
        elif round_no > 12 and (round_no % 2 != 0):
            atk_team = map_settings.ot_atk_team
            if atk_team == match.team_blue:
                def_team = match.team_orange
            else:
                def_team = match.team_blue

        # Even OT Rounds (14, 16, ...)
        else:
            def_team = map_settings.ot_atk_team
            if def_team == match.team_blue:
                atk_team = match.team_orange
            else:
                atk_team = match.team_blue

        # Set Score
        if round_no <= 1:
            score_blue = 0
            score_orange = 0
        else:
            score_blue = rounds.last().score_blue
            score_orange = rounds.last().score_orange

        if win_team == match.team_blue:
            score_blue += 1
        else:
            score_orange += 1

        new_round = Round(match=match, map=map, round_no=round_no, bombspot=bombspot, atk_team=atk_team,
                          def_team=def_team, of_team=of_team, win_type=win_type, win_team=win_team,
                          score_blue=score_blue, score_orange=score_orange, notes=notes)

        try:
            new_round.save()
        except DatabaseError:
            return JsonResponse({"error": "Database Error"}, status=500)

        messages.success(request, _('The round has been added successfully'))
        return JsonResponse({"status": "ok"})


@csrf_exempt
def finish_map(request, match_id, map_id):
    if request.method == 'GET':
        return JsonResponse({"status": "Method Not Allowed"}, status=405)

    data = JSONParser().parse(request)

    if data.get('finish_map'):
        match = Match.objects.filter(id=match_id).first()
        map = Map.objects.filter(id=map_id).first()
        last_round = Round.objects.filter(match=match, map=map).last()

        if last_round.score_blue > last_round.score_orange:
            win_team = match.team_blue
            match.score_blue += 1
        elif last_round.score_orange > last_round.score_blue:
            win_team = match.team_orange
            match.score_orange += 1
        else:
            win_team = None

        map_win = MapWins(match=match, map=map, win_team=win_team)
        try:
            map_win.save()
            match.save()
        except DatabaseError:
            return JsonResponse({"error": "Database Error"}, status=500)

        # Set Next URL
        map_win_len = len(MapWins.objects.filter(match=match).all())
        if match.best_of == 1:
            next_url = "/dashboard/matches/history"

        else:
            if map_win_len >= match.best_of:
                next_url = "/dashboard/matches/history"
            else:
                next_map = MapPlayOrder.objects.filter(match=match, order=(map_win_len + 1)).first()
                next_url = "/dashboard/matches/%s/map/%s/opbans" % (match.id, next_map.map.id)

        return JsonResponse({"status": "ok", "next_url": next_url})

    else:
        return JsonResponse({"status": "Bad Request"}, status=400)
