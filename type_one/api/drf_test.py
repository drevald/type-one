# from django.contrib.auth.models import User
from pytest_drf.views import UsesListEndpoint
from type_one.core.models import User
from django.urls import reverse
from pytest_drf import APIViewTest, AsUser, Returns200, UsesGetMethod
from pytest_lambda import lambda_fixture
import pytest

tester = lambda_fixture(
    lambda: User.objects.create(
        username='test',
        password='test'
    ))

@pytest.mark.django_db
class TestListRecords(
    APIViewTest,
    UsesListEndpoint,
    Returns200,
    AsUser('tester'),
):

    url = lambda_fixture(lambda: reverse('api:records'))

    def test_it_returns_profile(self, json):
        # expected = {
        #     'username': 'alice',
        #     'first_name': 'Alice',
        #     'last_name': 'Innchains',
        #     'email': 'alice@ali.ce',
        # }
        # actual = json
        # assert expected == actual
        pass