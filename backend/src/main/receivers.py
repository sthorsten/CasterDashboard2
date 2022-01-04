from django.db.models import signals
from django.dispatch.dispatcher import receiver
from util.image import convert_square_logo, deleteLogoFiles

from . import models

# pylint: disable=unused-argument


@receiver(signals.post_save, sender=models.League)
def league_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    new_logo, new_logo_small = convert_square_logo(
        instance.logo, instance.logoSmall, "leagues")
    instance.logo = new_logo
    instance.logoSmall = new_logo_small

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


@receiver(signals.pre_save, sender=models.Playday)
def playday_pre_save(instance, **kwargs):
    if not instance.name:
        instance.name = f"Playday {instance.playdayNo}"


# ToDo: Sponsor
@receiver(signals.post_save, sender=models.Sponsor)
def sponsor_post_save(instance, created, **kwargs):
    pass


@receiver(signals.post_save, sender=models.Team)
def team_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    new_logo, new_logo_small = convert_square_logo(
        instance.logo, instance.logoSmall, "teams")
    instance.logo = new_logo
    instance.logoSmall = new_logo_small

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty


@receiver(signals.pre_delete, sender=models.Team)
def team_pre_delete(instance, **kwargs):
    deleteLogoFiles(instance)
