from django.shortcuts import render
from rest_framework import viewsets

from book_service.permissions import IsAdminOrReadOnly
from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrReadOnly,)
