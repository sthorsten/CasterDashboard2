from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_match_data_to_consumers(match_instance):
    from dashboard.models.models import MatchMap
    from overlays.models.models import MatchOverlayData
    from dashboard.models.serializers import MatchSerializer

    if match_instance is None:
        return

    channel_layer = get_channel_layer()
    match_data = MatchSerializer(match_instance).data

    map_picks = MatchMap.objects.filter(
        match=match_instance, type__in=[2, 3]).all()
    maps = []
    for pick in map_picks:
        if pick.type == 2:
            maps.append({'map': pick.map.id, 'type': pick.type,
                        'status': pick.status, 'team': pick.choose_team.id})
        else:
            maps.append({'map': pick.map.id, 'type': pick.type, 'status': pick.status})

    for user in match_instance.user.all():
        from overlays.models.serializers import MatchOverlayDataSerializer

        match_overlay_data = MatchOverlayData.objects.get(user=user)
        match_overlay_data_serialized = MatchOverlayDataSerializer(
            match_overlay_data)
        data = {'match': match_data, 'maps': maps,
                'match_overlay_data': match_overlay_data_serialized.data}

        async_to_sync(channel_layer.group_send)(
            str(user) + "_match_data",
            {
                "type": "send_message",
                "message": data,
            }
        )
