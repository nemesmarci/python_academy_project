import unittest
from docgen.generator import DocumentGenerator
import os


class TestGenerator(unittest.TestCase):
    """Test the DocumentGenerator class"""

    def test_generate_random_file(self):
        document_generator = DocumentGenerator()
        metadata = document_generator.generate_metadata('general')
        document_generator.generate_random_file('/tmp/{}'.format(metadata['filename']))
        self.assertTrue(metadata)
        self.assertTrue(metadata['filename'])
        self.assertTrue(metadata['title'])
        self.assertTrue(metadata['description'])
        self.assertTrue(os.path.exists('/tmp/{}'.format(metadata['filename'])))
        os.remove('/tmp/{}'.format(metadata['filename']))
