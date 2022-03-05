from pathlib import Path
from typing import List


def GetFiles(path: Path) -> List[str]:
    """
    Возвращаем список файлов в директории, исключая .git-директории
    """
    items = path.glob('**/*')
    files = [str(item) for item in items 
             if item.is_file() and '/.git/' not in str(item)]

    return files


def ReadFile(path: Path) -> List[str]:
    """
    Считываем файл и возвращаем в виде списка строк
    """
    res = []

    with path.open(mode='r') as stream:
        line = stream.readline()
        while line:
            line = line.replace('\n', '')
            res.append(line)
            line = stream.readline()

    return res