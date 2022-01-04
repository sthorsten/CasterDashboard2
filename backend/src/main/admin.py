from django.contrib import admin
from django.utils.html import format_html
from . import models


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'public', 'customDesign', 'logoPreview', 'id')
    readonly_fields = ('id', 'created', 'lastModified',
                       'logoPreviewLarge', 'logoSmall')

    fieldsets = (
        ('Base information', {
         'fields': ('id', 'name', 'public', 'customDesign')}),
        ('Logo', {'fields': ('logo', 'logoSmall', 'logoPreviewLarge')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )
    ordering = ('name',)
    list_filter = ('public', 'customDesign')

    @admin.display(description="Logo preview")
    def logoPreview(self, obj):
        if obj.logoSmall:
            return format_html(f'<img src="{obj.logoSmall.url}" height="20px" width="20px" />')
        return ""

    @admin.display(description="Logo preview")
    def logoPreviewLarge(self, obj):
        if obj.logoSmall:
            return format_html(f'<img src="{obj.logoSmall.url}" />')
        return ""


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'seasonNo', 'league', 'id')
    readonly_fields = ('id', 'created', 'lastModified')
    fieldsets = (
        ('Base information', {
         'fields': ('id', 'name', 'seasonNo', 'league', 'playdayCount')}),
        ('Dates', {'fields': ('startDate', 'endDate')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )
    ordering = ('league', 'name', 'seasonNo')
    list_filter = ('league', 'seasonNo')


@admin.register(models.Playday)
class PlaydayAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'playdayNo', 'id')
    readonly_fields = ('id', 'created', 'lastModified')
    fieldsets = (
        (None, {'fields': ('id', 'name', 'season', 'playdayNo', 'date')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )

    ordering = ('season', 'name', 'playdayNo')
    list_filter = ('season', 'season__league', 'playdayNo')


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'id')
    readonly_fields = ('id', 'created', 'lastModified')
    fieldsets = (
        ('Base information', {'fields': ('id', 'name', 'league')}),
        ('Date information', {'fields': ('startDate', 'endDate')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )

    ordering = ('league', 'name')
    list_filter = ('league',)


@admin.register(models.Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'public', 'league', 'id')
    readonly_fields = ('id', 'created', 'lastModified')
    fieldsets = (
        (None, {'fields': ('id', 'name', 'public', 'league', 'logo')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )

    ordering = ('league', 'name')
    list_filter = ('league', 'public')


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'logoPreview', 'id')
    readonly_fields = ('id', 'created', 'lastModified',
                       'logoSmall', 'logoPreviewLarge')

    fieldsets = (
        ('Base information', {
         'fields': ('id', 'name')}),
        ('Logo', {'fields': ('logo', 'logoSmall', 'logoPreviewLarge')}),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created', 'lastModified')
        })
    )
    ordering = ('name',)

    @admin.display(description="Logo preview")
    def logoPreview(self, obj):
        if obj.logoSmall:
            return format_html(f'<img src="{obj.logoSmall.url}" height="20px" width="20px" />')
        return ""

    @admin.display(description="Logo preview")
    def logoPreviewLarge(self, obj):
        if obj.logoSmall:
            return format_html(f'<img src="{obj.logoSmall.url}" />')
        return ""
