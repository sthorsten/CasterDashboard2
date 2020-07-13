from django.urls import path

from dashboard.views import sites

urlpatterns = [
    path('', sites.index, name='index'),

    path('home', sites.home, name='home'),

    path('overlays/control-center', sites.overlay_control_center, name='control-center'),

    # Data
    path('data/leagues', sites.leagues, name='leagues'),
    path('data/seasons', sites.seasons, name='seasons'),
    path('data/teams', sites.teams, name='teams'),

]
