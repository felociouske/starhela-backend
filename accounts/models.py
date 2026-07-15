from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import COUNTRY_CHOICES


class User(AbstractUser):
    ROLE_CLIENT = "client"
    ROLE_PROVIDER = "provider"

    ROLE_CHOICES = [
        (ROLE_CLIENT, "Client"),
        (ROLE_PROVIDER, "Provider"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CLIENT)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email