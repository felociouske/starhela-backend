from django.conf import settings
from django.db import models

from accounts.constants import COUNTRY_CHOICES


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    nationality = models.CharField(
        max_length=10,
        choices=COUNTRY_CHOICES + [("OTHER", "Other")],
        default="OTHER",
    )
    photo = models.ImageField(upload_to="provider_photos/", blank=True, null=True)

    chat_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Flat fee in USD to start a chat with this provider",
    )

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True, help_text="Provider can be hidden from listings without deleting"
    )
    id_document = models.ImageField(
        upload_to="provider_verification/", blank=True, null=True,
        help_text="ID document for admin verification, not shown publicly",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.display_name} ({'verified' if self.is_verified else 'unverified'})"