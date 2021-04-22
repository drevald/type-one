import django
import hashlib
import unittest
import base64
import io
from django.test import Client
from django.test import TestCase
from django.test import TransactionTestCase
from django.template import RequestContext
from PIL import Image, ImageFilter
from type_one.core.models import User


class LogInTest(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'test'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/admin/login/', self.credentials, follow=True)
        # should be logged in now
        print(response.context)
        self.assertTrue(response.context['user'].is_active)

class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.username = "test"
        self.password = "test"
        user = User(username=self.username, password=self.username)
        user.save()
        self.client = Client()

    def test_ingredients(self):      

        response = self.client.post('/accounts/login',  data={"username":self.username, "password":self.password}, follow = True)
        # print(response.content)
        # print(type(response))
        # print(dir(response))
        # print(response._headers["location"])
        self.assertEqual(response.status_code, 200)
        print("user logged in")
        # how to check it is logged in?
        # how to find where client was forwarded to?

        response = self.client.get('/ingredients', follow = True)
        self.assertEqual(response.status_code, 200)
        print("list ingredients ok")

        response = self.client.post('/ingredients/create', follow = True)
        self.assertEqual(response.status_code, 200)
        print("create ingredient ok")

        response = self.client.get('/ingredients/0', follow = True)
        self.assertEqual(response.status_code, 200)
        print(response.context['form'].instance)
        self.assertNotEqual(response.context['form'].instance, None)
        print("ingredient detail ok")