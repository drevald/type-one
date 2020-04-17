from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Unit(models.Model):
    code = models.CharField(max_length=200)

class Insulin(models.Model):
    code = models.CharField(max_length=100)

class InsulinShot(models.Model):
    amount_units = models.FloatField()
    insulin = models.ForeignKey(Insulin, on_delete=models.CASCADE)
    time = models.TimeField()