import json
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Match, Team, Map

logger = logging.getLogger(__name__)


class OverlayStyle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


@receiver(post_save, sender=User)
def create_user_overlay_style(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating OverlayStyle via receiver" % instance)
        OverlayStyle.objects.create(user=instance)


class OverlayState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


@receiver(post_save, sender=User)
def create_user_overlay_state(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating OverlayState via receiver" % instance)
        OverlayState.objects.create(user=instance)


@receiver(post_save, sender=OverlayState)
def overlay_state_post_save(sender, instance, **kwargs):
    # Send message to Websocket Consumer
    channel_layer = get_channel_layer()
    data = {
        "start_state": instance.start_state,
        "ingame_state": instance.ingame_state,
        "maps_state": instance.maps_state,
        "opbans_state": instance.opbans_state,
        "rounds_state": instance.rounds_state,
        "social_state": instance.social_state,
        "poll_state": instance.poll_state,
        "timer_state": instance.timer_state,
        "ticker_state": instance.ticker_state,
        "next_match_state": instance.next_match_state,
    }
    async_to_sync(channel_layer.group_send)(
        str(instance.user) + "_overlay_state",
        {
            "type": "send_message",
            "message": data,
        }
    )


class MatchOverlayData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    current_map = models.ForeignKey(Map, on_delete=models.SET_NULL, blank=True, null=True)
    current_atk_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)

    def serialize(self):
        if self.current_match is not None:
            current_match = self.current_match.id
        else:
            current_match = 0

        if self.current_map is not None:
            current_map = self.current_map.id
        else:
            current_map = 0

        if self.current_atk_team is not None:
            current_atk_team = self.current_atk_team.id
        else:
            current_atk_team = 0

        return {'user': self.user.id, 'current_match': current_match, 'current_map': current_map,
                'current_atk_team': current_atk_team}

    def __str__(self):
        return "MatchOverlayData: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_match_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating MatchOverlayData via receiver" % instance)
        MatchOverlayData.objects.create(user=instance)


@receiver(post_save, sender=MatchOverlayData)
def match_overlay_data_post_save(sender, instance, **kwargs):
    # Send message to Websocket Consumer
    channel_layer = get_channel_layer()
    match_overlay_data = instance.serialize()
    match = instance.current_match
    match_data = match.serialize()
    data = {'match_overlay_data': match_overlay_data, 'match': match_data}
    async_to_sync(channel_layer.group_send)(
        str(instance.user) + "_match_data",
        {
            "type": "send_message",
            "message": data,
        }
    )


class PollOverlayData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    value_blue = models.IntegerField(default=0)
    value_draw = models.IntegerField(default=0)
    value_orange = models.IntegerField(default=0)

    def __str__(self):
        return "PollOverlayData: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_poll_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating PollOverlayData via receiver" % instance)
        PollOverlayData.objects.create(user=instance)


class SocialOverlayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    social_type = models.CharField(max_length=255, blank=True, null=True)
    social_title = models.CharField(max_length=255, blank=True, null=True)
    social_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "SocialOverlayData: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_social_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating SocialOverlayData via receiver" % instance)
        SocialOverlayData.objects.create(user=instance)


class TimerOverlayData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return "TimerOverlayData: " + str(self.user) + " - " + self.value


@receiver(post_save, sender=User)
def create_user_timer_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating TimerOverlayData via receiver" % instance)
        TimerOverlayData.objects.create(user=instance)


class TickerOverlayData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name="current_match")
    next_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True, related_name="next_match")
    timer = models.ForeignKey(TimerOverlayData, on_delete=models.SET_NULL, blank=True, null=True)
    custom_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return "TickerOverlayData: " + str(self.user)


@receiver(post_save, sender=User)
def create_user_ticker_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating TickerOverlayData via receiver" % instance)
        TickerOverlayData.objects.create(user=instance)


class NextMatchOverlayData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "NextMatchOverlayData: " + str(self.user) + ": " + str(self.match)


@receiver(post_save, sender=User)
def create_user_next_match_overlay_data(sender, instance, created, **kwargs):
    if created:
        logger.debug("[User %s] Creating NextMatchOverlayData via receiver" % instance)
        NextMatchOverlayData.objects.create(user=instance)
