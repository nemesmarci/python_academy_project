"""Module for managing repositories"""
from repositories.repository import Repository


class RepositoryManager(object):
    """Manage repositories"""

    def __init__(self):
        self._repos = []

    def load_repos(self, path):
        with open(path) as repolist:
            for line in repolist:
                line = line.strip('\n')
                print line.split('/')[-1]
                self._repos.append(Repository(line.split('/')[-1], line))
