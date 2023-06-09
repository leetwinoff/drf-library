from datetime import timedelta, datetime

import stripe
from django.utils import timezone
from django.utils.datetime_safe import date
from rest_framework import serializers

from borrowings.models import Borrowing
from borrowings.telegram_helper import (
    send_borrowing_notification,
    return_borrowing_notification,
)
from drf_library.settings import STRIPE_SECRET_KEY
from payments.models import Payment


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )
        read_only_fields = (
            "id",
            "borrow",
            "expected_return_date",
            "actual_return_date",
            "user",
            "is_active",
        )

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user

        if book.inventory > 0:
            if Borrowing.objects.filter(
                user=user, book_id=book, actual_return_date=None
            ).exists():
                raise serializers.ValidationError("You have already borrowed this book")
            book.inventory -= 1
            book.save()

            borrowing = Borrowing.objects.create(
                borrow=date.today(),
                expected_return_date=datetime.now() + timedelta(days=7),
                book_id=book.id,
                user=user,
            )
            send_borrowing_notification(borrowing)

            return borrowing
        raise serializers.ValidationError("Book is out of stock")


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )
        read_only_fields = (
            "id",
            "borrow",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )

    def update(self, instance, validated_data):
        borrowing = instance

        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError("Book has already been returned.")

        borrowing.mark_as_returned()
        return_borrowing_notification(borrowing)

        borrowing_days = (timezone.now() - borrowing.borrow).days

        borrowing_pay_amount = 0

        if borrowing_days > 0:
            daily_fee = borrowing.book.daily_fee
            borrowing_pay_amount = borrowing_days * daily_fee

        if borrowing_pay_amount == 0:
            raise serializers.ValidationError("Book returned successfully")
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
                user=self.context["request"].user,
            )

            payment.borrowing = borrowing
            payment.save()

            return session.url
