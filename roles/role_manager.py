from collections import defaultdict
from roles.role import  Role

class RoleManager(object):
    """Manage the user roles which are stored in a text file."""

    def __init__(self, storage_location):
        self._storage_location = storage_location

    def read_roles(self):
        """Read roles from the storage location."""
        with open(self._storage_location) as role_file:
            user_roles = defaultdict(list)
            for line in role_file:
                line = line.split(':')
                try:
                    user_id = int(line[0])
                    roles = line[1].lstrip(' ').rstrip('\n').split(',')
                    if roles:
                        for role in roles:
                            user_roles[user_id].append(Role(role))
                except ValueError:
                    pass
        return user_roles

    def write_roles(self, user_id, roles):
        """Write roles to the storage location."""
        user_roles = self.read_roles()
        user_roles[user_id] = roles
        with open(self._storage_location, 'w') as role_file:
            for user in user_roles:
                str_roles = []
                for role in user_roles[user]:
                    str_roles += [role._role]
                role_file.write("{}: {}\n".format(user, ",".join(str_roles)))
