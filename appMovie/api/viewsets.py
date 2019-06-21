import django_filters
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAuthenticatedOrReadOnly
from rest_framework.routers import SimpleRouter
from rest_framework.response import Response

from appMovie.api.filters import MovieFilterset
from appMovie.api.permissions import IsAuthenticatedOrReadOnlyCustom
from appMovie.api.serializers import MovieSerializer, MovieRateSerializer
from appMovie.models import MovieRate, Movie


class ExampleViewset(viewsets.ViewSet):

    def get_query_set(self):
        _filter = {}
        if 't' in self.request.query_params.keys():
            _filter.update(({'movie__title__icontains': self.request.query_params.get('t')}))
        return MovieRate.objects.filter(**_filter)

    def list(self, request):
        qs = self.get_query_set()
        return Response({'action': 'list'})

    def retrieve(self, request, slug=None):
        return Response({'action': 'retrieve'})

    def create(self, request):
        return Response({'action': 'create'})

    def update(self, request, slug=None):
        return Response({'action': 'update'})

    def destroy(self, request, slug=None):
        return Response({'action': 'destroy'})


class ExampleModelViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = MovieFilterset
    queryset = Movie.objects.all()
    serializer_classes = {
        'rate': MovieRateSerializer,
        'default': MovieSerializer
    }
    lookup_field = 'slug'

    def get_serializer_class(self):
        return self.serializer_classes[self.action] if self.action in self.serializer_classes.keys() else \
            self.serializer_classes['default']

    def get_serializer_context(self):
        context = super(ExampleModelViewset, self).get_serializer_context()
        context.update({'request': self.request})
        return context
