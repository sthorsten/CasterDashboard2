from asgiref.sync import sync_to_async
from sockets.sio_server import sio
from .models import Map, MapPool, BombSpot, Operator
from .serializers import MapSerializer, MapPoolSerializer, BombSpotSerializer, OperatorSerializer


def _get_maps():
    maps = Map.objects.all()
    serializer = MapSerializer(maps, many=True)
    return serializer.data


def _get_map(map_id, map_name):
    if map_id:
        map_result = Map.objects.get(id=map_id)
    elif map_name:
        map_result = Map.objects.get(name=map_name)
    else:
        return None
    serializer = MapSerializer(map_result)
    return serializer.data


def _get_mappools():
    mappools = MapPool.objects.all()
    serializer = MapPoolSerializer(mappools, many=True)
    return serializer.data


def _get_bombspot_bymap(map_id, map_name):
    if map_id:
        bombspots = BombSpot.objects.filter(map_id=map_id)
    elif map_name:
        bombspots = BombSpot.objects.filter(map__name=map_name)
    else:
        return None
    serializer = BombSpotSerializer(bombspots, many=True)
    return serializer.data


def _get_opererators(side):
    if side == "ATK":
        operators = Operator.objects.filter(side="ATK")
    elif side == "DEF":
        operators = Operator.objects.filter(side="DEF")
    else:
        operators = Operator.objects.all()
    serializer = OperatorSerializer(operators, many=True)
    return serializer.data


@sio.on("map:list", namespace="/core")
async def on_map_list(sid, data):
    maps = await sync_to_async(_get_maps)()
    return maps


@sio.on("map:get", namespace="/core")
async def on_map_get(sid, data):
    map_id = data.get("id")
    map_name = data.get("name")
    map_result = await sync_to_async(_get_map)(map_id, map_name)
    return map_result


@sio.on("mappool:list", namespace="/core")
async def on_mappool_list(sid, data):
    mappools = await sync_to_async(_get_mappools)()
    return mappools


@sio.on("bombspot:list", namespace="/core")
async def on_bombspot_list(sid, data):
    map_id = data.get("map_id")
    map_name = data.get("map_name")
    bombspots = await sync_to_async(_get_bombspot_bymap)(map_id, map_name)
    return bombspots


@sio.on("operator:list", namespace="/core")
async def on_operator_list(sid, data):
    side = data.get("side")
    operators = await sync_to_async(_get_opererators)(side)
    return operators
