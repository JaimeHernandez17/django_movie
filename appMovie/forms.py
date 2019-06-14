from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import datetime

from appMovie.models import MovieRate
from .models import Movie, Genre, Language, Country, MovieDirector, MovieActor


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = [
            'title',
            'duration',
            'release_date',
            'poster',
            'detail',
            'trailer_url',
            'genre',
            'original_language',
            'country',
            'directors',
            'actors',
        ]

        labels = {

            'title': 'Title',
            'duration': 'Duration',
            'release_date': 'Release_date',
            'poster': 'Poster',
            'detail': 'Detail',
            'trailer_url': 'Trailer_url',
            'genre': 'Genre',
            'original_language': 'Original_language',
            'country': 'Country',
            'directors': 'Directors',
            'actors': 'Actors',
        }

        widgets = {
            'release_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.Select(attrs={'class': 'form-control', 'type': 'date'}),
            'genre': forms.Select(attrs={'class': 'form-control', 'type': 'date'}),
            'original_language': forms.Select(attrs={'class': 'form-control', 'type': 'date'}),
            'directors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class MovieRateForm(forms.ModelForm):

    class Meta:
        model = MovieRate

        fields = {
            'rate', 'movie'
        }

        labels = {
            'rate': 'Rate',
            'movie': 'Movie',
        }



class SimpleForm(forms.ModelForm):
    class Meta:
        model = MovieRate
        fields = ('rate', 'movie')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SimpleForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(SimpleForm, self).clean()
        movie = data.get('movie')
        if MovieRate.objects.filter(user=self.user, movie=movie).exists():
            raise ValidationError(f'Movie rate with user {self.user.username} and movie {movie.title} already exists')
        return data

    def save(self, commit=True):
        instance = super(SimpleForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance
