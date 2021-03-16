from django.urls import re_path

from websockets.consumers import EchoConsumer, MatchDataConsumer
from websockets.new_consumers import *

websocket_urlpatterns = [
    re_path(r'ws/match/(?P<id>\w+)/$', MatchConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<id>\w+)/maps/$', MatchMapAllConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/$', MatchMapSingleConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/opbans/$', OpBansConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/rounds/$', RoundConsumer.as_asgi()),

    re_path(r'ws/match_group/(?P<user_id>\w+)/$', MatchGroupConsumer.as_asgi()),

    re_path(r'ws/overlays/state/(?P<user_id>\w+)/$', OverlayStateConsumer.as_asgi()),
    re_path(r'ws/overlays/data/(?P<user_id>\w+)/$', OverlayDataConsumer.as_asgi()),

    # Old

    re_path(r'ws/match_data/(?P<user>\w+)/$', MatchDataConsumer2.as_asgi()),
    re_path(r'ws/map_data/(?P<user>\w+)/$', MapDataConsumer2.as_asgi()),
    re_path(r'ws/match_map/(?P<user>\w+)/$', MatchMapConsumer2.as_asgi()),
    re_path(r'ws/match_map/id/(?P<match_map_id>\w+)/$', MatchMapConsumer3.as_asgi()),
    re_path(r'ws/round_data/(?P<match>\w+)/(?P<map>\w+)/$', RoundConsumer.as_asgi()),
    #re_path(r'ws/overlay_state/(?P<user>\w+)/$', OverlayStateConsumer2.as_asgi()),

    # Old
    re_path(r'ws/test/$', EchoConsumer),
    re_path(r'ws/overlays/state/$', OverlayStateConsumer),
    re_path(r'ws/overlays/match_data/$', MatchDataConsumer),
]
