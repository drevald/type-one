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
        response = self.client.get('/records', follow = True)
        self.assertEqual(response.status_code, 200)
        print("list records ok")

        response = self.client.post("/records/create/0", data={"insulin_amount": "1", "glucose_level":"8"}, follow = True)
        self.assertEqual(response.status_code, 200)
        print("create record ok")

        response = self.client.post("/records/1", follow = True)
        self.assertEqual(response.status_code, 200)
        print("record details ok")        
