import logging
from django.db.models import signals
from django.dispatch import receiver
from util import websocket

from . import models
from . import serializers

# pylint: disable=no-member


logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=models.Match)
def match_post_save(instance, created, **kwargs):
    serialized_data = serializers.MatchSerializer(instance).data
    websocket.send_server_data("match", "Match", serialized_data)


@receiver(signals.post_save, sender=models.MapBan)
def mapBan_post_save(instance, created, **kwargs):
    if created:
        # Update match status
        match = instance.match
        match.status = 'MAP_BAN'
        match.save()

        # Create match map if type 'pick'
        if instance.type == 'PICK':
            # Get existing match maps
            matchMaps = models.MatchMap.objects.filter(match=instance.match)

            matchMap = models.MatchMap(
                match=instance.match,
                map=instance.map,
                order=len(matchMaps) + 1
            )
            matchMap.save()

    # Send data via websocket
    serialized_data = serializers.MapBanSerializer(instance).data
    websocket.send_server_data("match", "MapBan", serialized_data)


@receiver(signals.post_save, sender=models.MatchMap)
def matchMap_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    if instance.atkTeam or instance.otAtkTeam:
        match = instance.match

        # Update def team
        if instance.atkTeam == match.teamBlue:
            instance.defTeam = match.teamOrange
        elif instance.atkTeam == match.teamOrange:
            instance.defTeam = match.teamBlue

        if instance.otAtkTeam == match.teamBlue:
            instance.otDefTeam = match.teamOrange
        elif instance.otAtkTeam == match.teamOrange:
            instance.otDefTeam = match.teamBlue

        # Update match status
        match.status = 'PLAYING'
        match.save()

        # Update own status
        if instance.status == 'CREATED':
            instance.status = 'PREPARING'

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty

    # Send data via websocket
    serialized_data = serializers.MatchMapSerializer(instance).data
    websocket.send_server_data("match", "MatchMap", serialized_data)


@receiver(signals.post_save, sender=models.OperatorBan)
def operatorBan_post_save(instance, created, **kwargs):
    # Set match map state
    matchMap = instance.matchMap
    if matchMap.status == 'PREPARING':
        matchMap.status = 'OPERATOR_BAN'
        matchMap.save()

    # Send data via websocket
    serialized_data = serializers.OperatorBanSerializer(instance).data
    websocket.send_server_data("match", "OperatorBan", serialized_data)


@receiver(signals.post_save, sender=models.Round)
def round_post_save(instance, created, **kwargs):
    matchMap = instance.matchMap
    match = instance.matchMap.match

    # Set match map state to playing
    if matchMap.status == 'OPERATOR_BAN':
        matchMap.status = 'PLAYING'
        matchMap.save()

    # Set match map score and possibly state to overtime
    if matchMap.status == 'PLAYING':
        # Set score
        if instance.winTeam == match.teamBlue:
            matchMap.scoreBlue = matchMap.scoreBlue + 1
        elif instance.winTeam == match.teamOrange:
            matchMap.scoreOrange = matchMap.scoreOrange + 1

        # Set status to overtime
        if (matchMap.scoreBlue + 1) >= 6 and (matchMap.scoreOrange + 1) >= 6:
            matchMap.status = 'OVERTIME'

        matchMap.save()

    # Send data via websocket
    serialized_data = serializers.RoundSerializer(instance).data
    websocket.send_server_data("match", "Round", serialized_data)


# @receiver(post_save, sender=models.Match)
# def match_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
#     # Set match status to finished?
#     if instance.state == 3:
#         if instance.best_of == 1:
#             if instance.score_blue == 1 or instance.score_orange == 1:
#                 logger.info("Setting match state to Finished.")

#                 instance.state = 4
#                 instance.save()
#                 return

#         elif instance.best_of == 2 or instance.best_of == 3:
#             if instance.score_blue == 2 or instance.score_orange == 2:
#                 logger.info("Setting match state to Finished.")

#                 instance.state = 4
#                 instance.save()
#                 return

#         elif instance.best_of == 5:
#             if instance.score_blue == 3 or instance.score_orange == 3:
#                 logger.info("Setting match state to Finished.")

#                 instance.state = 4
#                 instance.save()
#                 return


# @receiver(post_save, sender=models.MatchMap)
# def match_maps_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
#     # Set MatchMap state to Finished (3)
#     if instance.status == 2:
#         # Match finished

#         # Regular win: 7-X or X-7 with X < 6 // Overtime win: 8-X or X-8
#         if (instance.score_blue >= 7 and instance.score_orange < 6) \
#                 or (instance.score_orange >= 7 and instance.score_blue < 6) \
#                 or instance.score_blue >= 8 or instance.score_orange >= 8:

#             # Overtime win
#             if instance.score_blue == 8 or instance.score_orange == 8:
#                 logging.info(
#                     "Map Finished. Setting win type to 'Overtime Win'.")

#                 instance.win_type = 3
#             # Regular win
#             else:
#                 logging.info(
#                     "Map Finished. Setting win type to 'Regular Win'.")

#                 instance.win_type = 2

#             instance.status = 3
#             instance.save()

#             # Set match score equal to map score if BO1
#             if instance.match.best_of == 1:
#                 logging.info(
#                     "BO1 Match. Setting match win score to map score.")

#                 instance.match.score_blue = instance.score_blue
#                 instance.match.score_orange = instance.score_orange
#                 instance.match.save()

#             # Set match score
#             else:
#                 if instance.score_blue > instance.score_orange:
#                     instance.match.score_blue = instance.match.score_blue + 1
#                     instance.match.save()
#                 else:
#                     instance.match.score_orange = instance.match.score_orange + 1
#                     instance.match.save()

#         # Draw
#         elif instance.score_blue == 6 and instance.score_orange == 6:
#             logging.info("Map Finished. Setting win type to 'Draw'.")

#             instance.win_type = 4
#             instance.status = 3
#             instance.save()
#             return

#     # Set Match state to Map Ban (2)
#     if instance.match.state <= 1:
#         instance.match.state = 2
#         instance.match.save()

#     # Set Order
#     if instance.order == 0:
#         maps = models.MatchMap.objects.filter(match=instance.match).all()
#         instance.order = len(maps)
#         instance.save()

#     # Set Play Order
#     if instance.play_order == 0 and (instance.type == 2 or instance.type == 3):
#         maps = models.MatchMap.objects.filter(
#             match=instance.match, type__in=[2, 3]).all()
#         instance.play_order = len(maps)  # Not len(maps) + 1 because post_save
#         instance.save()


# @receiver(post_save, sender=models.OperatorBan)
# def operator_bans_post_save(sender, instance, **kwargs):  # pylint: disable=unused-argument
#     # Set Match state to Playing (3)
#     if instance.match.state <= 2:
#         logging.info(
#             "Started operator ban phase. Setting match state to 'Playing'.")

#         instance.match.state = 3
#         instance.match.save()

#     # Set MatchMap state to Playing (2)
#     match_map = models.MatchMap.objects.get(
#         match=instance.match, map=instance.map)
#     if match_map and match_map.status <= 1:
#         logging.info(
#             "Started operator ban phase. Setting match map state to 'Playing'.")

#         match_map.status = 2
#         match_map.save()
