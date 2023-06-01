from enum import Enum

from django.db import models


class CoverChoices(Enum):
    HARD = "HARD"
    SOFT = "SOFT"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    covers = models.CharField(
        max_length=4, choices=[(cover.name, cover.value) for cover in CoverChoices]
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title
