from rest_framework import serializers

from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "is_active",
        )


class BorrowSerializer(serializers.Serializer):
    pass


class ReturnBookSerializer(serializers.Serializer):
    pass
