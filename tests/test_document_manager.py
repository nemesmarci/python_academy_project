import unittest
from documents.document_manager import DocumentManager
from documents.document import Document
from docgen.generator import DocumentGenerator
import os
from shutil import rmtree
from storage_utils import storage_utils


class TestDocumentManager(unittest.TestCase):
    """Test the document manager class"""
    def __init__(self, *args, **kwargs):
        super(TestDocumentManager, self).__init__(*args, **kwargs)
        self.test_document_manager = DocumentManager('/tmp/docs')

    def test_add_doc(self):
        document_generator = DocumentGenerator()
        document_generator.generate_random_file('/tmp/random1')
        document_generator.generate_random_file('/tmp/random2')
        document = Document('Title', 'Description', 0, ['/tmp/random1', '/tmp/random2'], 'txt')
        self.test_document_manager.add_document(document)
        os.remove('/tmp/random1')
        os.remove('/tmp/random2')
        self.assertTrue(os.path.exists('/tmp/docs/0'))

    def test_remove_doc(self):
        self.test_document_manager.remove_document(0)
        self.assertFalse(storage_utils.get_user_ids('/tmp/docs'))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/docs'):
            rmtree('/tmp/docs')
