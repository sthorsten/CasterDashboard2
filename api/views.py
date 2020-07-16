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
from overlays.models import *


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


def add_new_team(request):
    if request.method == 'GET':
        return HttpResponse(status=405)

    elif request.method == 'POST':
        data = request.POST

        # Validate / Format
        if not len(data['team_name']) > 0:
            return HttpResponse(reason="no team_name", status=400)

        # Handle files
        if not request.FILES:
            if not len(data['logo_url']) > 0:
                if not (data['no_logo']):
                    return HttpResponse(reason="no logo", status=400)
                else:
                    try:
                        new_team = Team(name=data['team_name'], has_logo=False)
                        new_team.save()
                    except DatabaseError:
                        return HttpResponse(reason="database error", status=500)

                    return HttpResponse(content="ok", status=200)

            else:
                try:
                    new_team = Team(name=data['team_name'], has_logo=True)
                    new_team.save()
                    new_team.team_logo = 'teams/' + str(new_team.id) + ".png"
                    new_team.save()
                except DatabaseError:
                    return HttpResponse(reason="database error", status=500)

                try:
                    # Download and save file
                    url = data['logo_url']
                    r = requests.get(url, allow_redirects=True)
                    save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
                    open(save_path, 'wb').write(r.content)

                except requests.exceptions.RequestException:
                    new_team.delete()
                    return HttpResponse(reason="logo download failed", status=500)
                except OSError:
                    new_team.delete()
                    return HttpResponse(reason="logo save failed", status=500)

                return HttpResponse(content="ok", status=200)

        else:
            try:
                new_team = Team(name=data['team_name'], has_logo=True)
                new_team.save()
                new_team.team_logo = 'teams/' + str(new_team.id) + ".png"
                new_team.save()

            except DatabaseError:
                return HttpResponse(reason="database error", status=500)

            try:
                save_path = os.path.join(django_settings.MEDIA_ROOT, 'teams', str(new_team.id) + '.png')
                open(save_path, 'wb').write(request.FILES['logo_file'].read())
            except OSError:
                new_team.delete()
                return HttpResponse(reason="logo save failed", status=500)

            return HttpResponse(content="ok", status=200)
