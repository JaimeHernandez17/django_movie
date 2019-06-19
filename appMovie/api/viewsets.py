from rest_framework import viewsets, mixins
from rest_framework.routers import SimpleRouter
from rest_framework.response import Response

from appMovie.api.serializers import MovieSerializer
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
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'
