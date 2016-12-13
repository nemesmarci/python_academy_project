import os
from storage_utils import storage_utils
from users.user import User
from datetime import datetime


class UserManager(object):
    """Manage user objects"""

    def __init__(self, storage_location):
        self._storage_location = storage_location

    def save_user(self, user_id, user):
        """Save user to file"""
        with open('{}/{}'.format(self._storage_location, user_id), 'w') as user_file:
            user_file.write(user.first_name + '\n')
            user_file.write(user.family_name + '\n')
            user_file.write(datetime.strftime(user.birth, "%Y%m%d") + '\n')
            user_file.write(user.email + '\n')
            user_file.write(user.password + '\n')

    def load_user(self, user_id):
        """Load user from file"""
        with open('{}/{}'.format(self._storage_location, user_id)) as user_file:
            first_name = user_file.readline().rstrip('\n')
            family_name = user_file.readline().rstrip('\n')
            birth = datetime.strptime(user_file.readline().rstrip('\n'), "%Y%m%d").date()
            email = user_file.readline().rstrip('\n')
            password = user_file.readline().rstrip('\n')
        user = User(first_name, family_name, birth, email, password)
        return user

    def add_user(self, user):
        user_id = storage_utils.get_next_id(self._storage_location)
        self.save_user(user_id, user)
        return user_id

    def update_user(self, user_id, user):
        self.remove_user(user_id)
        self.save_user(user_id, user)

    def remove_user(self, user_id):
        user_file_path = '{}/{}'.format(self._storage_location, user_id)
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))

    def find_user_by_id(self, user_id):
        user_file_path = '{}/{}'.format(self._storage_location, user_id)
        if os.path.exists(user_file_path):
            user = self.load_user(user_id)
            return user
        else:
            raise ValueError('The user id {} does not exist!'.format(user_id))

    def find_users_by_name(self, name):
        for i in storage_utils.get_user_ids(self._storage_location):
            user = self.load_user(i)
            if user.first_name == name[1] and user.family_name == name[0]:
                return user
        return None

    def find_users_by_email(self, email):
        for i in storage_utils.get_user_ids(self._storage_location):
            user = self.load_user(i)
            if user.email == email:
                return user
        return None

    def find_users_by_role(self, role):
        pass
