from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets.models import Deposit

from .models import MpesaConfig, PaymentMethod
from .serializers import PaymentMethodSerializer


class MyCountryPaymentMethodsView(generics.ListAPIView):
    """Returns active payment methods for the logged-in user's own country."""

    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(
            country=self.request.user.country, is_active=True
        )


class PaymentMethodsByCountryView(generics.ListAPIView):
    """Lets the frontend fetch instructions for any country, e.g. at signup time."""

    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        country = self.kwargs["country_code"].upper()
        return PaymentMethod.objects.filter(country=country, is_active=True)


class MpesaInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.country != "KE":
            return Response({"detail": "This endpoint is only for Kenya users."}, status=400)

        config = MpesaConfig.objects.filter(name="kenya", is_enabled=True).first()
        if not config:
            return Response({"detail": "M-Pesa is not configured yet."}, status=400)

        deposit_id = request.data.get("deposit_id")
        amount = request.data.get("amount")
        if not deposit_id or not amount:
            return Response({"detail": "deposit_id and amount are required."}, status=400)

        try:
            deposit = Deposit.objects.get(id=deposit_id, user=user)
        except Deposit.DoesNotExist:
            return Response({"detail": "Deposit not found."}, status=404)

        deposit.amount = amount
        deposit.save(update_fields=["amount"])

        response_payload = {
            "status": "queued",
            "message": "M-Pesa payment request prepared. Replace the placeholder credentials in the admin panel with your live Safaricom keys to enable real STK push.",
            "business_shortcode": config.business_shortcode or "YOUR_TILL_NUMBER",
            "amount": float(amount),
            "deposit_id": deposit.id,
            "callback_url": config.callback_url or "",
        }
        return Response(response_payload, status=200)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def mpesa_callback(request):
    data = request.data or {}
    checkout_request_id = data.get("CheckoutRequestID") or data.get("checkout_request_id")
    result_code = data.get("ResultCode") or data.get("result_code")
    result_description = data.get("ResultDesc") or data.get("result_description")

    if checkout_request_id:
        Deposit.objects.filter(checkout_request_id=checkout_request_id).update(
            mpesa_request_id=checkout_request_id,
        )

    if result_code in {"0", 0}:
        deposits = Deposit.objects.filter(checkout_request_id=checkout_request_id)
        for deposit in deposits:
            if deposit.payment_method and deposit.payment_method.required_amount and deposit.amount >= deposit.payment_method.required_amount:
                deposit.status = Deposit.STATUS_APPROVED
                deposit.user.is_verified = True
                deposit.user.save(update_fields=["is_verified"])
                deposit.save(update_fields=["status"])

    return JsonResponse({"ResultCode": "0", "ResultDesc": "Accepted"})