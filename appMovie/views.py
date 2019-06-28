import time

import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from appMovie.api.filters import MovieFilterset, MovieFilterForView
from appMovie.api.serializers import MovieSerializer, MovieRateSerializer, MovieModelSerializer

from appMovie.forms import MovieForm, SimpleForm, MovieRateForm, TokenUserForm, DownloadForm
from appMovie.models import Movie, MovieRate, TokenUser
# from appMovie.tasks import download_movies
from appMovie.tasks import send_email, download_movies
from celery import signature, chord, group


def movieAdded(request):
    return render(request, 'success/successmovie.html')


def movieEdited(request):
    return render(request, 'success/successeditmovie.html')


def movieRated(request):
    return render(request, 'success/successmovierate.html')


def movieDownload(request):
    return render(request, 'success/moviedownloaded.html')


class SerializerExampleList(ListView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerializerExampleList, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'objects': JSONRenderer().render(MovieSerializer(self.get_queryset(), many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(context.get('objects'), **response_kwargs)


##########################################################
class SerializerExampleApiListView(ListAPIView):  ###list
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SerializerExampleApiDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):  ###detail
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    lookup_field = 'slug'


class SerializerExampleApiCreateListView(ListCreateAPIView):  ##crear y listar
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer


######################################################
class MovieRateListView(ListAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieRateDetailView(RetrieveAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class SerializerExampleDetail(DetailView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerializerExampleDetail, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'objects': JSONRenderer().render(MovieSerializer(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(context.get('objects'), **response_kwargs)


#################################################################

class LoginViewEdit(LoginView):
    form_class_token = TokenUserForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except Exception:
            return self.form_invalid(form)
        form_second = self.form_class_token()
        if form.is_valid():
            try:
                TokenUser.objects.get(user=user)
            except Exception:
                data = form_second.save(commit=False)
                Token.objects.get_or_create(user=user, defaults={'user': user})
                data.user = user
                data.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutViewEdit(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        TokenUser.objects.get(user=request.user.pk).delete()
        Token.objects.get(user=request.user.pk).delete()
        return super(LogoutViewEdit, self).dispatch(request, *args, **kwargs)


class ListMoviesView(ListView):
    template_name = 'listmovies.html'
    queryset = Movie.objects.all()
    paginate_by = 20


def search(request):
    movie_list = Movie.objects.all()
    movie_filter = MovieFilterForView(data=None, queryset=movie_list, request=request.GET, prefix=None)
    print(movie_filter.data.get('query'))
    return render(request, 'listmovie.html', {'filter': movie_filter})


class SearchMoviesView(ListView):
    template_name = 'listmovie.html'
    queryset = Movie.objects.all()

    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filterset_class = MovieFilterset

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('query') != None:
            return self.searchMovie(request)

    def get_queryset(self):
        qs = super(SearchMoviesView, self).get_queryset()
        return qs.order_by('-id')

    def searchMovie(self, request):
        busqueda = self.request.GET.get('query')
        busqueda = str(busqueda).lower()
        num = 0
        try:
            num = int(busqueda)
        except:
            pass
        try:
            if busqueda == None or busqueda == "":
                movie = None
                contex = {'movies': movie}
            elif Movie.objects.filter(title__icontains=busqueda):
                movie = Movie.objects.filter(title__icontains=busqueda)
                contex = {'movies': movie}
            return render(request, 'listmovie.html', contex)
        except Exception:
            contex = {'movies': 'no se encontraron coincidencias'}
            return render(request, 'listmovie.html', contex)


class HomeView(ListView):
    template_name = 'index.html'
    extra_context = {'title': 'My Internet movie database'}
    queryset = Movie.objects.all()
    paginate_by = 12

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        best_movie = MovieRate.objects.get_best_rated()[0]
        best_movie2 = MovieRate.objects.get_best_rated()[1]
        best_movie3 = MovieRate.objects.get_best_rated()[2]
        movie3 = Movie.objects.get(pk=best_movie3.get('movie'))
        movie2 = Movie.objects.get(pk=best_movie2.get('movie'))
        movie = Movie.objects.get(pk=best_movie.get('movie'))
        data.update({
            'best_rated_movie': movie,
            'best_rated_movie2': movie2,
            'best_rated_movie3': movie3,
            'best_rated_value': best_movie,
        })
        return data


class CreateMovie(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'CRUD/addmovie.html'
    form_class = MovieForm
    success_url = reverse_lazy('appMovie:movieadded')


class UpdateMovie(LoginRequiredMixin, UpdateView):
    model = Movie
    template_name = 'CRUD/editmovie.html'
    form_class = MovieForm
    success_url = reverse_lazy('appMovie:index')


class DeleteMovie(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'CRUD/deletemovie.html'
    success_url = reverse_lazy('appMovie:index')


class MovieDetailView(DetailView):
    queryset = Movie.objects.all()
    template_name = 'detail.movie.html'
    slug_field = 'slug'
    query_pk_and_slug = False

    def get_context_data(self, **kwargs):
        data = super(MovieDetailView, self).get_context_data(**kwargs)
        form = MovieRateForm()
        data.update({'form': form})
        return data


class MovieRateCreate(LoginRequiredMixin, CreateView):
    model = MovieRate
    form_class = MovieRateForm
    template_name = 'CRUD/addrate.html'
    success_url = reverse_lazy('appMovie:movierated')


class MovieFormExample(FormView):
    template_name = 'CRUD/addrate.html'
    form_class = SimpleForm
    success_url = reverse_lazy('appMovie:movierated')

    def form_invalid(self, form):
        print(form.errors)
        return super(MovieFormExample, self).form_invalid(form)


class DownloadMovieForm(FormView):
    template_name = 'CRUD/downloadform.html'
    form_class = DownloadForm
    success_url = reverse_lazy('appMovie:moviedownloaded')

    def form_valid(self, form):
        title = str(self.request.POST['title']).split(',')
        task_group = []
        for i in range(len(title)):
            if title[i][0] == ' ':
                title[i] = title[i][1:]
            task_group.append(download_movies.s(title[i]))

        chord(group(task_group), send_email.s()).delay()

        return super(DownloadMovieForm, self).form_valid(form)
