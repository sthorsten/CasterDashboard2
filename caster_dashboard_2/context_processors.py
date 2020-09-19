from caster_dashboard_2.version import get_current_version
from dashboard.models import LeagueGroup


def version_context(request):
    return {
        "version": get_current_version(),
        "theme": "dark",
    }


def profile_context(request):
    is_league_admin = False
    user = request.user
    league_groups = LeagueGroup.objects.all()
    for lg in league_groups:
        if lg.user == user and lg.rank == 'admin':
            is_league_admin = True

    return {
        "is_league_admin": is_league_admin
    }
