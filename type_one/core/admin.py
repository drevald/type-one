from django.contrib import admin
from .models import GlucoseUnit, Insulin, User, Ingredient, WeightUnit, IngredientUnit

admin.site.register(GlucoseUnit)
admin.site.register(Insulin)
admin.site.register(User)
admin.site.register(WeightUnit)
admin.site.register(IngredientUnit)