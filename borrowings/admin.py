from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "borrow",
        "expected_return_date",
        "actual_return_date",
        "book_id",
        "user_id",
    )
