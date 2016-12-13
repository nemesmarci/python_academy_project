class Document(object):
    """Document of the repository"""

    accepted_formats = ['txt', 'html', 'pdf', 'odt', 'ods', 'odp', 'doc',
                        'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'bmp', 'gif',
                        'jpg', 'jpeg', 'png']

    def __init__(self, title, description, author, files, doc_format):
        self.title = title
        self.description = description
        self.author = author
        self.files = files
        self.doc_format = doc_format
        self.state = 'new'
        self._is_public = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value:
            self._title = value
        else:
            raise ValueError("Title must not be empty.")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in ['new', 'pending', 'accepted', 'rejected']:
            self._state = value
        else:
            raise ValueError('The "{}" is an invalid document state!'.format(value))

    @property
    def doc_format(self):
        return self._doc_format

    @doc_format.setter
    def doc_format(self, value):
        if value in Document.accepted_formats:
            self._doc_format = value
        else:
            raise ValueError("File format '{}' is not accepted.".format(value))

    def is_public(self):
        return self._is_public

    def make_public(self):
        self._is_public = True

    def make_private(self):
        self._is_public = False
