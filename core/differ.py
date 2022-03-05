from git import Actor
from pathlib import Path
import shutil
from typing import List

from core.cleaner import Cleaner
from core.git import RepoWrapper


class Differ(RepoWrapper, Cleaner):
    DIFF_PATH: Path

    def __init__(self, path: Path, author: Actor, committer: Actor, clean_rules: List[str]):
        RepoWrapper.__init__(self, path, author, committer)
        Cleaner.__init__(self, clean_rules)

        self.DIFF_PATH = path

    def diff(self, sources: List[str]):
        # Для каждой версии сорцов
        for source in sources:
            print(f'Work with {Path(source).name}')
            # Копируем новую версию сорцов
            shutil.copytree(Path(source), self.DIFF_PATH, dirs_exist_ok=True)
            # Очищаем от мусора
            self.clean(self.DIFF_PATH)
            # Коммитим в git
            self.commit()

        # Делаем checkout для записи последнего коммита (без этого он почему то не создается) и закрываем объект-репозиторий
        self.checkout()

    def test(self):
        # Проверка видимости расширяемых классов
        print(self.author)          # RepoWrapper
        print(self.committer)       # RepoWrapper
        print(self.CLEAN_RULES)     # Cleaner