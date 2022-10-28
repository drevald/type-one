from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from datetime import timedelta
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit

class Record(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default=0)
    glucose_level = models.FloatField(null = True, default = 0)
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    insulin_amount = models.IntegerField(null = True, default = 0)
    insulin = models.ForeignKey(Insulin, on_delete = models.SET_NULL, null = True)
    bread_units = models.FloatField(null = True, default = 0)
    notes = models.CharField(max_length = 256, null = True, blank=True)
    calories = models.IntegerField(default=0, null=True, blank=True)
    def get_meals(self):
        meals = list(Meal.objects.filter(record=self))
        return meals
    def get_calories_today(self):
        records = list(Record.objects.filter(time__year=self.time.year, time__month=self.time.month, time__day=self.time.day))
        return sum(record.calories for record in records)

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name='meals', null = True)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField(default=1)
    def __str__(self):
        return f"{_(self.ingredient_unit.ingredient.name)} {self.quantity} {_(self.ingredient_unit.unit.name)}"
    def get_calories(self):
        return self.quantity * self.ingredient_unit.grams_in_unit * self.ingredient_unit.ingredient.energy_kKkal_per_100g

class Photo(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name='photos', null = True)
    data = models.TextField(null=False)
    thumb = models.TextField(null=False)