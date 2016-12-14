import unittest
import os
from shutil import rmtree
from roles.role_manager import RoleManager
from roles.role import Role


class TestRoleManager(unittest.TestCase):
    """Test the review manager class"""

    def __init__(self, *args, **kwargs):
        super(TestRoleManager, self).__init__(*args, **kwargs)
        self.test_role_manager = RoleManager('/tmp/repo1/roles.txt')

    def test_read_roles(self):
        if not os.path.exists('/tmp/repo1'):
            os.makedirs('/tmp/repo1')
        with open(self.test_role_manager._storage_location, 'w') as role_file:
            role_file.write('0 admin,visitor\n')
            role_file.write('1: admin,visitor\n')
        roles = self.test_role_manager.read_roles()
        self.assertTrue(roles[1][0]._role == 'admin')
        self.assertTrue(roles[1][1]._role == 'visitor')
        self.assertFalse(roles[0])

    def test_write_roles(self):
        self.test_role_manager.write_roles(0, [Role('admin')])
        user_roles = self.test_role_manager.read_roles()
        self.assertEqual(user_roles[0][0]._role, 'admin')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/repo1/roles.txt'):
            rmtree('/tmp/repo1')
