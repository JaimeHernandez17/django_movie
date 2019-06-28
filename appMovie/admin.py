from django.contrib import admin

from .models import *

admin.site.register(Movie)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(MovieRate)
admin.site.register(MovieActor)
admin.site.register(MovieDirector)
admin.site.register(TokenUser)
admin.site.register(Suggest)

