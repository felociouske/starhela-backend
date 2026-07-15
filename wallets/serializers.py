from rest_framework import serializers

from payments.models import PaymentMethod

from .models import Wallet, Transaction, Deposit, Withdrawal


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "currency", "balance", "held_balance", "updated_at"]
        read_only_fields = fields


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "type", "amount", "note", "created_at"]
        read_only_fields = fields


class DepositSerializer(serializers.ModelSerializer):
    payment_method = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(), required=False, allow_null=True
    )
    transaction_code = serializers.CharField(required=False, allow_blank=True, max_length=100)
    message = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        model = Deposit
        fields = [
            "id",
            "amount",
            "payment_method",
            "reference_code",
            "transaction_code",
            "message",
            "proof_image",
            "status",
            "admin_note",
            "created_at",
            "reviewed_at",
        ]
        read_only_fields = ["id", "status", "admin_note", "created_at", "reviewed_at"]

    def create(self, validated_data):
        payment_method = validated_data.pop("payment_method", None)
        transaction_code = validated_data.pop("transaction_code", None)
        message = validated_data.pop("message", "")
        amount = validated_data.get("amount")
        if amount is None:
            validated_data["amount"] = 0
        deposit = Deposit.objects.create(**validated_data)
        if payment_method is not None:
            deposit.payment_method = payment_method
        if transaction_code:
            deposit.transaction_code = transaction_code
        if transaction_code and not deposit.reference_code:
            deposit.reference_code = transaction_code
        if message:
            deposit.admin_note = message

        should_activate = False
        if payment_method and payment_method.required_amount and deposit.amount >= payment_method.required_amount:
            should_activate = True

        if should_activate:
            deposit.status = Deposit.STATUS_APPROVED
            deposit.user.is_verified = True
            deposit.user.save(update_fields=["is_verified"])

        deposit.save(update_fields=["payment_method", "transaction_code", "reference_code", "admin_note", "status"])
        return deposit


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = [
            "id",
            "amount",
            "payout_details",
            "status",
            "admin_note",
            "created_at",
            "reviewed_at",
        ]
        read_only_fields = ["id", "status", "admin_note", "created_at", "reviewed_at"]