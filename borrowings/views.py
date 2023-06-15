from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.permissions import IsAdminOrReadOnly
from borrowings.models import Borrowing

from borrowings.serializers import (
    BorrowingSerializer,
    ReturnBookSerializer,
    BorrowSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "return_book":
            return ReturnBookSerializer
        if self.action == "borrow_book":
            return BorrowSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user_id=user)

    @action(detail=False, methods=["POST"])
    def borrow(self, request, pk=None):
        serializer = BorrowSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()

        return Response(
            {"detail": "Book borrowed succesfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["POST"])
    def return_book(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        session_url = serializer.return_book()

        return Response({"detail": session_url}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["borrow_book", "return_book"]:
            return []
        return super().get_permissions()
