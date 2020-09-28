import logging
import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import DatabaseError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from pip._vendor import requests
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *
from caster_dashboard_2 import settings
from dashboard.models import MapBan
from overlays.models import *

logger = logging.getLogger(__name__)


###
# New Team Form
###

class NewTeamForm(View):
    def get(self, request):
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    def post(self, request):
        logger.info("[User: %s] Creating a new team..." % request.user)

        data = request.POST

        # Validate data
        if not data.get('name'):
            messages.error(request, _("No team name"), extra_tags=_("Team creation failed"))
            return redirect('/dashboard/data/teams')
        else:
            new_team = Team(name=data.get('name'))

        # Handle no logo
        if data.get('no_logo'):
            new_team.has_logo = False

            try:
                new_team.full_clean()
                new_team.save()
                messages.success(request, _('Team created successfully'))
            except ValidationError as e:
                logger.error('Invalid team data: ' + str(e))
                for m in e.messages:
                    messages.error(request, _("Invalid team data: ") + m, extra_tags=_("Team creation failed"))
            finally:
                return redirect('/dashboard/data/teams')

        # Handle uploaded logo
        if request.FILES:
            new_team.has_logo = True
            new_team.team_logo = request.FILES['team_logo']

            try:
                new_team.full_clean()
                new_team.save()
                messages.success(request, _('Team created successfully'))
            except ValidationError as e:
                logger.error('Invalid team logo: ' + str(e))
                for m in e.messages:
                    messages.error(request, _("Invalid team logo: ") + m, extra_tags=_("Team creation failed"))
            finally:
                return redirect('/dashboard/data/teams')

        # Handle file download
        try:
            url = data.get('team_logo_url')
            if not url:
                messages.error(_('No team logo!'), extra_tags=_("Team creation failed"))
                return redirect('/dashboard/data/teams')

            r = requests.get(url, allow_redirects=True)
            save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', data.get('name') + '.png')
            image_file = open(save_path, 'wb')
            image_file.write(r.content)
            image_file.close()

        except requests.exceptions.RequestException as e:
            logger.error('Team logo download failed: ' + str(e))
            messages.error(request, _('Team logo download failed! Please try uploading the logo manually'))

        try:
            new_team.team_logo = 'teams/' + data.get('name') + '.png'
            new_team.full_clean()
            new_team.save()
            messages.success(request, _('Team created successfully'))
        except ValidationError as e:
            try:
                if os.path.isfile(save_path):
                    os.remove(save_path)
            except OSError:
                logger.error("Unable to delete file: " + save_path)

            logger.error('Invalid team logo: ' + str(e))
            for m in e.messages:
                messages.error(request, _("Invalid team logo: ") + m, extra_tags=_("Team creation failed"))
        finally:
            return redirect('/dashboard/data/teams')


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
def overlay_style(request, user_id):
    try:
        overlay_style = OverlayStyle.objects.get(user=user_id)
    except OverlayStyle.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        serializer = OverlayStyleSerializer(overlay_style)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OverlayStyleSerializer(overlay_style, data=data)
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
def update_match_score(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return JsonResponse({"status": "Not Found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if data.get("score_blue") is not None:
            match.score_blue = data.get("score_blue")
        elif data.get("score_orange") is not None:
            match.score_orange = data.get("score_orange")
        else:
            return JsonResponse({"error": "Bad Request"}, status=400)

        try:
            match.save()
        except ValidationError:
            return JsonResponse({"error": "Internal Server Error"}, status=500)

        return JsonResponse({"status": "OK"})

@csrf_exempt
def map_ban(request, match_id):
    match = Match.objects.get(id=match_id)

    if request.method == 'GET':
        map_ban = MapBan.objects.filter(match=match).all().order_by("order")
        if not map_ban or len(map_ban) == 0:
            return JsonResponse({"status": "Not Found"}, status=404)

        data = []
        for map in map_ban:
            data.append({
                "match": map.match.id,
                "map": map.map.name,
                "map_id": map.map.id,
                "type": map.get_type_display(),
                "order": map.order,
                "play_order": map.play_order,
                "team": map.team.name,
                "team_id": map.team.id,
            })
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        map = Map.objects.get(id=data['map'])

        if data['type']:
            if data['type'] == "delete":
                map_ban = MapBan.objects.get(match=match, map=map)
                map_ban.delete()
                return JsonResponse({"status": "ok"})

        team = Team.objects.filter(id=data['team']).first()
        if not map or not team or not data['type'] or not data['order']:
            return JsonResponse({"status": "Bad Request"}, status=400)

        # Check if map is already in map_ban
        map_ban = MapBan.objects.filter(match=match, map=map)
        if map_ban:
            return JsonResponse({"status": "Duplicate"}, status=400)

        map_ban = MapBan(match=match, map=map, type=data['type'], order=data['order'], team=team)
        try:
            map_ban.save()
            return JsonResponse({"status": "ok"})
        except DatabaseError:
            return JsonResponse({"status": "Database Error"}, status=500)


@csrf_exempt
def map_settings(request, match_id, map_id):
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)

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
        match = Match.objects.get(id=match_id)
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
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)

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

        # Set current map
        match_overlay_data = MatchOverlayData.objects.get(user=request.user)
        match_overlay_data.current_map = map
        match_overlay_data.save()

        return JsonResponse({"status": "ok"})


@csrf_exempt
def rounds(request, match_id, map_id):
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)
    map_settings = MapSettings.objects.get(match=match, map=map)

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
            bombspot = BombSpot.objects.get(id=data['bombspot'])
        except BombSpot.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_type = WinType.objects.get(id=data['win_type'])
        except WinType.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            win_team = Team.objects.get(id=data['win_team'])
        except Team.DoesNotExist:
            return JsonResponse({"status": "Bad Request"}, status=400)

        try:
            of_team = Team.objects.get(id=data['of_team'])
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
        match = Match.objects.get(id=match_id)
        map = Map.objects.get(id=map_id)
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
            match.state = MatchState.objects.get(id=8)
            match.save()
            next_url = "/dashboard/matches/%s" % match.id

        else:
            if map_win_len >= match.best_of:
                match.state = MatchState.objects.get(id=8)
                match.save()
                next_url = "/dashboard/matches/%s" % match.id
            else:
                next_map = MapPlayOrder.objects.get(match=match, order=(map_win_len + 1))
                match.state = MatchState.objects.get(id=(2 + next_map.order))
                match.save()
                next_url = "/dashboard/matches/%s/map/%s/opbans" % (match.id, next_map.map.id)

        messages.info(request, _('Match Finished!'))
        return JsonResponse({"status": "ok", "next_url": next_url})

    else:
        return JsonResponse({"status": "Bad Request"}, status=400)
