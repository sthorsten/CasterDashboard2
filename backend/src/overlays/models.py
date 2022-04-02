""" Overlay model definitions

This file contains all models regarding overlays.

"""

import logging

from django.contrib.auth import get_user_model
from django.db import models

from main.models import League
from match.models import Match

logger = logging.getLogger(__name__)
User = get_user_model()


# pylint: disable=no-member

class CustomDesignStyle(models.Model):
    league = models.OneToOneField(League, on_delete=models.CASCADE)

    hasStartStyle = models.BooleanField(
        default=False, verbose_name="has start style")
    hasIngameStyle = models.BooleanField(
        default=False, verbose_name="has ingame style")
    hasMapBanStyle = models.BooleanField(
        default=False, verbose_name="has rounds style")
    hasRoundsStyle = models.BooleanField(
        default=False, verbose_name="has rounds style")
    hasFooterStyle = models.BooleanField(
        default=False, verbose_name="has footer style")

    def __str__(self) -> str:
        return str(f'CustomDesign ({self.league})')

    def __repr__(self) -> str:
        return f'<Custom Design {self.league}>'

    class Meta:
        verbose_name = "Custom Design Style"


class UserOverlay(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    overlayLeague = models.ForeignKey(
        League, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="overlay league")
    overlayMatch = models.ForeignKey(
        Match, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="overlay match")

    useCustomDesign = models.BooleanField(
        default=False, verbose_name="uses custom design")
    customDesignStyle = models.ForeignKey(
        CustomDesignStyle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="custom design style")

    def __str__(self) -> str:
        return str(f'UserOverlay ({self.user})')

    def __repr__(self) -> str:
        return f'<User Overlay {self.user}>'

    class Meta:
        verbose_name = "User Overlay"
