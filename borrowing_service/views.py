import stripe
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from book_service.permissions import IsAdminOrReadOnly
from borrowing_service.models import Borrowing

from borrowing_service.serializers import (
    BorrowingSerializer,
    ReturnBookSerializer,
)
from borrowing_service.telegram_helper import return_borrowing_notification
from drf_library.settings import STRIPE_SECRET_KEY
from payment_service.models import Payment


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
        return_borrowing_notification(borrowing)

        borrowing_days = (timezone.now() - borrowing.borrow).days

        borrowing_pay_amount = 0

        if borrowing_days > 0:
            daily_fee = borrowing.book_id.daily_fee
            borrowing_pay_amount = borrowing_days * daily_fee
        if borrowing_pay_amount == 0:
            return Response(
                {"detail": "Book has already been returned."}, status=status.HTTP_200_OK
            )
        else:
            stripe.api_key = STRIPE_SECRET_KEY

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(borrowing_pay_amount * 100),
                            "product_data": {
                                "name": "Borrowing Payment",
                                "description": "Payment for overdue borrowing",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="http://127.0.0.1:8000/api/payment_service/payments/success/",
                cancel_url="http://127.0.0.1:8000/api/payment_service/payments/cancel/",
            )

            payment = Payment.objects.create(
                status="PENDING",
                payment_type="PAYMENT",
                borrowing_id=borrowing.id,
                session_url=session.url,
                session_id=session.id,
                money_to_pay=borrowing_pay_amount,
                user=self.request.user,
            )

            payment.borrowing = borrowing
            payment.save()

            return Response(
                {"session_url": session.url},
                status=status.HTTP_200_OK,
            )

    def get_permissions(self):
        if self.action == "return_book":
            return []
        return super().get_permissions()
