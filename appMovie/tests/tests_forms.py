from django.contrib.auth.models import User
from django.test import TestCase

from appMovie.forms import SimpleForm
from appMovie.models import Movie


class SimpleFormTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test', email='test@test.com')
        self.movie = Movie.objects.create(title="test movie", duration=100, original_language="EN", country="USA")
        self.form = SimpleForm(user=self.user)

    def test_this_is_a_test(self):
        self.form.clean()