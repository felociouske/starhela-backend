from django.urls import path

from .views import (
    MyWalletView,
    MyTransactionsView,
    DepositListCreateView,
    WithdrawalListCreateView,
)

urlpatterns = [
    path("wallet/", MyWalletView.as_view(), name="my-wallet"),
    path("transactions/", MyTransactionsView.as_view(), name="my-transactions"),
    path("deposits/", DepositListCreateView.as_view(), name="deposits"),
    path("withdrawals/", WithdrawalListCreateView.as_view(), name="withdrawals"),
]