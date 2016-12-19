import unittest
import os
from shutil import rmtree
from repositories.repository_manager import RepositoryManager


class TestRepositoryManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRepositoryManager, self).__init__(*args, **kwargs)
        self._repo_manager = RepositoryManager()

    def test_load_repos(self):
        os.makedirs('/tmp/repos')
        with open('/tmp/repos/repolist', 'w') as repo_list:
            repo_list.write('/tmp/repos/repo1\n')
            repo_list.write('/tmp/repos/repo2\n')
        self._repo_manager.load_repos('/tmp/repos/repolist')
        self.assertTrue(os.path.exists('/tmp/repos/repo1'))
        self.assertTrue(os.path.exists('/tmp/repos/repo2'))
        rmtree('/tmp/repos')

