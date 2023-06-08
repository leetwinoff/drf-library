from django.test import TestCase

from book_service.models import Book
from book_service.serializers import BookSerializer


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
