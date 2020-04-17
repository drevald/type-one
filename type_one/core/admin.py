from django.contrib import admin
from .models import SugarLevelUnit, Insulin, Activity

admin.site.register(SugarLevelUnit)
admin.site.register(Insulin)
admin.site.register(Activity)