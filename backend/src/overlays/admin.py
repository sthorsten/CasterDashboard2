from django.contrib import admin

from . import models


@admin.register(models.CustomDesignStyle)
class CustomDesignStyleAdmin(admin.ModelAdmin):
    list_display = ('league', 'id')
    readonly_fields = ('id',)

    ordering = ('league',)


@admin.register(models.UserOverlay)
class UserOverlayAdmin(admin.ModelAdmin):
    list_display = ('user', 'overlayMatch', 'useCustomDesign', 'id')
    readonly_fields = ('id',)

    ordering = ('user',)
    list_filter = ('overlayLeague', 'overlayMatch', 'useCustomDesign')

    fieldsets = (
        ('Base information', {
         'fields': ('id', 'user')}),
        ('Overlay Data', {
         'fields': ('overlayLeague', 'overlayMatch')}),
        ('Custom Design', {
            'fields': ('useCustomDesign', 'customDesignStyle')
        })
    )
