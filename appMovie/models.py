import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Manager
from django.urls import reverse

from appMovie.queryset import MovieQuerySet, MovieRateQueryset


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    release_date = models.DateField()
    poster = models.ImageField()
    # total_rate = models.FloatField()
    detail = models.TextField(max_length=300)
    trailer_url = models.URLField(default='', blank=True)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.SET_NULL)
    original_language = models.ForeignKey('Language', null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.SET_NULL)
    directors = models.ManyToManyField('MovieDirector')
    actors = models.ManyToManyField('MovieActor')
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('appMovie:movie-detail', args=(self.title,))


class Language(models.Model):
    language = models.CharField(max_length=45)

    def __str__(self):
        return self.language


class Genre(models.Model):
    genre = models.CharField(max_length=45)

    def __str__(self):
        return self.genre


class Country(models.Model):
    country = models.CharField(max_length=45)

    def __str__(self):
        return self.country


class MovieRate(models.Model):
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    rate = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(default='', max_length=300)

    objects = MovieRateQueryset.as_manager()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return "{} - {}".format(self.user.username, self.movie.title)


class MovieActor(models.Model):
    name = models.CharField(max_length=45)
    age = models.PositiveIntegerField(default=18)

    def __str__(self):
        return self.name


class MovieDirector(models.Model):
    name = models.CharField(max_length=45)
    age = models.PositiveIntegerField(default=18)

    def __str__(self):
        return self.name


class TokenUser(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.token


class Suggest(models.Model):
    names_movies = models.CharField(max_length=200)

    def __str__(self):
        return self.names_movies
