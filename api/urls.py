from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as rest_views

from api import views
from api.views import *

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'profile', ProfileViewSet)

router.register(r'core/map', MapViewSet)
router.register(r'core/map_pool', MapPoolViewSet)
router.register(r'core/bomb_spot', BombSpotViewSet)
router.register(r'core/operator', OperatorViewSet)

router.register(r'data/league', LeagueViewSet)
router.register(r'data/league_group', LeagueGroupViewSet)
router.register(r'data/season', SeasonViewSet)
router.register(r'data/sponsor', SponsorViewSet)
router.register(r'data/team', TeamViewSet)

router.register(r'match', MatchViewSet)
router.register(r'matches/maps', MatchMapViewSet)
router.register(r'matches/opbans', OperatorBansViewSet)
router.register(r'matches/round', RoundViewSet)

router.register(r'overlay/style', OverlayStyleViewSet)
router.register(r'overlay/state', OverlayStateViewSet)
router.register(r'overlay/match_data', MatchOverlayDataViewSet)
router.register(r'overlay/poll_data', PollOverlayDataViewSet)
router.register(r'overlay/social_data', SocialOverlayDataViewSet)
router.register(r'overlay/timer_data', TimerOverlayDataViewSet)
router.register(r'overlay/ticker_data', TickerOverlayDataViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Overlays
    path('overlay/state/by_user/<int:user_id>/',
         OverlayStateViewSet.as_view({'get': 'get_by_user', 'post': 'post_by_user'})),
    # path('overlay/current_match/<int:user_id>/', views.set_current_match),

    # Match Data
    # Additional URLs
    path('matches/<int:match_id>/maps/', MatchMapViewSet.as_view({'get': 'match_maps'})),
    path('matches/<int:match_id>/share/', views.share_match),

    # Old
    # TODO: Refactor!
    # path('matches/<int:match_id>/update_score', views.update_match_score),
    # path('matches/map_ban/<int:match_id>/', views.map_ban),
    # path('matches/map_settings/<int:match_id>/<int:map_id>/', views.map_settings),
    # path('matches/swap_teams/<int:match_id>/', views.swap_teams),
    # path('matches/operator_bans/<int:match_id>/<int:map_id>/', views.operator_bans),
    # path('matches/rounds/<int:match_id>/<int:map_id>/', views.rounds),
    # path('matches/finish_map/<int:match_id>/<int:map_id>/', views.finish_map),

]

urlpatterns += [
    path('api-token-auth/', rest_views.obtain_auth_token)
]

