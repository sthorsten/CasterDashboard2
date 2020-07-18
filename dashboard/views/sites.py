import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import auth
from django.contrib import messages
from django.utils.translation import gettext as _

from dashboard.models import *
from overlays.models import *

logger = logging.getLogger(__name__)


def index(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/login')
    else:
        logger.info("[User %s] Login successful" % request.user)
        return redirect('home')


def login_view(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')


def register_success(requset):
    return render(requset, 'login/register-success.html')


def logout_view(request):
    logger.info("[User: %s] User logout" % request.user)
    logout(request)
    messages.success(request, _("You have been logged out! See you next time!"),
                     extra_tags=_("Logged out"))
    return redirect('/')


@login_required
def home(request):
    league_count = len(League.objects.all())
    match_count = len(Match.objects.all())
    round_count = len(Round.objects.all())
    social_count = len(SocialOverlayData.objects.filter(user=request.user).all())
    personal_match_count = len(Match.objects.filter(user=request.user).all())

    match_overlay_data = MatchOverlayData.objects.filter(user=request.user).first()
    if match_overlay_data.current_match:
        current_match = Match.objects.filter(id=match_overlay_data.current_match.id).first()
    else:
        current_match = None

    template_data = {
        'league_count': league_count,
        'match_count': match_count,
        'round_count': round_count,
        'social_count': social_count,
        'personal_match_count': personal_match_count,

        'match_overlay_data': match_overlay_data,
        'current_match': current_match,
    }

    return render(request, 'home.html', template_data)


'''
    Overlays
'''


@login_required
def overlay_control_center(request):
    overlay_styles = OverlayStyle.objects.filter(user=request.user).first()
    overlay_states = OverlayState.objects.filter(user=request.user).first()
    timer_overlay_data = TimerOverlayData.objects.filter(user=request.user).first()
    # Last 10 Matches
    matches = Match.objects.filter(user=request.user).order_by("-id").all()[:10]
    match_overlay_data = MatchOverlayData.objects.filter(user=request.user).first()
    if match_overlay_data.current_match:
        current_match = Match.objects.filter(id=match_overlay_data.current_match.id).first()
    else:
        current_match = None

    template_data = {
        'overlay_styles': overlay_styles,
        'overlay_states': overlay_states,
        'timer_overlay_data': timer_overlay_data,
        'matches': matches,
        'match_overlay_data': match_overlay_data,
        'current_match': current_match,
    }

    return render(request, 'overlays/control-center.html', template_data)


'''
    Data
'''


@login_required
def leagues(request):
    leagues = League.objects.all()
    league_groups = LeagueGroup.objects.all()

    template_data = {
        'leagues': leagues,
        'league_groups': league_groups,
    }

    return render(request, 'data/leagues.html', template_data)


@login_required
def seasons(request):
    seasons = Season.objects.all()
    leagues = League.objects.all()
    league_groups = LeagueGroup.objects.all()

    template_data = {
        'seasons': seasons,
        'leagues': leagues,
        'league_groups': league_groups,
    }

    return render(request, 'data/seasons.html', template_data)


@login_required
def teams(request):
    teams = Team.objects.all().order_by('name')

    template_data = {
        'teams': teams,
    }

    return render(request, 'data/teams.html', template_data)


'''
    Matches
'''


@login_required
def match_history(request):
    matches = Match.objects.filter(user=request.user).order_by("-id").all()

    template_data = {
        'matches': matches,
    }

    return render(request, 'matches/history.html', template_data)


@login_required
def match_create(request):
    league_groups = LeagueGroup.objects.filter(user=request.user).all()
    leagues = League.objects.order_by("name").all()
    seasons = Season.objects.order_by("name").all()
    teams = Team.objects.order_by("name").all()
    sponsors = Sponsor.objects.order_by("name").all()

    template_data = {
        'league_groups': league_groups,
        'leagues': leagues,
        'seasons': seasons,
        'teams': teams,
        'sponsors': sponsors,
    }

    return render(request, 'matches/create.html', template_data)


@login_required
def match_overview(request, match_id):
    match = Match.objects.filter(id=match_id).first()
    match_users = match.user.all()

    template_data = {
        'match': match,
        'match_users': match_users,
    }

    return render(request, 'matches/overview.html', template_data)
