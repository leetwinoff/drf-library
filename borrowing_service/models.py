from django.utils import timezone

from django.db import models

from book_service.models import Book
from user_services.models import User


class Borrowing(models.Model):
    borrow = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(weeks=1), editable=False
    )
    actual_return_date = models.DateTimeField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["actual_return_date"]

    def mark_as_returned(self):
        self.actual_return_date = timezone.now()
        self.save()
        self.book_id.inventory += 1
        self.book_id.save()
        self.user_id.borrowed_books.remove(self.book_id)

    @property
    def is_active(self):
        if self.actual_return_date is None:
            return True
        return False
