import django_filters
from django_filters.rest_framework import FilterSet

from appMovie.models import Movie


class MovieFilterset(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')


class MovieFilterForView(django_filters.FilterSet):
    query = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title']
