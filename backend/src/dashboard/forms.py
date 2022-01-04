from django.forms import *

from dashboard.models.models import Match


class NewMatchForm(ModelForm):
    bestof_choices = [
        (1, "Best Of 1"),
        (2, "Best Of 2"),
        (3, "Best Of 3"),
        (5, "Best Of 5")
    ]

    bestof = ChoiceField(widget=RadioSelect, choices=bestof_choices)

    class Meta:
        model = Match
        fields = ['league', 'season', 'bestof', 'title', 'subtitle', 'team_blue', 'team_orange', 'sponsors']
