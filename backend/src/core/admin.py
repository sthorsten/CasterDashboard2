from django.contrib import admin
from django.utils.html import format_html
from . import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'show', 'showUntil', 'id')
    readonly_fields = ('id', 'created', 'lastModified')
    fieldsets = (
        ('Base information', {'fields': ('id', 'title', 'type', 'text')}),
        ('Show notification', {'fields': ('show', 'showUntil')}),
        ('Metadata',
         {
             'classes': ('collapse',),
             'fields': ('created', 'lastModified')
         })
    )

    ordering = ('show', 'showUntil')


@admin.register(models.Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'imagePreview', 'id')
    readonly_fields = ('id', 'imagePreviewLarge')
    fields = ('id', 'name', 'image', 'imagePreviewLarge')
    ordering = ('name',)

    @admin.display(description="Image preview")
    def imagePreview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" height="30px" />')
        return ""

    @admin.display(description="Image preview")
    def imagePreviewLarge(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" />')
        return ""


@admin.register(models.MapPool)
class MapPoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id',)
    fields = ('id', 'name', 'maps')
    ordering = ('name',)


@admin.register(models.BombSpot)
class BombSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'map', 'id')
    readonly_fields = ('id',)
    fields = ('id', 'map', 'floor', 'name')
    ordering = ('map', 'floor', 'name')
    list_filter = ('map', 'floor')


@admin.register(models.Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'side', 'identifier', 'id')
    readonly_fields = ('id',)
    fields = ('id', 'identifier', 'side', 'name')
    ordering = ('side', 'name')
    list_filter = ('side',)
