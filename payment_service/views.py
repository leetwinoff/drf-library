from django.db.models import Q
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from book_service.permissions import IsAdminOrReadOnly
from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()


def success_url(request):
    return render(request, "success.html")


def cancel_url(request):
    return render(request, "cancel.html")
