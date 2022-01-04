from django_filters import rest_framework as filters
from . import models


class BombSpotFilter(filters.FilterSet):
    map_name = filters.CharFilter(
        field_name='map__name', lookup_expr='icontains')

    class Meta:
        model = models.BombSpot
        fields = ['map', 'floor']
