import logging
import math
from django.db.models import signals
from django.dispatch import receiver
from util import websocket

from . import models
from . import serializers

# pylint: disable=no-member


logger = logging.getLogger(__name__)

# region post_save


@receiver(signals.post_save, sender=models.Match)
def match_post_save(instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    # Set win team & win type & status
    if instance.bestOf == 1:
        if instance.scoreBlue > instance.scoreOrange:
            instance.winTeam = instance.teamBlue
            instance.winType = 'BLUE_WIN'
            instance.status = 'CLOSED'
        elif instance.scoreOrange > instance.scoreBlue:
            instance.winTeam = instance.teamOrange
            instance.winType = 'ORANGE_WIN'
            instance.status = 'CLOSED'

    elif instance.bestOf == 2:
        if instance.scoreBlue >= 2 and instance.scoreOrange < 2:
            instance.winTeam = instance.teamBlue
            instance.winType = 'BLUE_WIN'
            instance.status = 'CLOSED'
        elif instance.scoreOrange >= 2 and instance.scoreBlue < 2:
            instance.winTeam = instance.teamOrange
            instance.winType = 'ORANGE_WIN'
            instance.status = 'CLOSED'
        elif instance.scoreBlue == 1 and instance.scoreOrange == 1:
            instance.winType = 'DRAW'
            instance.status = 'CLOSED'

    elif instance.bestOf >= 3:  # BO3 and BO5
        # 2:0 or 2:1 for BO3 and 3:0 3:1 3:2 for BO5
        if instance.scoreBlue > math.floor(instance.bestOf / 2) and instance.scoreBlue > instance.scoreOrange:
            instance.winTeam = instance.teamBlue
            instance.winType = 'BLUE_WIN'
            instance.status = 'CLOSED'
        elif instance.scoreOrange > math.floor(instance.bestOf / 2) and instance.scoreOrange > instance.scoreBlue:
            instance.winTeam = instance.teamOrange
            instance.winType = 'ORANGE_WIN'
            instance.status = 'CLOSED'

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty

    # Send data via websocket
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

    match = instance.match

    if instance.atkTeam or instance.otAtkTeam:

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

    # Map finished
    if instance.status == 'FINISHED':

        # Set match map score & win type & match score
        if instance.scoreBlue == instance.scoreOrange:
            instance.winType = 'DRAW'

        elif instance.scoreBlue > 7 or instance.scoreOrange > 7:
            if instance.scoreBlue > instance.scoreOrange:
                instance.winTeam = match.teamBlue
                instance.winType = 'BLUE_OT_WIN'
                match.scoreBlue = match.scoreBlue + 1
            else:
                instance.winTeam = match.teamOrange
                instance.winType = 'ORANGE_OT_WIN'
                match.scoreOrange = match.scoreOrange + 1

        else:
            if instance.scoreBlue > instance.scoreOrange:
                instance.winTeam = match.teamBlue
                instance.winType = 'BLUE_WIN'
                match.scoreBlue = match.scoreBlue + 1
            else:
                instance.winTeam = match.teamOrange
                instance.winType = 'ORANGE_WIN'
                match.scoreOrange = match.scoreOrange + 1

        match.save()

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
    if hasattr(instance, '_dirty'):
        return

    matchMap = instance.matchMap
    match = instance.matchMap.match

    # Set match map state to playing
    if matchMap.status == 'OPERATOR_BAN':
        matchMap.status = 'PLAYING'
        matchMap.save()

    # Set match map score and possibly state to overtime
    if matchMap.status == 'PLAYING' or matchMap.status == 'OVERTIME':
        # Set score
        if instance.winTeam == match.teamBlue:
            matchMap.scoreBlue = matchMap.scoreBlue + 1
        elif instance.winTeam == match.teamOrange:
            matchMap.scoreOrange = matchMap.scoreOrange + 1

        # Set status to overtime
        if matchMap.status == 'PLAYING' and (matchMap.scoreBlue + 1) >= 6 and (matchMap.scoreOrange + 1) >= 6:
            matchMap.status = 'OVERTIME'

        matchMap.save()

    # Set round no
    allRounds = models.Round.objects.filter(matchMap=instance.matchMap)
    # not len + 1 because we are in post_save here!
    instance.roundNo = len(allRounds)

    try:
        instance._dirty = True  # pylint: disable=protected-access
        instance.save()
    finally:
        del instance._dirty

    # Send data via websocket
    serialized_data = serializers.RoundSerializer(instance).data
    websocket.send_server_data("match", "Round", serialized_data)


# endregion

# region post_delete

@receiver(signals.post_delete, sender=models.MapBan)
def mapBan_post_delete(sender, instance, **kwargs):
    # Send all data via websocket
    mapBans = models.MapBan.objects.filter(match=instance.match)
    if mapBans.count() == 0:
        websocket.send_mulit_server_data("match", "MapBan", [])
        return
    serialized_data = serializers.MapBanSerializer(mapBans, many=True).data
    websocket.send_mulit_server_data("match", "MapBan", serialized_data)

# endregion
