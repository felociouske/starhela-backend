from django.contrib import admin

from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "nationality", "chat_rate", "is_verified", "is_active", "created_at")
    list_filter = ("is_verified", "is_active", "nationality")
    search_fields = ("display_name", "user__email")
    actions = ["verify_providers", "unverify_providers"]

    def verify_providers(self, request, queryset):
        queryset.update(is_verified=True)

    verify_providers.short_description = "Mark selected providers as verified"

    def unverify_providers(self, request, queryset):
        queryset.update(is_verified=False)

    unverify_providers.short_description = "Mark selected providers as unverified"