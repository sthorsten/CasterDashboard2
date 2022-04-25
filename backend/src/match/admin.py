from django.contrib import admin
from . import models


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'leagueName', 'seasonName', 'playdayName',
                    'tournament', 'status', 'teamBlue', 'teamOrange', 'date', 'id')

    readonly_fields = ('id', 'created', 'lastModified', 'creator')
    fieldsets = (
        ('Base Information', {
            'fields': ('id', 'name', 'title', 'subTitle', 'bestOf', 'status', 'date')
        }),
        ('League Information', {
            'fields': ('league', 'playday', 'tournament')
        }),
        ('Teams and Score', {
            'fields': ('teamBlue', 'teamOrange', 'scoreBlue', 'scoreOrange', 'winTeam', 'winType')
        }),
        ('Access', {
            'fields': ('creator', 'shareMode', 'additionalUsers')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )
    ordering = ('-date',)
    list_filter = ('playday__season__league', 'playday__season',
                   'tournament__league', 'teamBlue', 'teamOrange', 'status')

    @admin.display(description="playday")
    def playdayName(self, obj):
        return obj.playday.name

    @admin.display(description="season")
    def seasonName(self, obj):
        return obj.playday.season.name

    @admin.display(description="league")
    def leagueName(self, obj):
        return obj.playday.season.league.name


@admin.register(models.MapBan)
class MapBanAdmin(admin.ModelAdmin):
    list_display = ('match', 'map', 'team', 'type', 'order', 'id')
    readonly_fields = ('id',)

    fieldsets = (
        ('Base Information', {
            'fields': ('id', 'match', 'map', 'team')
        }),
        ('Additional Information', {
            'fields': ('type', 'order', 'isDecider')
        })
    )
    ordering = ('match', 'order')
    list_filter = ('map', 'team')


@admin.register(models.MatchMap)
class MatchMapAdmin(admin.ModelAdmin):
    list_display = ('match', 'map', 'status', 'order',
                    'scoreBlue', 'scoreOrange', 'id')
    readonly_fields = ('id',)
    fieldsets = (
        ('Base Information', {
            'fields': ('id', 'status', 'order')
        }),
        ('Match Information', {
            'fields': ('match', 'map')
        }),
        ('Team Information', {
            'fields': ('atkTeam', 'defTeam', 'otAtkTeam', 'otDefTeam')
        }),
        ('Score', {
            'fields': ('scoreBlue', 'scoreOrange', 'winType', 'winTeam')
        })
    )
    ordering = ('match', 'order')
    list_filter = ('map', 'status', 'winType')


@admin.register(models.OperatorBan)
class OperatorBansAdmin(admin.ModelAdmin):
    list_display = ('operator', 'matchName', 'mapName', 'team', 'order', 'id')
    readonly_fields = ('id',)

    fieldsets = (
        ('Base Information', {
            'fields': ('id', 'matchMap')
        }),
        ('Operator Ban', {
            'fields': ('order', 'operator', 'team')
        })
    )

    ordering = ('matchMap', 'order')
    list_filter = ('matchMap__map', 'operator', 'team')

    @admin.display(description="match")
    def matchName(self, obj):
        return obj.matchMap.match

    @admin.display(description="map")
    def mapName(self, obj):
        return obj.matchMap.map


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('roundNo', 'matchName', 'mapName',
                    'bombSpot', 'winType', 'winTeam', 'id')
    readonly_fields = ('id',)

    fieldsets = (
        ('Base Information', {
            'fields': ('id', 'matchMap', 'roundNo')
        }),
        ('Round Information', {
            'fields': ('bombSpot', 'openingFragTeam', 'winTeam', 'winType')
        }),
        ('Notes', {
            'fields': ('notes',)
        })
    )

    ordering = ('matchMap', 'roundNo')
    list_filter = ('matchMap__map', 'winType', 'winTeam')

    @admin.display(description="match")
    def matchName(self, obj):
        return obj.matchMap.match

    @admin.display(description="map")
    def mapName(self, obj):
        return obj.matchMap.map
