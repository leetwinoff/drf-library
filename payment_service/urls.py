from django.urls import path

from payment_service.views import (
    PaymentListView,
    PaymentDetailView,
    success_url,
    cancel_url,
)

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("payments/success/", success_url, name="success"),
    path("payments/cancel/", cancel_url, name="success"),
]
app_name = "payment_service"
