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
    def get_prots(self):
        meals = self.get_meals()
        prot = 0
        for meal in meals:
            prot += (meal.ingredient_unit.ingredient.protein_per_100g * meal.ingredient_unit.grams_in_unit * meal.quantity)/100
        return prot
    def get_fats(self):
        meals = self.get_meals()
        fat = 0
        for meal in meals:
            fat += (meal.ingredient_unit.ingredient.fat_per_100g * meal.ingredient_unit.grams_in_unit * meal.quantity)/100            
        return fat    
    def get_carbs(self):
        meals = self.get_meals()
        carb = 0
        for meal in meals:
            carb += (meal.ingredient_unit.ingredient.carbohydrate_per_100g * meal.ingredient_unit.grams_in_unit * meal.quantity)/100            
        return carb        
    def get_calories_today(self):
        today = datetime.now()  
        today_start = datetime(today.year, today.month, today.day, 00, 00, 00)
        today_shifted = today_start + timedelta(hours = -3)
        t = [today_shifted.year, today_shifted.month, today_shifted.day, today_shifted.hour]
        records = Record.objects.raw('SELECT id, time FROM records_record where time > make_timestamp(%s, %s, %s, %s, 0, 0) ORDER BY time DESC', t)        
        sum = 0
        for record in records:
            sum += record.calories
        return sum

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name='meals', null = True)
    ingredient_unit = models.ForeignKey(IngredientUnit, on_delete = models.CASCADE)
    quantity = models.FloatField(default=1)
    def __str__(self):
        return f"{_(self.ingredient_unit.ingredient.name)} {self.quantity} {_(self.ingredient_unit.unit.name)}"
    def get_calories(self):
        return self.quantity * self.ingredient_unit.grams_in_unit * self.ingredient_unit.ingredient.energy_kKkal_per_100g * 0.01

class Photo(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name='photos', null = True)
    data = models.TextField(null=False)
    thumb = models.TextField(null=False)