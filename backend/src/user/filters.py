from django_filters import rest_framework as filters
from . import models


class ProfileFilter(filters.FilterSet):
    user_name = filters.CharFilter(
        field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = models.Profile
        fields = ['user', 'accountConfirmed']
