from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Insulin(models.Model):
    code = models.CharField(max_length=100)

class InsulinShot(models.Model):
    amount_units = models.FloatField()
    insulin = models.ForeignKey(Insulin, on_delete=models.CASCADE)

class SugarLevelUnit(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return self.code

class SugarLevel(models.Model):
    value = models.IntegerField()
    sugarUnit = models.ForeignKey(SugarLevelUnit, on_delete = models.CASCADE)

class Activity(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return self.code

class ActivityPeriod(models.Model):
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE)
    startTime = models.TimeField()
    endTime = models.TimeField()

class Unit(models.Model):
    code = models.CharField(max_length = 255)
    def __str__(self):
        return self.code

class Ingredient(models.Model):
    code = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    glycemicIndex = models.IntegerField()
    breadUnitsPer100g = models.FloatField()
    fatPer100g = models.IntegerField()
    carbohydratePer100g = models.IntegerField()
    proteinPer100g = models.IntegerField()
    energyKkalPer100g = models.IntegerField()
    def __str__(self):
        return self.name

class IngredientUnit(models.Model):
    unit = models.ForeignKey(Unit, on_delete = models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    gramsInUnit = models.FloatField()
    def __str__(self):
        return self.ingredient.code + "_" + self.unit.code

class Meal(models.Model):
    name = models.CharField(max_length = 255)

class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING)
    indredientUnitId = models.ForeignKey(IngredientUnit, on_delete = models.DO_NOTHING)
    ingredientWeightGrams = models.IntegerField()

class Record(models.Model):
    time = models.TimeField()
    sugarLevel = models.ForeignKey(SugarLevel, on_delete = models.DO_NOTHING)
    insulinShot = models.ForeignKey(InsulinShot, on_delete = models.DO_NOTHING)
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING)
    activityPeriod = models.ForeignKey(ActivityPeriod, on_delete = models.DO_NOTHING)
    notes = models.CharField(max_length = 1000)