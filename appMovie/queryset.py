from django.db.models import QuerySet, Sum, Count, FloatField


class MovieQuerySet(QuerySet):

    def get_by_year(self, year=None):
        if year:
            return self.filter(release_date=year)
        else:
            return self


class MovieRateQueryset(QuerySet):
    def get_best_rated(self):
        return self.values('movie').annotate(
            rate=Sum('rate') / Count('movie', output_field=FloatField())).order_by('-rate')

    def get_for_movie(self, movie):
        return self.filter(movie=movie)

    def get_rate_for_movie(self, movie):
        return self.get_for_movie(movie).get_best_rated()