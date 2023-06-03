from django.db import models

from user_services.models import User


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
