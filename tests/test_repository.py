import unittest
from repositories.repository import Repository
import os
from shutil import rmtree


class TestRepository(unittest.TestCase):
    """Test the repository class"""

    def test_init_repository(self):
        repository = Repository('repo1', '/tmp/repo1')
        self.assertTrue(os.path.exists('/tmp/repo1'))
        self.assertTrue(os.path.exists('/tmp/repo1/documents'))
        self.assertTrue(os.path.exists('/tmp/repo1/logs'))
        self.assertTrue(os.path.exists('/tmp/repo1/paths.ini'))
        self.assertTrue(os.path.exists('/tmp/repo1/projects'))
        self.assertTrue(os.path.exists('/tmp/repo1/roles.txt'))
        self.assertTrue(os.path.exists('/tmp/repo1/users'))
        rmtree('/tmp/repo1')