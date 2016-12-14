import os
from storage_utils import storage_utils
from users.user import User
from datetime import datetime
from collections import defaultdict
from roles.role import Role
from roles.role_manager import RoleManager


class UserManager(object):
    """Manage user objects"""

    def __init__(self, storage_location):
        self._storage_location = storage_location
        if not os.path.exists(self._storage_location):
            os.makedirs(self._storage_location)
        self._role_manager = RoleManager(os.path.join(storage_location, 'roles.txt'))

    def save_user(self, user_id, user):
        """Save user to file"""
        with open('{}/{}'.format(self._storage_location, user_id), 'w') as user_file:
            user_file.write(user.first_name + '\n')
            user_file.write(user.family_name + '\n')
            user_file.write(datetime.strftime(user.birth, "%Y%m%d") + '\n')
            user_file.write(user.email + '\n')
            user_file.write(user.password + '\n')
            self._role_manager.write_roles(user_id, user.roles)

    def load_user(self, user_id):
        """Load user from file"""
        try:
            with open('{}/{}'.format(self._storage_location, user_id)) as user_file:
                first_name = user_file.readline().rstrip('\n')
                family_name = user_file.readline().rstrip('\n')
                birth = datetime.strptime(user_file.readline().rstrip('\n'), "%Y%m%d").date()
                email = user_file.readline().rstrip('\n')
                password = user_file.readline().rstrip('\n')
            user = User(first_name, family_name, birth, email, password)
            user.roles = (self._role_manager.read_roles())[user_id]
        except:
            raise ValueError("No such user")
        return user

    def add_user(self, user):
        """Add user to the repository"""
        user_id = storage_utils.get_next_id(self._storage_location)
        self.save_user(user_id, user)
        return user_id

    def update_user(self, user_id, user):
        """Modify user data"""
        self.remove_user(user_id)
        self.save_user(user_id, user)

    def remove_user(self, user_id):
        "Remove user from the repository"
        user_file_path = '{}/{}'.format(self._storage_location, user_id)
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))

    def find_user_by_id(self, user_id):
        """Return a user with a given id"""
        user_file_path = '{}/{}'.format(self._storage_location, user_id)
        if os.path.exists(user_file_path):
            user = self.load_user(user_id)
            return user
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))

    def find_users_by_name(self, name):
        """Return all users whose name contains the given string"""
        users = []
        for i in storage_utils.get_user_ids(self._storage_location):
            user = self.load_user(i)
            if name.upper() in user.first_name.upper() or name.upper() in user.family_name.upper():
                users.append(user)
        return users

    def find_users_by_email(self, email):
        """Return all users whose email address contains the given string"""
        users = []
        for i in storage_utils.get_user_ids(self._storage_location):
            user = self.load_user(i)
            if email.upper() in user.email.upper():
                users.append(user)
        return users

    def find_users_by_role(self, role):
        """Return all users with the given role"""
        if role not in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
            raise ValueError("Invalid role: {}".format(role))
        users = []
        user_roles = self._role_manager.read_roles()
        for user_id in user_roles:
            for user_role in user_roles[user_id]:
                if role == user_role._role:
                    user = self.load_user(user_id)
                    users.append(user)
        return users

    def count_users(self):
        """Return the count of the users"""
        ids = storage_utils.get_user_ids(self._storage_location)
        return len(ids) if ids else 0

    @staticmethod
    def check_role_file(role_file):
        """Check a role files syntax """
        with open(role_file) as rf:
            if not rf.readlines():
                return
        with open(role_file) as rf:
            user_roles = defaultdict(list)
            for line in rf:
                if ':' not in line:
                    raise ValueError("Invalid role file, missing colon in {}".format(line))
                line_parts = line.split(':')
                if len(line_parts) != 2:
                    raise ValueError("Invalid role file, multiple colons in {}".format(line))
                try:
                    user_id = int(line_parts[0])
                    roles = line_parts[1].lstrip(' ').rstrip('\n').split(',')
                    if user_id not in user_roles:
                        user_roles[user_id] = []
                    else:
                        raise ValueError("Invalid role file, duplicated user identifier: {} in {}".format(user_id, line))
                    for role in roles:
                        if not role:
                            raise ValueError("Invalid role file, too many commas in {}".format(line))
                        if role not in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
                            raise ValueError("Invalid role file, {} is not a valid role in {}".format(role, line))
                        if role not in user_roles[user_id]:
                            user_roles[user_id] += [role]
                        else:
                            raise ValueError("Invalid role file, duplicated role: {} in {}".format(role, line))
                except ValueError:
                    raise ValueError("Invalid role file.")

    def add_role(self, user_id, role):
        """Add a role to a user"""
        if role not in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
            raise ValueError("Invalid role: {}".format(role))
        user = self.load_user(user_id)
        if not self.has_role(user_id, role):
            user.roles += [Role(role)]
            self.update_user(user_id, user)

    def has_role(self, user_id, role):
        """Check if a user has a role"""
        if role not in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
            raise ValueError("Invalid role: {}".format(role))
        user = self.load_user(user_id)
        for user_role in user.roles:
            if role == user_role._role:
                return True
        return False

    def remove_role(self, user_id, role):
        if role not in ['admin', 'manager', 'author', 'reviewer', 'visitor']:
            raise ValueError("Invalid role: {}".format(role))
        user = self.load_user(user_id)
        new_roles = []
        for user_role in user.roles:
            if role == user_role._role:
                pass
            else:
                new_roles += role
        user.roles = new_roles
        self.update_user(user_id, user)
