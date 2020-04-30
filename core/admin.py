from django.contrib import admin
from .models import GlucoseUnit, Insulin

admin.site.register(GlucoseUnit)
admin.site.register(Insulin)