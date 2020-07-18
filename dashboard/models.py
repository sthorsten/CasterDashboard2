import logging
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=0)

    def __str__(self):
        return "Profile: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating profile via receiver" % instance)
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Version(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    release_date = models.DateField(auto_now_add=True, blank=True)
    changelog = models.TextField()

    def __str__(self):
        return self.name


class Map(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BombSpot(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    floor = models.CharField(max_length=7, default='1F')
    bomb_spot = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.bomb_spot


class Operator(models.Model):
    name = models.CharField(max_length=255)
    side = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=255)
    is_restricted = models.BooleanField(default=True)
    league_logo = models.ImageField(upload_to="leagues", blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=League)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # Auto delete image
    if instance.league_logo:
        if os.path.isfile(instance.league_logo.path):
            os.remove(instance.league_logo.path)


class LeagueGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    rank = models.CharField(max_length=255, default="user")

    def __str__(self):
        return "LeagueGroup: " + str(self.user) + " / " + str(self.league) + " / " + self.rank


class Season(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    official_season = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=22)
    created = models.DateTimeField(auto_now_add=True)
    has_logo = models.BooleanField(default=False)
    team_logo = models.ImageField(upload_to='teams', blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Team)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # Auto delete image
    if instance.team_logo:
        if os.path.isfile(instance.team_logo.path):
            os.remove(instance.team_logo.path)


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    sponsor_logo = models.ImageField(upload_to="sponsors", blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Sponsor)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # Auto delete image
    if instance.sponsor_logo:
        if os.path.isfile(instance.sponsor_logo.path):
            os.remove(instance.sponsor_logo.path)


class MatchState(models.Model):
    state = models.CharField(max_length=255, default="created")

    def __str__(self):
        return self.state


class Match(models.Model):
    user = models.ManyToManyField(User)
    share_mode = models.CharField(max_length=5, blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    title = models.CharField(max_length=22)
    subtitle = models.CharField(max_length=22, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.ForeignKey(MatchState, default=1, on_delete=models.SET_DEFAULT)
    best_of = models.IntegerField(default=1)
    team_blue = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_blue")
    team_orange = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_orange")
    score_blue = models.IntegerField(default=0)
    score_orange = models.IntegerField(default=0)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="match_win_team")

    def __str__(self):
        return str(self.id)


class MapBan(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id) + "- Match: " + str(self.match)


class MapWins(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.map.name) + "- Match: " + str(self.match)


class OperatorBans(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.operator.name + " - Match: " + str(self.match)


class Round(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    round_no = models.IntegerField()
    bombspot = models.ForeignKey(BombSpot, on_delete=models.CASCADE)
    atk_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="atk_team")
    def_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="def_team")
    win_type = models.CharField(max_length=255)
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="round_win_team")
    score_blue = models.IntegerField()
    score_orange = models.IntegerField()

    def __str__(self):
        return str(self.round_no) + " - Match: " + str(self.match)
