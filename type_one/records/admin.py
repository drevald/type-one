from django.contrib import admin
from .models import GlucoseUnit, Insulin, User
from django.contrib.auth.admin import UserAdmin

class TypeOneAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('glucose_level_unit','long_acting_insulin','rapid_acting_insulin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('glucose_level_unit','long_acting_insulin','rapid_acting_insulin',)}),
    )

admin.site.register(GlucoseUnit)
admin.site.register(Insulin)
admin.site.register(User, TypeOneAdmin)