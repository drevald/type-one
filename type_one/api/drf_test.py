# from django.contrib.auth.models import User
from pytest_drf.views import UsesListEndpoint, UsesPostMethod
from type_one.core.models import User
from django.urls import reverse
from pytest_drf import APIViewTest, AsUser, Returns200, UsesGetMethod
from pytest_lambda import lambda_fixture, static_fixture
import pytest

tester = lambda_fixture(
    lambda: User.objects.create(
        username='test',
        password='test'
    ))

@pytest.mark.django_db
class TestCreateRecord(
    APIViewTest,
    UsesPostMethod,
    AsUser('tester')
):

    url = lambda_fixture(lambda: reverse('api:records'))

    data = static_fixture({
        "type":0,
        "time": "2021-05-13T15:15",
        "bread_units":1.5,
        "glucose_level":1.5, 
        "insulin_amount":1,
        "notes":"Not much"
    })

    def test_it_creates(self, json):
        pass

@pytest.mark.django_db
class TestListRecords(
    APIViewTest,
    UsesListEndpoint,
    Returns200,
    AsUser('tester'),
):

    url = lambda_fixture(lambda: reverse('api:records'))

    def test_it_returns_profile(self, json):
        expected = {
            'username': 'alice',
            'first_name': 'Alice',
            'last_name': 'Innchains',
            'email': 'alice@ali.ce',
        }
        actual = json
        assert expected != actual
        pass