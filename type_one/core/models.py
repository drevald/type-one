from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from .strings import string

class Insulin(models.Model):
    code = models.CharField(max_length=100)
    def __str__(self):
        return self.code

class SugarLevelUnit(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return self.code

class User(AbstractUser):
    sugar_level_unit = models.ForeignKey(SugarLevelUnit, on_delete = models.SET_NULL, null=True)
    long_acting_insulin = models.ForeignKey(Insulin, related_name='long', on_delete = models.SET_NULL, null=True)
    rapid_acting_insulin = models.ForeignKey(Insulin, related_name='rapid', on_delete = models.SET_NULL, null=True)

class InsulinShot(models.Model):
    amount_units = models.FloatField()
    insulin = models.ForeignKey(Insulin, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.amount_units)

class SugarLevel(models.Model):
    value = models.IntegerField()
    sugarUnit = models.ForeignKey(SugarLevelUnit, on_delete = models.DO_NOTHING)
    def __str__(self):
        return str(self.value) + " " + self.sugarUnit.code

class Activity(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return map[self.code]
    class Meta():
        verbose_name_plural = "Activities"

class ActivityPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete = models.DO_NOTHING)
    startTime = models.TimeField()
    endTime = models.TimeField()

class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length = 255)
    def __str__(self):
        return self.code

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length = 255)
    breadUnitsPer100g = models.FloatField()
    glycemicIndex = models.IntegerField()
    fatPer100g = models.IntegerField()
    carbohydratePer100g = models.IntegerField()
    proteinPer100g = models.IntegerField()
    energyKkalPer100g = models.IntegerField()
    def __str__(self):
        return self.code

class IngredientUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete = models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.DO_NOTHING)
    gramsInUnit = models.FloatField()
    def __str__(self):
        return self.ingredient.code + "_" + self.unit.code

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 255)

class MealIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING)
    indredientUnitId = models.ForeignKey(IngredientUnit, on_delete = models.DO_NOTHING)
    ingredientWeightGrams = models.IntegerField()

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.TimeField()
    sugarLevel = models.ForeignKey(SugarLevel, on_delete = models.DO_NOTHING, null=True)
    insulinShot = models.ForeignKey(InsulinShot, on_delete = models.DO_NOTHING, null=True)
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING, null=True)
    activityPeriod = models.ForeignKey(ActivityPeriod, on_delete = models.DO_NOTHING, null=True)
    notes = models.CharField(max_length = 1000, null=True)