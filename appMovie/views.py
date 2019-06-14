from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework_xml.renderers import XMLRenderer

from appMovie.api.serializers import MovieSerializer

from appMovie.forms import MovieForm, SimpleForm, MovieRateForm
from appMovie.models import Movie, MovieRate


def movieAdded(request):
    return render(request, 'success/successmovie.html')


def movieDeleted(request):
    return render(request, 'success/successdeletemovie.html')


def movieEdited(request):
    return render(request, 'success/successeditmovie.html')


def movieRated(request):
    return render(request, 'success/successmovierate.html')


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


class SerializerExampleApiList(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


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


class HomeView(ListView):
    template_name = 'index.html'
    extra_context = {'title': 'My Internet movie database'}
    queryset = Movie.objects.all()
    paginate_by = 4

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

    def searchMovie(self, request):
        busqueda = self.request.GET.get('q')
        num = 0
        try:
            num = int(busqueda)
        except:
            pass
        if busqueda == None or busqueda == "":
            movie = Movie.objects.all()
            contex = {'movies': movie}
        elif Movie.objects.filter(title__icontains=busqueda):
            movie = Movie.objects.filter(title__icontains=busqueda)
            contex = {'movies': movie, }
        elif Movie.objects.filter(genre__icontains=busqueda):
            movie = Movie.objects.filter(genre__icontains=busqueda)
            contex = {'movies': movie}
        elif Movie.objects.filter(actors__name__icontains=busqueda):
            movie = Movie.objects.filter(actors__name__icontains=busqueda)
            contex = {'movies': movie}
        elif Movie.objects.filter(directors__name__icontains=busqueda):
            movie = Movie.objects.filter(directors__name__icontains=busqueda)
            contex = {'movies': movie}
        elif Movie.objects.filter(year=num):
            movie = Movie.objects.filter(year=num)
            contex = {'movies': movie}
        else:
            contex = {'movies': 'no se encontraron conicidencias'}
        return render(request, 'movies.html', contex)


class CreateMovie(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'CRUD/addmovie.html'
    form_class = MovieForm
    success_url = reverse_lazy('appMovie:movieadded')


class UpdateMovie(LoginRequiredMixin, UpdateView):
    model = Movie
    template_name = 'CRUD/editmovie.html'
    form_class = MovieForm
    success_url = reverse_lazy('appMovie:movieedited')


class DeleteMovie(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'CRUD/deletemovie.html'
    success_url = reverse_lazy('appMovie:moviedeleted')


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


class MovieRateCreate(CreateView):
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
