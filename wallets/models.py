from django.conf import settings
from django.db import models

from accounts.constants import get_currency_for_country
from payments.models import PaymentMethod


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )
    currency = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    held_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} wallet ({self.currency})"


class Transaction(models.Model):
    TYPE_DEPOSIT = "deposit"
    TYPE_WITHDRAWAL = "withdrawal"
    TYPE_CHAT_HOLD = "chat_hold"
    TYPE_CHAT_RELEASE = "chat_release"
    TYPE_CHAT_REFUND = "chat_refund"

    TYPE_CHOICES = [
        (TYPE_DEPOSIT, "Deposit"),
        (TYPE_WITHDRAWAL, "Withdrawal"),
        (TYPE_CHAT_HOLD, "Chat Hold"),
        (TYPE_CHAT_RELEASE, "Chat Release"),
        (TYPE_CHAT_REFUND, "Chat Refund"),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} {self.amount} - {self.wallet.user.email}"


class Deposit(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deposits"
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        related_name="deposits",
        null=True,
        blank=True,
    )
    reference_code = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. M-Pesa/Mobile Money transaction code",
    )
    transaction_code = models.CharField(
        max_length=100,
        blank=True,
        help_text="Additional transaction/reference code from the payment proof",
    )
    checkout_request_id = models.CharField(max_length=100, blank=True)
    mpesa_request_id = models.CharField(max_length=100, blank=True)
    proof_image = models.ImageField(upload_to="deposit_proofs/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Deposit {self.amount} - {self.user.email} ({self.status})"


class Withdrawal(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals"
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payout_details = models.CharField(
        max_length=255, help_text="e.g. phone number to send mobile money to"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Withdrawal {self.amount} - {self.user.email} ({self.status})"