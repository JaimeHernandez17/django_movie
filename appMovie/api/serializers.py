from rest_framework import serializers
from appMovie.models import Movie, MovieRate


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=True)
    release_date = serializers.DateField(required=True)
    detail = serializers.CharField(required=True)
    trailer_url = serializers.URLField(required=True)
    slug = serializers.CharField()
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj):
        rates = MovieRate.objects.filter(movie__pk=obj.pk)
        if rates.exists():
            return rates.get_best_rated().first()['rate']

        return ''


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'duration', 'release_date', 'detail', 'trailer_url','poster')


class MovieRateSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='drf-movierate-detail')
    user = serializers.StringRelatedField()
    movie = serializers.HyperlinkedRelatedField(read_only=True, view_name='drf-movie-detail', lookup_field='slug')

    class Meta:
        model = MovieRate
        fields = ('movie', 'user', 'rate', 'id')
