from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_match_data_to_consumers(match_instance):
    from dashboard.models import MapBan
    from overlays.models import MatchOverlayData

    channel_layer = get_channel_layer()
    match_data = match_instance.serialize()

    map_picks = MapBan.objects.filter(match=match_instance, type__in=[2, 3]).all()
    maps = []
    for m in map_picks:
        if m.type == 2:
            maps.append({'map': m.map.id, 'type': m.type, 'status': m.status, 'team': m.team.id})
        else:
            maps.append({'map': m.map.id, 'type': m.type, 'status': m.status})

    for user in match_instance.user.all():
        match_overlay_data = MatchOverlayData.objects.get(user=user).serialize()
        data = {'match': match_data, 'maps': maps, 'match_overlay_data': match_overlay_data}

        async_to_sync(channel_layer.group_send)(
            str(user) + "_match_data",
            {
                "type": "send_message",
                "message": data,
            }
        )
