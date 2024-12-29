from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User(email="test@example.com")
        user.set_password("password123")
        user.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_create_user_without_email(self):
        user = User()
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_duplicate_email(self):
        user1 = User(email="test@example.com")
        user1.set_password("password123")
        user1.save()
        user2 = User(email="test@example.com")
        with self.assertRaises(ValidationError):
            user2.full_clean()
