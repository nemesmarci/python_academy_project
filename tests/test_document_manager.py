import unittest
from documents.document_manager import DocumentManager
from documents.document import Document
from docgen.generator import DocumentGenerator


class TestDocumentManager(unittest.TestCase):
    """Test the document manager class"""
    def __init__(self, *args, **kwargs):
        super(TestDocumentManager, self).__init__(*args, **kwargs)
        self.test_document_manager = DocumentManager('/tmp/docs')

    def test_add_doc(self):
        document_generator = DocumentGenerator()
        document_generator.generate_random_file('/tmp/random1')
        document_generator.generate_random_file('/tmp/random2')
        document = Document('Title', 'Description', 'Author', ['/tmp/random1', '/tmp/random2'], 'txt')
        self.test_document_manager.add_document(document)
