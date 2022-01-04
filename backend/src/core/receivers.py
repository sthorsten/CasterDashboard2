import logging

from django.db.models import signals
from django.dispatch.dispatcher import receiver
from util import websocket

from . import models
from . import serializers


# pylint: disable=unused-argument


logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=models.Notification)
def notification_post_save(instance, created, **kwargs):
    serialized_data = serializers.NotificationSerializer(instance).data
    websocket.send_server_data("core", "Notification", serialized_data)


@receiver(signals.post_save, sender=models.Map)
def map_post_save(sender, instance, created, **kwargs):
    if created:
        # Add map to "All" map pool
        logger.info("New map. Adding to 'All' map pool...")
        all_map_pool = models.MapPool.objects.get(name="All")
        all_map_pool.maps.add(instance)
        all_map_pool.save()

    serialized_data = serializers.MapSerializer(instance).data
    websocket.send_server_data("core", "Map", serialized_data)


@receiver(signals.post_save, sender=models.MapPool)
def mappool_post_save(instance, created, **kwargs):
    serialized_data = serializers.MapPoolSerializer(instance).data
    websocket.send_server_data("core", "MapPool", serialized_data)


@receiver(signals.post_save, sender=models.BombSpot)
def bombspot_post_save(instance, created, **kwargs):
    serialized_data = serializers.BombSpotSerializer(instance).data
    websocket.send_server_data("core", "BombSpot", serialized_data)


@receiver(signals.post_save, sender=models.Operator)
def operator_post_save(instance, created, **kwargs):
    serialized_data = serializers.OperatorSerializer(instance).data
    websocket.send_server_data("core", "Operator", serialized_data)
