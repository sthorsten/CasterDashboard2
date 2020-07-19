from django.urls import path

from dashboard.views import sites, forms

urlpatterns = [
    path('', sites.index, name='index'),

    path('home', sites.home, name='home'),

    # Matches
    path('matches/history', sites.match_history, name='history'),
    path('matches/create', sites.match_create, name='create'),
    path('matches/<int:match_id>', sites.match_overview, name='match-overview'),
    path('matches/<int:match_id>/maps', sites.match_maps, name='match-maps'),

    # Overlays
    path('overlays/control-center', sites.overlay_control_center, name='control-center'),

    # Data
    path('data/leagues', sites.leagues, name='leagues'),
    path('data/seasons', sites.seasons, name='seasons'),
    path('data/teams', sites.teams, name='teams'),

    # Forms
    path('data/teams/new', forms.new_team_form),
    path('data/teams/edit', forms.edit_team_form),
    path('matches/create/new', forms.new_match_form),

]
