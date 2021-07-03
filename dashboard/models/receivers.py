""" Main model receivers

This file contains all receivers to perform certain tasks before / after saving an instance / model.

"""

import os
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete, m2m_changed
from django.dispatch import receiver

from caster_dashboard_2.helpers.image_handler import convert_league_logo, convert_team_logo, \
    convert_sponsor_logo
from caster_dashboard_2 import settings as django_settings

from dashboard.models.models import League, Sponsor, Team, Match, MatchMap, OperatorBans, Round, \
    MatchGroup
from websockets.helper import send_match_data_to_consumers

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=League)
def league_pre_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    instance.full_clean()


@receiver(post_save, sender=League)
def league_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Rename file to id
    if instance.league_logo:
        if instance.league_logo.name.__contains__("_temp.png"):

            logger.info(
                f"Converting league logo for league '{str(instance)}': {instance.league_logo.name}...")

            convert_league_logo(instance.id, instance.league_logo.path)
            os.remove(instance.league_logo.path)

            instance.league_logo = f"leagues/{instance.id}_500.webp"
            instance.league_logo_small = f"leagues/{instance.id}_50.webp"
            instance.save()

            logger.info("League Logo saved successfully.")

    else:
        no_logo_path = os.path.join(
            django_settings.STATIC_ROOT, "img", "_nologo.png")

        logger.info(
            f"Setting default template logo for league '{str(instance)}'...")
        convert_league_logo(instance.id, no_logo_path)
        instance.league_logo = f"leagues/{instance.id}_500.webp"
        instance.league_logo_small = f"leagues/{instance.id}_50.webp"
        instance.save()

        logger.info("League Logo saved successfully.")


@receiver(pre_delete, sender=League)
def league_pre_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Auto delete image
    if instance.league_logo:
        if os.path.isfile(instance.league_logo.path):
            logger.info(
                f"Deleting league logo for league '{str(instance)}'...")
            os.remove(instance.league_logo.path)
            logger.info("League logo deleted successfully.")

    if instance.league_logo_small:
        if os.path.isfile(instance.league_logo_small.path):
            logger.info(
                f"Deleting league logo small for league '{str(instance)}'...")
            os.remove(instance.league_logo_small.path)
            logger.info("League logo small deleted successfully.")


@receiver(pre_save, sender=Sponsor)
def sponsor_pre_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    instance.full_clean()


@receiver(post_save, sender=Sponsor)
def sponsor_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Rename file to id
    if instance.sponsor_logo:
        if instance.sponsor_logo.name.__contains__("_temp.png"):
            logger.info(
                f"Converting sponsor logo for sponsor '{str(instance)}': {instance.sponsor_logo.name}...")

            convert_sponsor_logo(instance.id, instance.sponsor_logo.path)
            os.remove(instance.sponsor_logo.path)

            instance.sponsor_logo = f'sponsors/{instance.id}_100.webp'
            instance.save()

            logger.info("Sponsor logo saved successfully.")


@receiver(pre_delete, sender=Sponsor)
def sponsor_pre_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Auto delete image
    if instance.sponsor_logo:
        if instance.sponsor_logo.path:
            if os.path.exists(instance.sponsor_logo.path):
                logger.info(
                    f"Deleting sponsor logo for sponsor '{str(instance)}'...")
                os.remove(instance.sponsor_logo.path)
                logger.info("Sponsor logo deleted successfully.")


@receiver(pre_save, sender=Team)
def team_pre_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    instance.full_clean()


@receiver(post_save, sender=Team)
def team_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Rename file to id
    if instance.team_logo:
        if instance.team_logo.name.__contains__("_temp.png"):
            logger.info(
                f"Converting team logo for team '{str(instance)}': {instance.team_logo.name}...")

            convert_team_logo(instance.id, instance.team_logo.path)
            os.remove(instance.team_logo.path)

            instance.team_logo = f"teams/{instance.id}_500.webp"
            instance.team_logo_small = f"teams/{instance.id}_50.webp"
            instance.save()

            logger.info("Team logo saved successfully.")

    else:
        no_logo_path = os.path.join(
            django_settings.STATIC_ROOT, "img", "_nologo.png")

        logger.info(
            f"Setting default template logo for team '{str(instance)}'...")

        convert_team_logo(instance.id, no_logo_path)

        instance.team_logo = f"teams/{instance.id}_500.webp"
        instance.team_logo_small = f"teams/{instance.id}_50.webp"
        instance.save()

        logger.info("Team logo saved successfully.")


@receiver(pre_delete, sender=Team)
def team_pre_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Auto delete image
    if instance.team_logo:
        if os.path.isfile(instance.team_logo.path):
            logger.info(f"Deleting team logo for team '{str(instance)}'...")
            os.remove(instance.team_logo.path)
            logger.info("Team logo deleted successfully.")

    if instance.team_logo_small:
        if os.path.isfile(instance.team_logo_small.path):
            logger.info(
                f"Deleting team logo small for team '{str(instance)}'...")
            os.remove(instance.team_logo_small.path)
            logger.info("Team logo small deleted successfully.")


@receiver(post_save, sender=Match)
def match_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Set match status to finished?
    if instance.state == 3:
        if instance.best_of == 1:
            if instance.score_blue == 1 or instance.score_orange == 1:
                logger.info("Setting match state to Finished.")

                instance.state = 4
                instance.save()
                return

        elif instance.best_of == 2 or instance.best_of == 3:
            if instance.score_blue == 2 or instance.score_orange == 2:
                logger.info("Setting match state to Finished.")

                instance.state = 4
                instance.save()
                return

        elif instance.best_of == 5:
            if instance.score_blue == 3 or instance.score_orange == 3:
                logger.info("Setting match state to Finished.")

                instance.state = 4
                instance.save()
                return

    send_match_data_to_consumers(instance)

    # Send match data to websockets on change
    from dashboard.models.serializers import MatchSerializer
    channel_layer = get_channel_layer()
    group_name = f"match_{str(instance.id)}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchSerializer(instance).data
        }
    )


