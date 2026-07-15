from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.constants import get_currency_for_country
from .models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            user=instance,
            currency=get_currency_for_country(instance.country),
        )