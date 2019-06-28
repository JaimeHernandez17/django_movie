from io import StringIO

from django_movie.celery import app
from django.core.management import call_command
from .credentials import EMAILFROM, EMAIL_TO
from django.core.mail import send_mail
from celery import Task


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


@app.task()
def download_movies(moviename):
    result = call_command('download', '-s', moviename)
    movie_list = result.split(',')
    movie_list.pop(-1)
    return movie_list
    #send_email.delay(moviename)
