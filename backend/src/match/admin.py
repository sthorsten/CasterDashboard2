from django.contrib import admin
from . import models


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MapBan)
class MapBanAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MatchMap)
class MatchMapAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OperatorBan)
class OperatorBansAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    pass
