from django.urls import path

from .views import (
    MpesaInitiateView,
    MyCountryPaymentMethodsView,
    PaymentMethodsByCountryView,
    mpesa_callback,
)

urlpatterns = [
    path("payment-methods/mine/", MyCountryPaymentMethodsView.as_view(), name="my-payment-methods"),
    path(
        "payment-methods/<str:country_code>/",
        PaymentMethodsByCountryView.as_view(),
        name="payment-methods-by-country",
    ),
    path("mpesa/initiate/", MpesaInitiateView.as_view(), name="mpesa-initiate"),
    path("mpesa/callback/", mpesa_callback, name="mpesa-callback"),
]