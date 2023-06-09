from django.contrib import admin

from book_service.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "covers", "inventory", "daily_fee")
