from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import auth
from django.utils.translation import gettext as _

from dashboard.models import *
from overlays.models import *


def index(request):
    if auth.get_user(request).is_anonymous:
        return redirect('login')
    else:
        return redirect('home')


def login(request):
    return HttpResponse("<p>To Do!</p>")


@login_required
def home(request):
    league_count = len(League.objects.all())
    match_count = len(Match.objects.all())
    round_count = len(Round.objects.all())

    template_data = {
        'league_count': league_count,
        'match_count': match_count,
        'round_count': round_count,
    }

    return render(request, 'index.html', template_data)


@login_required
def overlay_control_center(request):
    overlay_styles = OverlayStyle.objects.filter(user=request.user).first()
    overlay_states = OverlayState.objects.filter(user=request.user).first()
    timer_overlay_data = TimerOverlayData.objects.filter(user=request.user).first()
    # Last 10 Matches
    matches = Match.objects.filter(user=request.user).order_by("-id").all()[:10]
    match_overlay_data = MatchOverlayData.objects.filter(user=request.user).first()
    current_match = Match.objects.filter(id=match_overlay_data.current_match.id).first()

    template_data = {
        'overlay_styles': overlay_styles,
        'overlay_states': overlay_states,
        'timer_overlay_data': timer_overlay_data,
        'matches': matches,
        'match_overlay_data': match_overlay_data,
        'current_match': current_match,
    }

    return render(request, 'overlays/control-center.html', template_data)
