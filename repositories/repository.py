"""Repository

The repository is in a dedicated directory.
This directory contains the following subdirectories by default:

    documents/        - document data and metadata files
    logs/             - logs of the repository events
    projects/         - project files
    users/            - user metadata files
    paths.ini         - the path of the main parts of the repository
    users/roles.txt   - user roles

The documents directory contains subdirectories which name is the document identifier.

For document metadata we save them to text files with the same name
and .info extension next to the directories.

The paths.ini file contains the (relative or absolute) paths of mentioned subdirectories.

The roles.txt contains the user ids and the list of assigned roles.
"""

import os
import shutil
from datetime import datetime
from iniformat.writer import write_ini_file
from iniformat.reader import read_ini_file
from documents.document_manager import DocumentManager
from documents.document import Document
from users.user_manager import UserManager
from reports.report import Report


class Repository(object):
    """Represents the document management system as a repository"""

    def __init__(self, name, location):
        self._name = name
        self._location = location
        self.load()
        self._document_manager = DocumentManager(os.path.join(self._location, self._doc_path))
        self._user_manager = UserManager(os.path.join(self._location, self._users_path))

    def load(self):
        """Try to load an existing repository"""
        if os.path.exists(self._location):
            if os.path.isdir(self._location):
                ini_content = read_ini_file('{}/paths.ini'.format(self._location))
                self._doc_path = ini_content['directories']['documents']
                self._logs_path = ini_content['directories']['logs']
                self._projects_path = ini_content['directories']['projects']
                self._users_path = ini_content['directories']['users']
            else:
                raise ValueError('The repository should be a directory!')
        else:
            self.initialize()

    def initialize(self):
        """Initialize a new repository"""
        os.makedirs(self._location)
        for dir_name in ['documents', 'logs', 'projects', 'users']:
            os.makedirs('{}/{}'.format(self._location, dir_name))
        role_file_path = '{}/users/roles.txt'.format(self._location)
        with open(role_file_path, 'w'):
            os.utime(role_file_path, None)
        self.create_default_path_file()
        self._doc_path = 'documents'
        self._logs_path = 'logs'
        self._projects_path = 'projects'
        self._users_path = 'users'
        self._creation_date = datetime.now()

    def create_default_path_file(self):
        """Creates an ini file with the default path settings"""
        data = {
            'directories': {
                'documents': 'documents',
                'logs': 'logs',
                'projects': 'projects',
                'users': 'users'
            }
        }
        write_ini_file('{}/paths.ini'.format(self._location), data)

    def import_documents(self, path):
        """Import documents from the given directory"""
        if not os.path.exists(path):
            raise ValueError('Invalid path')
        for file_name in os.listdir(path):
            _, ext = os.path.splitext(file_name)
            if ext == '.edd':
                edd = read_ini_file(os.path.join(path, file_name))
                doc_dict = edd['document']
                author_first_name, author_family_name = doc_dict['author'].split()
                doc_files = [os.path.join(path, x) for x in doc_dict['files'].split()]
                author_id = self._user_manager.find_user_id_by_full_name(
                    author_first_name, author_family_name)
                if author_id is not None:
                    document = Document(doc_dict['title'], doc_dict['description'],
                                        author_id, doc_files, doc_dict['type'])
                    self._document_manager.add_document(document)
                else:
                    raise ValueError("Author not in the repository")

    def export_documents(self, doc_ids, path):
        """Exports documents to the given directory"""
        docs_to_export = []
        try:
            for i in doc_ids:
                document = self._document_manager.find_document_by_id(i)
                if document.state != 'accepted' or not document.is_public():
                    raise ValueError("Document cannot be exported")
                else:
                    docs_to_export.append([i, document])
        except ValueError:
            raise ValueError("Error during export, cancelling process")
        if not os.path.exists(path):
            os.makedirs(path)
        for i, document in docs_to_export:
            for file_name in document.files:
                shutil.copy(os.path.join(
                    self._document_manager.doc_folder_path(i), file_name), path)
            author = self._user_manager.find_user_by_id(document.author)
            doc_dict = {}
            doc_dict['title'] = document.title
            doc_dict['description'] = document.description
            doc_dict['author'] = ' '.join([author.first_name, author.family_name])
            doc_dict['files'] = ' '.join(document.files)
            doc_dict['type'] = document.doc_format
            edd = {'document': doc_dict}
            write_ini_file(os.path.join(path, '{}.edd'.format(i)), edd)

    def create_backup(self, backup_name):
        """Creates a backup of the repository"""
        backup_path = os.path.join(self._location, 'backups', backup_name)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        else:
            raise ValueError("Backup name is already in use")
        paths_file_location = os.path.join(self._location, 'paths.ini')
        paths = read_ini_file(paths_file_location)
        for directory in paths['directories'].values():
            src = os.path.join(self._location, directory)
            dst = os.path.join(backup_path, directory)
            shutil.copytree(src, dst)
        with open(os.path.join(backup_path, 'backup.info'), 'w') as backup_info:
            backup_info.write('{}\n'.format(datetime.now()))
            n_users = self._user_manager.count_users()
            backup_info.write('{}\n'.format(n_users))
            n_documents = self._document_manager.count_documents()
            backup_info.write('{}\n'.format(n_documents))

    def restore_backup(self, backup_name):
        """Restores repository from backup"""
        backup_path = os.path.join(self._location, 'backups', backup_name)
        if not os.path.exists(backup_path):
            raise ValueError("Backup '{}' does not exists".format(backup_name))
        paths_file_location = os.path.join(self._location, 'paths.ini')
        paths = read_ini_file(paths_file_location)
        for directory in paths['directories'].values():
            shutil.rmtree(os.path.join(self._location, directory))
        os.remove(paths_file_location)
        self.create_default_path_file()
        paths = read_ini_file(paths_file_location)
        for directory in paths['directories'].values():
            src = os.path.join(backup_path, directory)
            dst = os.path.join(self._location, directory)
            shutil.copytree(src, dst)

    def show_backup_info(self, backup_name):
        backup_path = os.path.join(self._location, 'backups', backup_name)
        if not os.path.exists(backup_path):
            raise ValueError("Backup '{}' does not exists".format(backup_name))
        with open(os.path.join(backup_path, 'backup.info')) as backup_info:
            creation_date = backup_info.readline().strip('\n')
            n_users = int(backup_info.readline().strip('\n'))
            n_documents = int(backup_info.readline().strip('\n'))
            return creation_date, n_users, n_documents

    def create_report(self):
        report = Report()
        report.user_count = self._user_manager.count_users()
        report.document_count = self._document_manager.count_documents()
        roles = ['admin', 'manager', 'author', 'reviewer', 'visitor']
        users_by_role = {}
        for role in roles:
            users_by_role[role] = len(self._user_manager.find_users_by_role(role))
        report.user_count_by_roles = users_by_role
        return report
