from enum import Enum

from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "HARD"),
        ("SOFT", "SOFT"),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    covers = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title
