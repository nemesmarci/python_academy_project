import unittest
from docgen.generator import DocumentGenerator
from os import remove


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
        with open('/tmp/{}'.format(metadata['filename'])) as f:
            self.assertTrue(f)
        remove('/tmp/{}'.format(metadata['filename']))
