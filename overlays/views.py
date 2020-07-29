from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404

from dashboard.models import *
from overlays.models import *


def ingame(request, user_name):
    user = get_object_or_404(User, username=user_name)
    match_overlay_data = MatchOverlayData.objects.filter(user=user).first()
    match = match_overlay_data.current_match
    overlay_states = OverlayState.objects.filter(user=user).first()

    current_map = match_overlay_data.current_map
    if current_map:
        current_map_pick_team = MapBan.objects.filter(match=match, map=current_map).first().team
    else:
        current_map_pick_team = None

    template_data = {
        'match_overlay_data': match_overlay_data,
        'match': match,
        'current_map_pick_team': current_map_pick_team,

        'overlay_states': overlay_states,
    }

    return render(request, 'ingame.html', template_data)
