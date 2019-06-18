from datetime import datetime
import requests
from django.core.management.base import BaseCommand

from appMovie.models import Movie, Genre, MovieActor, MovieDirector, Country, Language, MovieRate


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)

    def handle(self, *args, **options):
        search = options['search']
        v = ''
        title = options['title']
        ids = []
        if search:
            v = 's'
        else:
            v = 't'
        response = requests.get('http://www.omdbapi.com/?' + v + '=' + title + '&plot=full&apikey=9f9a1efb')
        for i in response.json()['Search']:
            ids.append(i['imdbID'])

        movies = []

        for i in ids:
            response = requests.get('http://www.omdbapi.com/?i=' + i + '&plot=full&apikey=9f9a1efb')
            movies.append(response.json())

        for i in movies:
            poster = i['Poster']
            if poster == "N/A":
                poster = 'https://caiv.org/wp-content/plugins/smg-theme-tools/public/images/not-available-es.png'
                response2 = requests.get(poster)
                f = open('media/not-available-es.png', 'wb')
                f.write(response2.content)
                f.close()
            else:
                poster = i['Poster']
                response2 = requests.get(poster)
                f = open(f'media/{i["Title"]}.{str(poster).split(".")[-1]}', 'wb')
                f.write(response2.content)
                f.close()

            v_actors = str(i['Actors']).replace(', ', ',').split(',')
            for j in v_actors:
                MovieActor.objects.get_or_create(name=j)
            v_directors = str(i['Director']).replace(', ', ',').split(',')
            for k in v_directors:
                MovieDirector.objects.get_or_create(name=k)
            m_title = i['Title']
            duration = i['Runtime']
            if duration == "N/A":
                duration = 0
            else:
                duration = str(i['Runtime']).split(' ')[0]
            release_date = i['Released']
            if release_date == "N/A":
                release_date = '2000-05-12'
            else:
                release_date = datetime.strptime(i['Released'], '%d %b %Y')
            detail = i['Plot']
            if detail == "N/A":
                detail = ''
            else:
                detail = i['Plot']
            country = Country.objects.get_or_create(country=str(i['Country']).split(',')[0])
            genre = Genre.objects.get_or_create(genre=str(i['Genre']).split(',')[0])
            language = Language.objects.get_or_create(language=str(i['Language']).split(',')[0])
            if poster == "https://caiv.org/wp-content/plugins/smg-theme-tools/public/images/not-available-es.png":
                poster = 'not-available-es.png'
            else:
                poster = '{}.{}'.format(i['Title'], poster.split('.')[-1])
            print(poster)
            instance_movie, _ = Movie.objects.update_or_create(title=m_title, defaults={
                'title': m_title, 'duration': duration, 'release_date': release_date, 'detail': detail,
                'country': country[0],
                'genre': genre[0], 'original_language': language[0], 'poster': poster})
            for j in v_actors:
                instance_movie.actors.add(MovieActor.objects.get(name=j))
            for k in v_directors:
                instance_movie.directors.add(MovieDirector.objects.get(name=k))

        print(search)
        print(title)
