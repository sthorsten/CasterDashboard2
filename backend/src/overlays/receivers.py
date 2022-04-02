from django.db.models import signals
from django.dispatch import receiver
from util import websocket
from . import models
from . import serializers


@receiver(signals.post_save, sender=models.CustomDesignStyle)
def custom_design_style_post_save(instance, created, **kwargs):
    # Send data via websocket
    serialized_data = serializers.CustomDesignStyleSerializer(instance).data
    websocket.send_server_data(
        "overlays", "CustomDesignStyle", serialized_data)


@receiver(signals.post_save, sender=models.UserOverlay)
def user_overlay_post_save(instance, created, **kwargs):
    # Send data via websocket
    serialized_data = serializers.UserOverlaySerializer(instance).data
    websocket.send_server_data("overlays", "UserOverlay", serialized_data)
