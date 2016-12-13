import unittest
from users.user import User
from datetime import date


class TestUser(unittest.TestCase):
    """Test the user class"""

    def test_create_user(self):
        first_name = "User1"
        family_name = "Test"
        birth = date(1990,1,1)
        email = "user1@test.org"
        test_user = User(first_name, family_name, birth, email, "secret")
        self.assertTrue(test_user)
        self.assertEqual(test_user.family_name, family_name)
        self.assertEqual(test_user.first_name, first_name)
        self.assertEqual(test_user.birth, birth)
        self.assertEqual(test_user.email, email)
        self.assertEqual(test_user.password, "secret")

    def test_create_user_wrong_email(self):
        self.assertRaises(ValueError, User, "User3", "Test", date(2016,12,12), "not_an.email@address", "secret")

    def test_create_user_wrong_birth_date(self):
        self.assertRaises(TypeError, User, "User3", "Test", "1", "user3@test.org", "secret")

    def test_create_user_empty_field(self):
        self.assertRaises(ValueError, User, "", "Test", date(2016,1,1), "unknown@test.org", "secret")

