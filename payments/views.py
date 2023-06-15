from django.db.models import Q
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from books.permissions import IsAdminOrReadOnly
from payments.models import Payment
from payments.serializers import PaymentSerializer


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
