from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from .strings import string
import json

class Insulin(models.Model):
    code = models.CharField(max_length=100)
    def __str__(self):
        return string[self.code]

class SugarLevelUnit(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return string[self.code]

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
    sugar_unit = models.ForeignKey(SugarLevelUnit, on_delete = models.DO_NOTHING)
    def __str__(self):
        return str(self.value) + " " + self.sugar_unit.code

class Activity(models.Model):
    code = models.CharField(max_length = 100)
    def __str__(self):
        return map[self.code]
    class Meta():
        verbose_name_plural = "Activities"

class ActivityPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete = models.DO_NOTHING)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length = 255)
    def __str__(self):
        return self.code

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length = 255)
    bread_units_per_100g = models.FloatField()
    glycemic_index = models.IntegerField()
    fat_per_100g = models.IntegerField()
    carbohydrate_per_100g = models.IntegerField()
    protein_per_100g = models.IntegerField()
    energy_kKkal_per_100g = models.IntegerField()
    def __str__(self):
        return string[self.code]

class IngredientUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete = models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.DO_NOTHING)
    grams_int_unit = models.FloatField()
    def __str__(self):
        return self.ingredient.code + "_" + self.unit.code

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 255)

class MealIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING, related_name='meal_ingredients')
    indredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.DO_NOTHING)
    ingredient_units = models.FloatField()
    ingredient_weight_grams = models.IntegerField()

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.TimeField()
    sugar_level = models.ForeignKey(SugarLevel, on_delete = models.DO_NOTHING, null=True)
    insulin_shot = models.ForeignKey(InsulinShot, on_delete = models.DO_NOTHING, null=True)
    meal = models.ForeignKey(Meal, on_delete = models.DO_NOTHING, null=True)
    activity_period = models.ForeignKey(ActivityPeriod, on_delete = models.DO_NOTHING, null=True)
    notes = models.CharField(max_length = 1000, null=True)