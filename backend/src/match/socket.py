from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from sockets.sio_server import sio
from .models import Match
from .serializers import MatchSerializer


def _list_matches():
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return serializer.data


def _list_matches_paginated(page):
    matches = Match.objects.all()
    paginator = Paginator(matches, 20)
    data = paginator.page(page)
    serializer = MatchSerializer(data, many=True)
    return [paginator.count, paginator.num_pages, serializer.data]


def _get_match(match_id):
    if match_id:
        match_result = Match.objects.get(id=match_id)
    else:
        return None
    serializer = MatchSerializer(match_result)
    return serializer.data


def _create_match(data):
    serializer = MatchSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors


def _update_match(match_id, data):
    if match_id:
        match = Match.objects.get(id=match_id)
    else:
        return None
    serializer = MatchSerializer(match, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors


@sio.on("match:list", namespace="/match")
async def on_match_list(sid, data):
    paginated = data.get("paginated")
    page = data.get("page")
    if paginated and page:
        [total, pages, data] = await sync_to_async(_list_matches_paginated)(page)
        return {"total": total, "page": page, "totalPages": pages, "data": data}
    else:
        matches = await sync_to_async(_list_matches)()
        return matches


@sio.on("match:get", namespace="/match")
async def on_match_get(sid, data):
    match_id = data.get("id")
    match = await sync_to_async(_get_match)(match_id)
    return match


@sio.on("match:create", namespace="/match")
async def on_match_create(sid, data):
    match = await sync_to_async(_create_match)(data)
    return match


@sio.on("match:update", namespace="/match")
async def on_match_update(sid, data):
    match_id = data.get("id")
    match = await sync_to_async(_update_match)(match_id, data)
    return match
