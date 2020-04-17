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

class SugarLevelUnit(models.Model):
    code = models.CharField(max_length=100)

class SugarLevel(models.Model):
    value = models.IntegerField()
    sugarUnit = models.ForeignKey(SugarLevelUnit, on_delete=models.CASCADE)

class Activity(models.Model):
    activityCode = models.CharField(max_length=100)

class ActivityPeriod(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    startTime = models.TimeField();
    endTime = models.TimeField();

class Unit:
    name = models.CharField(max_length=255);

class IngredientUnit(models.Model):
    pass



