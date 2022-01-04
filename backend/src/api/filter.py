from django_filters import BaseInFilter, NumberFilter, FilterSet

from dashboard.models.models import Season


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class SeasonFilter(FilterSet):
    league__in = NumberInFilter(field_name='league', lookup_expr='in')

    class Meta:
        model = Season
        fields = ['league', 'official_season', 'name']