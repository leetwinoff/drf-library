from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from book_service.permissions import IsAdminOrReadOnly
from borrowing_service.models import Borrowing

from borrowing_service.serializers import (
    BorrowingSerializer,
    ReturnBookSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "return_book":
            return ReturnBookSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user_id=user)

    @action(detail=True, methods=["POST"])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "Book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.mark_as_returned()
        return Response(
            {"detail": "Book returned successfully."}, status=status.HTTP_200_OK
        )

    def get_permissions(self):
        if self.action == "return_book":
            return []
        return super().get_permissions()
