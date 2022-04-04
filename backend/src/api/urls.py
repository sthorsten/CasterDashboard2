from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from api import views
from api.tokens import CustomTokenObtainPairView

# new
import core.views as coreViews
import main.views as mainViews
import match.views as matchViews
import overlays.views as overlayViews
import user.views as userViews


router = routers.DefaultRouter()
router.register(r'user/user', userViews.UserViewSet)
router.register(r'user/profile', userViews.ProfileViewSet)
router.register(r'user/leaguegroup', userViews.LeagueAccessGroupViewSet)

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
router.register(r'match/mapban', matchViews.MapBanViewSet)
router.register(r'match/matchmap', matchViews.MatchMapViewSet)
router.register(r'match/operatorban', matchViews.OperatorBansViewSet)
router.register(r'match/round', matchViews.RoundViewSet)

router.register(r'overlay/user', overlayViews.UserOverlayViewSet)
router.register(r'overlay/style', overlayViews.CustomDesignStyleViewSet)

urlpatterns = [
    # SimpleJWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/me/', userViews.LoggedInUserView.as_view(),
         name='loggedIn_user_view'),

    path(r'version/', views.version),
    # path(r'register/', views.register),
    # path(r'register/confirm/', views.register_confirm),
    # path(r'users/change-user-data/', views.change_user_data),
    # path(r'users/change-password/', views.change_password)
]

urlpatterns += router.urls
