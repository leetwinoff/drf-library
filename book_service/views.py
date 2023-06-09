from datetime import timedelta

from django.utils.datetime_safe import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from book_service.models import Book
from book_service.permissions import IsAdminOrReadOnly
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowSerializer
from borrowing_service.telegram_helper import send_borrowing_notification


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "borrow":
            return BorrowSerializer
        return BookSerializer

    @action(detail=True, methods=["POST"])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if book.inventory > 0:
            if Borrowing.objects.filter(
                user_id=user, id=book.id, actual_return_date=None
            ).exists():
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
                expected_return_date=date.today() + timedelta(days=7),
                book_id=book,
                user_id=user,
            )
            send_borrowing_notification(borrowing)

            return Response(
                {"detail": "Book borrowed successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Book is out of stock"}, status=status.HTTP_204_NO_CONTENT
        )

    def get_permissions(self):
        if self.action == "borrow":
            return [IsAuthenticated()]
        return super().get_permissions()
