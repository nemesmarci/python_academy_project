"""Project module"""


class Project(object):
    """Represents a project in the repository"""

    def __init__(self, name, description, members=None, documents=None):
        self.name = name
        self.description = description
        self.members = members
        self.documents = documents

    @property
    def name(self):
        """Name of the project"""
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = value
        else:
            raise ValueError("Project name cannot be empty")

    @property
    def description(self):
        """Description of the project"""
        return self._description

    @description.setter
    def description(self, value):
        if value:
            self._description = value
        else:
            raise ValueError("Project description cannot be empty")

    @property
    def members(self):
        """Members of the project"""
        return self._members

    @members.setter
    def members(self, value):
        if isinstance(value, list):
            self._members = value
        else:
            raise ValueError("Project members must be a list")

    @property
    def documents(self):
        """Documents in the project"""
        return self._documents

    @documents.setter
    def documents(self, value):
        if isinstance(value, list):
            self._documents = value
        else:
            raise ValueError("Project documents must be a list")
