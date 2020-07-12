from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from api.serializers import *
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
