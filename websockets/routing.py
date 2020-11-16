from django.urls import re_path

from websockets.consumers import EchoConsumer, OverlayStateConsumer, MatchDataConsumer
from websockets.new_consumers import MatchDataConsumer2, MatchMapConsumer2, RoundDataConsumer2, OverlayStateConsumer2

websocket_urlpatterns = [
    re_path(r'ws/match_data/(?P<user>\w+)/$', MatchDataConsumer2.as_asgi()),
    re_path(r'ws/match_map/(?P<user>\w+)/$', MatchMapConsumer2.as_asgi()),
    re_path(r'ws/round_data/(?P<match>\w+)/(?P<map>\w+)/$', RoundDataConsumer2.as_asgi()),
    re_path(r'ws/overlay_state/(?P<user>\w+)/$', OverlayStateConsumer2.as_asgi()),

    # Old
    re_path(r'ws/test/$', EchoConsumer),
    re_path(r'ws/overlays/state/$', OverlayStateConsumer),
    re_path(r'ws/overlays/match_data/$', MatchDataConsumer),
]
