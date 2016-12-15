"""Repository

The repository is in a dedicated directory. This directory contains the following subdirectories by default:

    documents/        - document data and metadata files
    logs/             - logs of the repository events
    projects/         - project files
    users/            - user metadata files
    paths.ini         - the path of the main parts of the repository
    users/roles.txt   - user roles

The documents directory contains subdirectories which name is the document identifier.

For document metadata we save them to text files with the same name and .info extension next to the directories.

The paths.ini file contains the (relative or absolute) paths of mentioned subdirectories.

The roles.txt contains the user ids and the list of assigned roles.
"""

from datetime import datetime
import os
from iniformat.writer import write_ini_file
from iniformat.reader import read_ini_file
from documents.document_manager import DocumentManager
from documents.document import Document
from users.user_manager import UserManager


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
        role_file_path = '{}/roles.txt'.format(self._location)
        with open(role_file_path, 'w') as role_file:
            os.utime(role_file_path, None)
        self.create_default_path_file()
        self._doc_path = 'documents'
        self._logs_path = 'logs'
        self._projects_path = 'projects'
        self._users_path = 'users'
        self._creation_date = datetime.now()

    def create_default_path_file(self):
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
        if not os.path.exists(path):
            raise ValueError('Invalid path')
        for file_name in os.listdir(path):
            _, ext = os.path.splitext(file_name)
            if ext == '.edd':
                edd = read_ini_file(os.path.join(path, file_name))
                doc_dict = edd['document']
                author_first_name, author_family_name = doc_dict['author'].split()
                doc_files = [os.path.join(path, x) for x in doc_dict['files'].split()]
                author_id = self._user_manager.find_user_id_by_full_name(author_first_name, author_family_name)
                if author_id is not None:
                    document = Document(doc_dict['title'], doc_dict['description'],
                                        author_id, doc_files, doc_dict['type'])
                    self._document_manager.add_document(document)
                else:
                    raise ValueError("Author not in the repository")

    def export_documents(self, doc_ids, path):
        pass
