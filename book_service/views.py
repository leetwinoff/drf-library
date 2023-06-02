from datetime import timedelta

from django.shortcuts import render
from django.utils.datetime_safe import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from book_service.models import Book
from book_service.permissions import IsAdminOrReadOnly
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "borrow":
            return BorrowingSerializer
        return BookSerializer

    @action(detail=True, methods=["POST"])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if book.inventory > 0:
            if user.borrowed_books.filter(id=book.id).exists():
                return Response(
                    {"detail": "You have already borrowed this book"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.borrowed_books.add(book)
            book.inventory -= 1
            book.save()
            user.save()

            borrowing = Borrowing.objects.create(
                borrow=date.today(),
                expected_return_date=date.today() + timedelta(weeks=1),
                book_id=book,
                user_id=user,
            )

            return Response(
                {"detail": "Book borrowed succesfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Book is out of stock"}, status=status.HTTP_204_NO_CONTENT
        )

    def get_permissions(self):
        if self.action == "borrow":
            return []
        return super().get_permissions()
