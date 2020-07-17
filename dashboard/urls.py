from django.urls import path

from dashboard.views import sites, forms

urlpatterns = [
    path('', sites.index, name='index'),

    path('home', sites.home, name='home'),

    # Matches
    path('matches/history', sites.match_history, name='history'),
    path('matches/create', sites.match_create, name='create'),

    # Overlays
    path('overlays/control-center', sites.overlay_control_center, name='control-center'),

    # Data
    path('data/leagues', sites.leagues, name='leagues'),
    path('data/seasons', sites.seasons, name='seasons'),
    path('data/teams', sites.teams, name='teams'),

    # Forms
    path('matches/create/new', forms.new_match_form),

]
