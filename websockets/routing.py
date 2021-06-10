from django.urls import re_path

from websockets.new_consumers import MatchConsumer, MatchMapAllConsumer, MatchMapSingleConsumer, \
    OpBansConsumer, RoundConsumer, MatchGroupConsumer, OverlayStateConsumer, OverlayDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/match/(?P<id>\w+)/$', MatchConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<id>\w+)/maps/$', MatchMapAllConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/$',
            MatchMapSingleConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/opbans/$',
            OpBansConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/map/(?P<map_id>\w+)/rounds/$',
            RoundConsumer.as_asgi()),

    re_path(r'ws/match_group/(?P<user_id>\w+)/$',
            MatchGroupConsumer.as_asgi()),

    re_path(r'ws/overlays/state/(?P<user_id>\w+)/$',
            OverlayStateConsumer.as_asgi()),
    re_path(r'ws/overlays/data/(?P<user_id>\w+)/$',
            OverlayDataConsumer.as_asgi()),
]
