from user_services.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from datetime import date, timedelta
from book_service.models import Book
from borrowing_service.models import Borrowing
from book_service.serializers import BookSerializer
from borrowing_service.serializers import BorrowSerializer
from book_service.views import BookViewSet


class BookModelTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "covers": "SOFT",
            "inventory": 10,
            "daily_fee": 1.99,
        }

    def test_book_creation(self):
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.title, self.book_data["title"])
        self.assertEqual(book.author, self.book_data["author"])
        self.assertEqual(book.covers, self.book_data["covers"])
        self.assertEqual(book.inventory, self.book_data["inventory"])
        self.assertEqual(book.daily_fee, self.book_data["daily_fee"])


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            "id": 1,
            "title": "Test Book",
            "author": "Test Author",
            "covers": "SOFT",
            "inventory": 10,
            "daily_fee": 1.99,
        }
        self.serializer = BookSerializer(data=self.book_data)

    def test_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_serializer(self):
        invalid_data = {
            "id": 1,
            "title": "Test Book",
            "author": "Test Author",
            "covers": "HARD",
            "inventory": 0,
            "daily_fee": "invalid_fee",
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BookViewSet.as_view({"post": "borrow"})
        self.user = User.objects.create(username="testuser")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            covers="SOFT",
            inventory=1,
            daily_fee=1.99,
        )
        self.book_serializer = BookSerializer(self.book)
        self.borrow_serializer = BorrowSerializer(self.book)

    def test_borrow_book(self):
        request = self.factory.post("/books/1/borrow/")
        request.user = self.user
        response = self.view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"detail": "Book borrowed successfully"})

        self.book.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.book.inventory, 0)
        self.assertIn(self.book, self.user.borrowed_books.all())

        borrowing = Borrowing.objects.last()
        self.assertEqual(borrowing.book_id, self.book)
        self.assertEqual(borrowing.user_id, self.user)
        self.assertEqual(borrowing.borrow.date(), date.today())
        expected_return_date = date.today() + timedelta(days=7)
        self.assertEqual(borrowing.expected_return_date.date(), expected_return_date)

        self.book.inventory += 1
        self.book.save()

        # Attempt to borrow the book again (should fail)
        request = self.factory.post("/books/1/borrow/")
        request.user = self.user
        response = self.view(request, pk=1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, {"detail": "You have already borrowed this book"}
        )

    def test_book_out_of_stock(self):
        self.book.inventory -= 1
        self.book.save()

        request = self.factory.post("/books/1/borrow/")
        request.user = self.user
        response = self.view(request, pk=1)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"detail": "Book is out of stock"})
