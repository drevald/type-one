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

class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.client = Client()

    def test_records(self):        
        response = self.client.get('/records')
        self.assertEqual(response.status_code, 200)
        print(response.context['object_list'])
        print(len(response.context['object_list']))
