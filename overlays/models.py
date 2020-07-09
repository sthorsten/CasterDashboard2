from django.contrib.auth.models import User
from django.db import models

from dashboard.models import Match, Team, Map


class OverlayStyle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_style = models.CharField(max_length=255, default="default")
    ingame_style = models.CharField(max_length=255, default="default")
    ingame_logos = models.BooleanField(default=True)
    opbans_style = models.CharField(max_length=255, default="default")
    maps_style = models.CharField(max_length=255, default="default")
    rounds_style = models.CharField(max_length=255, default="default")
    timer_style = models.CharField(max_length=255, default="default")
    next_match_style = models.CharField(max_length=255, default="default")

    def __str__(self):
        return "OverlayStyle: " + str(self.user)


class OverlayState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_state = models.BooleanField(default=True)
    ingame_state = models.BooleanField(default=True)
    maps_state = models.BooleanField(default=False)
    opbans_state = models.BooleanField(default=True)
    rounds_state = models.BooleanField(default=False)

    social_state = models.BooleanField(default=False)
    poll_state = models.BooleanField(default=False)
    timer_state = models.BooleanField(default=False)
    ticker_state = models.BooleanField(default=False)
    next_match_state = models.BooleanField(default=False)

    def __str__(self):
        return "OverlayState: " + str(self.user)


class MatchOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    current_map = models.ForeignKey(Map, on_delete=models.SET_NULL, blank=True, null=True)
    current_atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "MatchOverlayData: " + str(self.user)


class PollOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    value_blue = models.IntegerField(default=0)
    value_draw = models.IntegerField(default=0)
    value_orange = models.IntegerField(default=0)

    def __str__(self):
        return "PollOverlayData: " + str(self.user)


class SocialOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    social_type = models.CharField(max_length=255)
    social_title = models.CharField(max_length=255)
    social_text = models.CharField(max_length=255)

    def __str__(self):
        return "SocialOverlayData: " + str(self.user)


class TimerOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return "TimerOverlayData: " + str(self.user) + " - " + self.value


class TickerOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name="current_match")
    next_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True, related_name="next_match")
    timer = models.ForeignKey(TimerOverlayData, default="00:00", on_delete=models.SET_DEFAULT)
    custom_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return "TickerOverlayData: " + str(self.user)


class NextMatchOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "NextMatchOverlayData: " + str(self.user) + ": " + str(self.match)
