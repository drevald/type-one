from django.db import models
from type_one.core.models import Record

class Ingredient(models.Model):
    name = models.CharField(max_length = 255)
    bread_units_per_100g = models.FloatField()##
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

class Meal(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE, null = True)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField(default=0)