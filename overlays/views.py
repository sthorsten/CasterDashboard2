from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404

from dashboard.models import *
from overlays.models import *


def start(request, user_name):
    user = get_object_or_404(User, username=user_name)
    match_overlay_data = MatchOverlayData.objects.get(user=user)
    match = match_overlay_data.current_match
    overlay_states = OverlayState.objects.get(user=user)

    template_data = {
        'overlay_user': user,
        'match_overlay_data': match_overlay_data,
        'match': match,
        'overlay_states': overlay_states,
    }

    return render(request, 'start.html', template_data)


def ingame(request, user_name):
    user = get_object_or_404(User, username=user_name)
    overlay_styles = OverlayStyle.objects.get(user=user)
    match_overlay_data = MatchOverlayData.objects.get(user=user)
    match = match_overlay_data.current_match

    sponsors = []
    for s in match.sponsors.all():
        sponsors.append(s)

    overlay_states = OverlayState.objects.get(user=user)

    current_map_order = match.state.id - 2
    if 1 <= current_map_order <= 5:
        current_map = MapPlayOrder.objects.get(match=match, order=current_map_order).map
        current_map_pick_team = MapBan.objects.get(match=match, map=current_map).team
    else:
        current_map_pick_team = None

    template_data = {
        'overlay_user': user,
        'overlay_styles': overlay_styles,
        'match_overlay_data': match_overlay_data,
        'match': match,
        'sponsors': sponsors,
        'current_map_pick_team': current_map_pick_team,

        'overlay_states': overlay_states,
    }

    return render(request, 'ingame.html', template_data)


def maps(request, user_name):
    user = get_object_or_404(User, username=user_name)
    match_overlay_data = MatchOverlayData.objects.get(user=user)
    match = match_overlay_data.current_match
    map_query = MapBan.objects.filter(match=match).all()
    overlay_states = OverlayState.objects.get(user=user)

    maps = []

    for m in map_query:
        maps.append(m)

    template_data = {
        'overlay_user': user,
        'match_overlay_data': match_overlay_data,
        'match': match,
        'maps': maps,
        'overlay_states': overlay_states,
    }

    return render(request, 'maps.html', template_data)


def opbans(request, user_name):
    user = get_object_or_404(User, username=user_name)
    match_overlay_data = MatchOverlayData.objects.get(user=user)
    match = match_overlay_data.current_match
    current_map = match_overlay_data.current_map
    overlay_states = OverlayState.objects.get(user=user)
    opbans = OperatorBans.objects.filter(match=match, map=current_map).all()

    template_data = {
        'overlay_user': user,
        'match_overlay_data': match_overlay_data,
        'match': match,
        'current_map': current_map,
        'overlay_states': overlay_states,
        'opbans': opbans,
    }

    return render(request, 'opbans.html', template_data)


def rounds(request, user_name):
    return
