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
    code = models.CharField(max_length = 100)

class SugarLevel(models.Model):
    value = models.IntegerField()
    sugarUnit = models.ForeignKey(SugarLevelUnit, on_delete = models.CASCADE)

class Activity(models.Model):
    activityCode = models.CharField(max_length = 100)

class ActivityPeriod(models.Model):
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE)
    startTime = models.TimeField();
    endTime = models.TimeField();

class Unit(models.Model):
    name = models.CharField(max_length = 255);

class IngredientType(models.Model):
    code = models.CharField(max_length = 255);

class Ingredient(models.Model):
    ingredientType = models.ForeignKey(Activity, on_delete = models.CASCADE)
    code = models.CharField(max_length = 255);
    name = models.CharField(max_length = 255);
    glycemicIndex = models.IntegerField();
    breadUnitsPer100g = models.FloatField();
    fatPer100g = models.IntegerField();
    carbohydratePer100g = models.IntegerField();
    proteinPer100g = models.IntegerField();
    energyKkalPer100g = models.IntegerField();

class IngredientUnit(models.Model):
    unit = models.ForeignKey(Unit, on_delete = models.CASCADE);
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE);
    gramsInUnit = models.FloatField();

class Meal(models.Model):
    name = models.CharField(max_length= 255);

class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING);
    indredientUnitId = models.ForeignKey(IngredientUnit, on_delete = models.DO_NOTHING);
    ingredientWeightGrams = models.IntegerField();

class Record(models.Model):
    time = models.TimeField();
    sugarLevel = models.ForeignKey(SugarLevel, on_delete = models.DO_NOTHING); 
    insulinShot = models.ForeignKey(InsulinShot, on_delete = models.DO_NOTHING);
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING);
    activityPeriod = models.ForeignKey(ActivityPeriod, on_delete = models.DO_NOTHING);
    notes = models.CharField(max_length=1000);    
