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
    time = models.DateTimeField()
    glucose_level = models.IntegerField(null = True, default = 0)
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    insulin_amount = models.FloatField(null = True, default = 0)
    insulin = models.ForeignKey(Insulin, on_delete = models.SET_NULL, null = True)
    notes = models.CharField(max_length = 256, null = True)

class Ingredient(models.Model):
    name = models.CharField(max_length = 255)
    bread_units_per_100g = models.FloatField()
    glycemic_index = models.IntegerField()
    fat_per_100g = models.IntegerField()
    carbohydrate_per_100g = models.IntegerField()
    protein_per_100g = models.IntegerField()
    energy_kKkal_per_100g = models.IntegerField()
    def __str__(self):
        return self.name

class WeightUnit(models.Model):
    name = models.CharField(max_length = 32)
    def __str__(self):
        return self.name  

class IngredientUnit(models.Model):
    unit = models.ForeignKey(WeightUnit, on_delete = models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.DO_NOTHING)
    grams_in_unit = models.FloatField()
    def __str__(self):
        return self.ingredient.name + "_" + self.unit.name   

class MealIngredient(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE, null = True)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField()


  


