""" Main model receivers

This file contains all receivers to perform certain tasks before / after saving an instance / model.

"""

import os
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver

from caster_dashboard_2.helpers.image_handler import convert_league_logo, convert_team_logo, convert_sponsor_logo
from caster_dashboard_2.settings import base as django_settings

from dashboard.models.models import League, Sponsor, Team, Match, MatchMap, OperatorBans, Round
from websockets.helper import send_match_data_to_consumers

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=League)
def league_pre_save(sender, instance, **kwargs):
    instance.full_clean()


@receiver(post_save, sender=League)
def league_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.league_logo:
        if not instance.league_logo.name.__contains__(str(instance.id) + "_500.webp"):
            convert_league_logo(instance.id, instance.league_logo.path)
            os.remove(instance.league_logo.path)

            instance.league_logo = "leagues/%(id)s_500.webp" % ({'id': instance.id})
            instance.league_logo_small = "leagues/%(id)s_50.webp" % ({'id': instance.id})
            instance.save()

    else:
        no_logo_path = os.path.join(django_settings.MEDIA_ROOT, "teams", "_nologo.png")
        convert_league_logo(instance.id, no_logo_path)

        instance.league_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
        instance.league_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
        instance.save()


@receiver(pre_delete, sender=League)
def league_pre_delete(sender, instance, **kwargs):
    # Auto delete image
    if instance.league_logo:
        if os.path.isfile(instance.league_logo.path):
            os.remove(instance.league_logo.path)


@receiver(pre_save, sender=Sponsor)
def sponsor_pre_save(sender, instance, **kwargs):
    instance.full_clean()


@receiver(post_save, sender=Sponsor)
def sponsor_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.sponsor_logo:
        if not instance.sponsor_logo.name.__contains__(str(instance.id) + "_100.webp"):
            convert_sponsor_logo(instance.id, instance.sponsor_logo.path)
            os.remove(instance.sponsor_logo.path)

            instance.sponsor_logo = f'sponsors/{instance.id}_100.webp'
            instance.save()


@receiver(pre_delete, sender=Sponsor)
def sponsor_pre_delete(sender, instance, **kwargs):
    if instance.sponsor_logo:
        logo = instance.sponsor_logo.path
        # Auto delete image
        if logo:
            if os.path.exists(instance.sponsor_logo.path):
                os.remove(instance.sponsor_logo.path)


@receiver(pre_save, sender=Team)
def team_pre_save(sender, instance, **kwargs):
    instance.full_clean()


@receiver(post_save, sender=Team)
def team_post_save(sender, instance, **kwargs):
    # Rename file to id
    if instance.team_logo:
        if not instance.team_logo.name.__contains__(str(instance.id) + "_500.webp"):
            convert_team_logo(instance.id, instance.team_logo.path)
            os.remove(instance.team_logo.path)

            instance.team_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
            instance.team_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
            instance.save()

    else:
        no_logo_path = os.path.join(django_settings.BASE_DIR, "static", "img", "_nologo.png")
        convert_team_logo(instance.id, no_logo_path)

        instance.team_logo = "teams/%(id)s_500.webp" % ({'id': instance.id})
        instance.team_logo_small = "teams/%(id)s_50.webp" % ({'id': instance.id})
        instance.save()


@receiver(pre_delete, sender=Team)
def team_pre_delete(sender, instance, **kwargs):
    # Auto delete images
    try:
        team_logo = instance.team_logo.path
        os.remove(team_logo)
    except ValueError as e:
        logger.error("Failed to get team logo: " + str(e))
    except FileNotFoundError as e:
        logger.error("Failed to delete team logo: " + str(e))

    try:
        team_logo_small = instance.team_logo_small.path
        os.remove(team_logo_small)
    except ValueError as e:
        logger.error("Failed to get team logo: " + str(e))
    except FileNotFoundError as e:
        logger.error("Failed to delete team logo: " + str(e))


@receiver(post_save, sender=Match)
def match_post_save(sender, instance, **kwargs):
    send_match_data_to_consumers(instance)

    # Send match to websockets on change
    from dashboard.models.serializers import MatchSerializer
    serialized_data = MatchSerializer(instance)
    channel_layer = get_channel_layer()
    for user in instance.user.all():
        async_to_sync(channel_layer.group_send)(
            "match_data_" + user.username,
            {
                'type': 'send_to_client',
                'data': serialized_data.data
            }
        )


@receiver(post_save, sender=MatchMap)
def match_maps_post_save(sender, instance, **kwargs):
    # Set MatchMap state to Finished (3)
    if instance.status == 2:
        # Match finished

        # Regular win: 7-X or X-7 with X < 6 // Overtime win: 8-X or X-8
        if (instance.score_blue >= 7 and instance.score_orange < 6) \
                or (instance.score_orange >= 7 and instance.score_blue < 6) \
                or instance.score_blue >= 8 or instance.score_orange >= 8:

            # Overtime win
            if instance.score_blue == 8 or instance.score_orange == 8:
                instance.win_type = 3
            # Regular win
            else:
                instance.win_type = 2

            instance.status = 3
            instance.save()

            if instance.score_blue > instance.score_orange:
                instance.match.score_blue = instance.match.score_blue + 1
                instance.match.save()
            else:
                instance.match.score_orange = instance.match.score_orange + 1
                instance.match.save()

        # Draw
        elif instance.score_blue == 6 and instance.score_orange == 6:
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
        maps = MatchMap.objects.filter(match=instance.match, type__in=[2, 3]).all()
        instance.play_order = len(maps)  # Not len(maps) + 1 because post_save
        instance.save()

    # Send data to websockets on change
    from dashboard.models.serializers import MatchMapSerializer
    channel_layer = get_channel_layer()

    # MatchMapsAll
    matchMaps = MatchMap.objects.filter(match=instance.match)
    group_name = f"matches_{str(instance.match.id)}_maps"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchMapSerializer(matchMaps, many=True).data
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
def match_maps_post_delete(sender, instance, **kwargs):
    # Send data to websockets on change
    from dashboard.models.serializers import MatchMapSerializer
    channel_layer = get_channel_layer()

    # Get Match maps
    matchMaps = MatchMap.objects.filter(match=instance.match)

    # Set channels group name
    group_name = f"matches_{str(instance.match.id)}_maps"

    # Send match maps to client(s)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_to_client',
            'data': MatchMapSerializer(matchMaps, many=True).data
        }
    )


@receiver(post_save, sender=OperatorBans)
def operator_bans_post_save(sender, instance, **kwargs):
    # Set Match state to Playing (3)
    if instance.match.state <= 2:
        instance.match.state = 3
        instance.match.save()

    # Set MatchMap state to Playing (2)
    match_map = MatchMap.objects.get(match=instance.match, map=instance.map)
    if match_map and match_map.status <= 1:
        match_map.status = 2
        match_map.save()


@receiver(post_save, sender=Round)
def round_post_save(sender, instance, **kwargs):
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
def round_post_delete(sender, instance, **kwargs):
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
