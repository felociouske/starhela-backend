from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "country", "is_verified_display", "created_at")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Starhela info", {"fields": ("role", "country", "phone_number")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Starhela info", {"fields": ("email", "role", "country", "phone_number")}),
    )
    ordering = ("-created_at",)

    def is_verified_display(self, obj):
        return getattr(getattr(obj, "provider_profile", None), "is_verified", "-")
    is_verified_display.short_description = "Verified provider"


admin.site.register(User, UserAdmin)