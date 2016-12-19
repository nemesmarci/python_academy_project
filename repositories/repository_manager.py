"""Module for managing repositories"""
import os
from repositories.repository import Repository


class RepositoryManager(object):
    """Manage repositories"""

    def __init__(self):
        self._repos = {}

    def load_repos(self, path):
        with open(os.path.join(path, 'repolist')) as repolist:
            for line in repolist:
                line = line.strip('\n')
                repo_name = line.split('/')[-1]
                repo_path = os.path.join(path, repo_name)
                self._repos[repo_name] = Repository(repo_name, repo_path)
        return self._repos.keys()
