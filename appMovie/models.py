from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=45, null=False)
    duration = models.TimeField(null=False)
    release_date = models.DateField(null=False)
    poster = models.ImageField(null=False)
    detail = models.TextField(max_length=150, null=False)
    trailer_url = models.URLField(null=False)
    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))), null=False)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.CASCADE)
    original_language = models.ForeignKey('Language', null=True, blank=True, on_delete=models.CASCADE)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.CASCADE)
    directors = models.ForeignKey('MovieDirector', null=True, blank=True, on_delete=models.CASCADE)
    actors = models.ForeignKey('MovieActor', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Language(models.Model):
    language = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.language


class Genre(models.Model):
    genre = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.genre


class Country(models.Model):
    country = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.country


class MovieRate(models.Model):
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150, null=False)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.movie.title)


class MovieActor(models.Model):
    name = models.CharField(max_length=45, null=False)
    age = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class MovieDirector(models.Model):
    name = models.CharField(max_length=45, null=False)
    age = models.IntegerField(null=False)

    def __str__(self):
        return self.name
