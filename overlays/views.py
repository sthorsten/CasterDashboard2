from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404

from dashboard.models import *
from overlays.models import *


def ingame(request, user_name):
    user = get_object_or_404(User, username=user_name)
    match_overlay_data = MatchOverlayData.objects.get(user=user)
    match = match_overlay_data.current_match
    overlay_states = OverlayState.objects.get(user=user)

    current_map_order = match.state.id - 2
    if 1 <= current_map_order <= 5:
        current_map = MapPlayOrder.objects.get(match=match, order=current_map_order).map
        current_map_pick_team = MapBan.objects.get(match=match, map=current_map).team
    else:
        current_map_pick_team = None

    template_data = {
        'match_overlay_data': match_overlay_data,
        'match': match,
        'current_map_pick_team': current_map_pick_team,

        'overlay_states': overlay_states,
    }

    return render(request, 'ingame.html', template_data)
