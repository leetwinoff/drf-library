from django.db import models

from user_services.models import User


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    )
    TYPE_CHOICES = (
        ("PAYMENT", "Payment"),
        ("FINE", "Fine"),
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default="PENDING")
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing_id = models.IntegerField()
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
