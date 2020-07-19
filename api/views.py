import logging
import os

from django.conf import settings as django_settings
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
        return HttpResponse(status=404)

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
        return HttpResponse(status=404)

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
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MatchOverlayDataSerializer(match_overlay_data)
        return JsonResponse(serializer.data)

    else:
        return JsonResponse(data={"error": "method not allowed"}, status=405)


@csrf_exempt
def set_current_match(request, user_id):
    try:
        match_overlay_data = MatchOverlayData.objects.get(user=user_id)
    except MatchOverlayData.DoesNotExist:
        return HttpResponse(status=404)

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
        return HttpResponse(status=404)

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
