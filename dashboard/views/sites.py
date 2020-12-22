import logging

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from dashboard.forms import NewMatchForm
from dashboard.models.models import Map, BombSpot, Operator, League, LeagueGroup, Season, Sponsor, Team, Match, \
    MatchMap, OperatorBans, Round

from overlays.models.models import OverlayStyle, OverlayState, MatchOverlayData, SocialOverlayData, TimerOverlayData

logger = logging.getLogger(__name__)


def index(request):
    if auth.get_user(request).is_anonymous:
        return redirect('/login')
    else:
        logger.info("[User %s] Login successful" % request.user)
        return redirect('home')


def error_500(request, exception=None):
    return render(request, "errors/error500.html", status=500)


def error_404(request, exception=None):
    return render(request, "errors/error404.html", status=404)


def login_view(request):
    next_url = request.GET.get('next', None)
    return render(request, 'login/login.html', {'next_url': next_url})


def register(request):
    return render(request, 'login/register.html')


def register_success(request):
    return render(request, 'login/register-success.html')


def logout_view(request):
    logger.info("[User: %s] User logout" % request.user)
    logout(request)
    messages.success(request, _("You have been logged out! See you next time!"),
                     extra_tags=_("Logged out"))
    return redirect('/')


@login_required
def home(request):
    team_count = len(Team.objects.all())
    match_count = len(Match.objects.all())
    round_count = len(Round.objects.all())
    social_count = len(SocialOverlayData.objects.filter(user=request.user).all())
    personal_match_count = len(Match.objects.filter(user=request.user).all())

    match_overlay_data = MatchOverlayData.objects.get(user=request.user)

    if match_overlay_data.current_match:
        current_match = Match.objects.get(id=match_overlay_data.current_match.id)
    else:
        current_match = None

    template_data = {
        'team_count': team_count,
        'match_count': match_count,
        'round_count': round_count,
        'social_count': social_count,
        'personal_match_count': personal_match_count,

        'match_overlay_data': match_overlay_data,
        'current_match': current_match,
    }

    return render(request, 'home.html', template_data)


'''
    Settings
'''


@login_required
def settings_league_admin(request):
    league_groups = LeagueGroup.objects.all()
    admin_leagues = []

    for lg in league_groups:
        if lg.user == request.user and lg.rank == 'admin':
            admin_leagues.append(lg.league)

    template_data = {
        "admin_leagues": admin_leagues,
    }

    return render(request, 'settings/league_admin.html', template_data)


'''
    Overlays
'''


@login_required
def overlay_control_center(request):
    overlay_styles = OverlayStyle.objects.get(user=request.user)
    overlay_states = OverlayState.objects.get(user=request.user)
    timer_overlay_data = TimerOverlayData.objects.get(user=request.user)
    # Last 10 Matches
    matches = Match.objects.filter(user=request.user).order_by("-id").all()[:10]
    match_overlay_data = MatchOverlayData.objects.get(user=request.user)
    if match_overlay_data.current_match:
        current_match = Match.objects.get(id=match_overlay_data.current_match.id)
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


@login_required
def popout_overlay_toggles(request):
    overlay_states = OverlayState.objects.get(user=request.user)

    template_data = {
        'overlay_states': overlay_states,
    }

    return render(request, 'popouts/overlay-toggles.html', template_data)


@login_required
def overlay_customize(request):
    leagues = League.objects.all()
    league_groups = LeagueGroup.objects.all()
    overlay_styles = OverlayStyle.objects.get(user=request.user)

    template_data = {
        'leagues': leagues,
        'league_groups': league_groups,
        'overlay_styles': overlay_styles
    }

    return render(request, 'overlays/customize.html', template_data)


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
def sponsors(request):
    sponsors = Sponsor.objects.all()
    leagues = League.objects.all()
    league_groups = LeagueGroup.objects.all()

    template_data = {
        'sponsors': sponsors,
        'leagues': leagues,
        'league_groups': league_groups,
    }

    return render(request, 'data/sponsors.html', template_data)


@login_required
def teams(request):
    template_data = {}

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
    form = NewMatchForm()

    template_data = {
        'league_groups': league_groups,
        'leagues': leagues,
        'seasons': seasons,
        'teams': teams,
        'sponsors': sponsors,
        'form': form,
    }

    return render(request, 'matches/create.html', template_data)


@login_required
def match_overview(request, match_id):
    users = User.objects.all()
    match = Match.objects.get(id=match_id)
    match_users = match.user.all()
    match_sponsors = []
    for s in match.sponsors.all():
        match_sponsors.append(s)

    template_data = {
        'users': users,
        'match': match,
        'match_users': match_users,
        'match_sponsors': match_sponsors,
    }

    return render(request, 'matches/overview.html', template_data)


@login_required
def match_details(request, match_id):
    match = Match.objects.get(id=match_id)
    map_bans = MatchMap.objects.filter(match=match).all().order_by("order")
    operator_bans = OperatorBans.objects.filter(match=match).all()
    rounds = Round.objects.filter(match=match).all()

    template_data = {
        'match': match,
        'map_bans': map_bans,
        'operator_bans': operator_bans,
        'rounds': rounds,
    }

    return render(request, 'matches/details.html', template_data)


@login_required
def match_maps(request, match_id):
    match = Match.objects.get(id=match_id)
    maps = Map.objects.all()

    if match.state == 3 or match.state == 4:
        try:
            next_map_id = MatchMap.objects.get(match=match, status=2).map.id
        except MatchMap.DoesNotExist:
            next_map_id = None
    else:
        try:
            next_map_id = MatchMap.objects.get(match=match, play_order=1).map.id
        except MatchMap.DoesNotExist:
            next_map_id = None

    template_data = {
        'match': match,
        'maps': maps,
        'next_map_id': next_map_id,
    }

    return render(request, 'matches/maps.html', template_data)


@login_required
def match_opbans(request, match_id, map_id):
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)
    current_match_map = MatchMap.objects.get(match=match_id, map=map_id)
    atk_ops = Operator.objects.filter(side="ATK").order_by('name')
    def_ops = Operator.objects.filter(side="DEF").order_by('name')
    operator_ban_query = OperatorBans.objects.filter(match_id=match.id, map_id=map.id).all()

    operator_bans = []
    for op in operator_ban_query:
        operator_bans.append(op)

    template_data = {
        'match': match,
        'map': map,
        'current_match_map': current_match_map,
        'atk_ops': atk_ops,
        'def_ops': def_ops,
        'operator_bans': operator_bans,
    }

    return render(request, 'matches/opbans.html', template_data)


@login_required
def match_rounds(request, match_id, map_id):
    match = Match.objects.get(id=match_id)
    map = Map.objects.get(id=map_id)
    bomb_spots = BombSpot.objects.filter(map=map).all()
    rounds = Round.objects.filter(match=match, map=map).all()

    template_data = {
        'match': match,
        'map': map,
        'bomb_spots': bomb_spots,
        'rounds': rounds,
    }

    return render(request, 'matches/rounds.html', template_data)


# Vue

def teams_vue(request):
    return render(request, 'data/teams-vue.html')
