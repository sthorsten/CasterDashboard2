from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'accountConfirmed', 'id')
    readonly_fields = ('id', 'registrationToken')
    fields = ('id', 'user', 'accountConfirmed', 'registrationToken')
    ordering = ('user',)
    list_filter = ('accountConfirmed',)


@admin.register(models.LeagueAccessGroup)
class LeagueAccessGroupAdmin(admin.ModelAdmin):
    pass
