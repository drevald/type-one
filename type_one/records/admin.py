from django.contrib import admin
from .models import GlucoseUnit, Insulin, User

admin.site.register(GlucoseUnit)
admin.site.register(Insulin)
admin.site.register(User)