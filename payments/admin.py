from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "payment_type",
        "borrowing_id",
        "session_url",
        "session_id",
        "money_to_pay",
    )
