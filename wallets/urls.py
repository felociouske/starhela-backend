from django.urls import path

from .views import (
    MyWalletView,
    MyTransactionsView,
    DepositListCreateView,
    MyDepositsView,
    WithdrawalListCreateView,
)

urlpatterns = [
    path("wallet/", MyWalletView.as_view(), name="my-wallet"),
    path("transactions/", MyTransactionsView.as_view(), name="my-transactions"),
    path("deposits/mine/", MyDepositsView.as_view(), name="my-deposits"),
    path("deposits/", DepositListCreateView.as_view(), name="deposits"),
    path("withdrawals/", WithdrawalListCreateView.as_view(), name="withdrawals"),
]