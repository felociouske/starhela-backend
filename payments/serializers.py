from rest_framework import serializers

from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    country_display = serializers.CharField(source="get_country_display", read_only=True)

    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "country",
            "country_display",
            "method_name",
            "account_name",
            "account_number",
            "payment_link",
            "required_amount",
            "instructions",
        ]
        read_only_fields = fields