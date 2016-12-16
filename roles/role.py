"""Role module"""


class Role(object):
    """Represents the roles of the users"""

    def __init__(self, role):
        self.role = role

    @property
    def role(self):
        """Role name"""
        return self._role

    @role.setter
    def role(self, value):
        if value in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
            self._role = value
        else:
            raise ValueError('"{}" is an invalid role!'.format(value))
