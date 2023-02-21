# from django.contrib.auth.models import User
from pytest_drf.views import UsesListEndpoint, UsesPostMethod
from type_one.core.models import User
from django.urls import reverse
from pytest_drf import APIViewTest, AsUser, Returns200, UsesGetMethod
from pytest_lambda import lambda_fixture, static_fixture
import pytest

tester = lambda_fixture(
    lambda: User.objects.create(
        username='someone',
        password='someone'
    ))

@pytest.mark.django_db
class TestCreateRecord(APIViewTest, UsesPostMethod, AsUser('tester')):
    url = lambda_fixture(lambda: reverse('api:records'))
    def test_something(self, json):
        pass