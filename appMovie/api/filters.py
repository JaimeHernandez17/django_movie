import django_filters
from django_filters.rest_framework import FilterSet


class MovieFilterset(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
