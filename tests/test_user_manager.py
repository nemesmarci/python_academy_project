import unittest
from users.user_manager import UserManager
from users.user import User
from datetime import date
import os
from shutil import rmtree


class TestUserManager(unittest.TestCase):
    """Test the user manager class"""

    def __init__(self, *args, **kwargs):
        super(TestUserManager, self).__init__(*args, **kwargs)
        self.test_user_manager = UserManager('/tmp/users')

    def test1_save_user(self):
        if not os.path.exists('/tmp/users'):
            os.makedirs('/tmp/users')
        test_user = User("User1", "Test", date(2016, 12, 12), "user1@test.org", "secret")
        self.test_user_manager.save_user(1, test_user)
        self.assertTrue(os.path.exists('/tmp/users/1'))
        with open('/tmp/users/1') as f:
            lines = f.readlines()
            self.assertEqual('User1\n', lines[0])
            self.assertEqual('Test\n', lines[1])
            self.assertEqual("20161212"+'\n', lines[2])
            self.assertEqual('user1@test.org\n', lines[3])
            self.assertEqual('secret\n', lines[4])

    def test2_add_user(self):
        test_user = User("User2", "Test", date(1990, 1, 1), "user2@test.org", "secret")
        self.test_user_manager.add_user(test_user)
        self.assertTrue(os.path.exists('/tmp/users/2'))

    def test3_load_user(self):
        user = self.test_user_manager.load_user(1)
        self.assertEqual('User1', user.first_name)
        self.assertEqual('Test', user.family_name)
        self.assertEqual("2016-12-12", str(user.birth))
        self.assertEqual('user1@test.org', user.email)
        self.assertEqual('secret', user.password)

    def test4_update_user(self):
        test_user = User("User3", "Test", date(1993, 1, 1), "user3@test.org", "secret")
        self.test_user_manager.update_user(2, test_user)
        test_user2 = self.test_user_manager.load_user(2)
        self.assertEqual(test_user2.first_name, test_user.first_name)
        self.assertEqual(test_user2.family_name, test_user.family_name)
        self.assertEqual(test_user2.birth, test_user.birth)
        self.assertEqual(test_user2.email, test_user.email)
        self.assertEqual(test_user2.password, test_user.password)

    def test5_remove_user(self):
        self.test_user_manager.remove_user(2)
        self.assertFalse(os.path.exists('/tmp/users/2'))

    def test6_find_user(self):
        test_user2 = User("User2", "Test", date(1990, 1, 1), "user2@test.org", "secret")
        test_user3 = User("User3", "Test", date(1990, 1, 1), "user3@test.org", "secret")
        test_user4 = User("User4", "Test", date(1990, 1, 1), "user4@test.org", "secret")
        self.test_user_manager.add_user(test_user2)
        self.test_user_manager.add_user(test_user3)
        self.test_user_manager.add_user(test_user4)
        user = self.test_user_manager.find_user_by_id(3)
        self.assertTrue(user.first_name == "User3")
        user = self.test_user_manager.find_users_by_email('user4@test.org')
        self.assertTrue(user.first_name == "User4")
        user = self.test_user_manager.find_users_by_name(["Test","User2"])
        self.assertTrue(user.email == "user2@test.org")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/users'):
            rmtree('/tmp/users')
