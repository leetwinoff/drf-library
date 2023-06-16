from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.permissions import IsAdminOrReadOnly
from borrowings.models import Borrowing

from borrowings.serializers import (
    ReturnBookSerializer,
    BorrowSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return BorrowSerializer
        if self.action in ["retrieve", "return_book"]:
            return ReturnBookSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user_id=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.create(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(borrowing).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["POST"])
    def return_book(self, request, *args, **kwargs):
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["list", "create", "retrieve", "return_book"]:
            return []
        return super().get_permissions()
