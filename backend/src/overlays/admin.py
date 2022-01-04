from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from . import models


@admin.register(models.OverlayStyle)
class OverlayStyleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OverlayState)
class OverlayStateAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.MatchOverlayData)
# class MatchOverlayDataAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.PollOverlayData)
class PollOverlayDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SocialOverlayData)
class SocialOverlayDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TimerOverlayData)
class TimerOverlayDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TickerOverlayData)
class TickerOverlayDataAdmin(admin.ModelAdmin):
    pass
