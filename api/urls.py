from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from rest_framework_simplejwt.views import TokenRefreshView

from api import views
from api.tokens import CustomTokenObtainPairView
from api.views import UserViewSet, ProfileViewSet, NotificationViewSet, MapViewSet, \
    MapPoolViewSet, BombSpotViewSet, OperatorViewSet, LeagueViewSet, LeagueGroupViewSet, \
    SeasonViewSet, SponsorViewSet, TeamViewSet, MatchViewSet, MatchMapViewSet, \
    OperatorBansViewSet, RoundViewSet, MatchGroupViewSet, OverlayStyleViewSet, \
    OverlayStateViewSet, MatchOverlayDataViewSet, PollOverlayDataViewSet, \
    SocialOverlayDataViewSet, TimerOverlayDataViewSet, TickerOverlayDataViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'notification', NotificationViewSet)

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
router.register(r'match_groups', MatchGroupViewSet)

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

    # SimpleJWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Overlays
    path('overlay/state/by_user/<int:user_id>/',
         OverlayStateViewSet.as_view({'get': 'get_by_user', 'post': 'post_by_user'})),

    # Match Data
    # Additional URLs
    path('matches/<int:match_id>/maps/',
         MatchMapViewSet.as_view({'get': 'match_maps'})),
    path('matches/<int:match_id>/share/', views.share_match),

    path(r'version/', views.version),
    path(r'register/', views.register),
    path(r'register/confirm/', views.register_confirm),
    path(r'users/change-user-data/', views.change_user_data),
    path(r'users/change-password/', views.change_password)
]

urlpatterns += [
    path('api-token-auth/', rest_views.obtain_auth_token)
]
