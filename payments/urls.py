from django.urls import path

from payments.views import (
    PaymentListView,
    PaymentDetailView,
    success_url,
    cancel_url,
)

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path(
        "<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),
    path("success/", success_url, name="success"),
    path("cancel/", cancel_url, name="success"),
]
app_name = "payments"
