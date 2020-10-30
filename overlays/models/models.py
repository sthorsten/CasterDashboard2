""" Overlay model definitions

This file contains all models regarding overlays.

"""

import logging
import secrets

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from dashboard.models.models import Match, Team, Map, Profile
from websockets.helper import send_match_data_to_consumers

logger = logging.getLogger(__name__)


class OverlayStyle(models.Model):
    # Represents the currently selected overlay styles

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_style = models.CharField(max_length=255, default="default")
    ingame_style = models.CharField(max_length=255, default="default")
    ingame_names = models.BooleanField(default=True)
    opbans_style = models.CharField(max_length=255, default="default")
    maps_style = models.CharField(max_length=255, default="default")
    rounds_style = models.CharField(max_length=255, default="default")
    timer_style = models.CharField(max_length=255, default="default")

    def __str__(self):
        return f'Overlay Style: {str(self.user)}'


class OverlayState(models.Model):
    # Represents the overlay state for each overlay

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

    def __str__(self):
        return f'Overlay State: {str(self.user)}'


@receiver(post_save, sender=OverlayState)
def overlay_state_post_save(sender, instance, **kwargs):
    # Sends overlay state message to websockets on change
    from overlays.models.serializers import OverlayStateSerializer

    channel_layer = get_channel_layer()
    data = OverlayStateSerializer(instance).data
    async_to_sync(channel_layer.group_send)(
        str(instance.user) + "_overlay_state",
        {
            "type": "send_message",
            "message": data,
        }
    )


class MatchOverlayData(models.Model):
    # Hold the current and next match a user selected for use in the overlays

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='current_match')
    next_match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=True, null=True, related_name='next_match')

    def __str__(self):
        return f'Match Overlay Data: {str(self.user)}'


@receiver(post_save, sender=MatchOverlayData)
def match_overlay_data_post_save(sender, instance, **kwargs):
    # Send the new match data to websockets on change
    send_match_data_to_consumers(instance.current_match)


class PollOverlayData(models.Model):
    # Represents poll data used by in the poll overlay

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value_blue = models.IntegerField(default=0)
    value_draw = models.IntegerField(default=0)
    value_orange = models.IntegerField(default=0)

    def __str__(self):
        return f'Poll Overlay Data: {str(self.user)}'


class SocialOverlayData(models.Model):
    # Represents a line that is being displayed and switched through in the social overlay

    TYPE_CHOICES = [
        (1, "League"),
        (2, "Twitch"),
        (3, "Twitter"),
        (4, "YouTube"),
        (5, "Instagram"),
        (6, "Facebook"),
        (7, "Website"),
        (8, "Other")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Social Overlay Data: {str(self.user)}'


class TimerOverlayData(models.Model):
    # Represents a timer or a clock in the overlay

    MODE_CHOICES = [
        (1, 'Clock'),
        (2, 'Timer')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mode = models.IntegerField(choices=MODE_CHOICES, default=1)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'Timer Overlay Data: {str(self.user)}'


class TickerOverlayData(models.Model):
    # Represents additional text in the ticker overlay

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Ticker Overlay Data: {str(self.user)}'


@receiver(post_save, sender=User)
def new_user_post_save(sender, instance, created, **kwargs):
    # Create overlay entries when a new user is created

    if created:
        registration_token = secrets.token_hex(64)
        Profile.objects.create(user=instance, registration_token=registration_token)
        Token.objects.get_or_create(user=instance)

        OverlayStyle.objects.create(user=instance)
        OverlayState.objects.create(user=instance)
        MatchOverlayData.objects.create(user=instance)
        PollOverlayData.objects.create(user=instance)
        SocialOverlayData.objects.create(user=instance)
        TimerOverlayData.objects.create(user=instance)
        TickerOverlayData.objects.create(user=instance)
