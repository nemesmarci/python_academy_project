"""Document module"""


class Document(object):
    """Represents a document in the repository"""

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
        """Document title"""
        return self._title

    @title.setter
    def title(self, value):
        if value:
            self._title = value
        else:
            raise ValueError("Title must not be empty.")

    @property
    def description(self):
        """Document description"""
        return self._description

    @description.setter
    def description(self, value):
        if value:
            self._description = value
        else:
            raise ValueError("Description must not be empty.")

    @property
    def author(self):
        """Id of documents author"""
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, int):
            self._author = value
        else:
            raise ValueError("Author must be a user id.")

    @property
    def files(self):
        """Files of the document"""
        return self._files

    @files.setter
    def files(self, value):
        if value:
            self._files = value
        else:
            raise ValueError("Files list must not be empty.")

    @property
    def state(self):
        """State of the document"""
        return self._state

    @state.setter
    def state(self, value):
        if value in ['new', 'pending', 'accepted', 'rejected']:
            self._state = value
        else:
            raise ValueError('The "{}" is an invalid document state!'.format(value))

    @property
    def doc_format(self):
        """Format of the document"""
        return self._doc_format

    @doc_format.setter
    def doc_format(self, value):
        if value in Document.accepted_formats:
            self._doc_format = value
        else:
            raise ValueError("File format '{}' is not accepted.".format(value))

    def is_public(self):
        """Returns if the document is public"""
        return self._is_public

    def make_public(self):
        """Makes the document public"""
        self._is_public = True

    def make_private(self):
        """Makes the document private"""
        self._is_public = False

    def change_state(self, new_state):
        """Changes the state of the document"""
        possible_states = {'new':['pending'], 'pending':['accepted', 'rejected'],
                           'accepted':[], 'rejected':[]}
        curr_state = self.state
        if new_state in possible_states[curr_state]:
            self.state = new_state
        else:
            raise ValueError("Invalid status change.")

    def change_state_directly(self, new_state):
        """Changes the state if the document regardless of the precvious state, used for loading"""
        if new_state in ['new', 'pending', 'accepted', 'rejected']:
            self.state = new_state
        else:
            raise ValueError("Invalid status")
