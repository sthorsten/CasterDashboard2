"""Dashboard Model Admins

All dashboard models have an admin page which is defined here.
Most admin pages have customized list columns and details page categories.
"""

from django.contrib import admin
from django.utils.translation import gettext as _

from dashboard.models.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'confirmed')


class BombSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'map', 'floor')


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'side')


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_restricted', 'has_custom_overlay')
    fieldsets = [
        (_("Base Information"), {'fields': ['name', 'is_restricted', 'has_custom_overlay']}),
        (_("Logos"), {'fields': ['league_logo', 'league_logo_small']})
    ]


class LeagueGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'league', 'rank')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'official_season', 'start_date', 'end_date')
    fieldsets = [
        (_("Base Information"), {'fields': ['name', 'league', 'official_season']}),
        (_("Dates"), {'fields': ['start_date', 'end_date']})
    ]


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'public', 'league')
    fieldsets = [
        (_("Base Information"), {'fields': ['name', 'public', 'league']}),
        (_("Logos"), {'fields': ['sponsor_logo', 'light_logo', 'dark_logo']})
    ]


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    readonly_fields = ('created',)
    fieldsets = [
        (_("Base Information"), {'fields': ['name', 'created']}),
        (_("Logos"), {'fields': ['team_logo', 'team_logo_small']})
    ]


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'league', 'team_blue', 'team_orange', 'state', 'created')
    readonly_fields = ('created',)
    fieldsets = [
        (_("Base Information"), {'fields': ['title', 'subtitle', 'best_of', 'state', 'created']}),
        (_("Match Details"), {'fields': ['league', 'season', 'team_blue', 'team_orange', 'sponsors']}),
        (_("Results"), {'fields': ['score_blue', 'score_orange', 'win_team']}),
        (_("Access"), {'fields': ['user', 'share_mode']})
    ]


class MatchMapAdmin(admin.ModelAdmin):
    list_display = ('map', 'match', 'type', 'order', 'play_order', 'choose_team', 'status')
    fieldsets = [
        (_("Base Information"), {'fields': ['match', 'map', 'status']}),
        (_("Map Details"), {'fields': ['type', 'order', 'play_order']}),
        (_("Team Details"), {'fields': ['choose_team', 'atk_team', 'ot_atk_team']}),
        (_("Results"), {'fields': ['score_blue', 'score_orange', 'win_type', 'win_team']}),
    ]


class OperatorBansAdmin(admin.ModelAdmin):
    list_display = ('operator', 'match', 'map', 'team', 'order')
    fieldsets = [
        (_("Base Information"), {'fields': ['match', 'map']}),
        (_("Details"), {'fields': ['operator', 'order', 'team']}),
    ]


class RoundAdmin(admin.ModelAdmin):
    list_display = ('round_no', 'match', 'map', 'bomb_spot', 'win_type', 'score_blue', 'score_orange')
    fieldsets = [
        (_("Base Information"), {'fields': ['match', 'map', 'round_no']}),
        (_("Round Details"), {'fields': ['bomb_spot', 'win_type', 'win_team', 'notes']}),
        (_("Team Details"), {'fields': ['atk_team', 'def_team', 'of_team']}),
        (_("Results"), {'fields': ['score_blue', 'score_orange']}),
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Map)
admin.site.register(MapPool)
admin.site.register(BombSpot, BombSpotAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueGroup, LeagueGroupAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchMap, MatchMapAdmin)
admin.site.register(OperatorBans, OperatorBansAdmin)
admin.site.register(Round, RoundAdmin)
