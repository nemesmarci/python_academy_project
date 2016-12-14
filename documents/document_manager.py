from documents.document import Document
from storage_utils import storage_utils
import os
import shutil


class DocumentManager(object):
    """Manage documents"""

    def __init__(self, _storage_location):
        self._storage_location = _storage_location
        if not os.path.exists(_storage_location):
            os.makedirs(_storage_location)

    def add_document(self, document):
        document_id = storage_utils.get_next_id(self._storage_location)
        document_id = str(document_id)
        doc_folder = os.path.join(self._storage_location, document_id)
        os.makedirs(doc_folder)
        for doc_file in document.files:
            shutil.copy(doc_file, doc_folder)
        new_files = []
        for file_name in os.listdir(doc_folder):
            new_files.append(file_name)
        document.files = new_files
        with open(os.path.join(self._storage_location, str(document_id)) + '.info', 'w') as info_file:
            info_file.write(document.title + '\n')
            info_file.write(document.description + '\n')
            info_file.write(document.author + '\n')
            info_file.write(','.join(document.files) + '\n')
            info_file.write(document.format + '\n')
            info_file.write(document.state + '\n')
            info_file.write(str(document.is_public()) + '\n')
        return document_id

    def update_document(self, document_id, document):
        pass

    def remove_document(self, document_id):
        pass

    def list_documents(self):
        pass

    def find_documents_by_name(self, name):
        pass

    def find_documents_by_author(self, author):
        pass

    def find_documents_by_format(self, format):
        pass
