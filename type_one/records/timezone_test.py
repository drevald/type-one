from django.test import TestCase
from type_one.records.models import Record
from type_one.core.models import User
from datetime import datetime
from datetime import timezone

class TimezoneTestCase(TestCase):

    def setUp(self):
        stamp_one = datetime(2023, 2, 20, 8, 57, 26, tzinfo=timezone.utc)
        stamp_two = datetime(2023, 2, 20, 9, 1, 18,  tzinfo=timezone.utc)        
        user = User.objects.create_user(username = 'test', password = 'test')
        record_one = Record.objects.create(user_id = user.id)
        record_two = Record.objects.create(user_id = user.id)
        record_one.time = stamp_one
        record_two.time = stamp_two
        record_one.save()ssh 
        record_two.save()

    def test_record_has_timestamp(self):
        records = Record.objects.filter(time__year=2023, time__month=2, time__day=20)
        self.assertTrue(len(records) == 2)
