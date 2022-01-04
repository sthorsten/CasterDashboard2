from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from api import views
from api.tokens import CustomTokenObtainPairView
from api.views import UserViewSet

# new
import core.views as coreViews
import main.views as mainViews
import match.views as matchViews
import overlays.views as overlayViews
import user.views as userViews


router = routers.DefaultRouter()
router.register(r'user/user', UserViewSet)
router.register(r'user/profile', userViews.ProfileViewSet)
router.register(r'user/league_group', userViews.LeagueAccessGroupViewSet)

router.register(r'core/notification', coreViews.NotificationViewSet)
router.register(r'core/map', coreViews.MapViewSet)
router.register(r'core/mappool', coreViews.MapPoolViewSet)
router.register(r'core/bombspot', coreViews.BombSpotViewSet)
router.register(r'core/operator', coreViews.OperatorViewSet)

router.register(r'main/league', mainViews.LeagueViewSet)
router.register(r'main/season', mainViews.SeasonViewSet)
router.register(r'main/playday', mainViews.PlaydayViewSet)
router.register(r'main/tournament', mainViews.TournamentViewSet)
router.register(r'main/sponsor', mainViews.SponsorViewSet)
router.register(r'main/team', mainViews.TeamViewSet)

router.register(r'match/match', matchViews.MatchViewSet)
router.register(r'matches/maps', matchViews.MatchMapViewSet)
router.register(r'matches/opbans', matchViews.OperatorBansViewSet)
router.register(r'matches/round', matchViews.RoundViewSet)
router.register(r'match_groups', matchViews.MatchGroupViewSet)

router.register(r'overlay/style', overlayViews.OverlayStyleViewSet)
router.register(r'overlay/state', overlayViews.OverlayStateViewSet)
router.register(r'overlay/match_data', overlayViews.MatchOverlayDataViewSet)
router.register(r'overlay/poll_data', overlayViews.PollOverlayDataViewSet)
router.register(r'overlay/social_data', overlayViews.SocialOverlayDataViewSet)
router.register(r'overlay/timer_data', overlayViews.TimerOverlayDataViewSet)
router.register(r'overlay/ticker_data', overlayViews.TickerOverlayDataViewSet)

urlpatterns = [
    # SimpleJWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Overlays
    # path('overlay/state/by_user/<int:user_id>/',
    #     OverlayStateViewSet.as_view({'get': 'get_by_user', 'post': 'post_by_user'})),

    # Match Data
    # Additional URLs
    # path('matches/<int:match_id>/maps/',
    #     MatchMapViewSet.as_view({'get': 'match_maps'})),
    path('matches/<int:match_id>/share/', views.share_match),

    path(r'version/', views.version),
    path(r'register/', views.register),
    path(r'register/confirm/', views.register_confirm),
    path(r'users/change-user-data/', views.change_user_data),
    path(r'users/change-password/', views.change_password)
]

urlpatterns += router.urls
