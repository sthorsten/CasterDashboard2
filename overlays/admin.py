from django.contrib import admin

from overlays.models.models import OverlayStyle, OverlayState, MatchOverlayData, PollOverlayData, \
    SocialOverlayData, TimerOverlayData, TickerOverlayData

admin.site.register(OverlayStyle)
admin.site.register(OverlayState)
admin.site.register(MatchOverlayData)
admin.site.register(PollOverlayData)
admin.site.register(SocialOverlayData)
admin.site.register(TimerOverlayData)
admin.site.register(TickerOverlayData)
