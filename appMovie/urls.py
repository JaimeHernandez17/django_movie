from django.urls import path

from appMovie.views import MovieDetailView, HomeView, CreateMovie, UpdateMovie, DeleteMovie, movieAdded, \
    movieEdited, movieRated, MovieRateCreate, SerializerExampleDetail, \
    SerializerExampleApiCreateListView, SerializerExampleApiDetailUpdateDeleteView, LoginViewEdit, \
    LogoutViewEdit, SearchMoviesView, ListMoviesView, DownloadMovieForm, movieDownload

app_name = 'appMovie'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('accounts/login/', LoginViewEdit.as_view(template_name='registration/login.html'), name='login'),
    path('logout', LogoutViewEdit.as_view(), name='logout'),
    ###
    path('addmovie/', CreateMovie.as_view(template_name='CRUD/addmovie.html'), name='addmovie'),
    path('downloadmovie/', DownloadMovieForm.as_view(), name='download'),
    path('addmovierate/', MovieRateCreate.as_view(), name='addmovierate'),
    path('editmovie/<slug>/', UpdateMovie.as_view(), name='editmovie'),
    path('deletemovie/<slug>/', DeleteMovie.as_view(template_name='CRUD/deletemovie.html'), name='deletemovie'),
    ###
    path('movies/<slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('listmovies/', ListMoviesView.as_view(),
         name='listmovies'),
    path('searchmovies/', SearchMoviesView.as_view(), name='searchmovies'),
    path('detailapi/<slug>/', SerializerExampleDetail.as_view(), name='detailapi'),
    ###
    path('movie/', SerializerExampleApiCreateListView.as_view(), name='create-list-movie'),
    path('movie/<slug>', SerializerExampleApiDetailUpdateDeleteView.as_view(), name='detailt-update-delete-movie'),
    ###
    path('movieadded/', movieAdded, name="movieadded"),
    path('movieedited/', movieEdited, name="movieedited"),
    path('movierated/', movieRated, name="movierated"),
    path('moviedownloaded/', movieDownload, name="moviedownloaded"),
    ##
]
