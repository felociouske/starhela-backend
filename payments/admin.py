from django.contrib import admin

from .models import MpesaConfig, PaymentMethod


@admin.register(MpesaConfig)
class MpesaConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_enabled",
        "business_shortcode",
        "environment",
        "required_amount",
    )
    search_fields = ("name", "business_shortcode", "callback_url")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "method_name",
        "account_number",
        "required_amount",
        "payment_link",
        "is_active",
        "display_order",
    )
    list_filter = ("country", "is_active")
    ordering = ("country", "display_order")
    search_fields = ("method_name", "account_number", "instructions")