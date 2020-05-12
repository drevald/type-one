from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from ..core.models import User, GlucoseUnit, Insulin
from ..ingredients.models import Ingredient, IngredientUnit

class Record(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    type = models.IntegerField(default=0)
    glucose_level = models.IntegerField(null = True, default = 0)
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    insulin_amount = models.FloatField(null = True, default = 0)
    insulin = models.ForeignKey(Insulin, on_delete = models.SET_NULL, null = True)
    bread_units = models.FloatField(null = True, default = 0)
    notes = models.CharField(max_length = 256, null = True)

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name='meals', null = True)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField(default=1)
    def __str__(self):
        return self.ingredient_unit.ingredient.name + " " + str(self.quantity) + " " + self.ingredient_unit.unit.name