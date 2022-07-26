from asgiref.sync import sync_to_async
from sockets.sio_server import sio
from .models import League, Playday, Season, Sponsor, Team
from .serializers import LeagueSerializer, PlaydaySerializer, SeasonSerializer, SponsorSerializer, TeamSerializer


def _list_leagues():
    leagues = League.objects.all()
    serializer = LeagueSerializer(leagues, many=True)
    return serializer.data


def _get_league(league_id):
    if league_id:
        league_result = League.objects.get(id=league_id)
    else:
        return None
    serializer = LeagueSerializer(league_result)
    return serializer.data


def _list_seasons():
    seasons = Season.objects.all()
    serializer = SeasonSerializer(seasons, many=True)
    return serializer.data


def _get_season(season_id):
    if season_id:
        season_result = Season.objects.get(id=season_id)
    else:
        return None
    serializer = SeasonSerializer(season_result)
    return serializer.data


def _get_seasons_by_league(league_id):
    if league_id:
        seasons = Season.objects.filter(league=league_id)
    else:
        return None
    serializer = SeasonSerializer(seasons, many=True)
    return serializer.data


def _list_playdays():
    playdays = Playday.objects.all()
    serializer = PlaydaySerializer(playdays, many=True)
    return serializer.data


def _get_playday(playday_id):
    if playday_id:
        playday_result = Playday.objects.get(id=playday_id)
    else:
        return None
    serializer = PlaydaySerializer(playday_result)
    return serializer.data


def _get_playdays_by_season(season_id):
    if season_id:
        playdays = Playday.objects.filter(season=season_id)
    else:
        return None
    serializer = PlaydaySerializer(playdays, many=True)
    return serializer.data


def _list_sponsors():
    sponsors = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsors, many=True)
    return serializer.data


def _get_sponsor(sponsor_id):
    if sponsor_id:
        sponsor_result = Sponsor.objects.get(id=sponsor_id)
    else:
        return None
    serializer = SponsorSerializer(sponsor_result)
    return serializer.data


def _list_teams():
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return serializer.data


def _get_team(team_id, team_name):
    if team_id:
        team_result = Team.objects.get(id=team_id)
    elif team_name:
        team_result = Team.objects.get(name=team_name)
    else:
        return None
    serializer = TeamSerializer(team_result)
    return serializer.data


@sio.on("league:list", namespace="/main")
async def on_league_list(sid, data):
    leagues = await sync_to_async(_list_leagues)()
    return leagues


@sio.on("league:get", namespace="/main")
async def on_league_get(sid, data):
    league_id = data.get("id")
    league = await sync_to_async(_get_league)(league_id)
    return league


@sio.on("season:list", namespace="/main")
async def on_season_list(sid, data):
    league_id = data.get("league")
    if league_id:
        seasons = await sync_to_async(_get_seasons_by_league)(league_id)
    else:
        seasons = await sync_to_async(_list_seasons)()
    return seasons


@sio.on("season:get", namespace="/main")
async def on_season_get(sid, data):
    season_id = data.get("id")
    season = await sync_to_async(_get_season)(season_id)
    return season


@sio.on("playday:list", namespace="/main")
async def on_playday_list(sid, data):
    season_id = data.get("season")
    if season_id:
        playdays = await sync_to_async(_get_playdays_by_season)(season_id)
    else:
        playdays = await sync_to_async(_list_playdays)()
    return playdays


@sio.on("playday:get", namespace="/main")
async def on_playday_get(sid, data):
    playday_id = data.get("id")
    playday = await sync_to_async(_get_playday)(playday_id)
    return playday


@sio.on("sponsor:list", namespace="/main")
async def on_sponsor_list(sid, data):
    sponsors = await sync_to_async(_list_sponsors)()
    return sponsors


@sio.on("sponsor:get", namespace="/main")
async def on_sponsor_get(sid, data):
    sponsor_id = data.get("id")
    sponsor = await sync_to_async(_get_sponsor)(sponsor_id)
    return sponsor


@sio.on("team:list", namespace="/main")
async def on_team_list(sid, data):
    teams = await sync_to_async(_list_teams)()
    return teams


@sio.on("team:get", namespace="/main")
async def on_team_get(sid, data):
    team_id = data.get("id")
    team_name = data.get("name")
    team = await sync_to_async(_get_team)(team_id, team_name)
    return team
