from asgiref.sync import async_to_sync
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from util.image import convert_square_logo, deleteLogoFiles

from sockets.sio_server import sio

from . import models
from . import serializers

# pylint: disable=unused-argument


@receiver(signals.post_save, sender=models.League)
def league_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    new_logo, new_logo_small = convert_square_logo(
        instance.logo, instance.logoSmall, "leagues")
    instance.logo = new_logo
    instance.logoSmall = new_logo_small

    serialized_data = serializers.LeagueSerializer(instance).data
    async_to_sync(sio.emit)("league:update",
                            serialized_data, namespace="/main")

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty


@receiver(signals.pre_delete, sender=models.League)
def league_pre_delete(instance, **kwargs):
    deleteLogoFiles(instance)


@receiver(signals.pre_save, sender=models.Season)
def season_pre_save(instance, **kwargs):
    if not instance.name:
        instance.name = f"Season {instance.seasonNo}"


@receiver(signals.post_save, sender=models.Season)
def season_post_save(instance, **kwargs):
    serialized_data = serializers.SeasonSerializer(instance).data
    async_to_sync(sio.emit)("season:update",
                            serialized_data, namespace="/main")


@receiver(signals.pre_save, sender=models.Playday)
def playday_pre_save(instance, **kwargs):
    if not instance.name:
        instance.name = f"Playday {instance.playdayNo}"


@receiver(signals.post_save, sender=models.Playday)
def playday_post_save(instance, **kwargs):
    serialized_data = serializers.PlaydaySerializer(instance).data
    async_to_sync(sio.emit)("playday:update",
                            serialized_data, namespace="/main")


@receiver(signals.post_save, sender=models.Tournament)
def tournament_post_save(instance, **kwargs):
    serialized_data = serializers.TournamentSerializer(instance).data
    async_to_sync(sio.emit)("tournament:update",
                            serialized_data, namespace="/main")


@receiver(signals.post_save, sender=models.Sponsor)
def sponsor_post_save(instance, created, **kwargs):
    serialized_data = serializers.SponsorSerializer(instance).data
    async_to_sync(sio.emit)("sponsor:update",
                            serialized_data, namespace="/main")


@receiver(signals.post_save, sender=models.Team)
def team_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    new_logo, new_logo_small = convert_square_logo(
        instance.logo, instance.logoSmall, "teams")
    instance.logo = new_logo
    instance.logoSmall = new_logo_small

    serialized_data = serializers.TeamSerializer(instance).data
    async_to_sync(sio.emit)("team:update",
                            serialized_data, namespace="/main")

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty


@receiver(signals.pre_delete, sender=models.Team)
def team_pre_delete(instance, **kwargs):
    deleteLogoFiles(instance)
