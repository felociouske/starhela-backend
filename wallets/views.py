from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, Transaction, Deposit, Withdrawal
from .serializers import (
    WalletSerializer,
    TransactionSerializer,
    DepositSerializer,
    WithdrawalSerializer,
)


class MyWalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(
            user=request.user, defaults={"currency": "USD"}
        )
        return Response(WalletSerializer(wallet).data)


class MyTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user).order_by("-created_at")


class DepositListCreateView(generics.ListCreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyDepositsView(generics.ListAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user).order_by("-created_at")


class WithdrawalListCreateView(generics.ListCreateAPIView):
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        wallet = self.request.user.wallet
        amount = serializer.validated_data["amount"]

        if amount > wallet.balance:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"amount": "Insufficient balance."})

        serializer.save(user=self.request.user)