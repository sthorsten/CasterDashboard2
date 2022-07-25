import logging

from asgiref.sync import async_to_sync
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from sockets.sio_server import sio

from . import models
from . import serializers


# pylint: disable=unused-argument


logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=models.Notification)
def notification_post_save(instance, created, **kwargs):
    pass
    #serialized_data = serializers.NotificationSerializer(instance).data
    #websocket.send_server_data("core", "Notification", serialized_data)


@receiver(signals.post_save, sender=models.Map)
def map_post_save(sender, instance, created, **kwargs):
    if created:
        # Add map to "All" map pool
        logger.info("New map. Adding to 'All' map pool...")
        all_map_pool = models.MapPool.objects.get(name="All")
        all_map_pool.maps.add(instance)
        all_map_pool.save()

    serialized_data = serializers.MapSerializer(instance).data
    async_to_sync(sio.emit)("map:update", serialized_data, namespace="/core")


@receiver(signals.post_save, sender=models.MapPool)
def mappool_post_save(instance, created, **kwargs):
    serialized_data = serializers.MapPoolSerializer(instance).data
    async_to_sync(sio.emit)("mappool:update",
                            serialized_data, namespace="/core")


@receiver(signals.post_save, sender=models.BombSpot)
def bombspot_post_save(instance, created, **kwargs):
    serialized_data = serializers.BombSpotSerializer(instance).data
    async_to_sync(sio.emit)("bombspot:update",
                            serialized_data, namespace="/core")


@receiver(signals.post_save, sender=models.Operator)
def operator_post_save(instance, created, **kwargs):
    serialized_data = serializers.OperatorSerializer(instance).data
    async_to_sync(sio.emit)("operator:update",
                            serialized_data, namespace="/core")
