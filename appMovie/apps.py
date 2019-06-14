from django.apps import AppConfig


class AppmovieConfig(AppConfig):
    name = 'appMovie'
    verbose_name = 'Django Movie Database'

    def ready(self):
        import appMovie.signals
