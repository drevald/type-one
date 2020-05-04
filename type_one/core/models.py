from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.

class Insulin(models.Model):
    name = models.CharField(max_length = 32)
    def __str__(self): 
        return self.name

class GlucoseUnit(models.Model):
    name = models.CharField(max_length = 32)
    ratio_to_mmol_l = models.FloatField()
    def __str__(self): 
        return self.name

class User(AbstractUser):
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    long_acting_insulin = models.ForeignKey(Insulin, related_name='long', on_delete = models.SET_NULL, null=True)
    rapid_acting_insulin = models.ForeignKey(Insulin, related_name='rapid', on_delete = models.SET_NULL, null=True)

class Record(models.Model):
    time = models.DateTimeField(auto_now=True)
    type = models.IntegerField(default=0)
    glucose_level = models.IntegerField(null = True, default = 0)
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    insulin_amount = models.FloatField(null = True, default = 0)
    insulin = models.ForeignKey(Insulin, on_delete = models.SET_NULL, null = True)
    bread_units = models.FloatField(null = True, default = 0)
    notes = models.CharField(max_length = 256, null = True)