from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import path
from appMovie.views import MovieDetailView, HomeView, CreateMovie, UpdateMovie, DeleteMovie, movieAdded, movieDeleted, \
    movieEdited, movieRated, MovieRateCreate, SerializerExampleDetail, SerializerExampleApiList

app_name = 'appMovie'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout', logout_then_login, name='logout'),
    path('movies/<slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('addmovie/', CreateMovie.as_view(template_name='CRUD/addmovie.html'), name='addmovie'),
    path('addmovierate/', MovieRateCreate.as_view(), name='addmovierate'),
    path('editmovie/<slug>/', UpdateMovie.as_view(), name='editmovie'),
    path('deletemovie/<slug>/', DeleteMovie.as_view(template_name='CRUD/deletemovie.html'), name='deletemovie'),
    path('movieadded/', movieAdded, name="movieadded"),
    path('moviedeleted/', movieDeleted, name="moviedeleted"),
    path('movieedited/', movieEdited, name="movieedited"),
    path('movierated/', movieRated, name="movierated"),
    path('listapi/', SerializerExampleApiList.as_view(), name='listapi'),
    path('detailapi/<slug>/', SerializerExampleDetail.as_view(), name='detailapi'),

    # path('', views.login, name="login"),
    # path('', HomeView.as_view(), name='home'),

]
