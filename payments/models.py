from django.db import models

from accounts.constants import COUNTRY_CHOICES


class MpesaConfig(models.Model):
    name = models.CharField(max_length=50, default="kenya", unique=True)
    is_enabled = models.BooleanField(default=False)
    business_shortcode = models.CharField(
        max_length=20,
        blank=True,
        help_text="Safaricom till number or shortcode",
    )
    consumer_key = models.CharField(max_length=255, blank=True)
    consumer_secret = models.CharField(max_length=255, blank=True)
    passkey = models.CharField(max_length=500, blank=True)
    callback_url = models.URLField(blank=True, help_text="Your callback URL for M-Pesa")
    environment = models.CharField(
        max_length=20,
        choices=[("sandbox", "Sandbox"), ("production", "Production")],
        default="sandbox",
    )
    instructions = models.TextField(blank=True, help_text="Display instructions for the user")
    required_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=550,
        help_text="Amount required for activation",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "M-Pesa configuration"
        verbose_name_plural = "M-Pesa configurations"

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
    method_name = models.CharField(
        max_length=100, help_text="e.g. MTN Mobile Money, M-Pesa, Airtel Money"
    )
    account_name = models.CharField(max_length=150, blank=True)
    account_number = models.CharField(
        max_length=100, help_text="Till number, paybill, phone number, etc."
    )
    payment_link = models.URLField(blank=True, help_text="External payment link for Eversend or similar")
    required_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Minimum amount required to auto-activate the account",
    )
    instructions = models.TextField(
        help_text="Step by step guide shown to the user, e.g. Go to M-Pesa > Lipa na M-Pesa > ..."
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["country", "display_order"]

    def __str__(self):
        return f"{self.get_country_display()} - {self.method_name}"