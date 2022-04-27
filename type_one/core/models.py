from django.contrib.auth.models import AbstractUser
from django.db import models

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
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True, blank=True)
    long_acting_insulin = models.ForeignKey(Insulin, related_name='long_insulin_users', on_delete = models.SET_NULL, null=True, blank=True)
    rapid_acting_insulin = models.ForeignKey(Insulin, related_name='rapid_insulin_users', on_delete = models.SET_NULL, null=True, blank=True)
    show_long_insulin = models.BooleanField(default = True)
    show_rapid_insulin = models.BooleanField(default = True)
    show_sugar = models.BooleanField(default = True)
    show_calories = models.BooleanField(default = False)
    show_bread_units = models.BooleanField(default = False)
    def show_insulin(self):
        return self.show_long_insulin or self.show_rapid_insulin