from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/overlays/state/$', consumers.OverlayStateConsumer),
    re_path(r'ws/overlays/match_data/$', consumers.MatchDataConsumer),
]