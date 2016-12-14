import unittest
from roles.role import Role


class TestUserRoles(unittest.TestCase):
    """Test the user role functions"""
    def test_valid_role(self):
        test_role = Role('admin')
        self.assertTrue(test_role._role == 'admin')

    def test_invalid_role(self):
        self.assertRaises(ValueError, Role, 'auditor')