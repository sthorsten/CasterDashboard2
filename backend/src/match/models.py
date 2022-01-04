from django.db import models
from django.contrib.auth import get_user_model
from core.models import Map, BombSpot, Operator
from main.models import League, Season, Sponsor, Team

# pylint: disable=no-member

User = get_user_model()


class Match(models.Model):
    """ Represents a Rainbow Six Siege match
        Matches are the core of this program and utilizes most of the other models.
    """

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
    sponsors = models.ManyToManyField(Sponsor)
    subtitle = models.CharField(max_length=22, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATUS_CHOICES, default=1)
    best_of = models.IntegerField(default=1)
    team_blue = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_team_blue")
    team_orange = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_team_orange")
    score_blue = models.IntegerField(default=0)
    score_orange = models.IntegerField(default=0)
    win_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=True, null=True, related_name="match_win_team")

    def __str__(self) -> str:
        return f'{str(self.id)}: {str(self.team_blue)} vs. {str(self.team_orange)}'


class MatchMap(models.Model):
    """Represents a map being either banned in the Map Pick & Ban phase or being played in a match by it's teams"""

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
    choose_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name='choose_team')
    atk_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="map_atk_team")
    ot_atk_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="ot_atk_team")
    win_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True, related_name='map_win_team')
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

    def __str__(self) -> str:
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
    atk_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="round_atk_team")
    def_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="round_def_team")
    of_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE, related_name="round_of_team")
    win_type = models.IntegerField(choices=WIN_TYPE_CHOICES, default=1)
    win_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="round_win_team")
    score_blue = models.IntegerField()
    score_orange = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{str(self.round_no)} (Match: {str(self.match.id)}, Map: {str(self.map)})'


class MatchGroup(models.Model):
    # Represents a group of matches, i.e. a tournament, matches of the day, etc.

    name = models.CharField(max_length=255)
    date = models.DateField()
    users = models.ManyToManyField(get_user_model())
    matches = models.ManyToManyField(Match)

    def __str__(self) -> str:
        return str(self.name)
