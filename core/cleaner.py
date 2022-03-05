from pathlib import Path
from typing import List

from core.file import GetFiles


DELETE = True

class Cleaner(object):
    CLEAN_RULES: List[str]

    def __init__(self, clean_rules: List[str]) -> None:
        self.CLEAN_RULES = clean_rules

    def check(self, rel_file_path: str):
        
        for rule in self.CLEAN_RULES:
            if rule in rel_file_path:
                return DELETE

        return not DELETE

    def clean(self, path: Path):
        PARENT_DIRECTORY = str(path)

        for abs_file_path in GetFiles(path):
            rel_file_path = abs_file_path.replace(PARENT_DIRECTORY, '')

            if DELETE == self.check(rel_file_path):
                Path(abs_file_path).unlink()
            