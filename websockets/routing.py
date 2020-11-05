from django.urls import re_path

from websockets.consumers import EchoConsumer, OverlayStateConsumer, MatchDataConsumer
from websockets.new_consumers import MatchDataConsumer2

websocket_urlpatterns = [
    re_path(r'ws/match_data/(?P<user>\w+)/$', MatchDataConsumer2),
    re_path(r'ws/test/$', EchoConsumer),
    re_path(r'ws/overlays/state/$', OverlayStateConsumer),
    re_path(r'ws/overlays/match_data/$', MatchDataConsumer),
]