@receiver(post_save, sender=MatchMap)
def match_maps_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Set MatchMap state to Finished (3)
    if instance.status == 2:
        # Match finished

        # Regular win: 7-X or X-7 with X < 6 // Overtime win: 8-X or X-8
        if (instance.score_blue >= 7 and instance.score_orange < 6) \
                or (instance.score_orange >= 7 and instance.score_blue < 6) \
                or instance.score_blue >= 8 or instance.score_orange >= 8:

            # Overtime win
            if instance.score_blue == 8 or instance.score_orange == 8:
                logging.info(
                    "Map Finished. Setting win type to 'Overtime Win'.")

                instance.win_type = 3
            # Regular win
            else:
                logging.info(
                    "Map Finished. Setting win type to 'Regular Win'.")

                instance.win_type = 2

            instance.status = 3
            instance.save()

            # Set match score equal to map score if BO1
            if instance.match.best_of == 1:
                logging.info(
                    "BO1 Match. Setting match win score to map score.")

                instance.match.score_blue = instance.score_blue
                instance.match.score_orange = instance.score_orange
                instance.match.save()

            # Set match score
            else:
                if instance.score_blue > instance.score_orange:
                    instance.match.score_blue = instance.match.score_blue + 1
                    instance.match.save()
                else:
                    instance.match.score_orange = instance.match.score_orange + 1
                    instance.match.save()

        # Draw
        elif instance.score_blue == 6 and instance.score_orange == 6:
            logging.info("Map Finished. Setting win type to 'Draw'.")

            instance.win_type = 4
            instance.status = 3
            instance.save()
            return

    # Set Match state to Map Ban (2)
    if instance.match.state <= 1:
        instance.match.state = 2
        instance.match.save()

    # Set Order
    if instance.order == 0:
        maps = MatchMap.objects.filter(match=instance.match).all()
        instance.order = len(maps)
        instance.save()

    # Set Play Order
    if instance.play_order == 0 and (instance.type == 2 or instance.type == 3):
        maps = MatchMap.objects.filter(
            match=instance.match, type__in=[2, 3]).all()
        instance.play_order = len(maps)  # Not len(maps) + 1 because post_save
        instance.save()

    # Send data to websockets on change
    from dashboard.models.serializers import MatchMapSerializer
    channel_layer = get_channel_layer()

    # MatchMapsAll
    match_maps = MatchMap.objects.filter(
        match=instance.match).order_by('order')
    group_name = f"matches_{str(instance.match.id)}_maps"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchMapSerializer(match_maps, many=True).data
        }
    )

    # MatchMapSingle
    group_name = f"matches_{str(instance.match.id)}_map_{str(instance.map.id)}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchMapSerializer(instance).data
        }
    )


@receiver(post_delete, sender=MatchMap)
def match_maps_post_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Send data to websockets on change
    from dashboard.models.serializers import MatchMapSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    match_maps = MatchMap.objects.filter(
        match=instance.match).order_by('order')

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_maps"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchMapSerializer(match_maps, many=True).data
        }
    )


@receiver(post_save, sender=OperatorBans)
def operator_bans_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Set Match state to Playing (3)
    if instance.match.state <= 2:
        logging.info(
            "Started operator ban phase. Setting match state to 'Playing'.")

        instance.match.state = 3
        instance.match.save()

    # Set MatchMap state to Playing (2)
    match_map = MatchMap.objects.get(match=instance.match, map=instance.map)
    if match_map and match_map.status <= 1:
        logging.info(
            "Started operator ban phase. Setting match map state to 'Playing'.")

        match_map.status = 2
        match_map.save()

    # Send data to websockets on change
    from dashboard.models.serializers import OperatorBanSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    opbans = OperatorBans.objects.filter(
        match=instance.match, map=instance.map)

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_map_{str(instance.map.id)}_opbans"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': OperatorBanSerializer(opbans, many=True).data
        }
    )


@receiver(post_delete, sender=OperatorBans)
def operator_bans_post_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Send data to websockets on change
    from dashboard.models.serializers import OperatorBanSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    opbans = OperatorBans.objects.filter(
        match=instance.match, map=instance.map)

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_map_{str(instance.map.id)}_opbans"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': OperatorBanSerializer(opbans, many=True).data
        }
    )


@receiver(post_save, sender=Round)
def round_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Send data to websockets on change
    from dashboard.models.serializers import RoundSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    rounds = Round.objects.filter(match=instance.match, map=instance.map)

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_map_{str(instance.map.id)}_rounds"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': RoundSerializer(rounds, many=True).data
        }
    )


@receiver(post_delete, sender=Round)
def round_post_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    # Send data to websockets on change
    from dashboard.models.serializers import RoundSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    rounds = Round.objects.filter(match=instance.match, map=instance.map)

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_map_{str(instance.map.id)}_rounds"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': RoundSerializer(rounds, many=True).data
        }
    )


@receiver(m2m_changed, sender=MatchGroup.matches.through)
def match_group_post_save(sender, instance, action, **kwargs):  # pylint: disable=unused-argument
    if action != "post_remove" and action != "post_add":
        return

    # Send data to websockets on change
    from dashboard.models.serializers import MatchGroupSerializer
    channel_layer = get_channel_layer()

    data = MatchGroupSerializer(instance).data

    # Send match maps to client(s)
    for user in instance.users.all():
        async_to_sync(channel_layer.group_send)(
            f"match_group_{str(user.id)}",
            {
                'type': 'send_to_client',
                'data': data
            }
        )
