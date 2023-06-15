from django.test import TestCase
from django.utils import timezone

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer
from users.models import User


class BorrowingTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", inventory=5, daily_fee=1.50)
        self.user = User.objects.create(username="testuser")

    def test_borrowing_create(self):
        borrowing = Borrowing.objects.create(book_id=self.book, user_id=self.user)

        self.assertIsNone(borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 5)
        self.assertEqual(self.book.daily_fee, 1.50)


class BorrowingSerializerTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", inventory=5, daily_fee=1.99)
        self.user = User.objects.create(username="testuser")
        self.borrowing_data = {
            "borrow": timezone.now(),
            "expected_return_date": timezone.now() + timezone.timedelta(weeks=1),
            "actual_return_date": None,
            "book_id": self.book.id,
            "user_id": self.user.id,
            "is_active": True,
        }

    def test_borrowing_serializer(self):
        serializer = BorrowingSerializer(data=self.borrowing_data)
        self.assertTrue(serializer.is_valid())

        borrowing = serializer.save()

        self.assertIsNone(borrowing.actual_return_date)
        self.assertEqual(borrowing.book_id, self.book)
        self.assertEqual(borrowing.user_id, self.user)
        self.assertTrue(borrowing.is_active)
