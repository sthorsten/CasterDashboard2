""" Main model definitions

This file contains all main models (excluding Overlay models) for the dashboard.
Serializers and receivers can be found in the serializers.py and receivers.py file respectively.

"""

import logging
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from dashboard.validators import *

logger = logging.getLogger(__name__)


class Profile(models.Model):
    # The profile extends django's default user model to allow for a few extra fields

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=128, blank=True, null=True)
    confirmed = models.BooleanField(default=0)

    def __str__(self):
        return str(self.user)


class Map(models.Model):
    # Represents a map in Rainbow Six Siege

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MapPool(models.Model):
    # A collection of maps (e.g. Competetive, Ranked, Casual Map Pool)

    name = models.CharField(max_length=255)
    maps = models.ManyToManyField(Map)

    def __str__(self):
        return self.name


class BombSpot(models.Model):
    # Represents a bomb spot location in Rainbow Six Siege

    FLOOR_CHOICES = [
        ('B', 'Basement'),
        ('1F', 'First Floor'),
        ('2F', 'Second Floor'),
        ('3F', 'Third Floor'),
        ('EXT', "Exterior")
    ]

    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    floor = models.CharField(max_length=3, choices=FLOOR_CHOICES, default='1F')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(map)}: {self.floor} - {self.name}'


class Operator(models.Model):
    # Represents an Operator in Rainbow Six Siege

    name = models.CharField(max_length=255)
    side = models.CharField(max_length=3)

    def __str__(self):
        return self.name


def league_logo_path(instance, filename):
    return f'leagues/{instance.id}.png'


class League(models.Model):
    # Represents a league
    # Leagues have their own management and logo to be displayed in the overlays
    # Matches are usually first being categorized into leagues

    name = models.CharField(max_length=255)
    is_restricted = models.BooleanField(default=True)
    has_custom_overlay = models.BooleanField(default=False)
    league_logo = models.ImageField(upload_to=league_logo_path, validators=[validate_square_logo], blank=True,
                                    null=True)
    league_logo_small = models.ImageField(upload_to=league_logo_path, blank=True, null=True)

    def __str__(self):
        return self.name


class LeagueGroup(models.Model):
    # Represents how a user can interact with a league

    RANK_CHOICES = [
        # Users can see, create and manage own matches in the league
        # Operators can additionally see all matches even from other users in the league, but read only
        # Managers have additional write access to all league matches from other users
        # Admins can additionally manage the league, create sponsors, etc.

        (1, 'User'),
        (2, 'Operator'),
        (3, 'Manager'),
        (4, 'Admin')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    rank = models.IntegerField(choices=RANK_CHOICES, default=1)

    def __str__(self):
        return f'{str(self.league)}: {str(self.user)} ({self.get_rank_display()})'


class Season(models.Model):
    # Represents either an official "generic" Rainbow Six Siege season (as released by Ubisoft)
    # or a custom one for categorizing matches.
    # A season can also be associated with a league to allow for even more detailed categorizing of matches
    # as well as being able to restrict access to that season

    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    official_season = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        # Include the league in brackets if the season belongs to a league
        if self.league is None:
            return self.name
        else:
            return f'{self.name} ({str(self.league)})'


def team_logo_path(instance, filename):
    if instance.id:
        return f'teams/{instance.id}.png'
    else:
        return f'teams/{filename}'


class Sponsor(models.Model):
    # Represents a sponsor, that are either available to all users or can be associated with a league
    # Sponsor logos are displayed in various overlays

    name = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    sponsor_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    light_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    dark_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    # Represents a team that plays in matches

    name = models.CharField(max_length=22, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    team_logo = models.ImageField(upload_to=team_logo_path, validators=[validate_square_logo], blank=True, null=True)
    team_logo_small = models.ImageField(upload_to=team_logo_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    # Represents a Rainbow Six Siege match
    # Matches are the core of this program and utilizes most of the other models.

    SHARE_MODE_CHOICES = [
        # Options on what access is granted to a user if it is shared with one.

        (1, "None"),
        (2, "Read Only"),
        (3, "Read Write")
    ]

    STATUS_CHOICES = [
        (1, "Created"),
        (2, "Map Ban"),
        (3, "Playing"),
        (4, "Finished"),
        (5, "Dummy")
    ]

    user = models.ManyToManyField(User)
    share_mode = models.IntegerField(choices=SHARE_MODE_CHOICES, default=1)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    title = models.CharField(max_length=22)
    sponsors = models.ManyToManyField(Sponsor, blank=True, null=True)
    subtitle = models.CharField(max_length=22, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATUS_CHOICES, default=1)
    best_of = models.IntegerField(default=1)
    team_blue = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="match_team_blue")
    team_orange = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="match_team_orange")
    score_blue = models.IntegerField(default=0)
    score_orange = models.IntegerField(default=0)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="match_win_team")

    def __str__(self):
        return f'{str(self.id)}: {str(self.team_blue)} vs. {str(self.team_orange)}'


class MatchMap(models.Model):
    # Represents a map being either banned in the Map Pick & Ban phase or being played in a match by it's teams

    TYPE_CHOICES = [
        (1, "Ban"),
        (2, "Pick"),
        (3, "Decider"),
        (4, "Default Ban")
    ]

    STATUS_CHOICES = [
        (1, "Created"),
        (2, "Playing"),
        (3, "Finished")
    ]

    WIN_TYPE_CHOICES = [
        (1, "None"),
        (2, "Regular Win"),
        (3, "Overtime Win"),
        (4, "Draw")
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    order = models.IntegerField(default=0)
    play_order = models.IntegerField(default=0)
    choose_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='choose_team')
    atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="map_atk_team")
    ot_atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="ot_atk_team")
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='map_win_team')
    win_type = models.IntegerField(choices=WIN_TYPE_CHOICES, default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    score_blue = models.IntegerField(default=0)
    score_orange = models.IntegerField(default=0)

    def __str__(self):
        return f'{str(self.id)}: {str(self.map)} (Match {self.match.id})'


class OperatorBans(models.Model):
    # Represents an operator that is being banned by a team during a map in a match

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f'{str(self.operator)} (Match: {self.match.id}, Map: {str(self.map)})'


class Round(models.Model):
    # Represents a single round of a match being played

    WIN_TYPE_CHOICES = [
        (1, "Kills"),
        (2, "Defuser Planted"),
        (3, "Defuser Disabled"),
        (4, "Time")
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    round_no = models.IntegerField()
    bomb_spot = models.ForeignKey(BombSpot, on_delete=models.CASCADE)
    atk_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_atk_team")
    def_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_def_team")
    of_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name="round_of_team")
    win_type = models.IntegerField(choices=WIN_TYPE_CHOICES, default=1)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_win_team")
    score_blue = models.IntegerField()
    score_orange = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{str(self.round_no)} (Match: {str(self.match.id)}, Map: {str(self.map)})'
