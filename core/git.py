from pathlib import Path
from typing import Any
from git import Repo, Actor  # https://gitpython.readthedocs.io/en/stable/tutorial.html#examining-references
                             # https://www.programcreek.com/python/example/94623/git.Repo.init


class RepoWrapper(object):
    repo: Repo
    index: Any
    author: Actor
    committer: Actor

    current_version: int = 1
    last_commit = None

    def __init__(self, path: Path, author: Actor, committer: Actor):
        self.author = author
        self.committer = committer

        self.repo = Repo.init(path)
        self.index = self.repo.index
    
    def commit(self, message: str = ''):
        """
        Коммитим очередную версию сорцов и добавляем коммент с инкрементированной версией
        """
        message = f'Init v{self.current_version}' if not message else message
        self.current_version += 1

        self.index.add('*')
        commit_object = self.index.commit(
            message,
            author=self.author,
            committer=self.committer
        )

        self.last_commit = commit_object

        return self

    def checkout(self):
        """
        Без этого последний коммит не засчитается
        """
        self.repo.git.checkout(self.last_commit.hexsha)
        self.repo.close()