from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers, serializers, viewsets
from api.serializers import *

from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

router.register(r'bombspots', BombSpotViewSet)

router.register(r'data/leagues', LeagueViewSet)
router.register(r'data/seasons', SeasonViewSet)
router.register(r'data/sponsors', SponsorViewSet)
router.register(r'data/teams', TeamViewSet)

router.register(r'matches', MatchViewSet)
router.register(r'matchstate', MatchStateViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url('forms/teams/new', views.NewTeamForm.as_view()),

    # Overlays
    path('overlay/overlay_state/<int:user_id>/', views.overlay_state),
    path('overlay/overlay_style/<int:user_id>', views.overlay_style),
    path('overlay/timer_overlay_data/<int:user_id>/', views.timer_overlay_data),
    path('overlay/current_match/<int:user_id>/', views.set_current_match),
    path('overlay/next_match/<int:user_id>/', views.set_next_match),

    # Match Data
    path('matches/<int:match_id>/update_score', views.update_match_score),
    path('matches/map_ban/<int:match_id>/', views.map_ban),
    path('matches/map_settings/<int:match_id>/<int:map_id>/', views.map_settings),
    path('matches/swap_teams/<int:match_id>/', views.swap_teams),
    path('matches/operator_bans/<int:match_id>/<int:map_id>/', views.operator_bans),
    path('matches/rounds/<int:match_id>/<int:map_id>/', views.rounds),
    path('matches/finish_map/<int:match_id>/<int:map_id>/', views.finish_map),

]
