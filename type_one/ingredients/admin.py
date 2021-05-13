from django.contrib import admin
from .models import Ingredient, WeightUnit, IngredientUnit

admin.site.register(WeightUnit)
admin.site.register(IngredientUnit)