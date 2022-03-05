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


def GetFileExtension(path: Path):
    filename = path.name
    parts = filename.split('.')
    
    if len(parts) == 1 \
        or len(parts) == 2 and parts[0] == '':
        # '.test' or 'test'
        file_ext = ''
    else:
        # a.b.test.txt
        file_ext = parts[-1]

    return file_ext


def GetStatisticFiles(path: Path):
    """
    Проходим по всем файлам и возращаем, какие есть расширения у этих файлов.
    Необходимо для определения, что есть вообще в репозитории
    """

    res = dict()

    for path in GetFiles(path):
        file_ext = GetFileExtension(Path(path))
        if file_ext not in res.keys():
            res[file_ext] = []

        res[file_ext].append(path)

    return res
