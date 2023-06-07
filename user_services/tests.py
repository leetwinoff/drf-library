from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.serializers import ValidationError
from user_services.serializers import UserSerializer

User = get_user_model()


class UserSerializerTestCase(TestCase):
    def test_create_regular_user(self):
        user_data = {
            "username": "username",
            "email": "username@test.com",
            "password": "password123",
            "is_staff": False,
            "borrowed_books": [],
        }

        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(user.username, "username")
        self.assertEqual(user.email, "username@test.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertEqual(user.borrowed_books.count(), 0)

    def test_create_regular_user_with_invalid_data(self):
        user_data = {
            "username": "username",
            "email": "username@test.com",
            "password": "pass",
            "is_staff": False,
            "borrowed_books": [],
        }

        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
