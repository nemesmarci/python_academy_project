import unittest
import os
from repositories.repository import Repository
from shutil import rmtree
from users.user import User
from datetime import date
from documents.document import Document


class TestRepository(unittest.TestCase):
    """Test the repository class"""

    def test_init_repository(self):
        repository = Repository('repo1', '/tmp/repo1')
        self.assertTrue(os.path.exists('/tmp/repo1'))
        self.assertTrue(os.path.exists('/tmp/repo1/documents'))
        self.assertTrue(os.path.exists('/tmp/repo1/logs'))
        self.assertTrue(os.path.exists('/tmp/repo1/paths.ini'))
        self.assertTrue(os.path.exists('/tmp/repo1/projects'))
        self.assertTrue(os.path.exists('/tmp/repo1/users/roles.txt'))
        self.assertTrue(os.path.exists('/tmp/repo1/users'))
        rmtree('/tmp/repo1')

    def test_create_backup(self):
        repository = Repository('repo2', '/tmp/repo2')
        user = User('user1', 'test', date(1990,1,1), 'user1@test.org', 'secret')
        repository._user_manager.add_user(user)
        repository.create_backup('bak')
        self.assertTrue(os.path.exists(os.path.join(repository._location, 'backups', 'bak')))
        _, n_users, _ = repository.show_backup_info('bak')
        self.assertEqual(n_users, 1)
        rmtree('/tmp/repo2')

    def test_restore_repository(self):
        repository = Repository('repo3', '/tmp/repo3')
        user1 = User('user1', 'test', date(1990, 1, 1), 'user1@test.org', 'secret')
        repository._user_manager.add_user(user1)
        repository.create_backup('one_user')
        user2 = User('user2', 'test', date(1990, 1, 1), 'user2@test.org', 'secret')
        user3 = User('user3', 'test', date(1990, 1, 1), 'user3@test.org', 'secret')
        repository._user_manager.add_user(user2)
        repository._user_manager.add_user(user3)
        repository.create_backup('three_users')
        repository.restore_backup('one_user')
        self.assertEqual(repository._user_manager.count_users(), 1)
        repository.restore_backup('three_users')
        self.assertEqual(repository._user_manager.count_users(), 3)
        rmtree('/tmp/repo3')

    def test_show_backup_info(self):
        repository = Repository('repo4', '/tmp/repo4')
        user1 = User('user1', 'test', date(1990, 1, 1), 'user1@test.org', 'secret')
        document1 = Document('title', 'description', 0, ['/tmp/repo4/paths.ini'], 'txt')
        repository._user_manager.add_user(user1)
        repository._document_manager.add_document(document1)
        repository.create_backup('bak')
        _, n_users, n_documents = repository.show_backup_info('bak')
        self.assertEqual(n_users, 1)
        self.assertEqual(n_documents, 1)
        rmtree('/tmp/repo4')
