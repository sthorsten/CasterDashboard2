from django.urls import re_path

from websockets.consumers import EchoConsumer, OverlayStateConsumer, MatchDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/test/$', EchoConsumer),
    re_path(r'ws/overlays/state/$', OverlayStateConsumer),
    re_path(r'ws/overlays/match_data/$', MatchDataConsumer),
]