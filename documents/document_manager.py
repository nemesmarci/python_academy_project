"""Module for managing documents in the repository"""

import os
import shutil
from documents.document import Document
from storage_utils import storage_utils


class DocumentManager(object):
    """Manage documents"""

    def __init__(self, _storage_location):
        self._storage_location = _storage_location
        if not os.path.exists(_storage_location):
            os.makedirs(_storage_location)

    def add_document(self, document):
        """Adds document to the repository"""
        document_id = storage_utils.get_next_id(self._storage_location)
        doc_folder = self.doc_folder_path(document_id)
        os.makedirs(doc_folder)
        for doc_file in document.files:
            shutil.copy(doc_file, doc_folder)
        new_files = []
        for file_name in os.listdir(doc_folder):
            new_files.append(file_name)
        document.files = new_files
        with open(self.info_file_path(document_id), 'w') as info_file:
            info_file.write(document.title + '\n')
            info_file.write(document.description + '\n')
            info_file.write(str(document.author) + '\n')
            info_file.write(','.join(document.files) + '\n')
            info_file.write(document.doc_format + '\n')
            info_file.write(document.state + '\n')
            info_file.write(str(document.is_public()) + '\n')
        return document_id

    def update_document(self, document_id, document):
        """Updates a document"""
        if document_id in self.list_documents():
            self.remove_document(document_id)
            new_id = self.add_document(document)
            os.rename(self.info_file_path(new_id), self.info_file_path(document_id))
            os.rename(self.doc_folder_path(new_id), self.doc_folder_path(document_id))
        else:
            raise ValueError("Invalid document id")

    def remove_document(self, document_id):
        """Removes a document from the repository"""
        if document_id in self.list_documents():
            shutil.rmtree(self.doc_folder_path(document_id))
            os.remove(self.info_file_path(document_id))
        else:
            raise ValueError("Invalid document id")

    def list_documents(self):
        """Returns the list of document identifiers"""
        ids = storage_utils.get_doc_ids(self._storage_location)
        return ids if ids else []

    def info_file_path(self, document_id):
        """Returns the path of the document metadata file"""
        return os.path.join(self._storage_location, str(document_id) + '.info')

    def doc_folder_path(self, document_id):
        """Returns the path of the folder containing the documents files"""
        return os.path.join(self._storage_location, str(document_id))

    def find_document_by_id(self, document_id):
        """Returns a document with the given id"""
        if document_id in self.list_documents():
            with open(self.info_file_path(document_id)) as info_file:
                title = info_file.readline().rstrip('\n')
                description = info_file.readline().rstrip('\n')
                author = int(info_file.readline().rstrip('\n'))
                files = info_file.readline().rstrip('\n').split(',')
                doc_format = info_file.readline().rstrip('\n')
                state = info_file.readline().rstrip('\n')
                is_public = True if info_file.readline().rstrip('\n') == 'True' else False
            document = Document(title, description, author, files, doc_format)
            if is_public:
                document.make_public()
            document.change_state_directly(state)
            return document
        else:
            raise ValueError("Invalid document id")

    def find_documents_by_title(self, title):
        """Returns all documents that have a matching title"""
        documents = []
        for document_id in self.list_documents():
            document = self.find_document_by_id(document_id)
            if title.upper() in document.title.upper():
                documents.append(document)
        return documents

    def find_documents_by_author(self, author):
        """Returns all documents that have a matching author"""
        documents = []
        for document_id in self.list_documents():
            document = self.find_document_by_id(document_id)
            if author == document.author:
                documents.append(document)
        return documents

    def find_documents_by_format(self, doc_format):
        """Returns all documents that have a matching format"""
        documents = []
        for document_id in self.list_documents():
            document = self.find_document_by_id(document_id)
            if doc_format.upper() in document.doc_format.upper():
                documents.append(document)
        return documents

    def count_documents(self):
        """Counts the documents"""
        ids = storage_utils.get_doc_ids(self._storage_location)
        return len(ids) if ids else 0
