"""Module for managing projects in the repository"""

import os
from storage_utils import storage_utils
from projects.project import Project


class ProjectManager(object):
    """Manage projects"""

    def __init__(self, storage_location, user_manager):
        self._storage_location = storage_location
        self._user_manager = user_manager

    def count_projects(self):
        """Return project count"""
        ids = storage_utils.get_proj_ids(self._storage_location)
        return len(ids) if ids else 0

    def save_project(self, project_id, project):
        """Save project with given id"""
        with open('{}/{}'.format(self._storage_location, project_id), 'w') as project_file:
            project_file.write(project.name + '\n')
            project_file.write(project.description + '\n')
            project_file.write(",".join(project.members) + '\n')
            project_file.write(",".join(project.documents) + '\n')

    def add_project(self, project):
        """Add project to the repository"""
        project_id = storage_utils.get_next_id(self._storage_location)
        self.save_project(project_id, project)
        return project_id

    def remove_project(self, project_id):
        """Remove project from the repository"""
        project_file_path = '{}/{}'.format(self._storage_location, project_id)
        if os.path.exists(project_file_path):
            os.remove(project_file_path)
        else:
            raise ValueError('The project id {} does not exist!'.format(project_id))

    def find_project_by_id(self, project_id):
        """Returns project with given id"""
        try:
            with open('{}/{}'.format(self._storage_location, project_id)) as project_file:
                name = project_file.readline().rstrip('\n')
                description = project_file.readline().rstrip('\n')
                members = project_file.readline().rstrip('\n').split(',')
                documents = project_file.readline().rstrip('\n').split(',')
                project = Project(name, description, members, documents)
        except:
            raise ValueError("No such project")
        return project

    def update_project(self, project_id, project):
        """Modify project data"""
        self.remove_project(project_id)
        self.save_project(project_id, project)

    def find_projects_by_name(self, name):
        """Return all projects which name contains the given string"""
        projects = []
        for i in storage_utils.get_proj_ids(self._storage_location):
            project = self.find_project_by_id(i)
            if name.upper() in project.name.upper():
                projects.append(project)
        return projects

    def has_required_roles(self, project):
        """Check if a project has the required members"""
        has_admin = False
        has_manager = False
        for user_id in project.members:
            user = self._user_manager.find_user_by_id(user_id)
            if 'admin' in user.roles:
                has_admin = True
            if 'manager' in user.roles:
                has_manager = True
            if has_admin and has_manager:
                return True
        return False
