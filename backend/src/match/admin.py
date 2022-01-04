from django.contrib import admin
from . import models


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MatchMap)
class MatchMapAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OperatorBans)
class OperatorBansAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MatchGroup)
class MatchGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
