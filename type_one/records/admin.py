from django.contrib import admin
from .models import GlucoseUnit, Insulin, User
from django.contrib.auth.admin import UserAdmin

class TypeOneAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('glucose_level_unit','long_acting_insulin','rapid_acting_insulin','show_long_insulin','show_rapid_insulin','show_sugar','show_calories','show_bread_units',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('glucose_level_unit','long_acting_insulin','rapid_acting_insulin','show_long_insulin','show_rapid_insulin','show_sugar','show_calories','show_bread_units',)}),
    )

admin.site.register(GlucoseUnit)
admin.site.register(Insulin)
admin.site.register(User, TypeOneAdmin)