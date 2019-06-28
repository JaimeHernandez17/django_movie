from io import StringIO

from appMovie.models import Suggest
from django_movie.celery import app
from django.core.management import call_command
from .credentials import EMAILFROM, EMAIL_TO
from django.core.mail import send_mail
from celery import Task, chord, group


@app.task()
def add(x, y):
    print(x + y)
    return x + y


@app.task()
def send_email(movie_list):
    message = f'The next movies has been added to the database:\n'
    for i in movie_list:
        message += f'* {i}\n'
    send_mail(
        'Movies added',
        message,
        EMAILFROM,
        [EMAIL_TO],
        fail_silently=False,
    )

@app.task
def send_email_error(message):
    send_mail(
        'Movies not added',
        message,
        EMAILFROM,
        [EMAIL_TO],
        fail_silently=False,
    )
    pass


@app.task
def save_titles(titles):
    Suggest.objects.update_or_create(names_movies=titles, defaults={'names_movies': titles})


@app.task
def search_in_db():
    movies = Suggest.objects.all()
    task_group = []
    if len(movies) > 1:
        for i in movies:
            task_group.append(download_movies.s(i.names_movies))
            i.delete()
        chord(group(task_group), send_email.s()).delay()
    else:
        send_email_error.s('Films were not added because they do not exist "Suggest"')()


@app.task()
def download_movies(moviename):
    result = call_command('download', '-s', moviename)
    movie_list = result.split(',')
    movie_list.pop(-1)
    return movie_list
