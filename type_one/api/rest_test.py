import pytest
from type_one import settings
from type_one.core.models import User
from django.test import Client
import json

@pytest.mark.django_db
def test_login():
    user = User.objects.create_user(username='test', password='test')
    client = Client()
    response = client.post('/api/token/',  data={"username":"test", "password":"test"}, follow = True)
    assert response.status_code == 200
    decoder = json.JSONDecoder()
    access_key = decoder.decode(response.content.decode('utf-8'))['access']
    print("TEST", access_key)
    user.delete()