from django.db import models
from ..core.models import User, GlucoseUnit, Insulin

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length = 255)
    bread_units_per_100g = models.FloatField()##
    glycemic_index = models.IntegerField(null=True, default=50)
    fat_per_100g = models.IntegerField()
    carbohydrate_per_100g = models.IntegerField()
    protein_per_100g = models.IntegerField()
    energy_kKkal_per_100g = models.IntegerField()
    def __str__(self):
        return self.name

class WeightUnit(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length = 32)
    def __str__(self):
        return self.name  

class IngredientUnit(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    unit = models.ForeignKey(WeightUnit, on_delete = models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    grams_in_unit = models.FloatField()
    def __str__(self):
        return self.ingredient.name + ", " + self.unit.name

