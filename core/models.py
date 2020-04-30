from django.db import models

# Create your models here.

class Insulin(models.Model):
    name = models.CharField()

class GlucoseUnit():
    name = models.CharField()
    ratio_to_mmol_l = models.FloatField()

class Record(models.Model):
    glucose_level = models.IntegerField()
    glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL)
    insulin_amount = models.FloatField()
    insulin_type = models.ForeignKey(Insulin, on_delete = models.SET_NULL)
    notes = models.CharField()

class MealIngredient(modelsModel):
    record = models.ForeignKey(Record, on_delete = models.CASCADE)
    ingredinet = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField()

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
    name = models.CharField()
    ratio_to_gramm = models.FloatField()
    def __str__(self):
        return self.name    

class IngredientUnit(models.Model):
    unit = models.ForeignKey(WeightUnit, on_delete = models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete = models.DO_NOTHING)
    grams_int_unit = models.FloatField()
    def __str__(self):
        return self.ingredient.name + "_" + self.unit.name
