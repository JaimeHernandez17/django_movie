from rest_framework import serializers
from appMovie.models import Movie


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=True)
    release_date = serializers.DateField(required=True)
    detail = serializers.CharField(required=True)
    trailer_url = serializers.URLField(required=True)
    slug = serializers.CharField()
