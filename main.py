import argparse

from pathlib import Path
from git import Actor

from core.differ import Differ
from core.file import ReadFile, GetFiles, GetStatisticFiles


"""
Usage:

python main.py -i source.list -o out -r all

or 

python main.py -i out -o stats.txt -s

"""


def arg_parser():
    parser = argparse.ArgumentParser(description='Source differ')

    parser.add_argument('-i', '--input', help='List source paths (file path)', default='source.list', required=True)
    parser.add_argument('-o', '--output', help='Directory for the local git-repo', required=True)
    parser.add_argument('-r', '--rules', help='Cleaner\'s rules (ex see ./rules/: all,media,test,mock,...)', default='all', required=False)
    parser.add_argument('-s', help='Get file statistics', default=False, required=False, action='store_true')

    parser.add_argument('--author', help='Author for git-repo', default='cleaner@example.com', required=False)
    parser.add_argument('--committer', help='Committer for git-repo', default='cleaner@example.com', required=False)

    args = parser.parse_args()

    return args


def load_rules(path: Path):
    """
    Собираем в словарь правила для очистки коммитов из директории path
    """
    res = dict()

    rules = GetFiles(path)

    for rule in rules:
        rule_path = Path(rule)
        rule_name = rule_path.name.split('.')[0]  # remove '.rule'
        
        res[rule_name] = ReadFile(rule_path)

    return res


if __name__ == '__main__':
    args = arg_parser()

    assert Path(args.input).exists(), f'The file doesn\'t exist: {args.input}'

    if args.s:
        stats = GetStatisticFiles(Path(args.input))
        print(f'Extensions: {stats.keys()}')
        
        with Path(args.output).open(mode='w') as out_stream:
            out_stream.write(str(stats))
        
        exit(0)

    assert Path(args.output).exists(), f'The file doesn\'t exist: {args.output}'
 
    author = Actor(args.author.split('@')[0], args.author)
    committer = Actor(args.committer.split('@')[0], args.committer)

    # Считываем все пути до сорцов (один путь — одна версия)
    SOURCES = ReadFile(Path(args.input))
    assert SOURCES, 'Source path list is empty!'
    for src_path in SOURCES:
        assert Path(src_path).exists(), f'The file doesn\'t exist: {src_path}'

    # Загружаем все доступные правила (возвращается словарь {'название' -> 'набор правил'})
    RULES = load_rules(Path('rules'))

    # Выбираем только те правила, что нам нужны
    if args.rules == 'all':
        res = []
        for rule_name in RULES:
            res = res + RULES[rule_name]
            
        RULES = res
    elif args.rules in RULES:
        RULES = RULES[args.rules]
    else:
        RULES = []
        
    # Инициализируем объект для создания диффа
    differ = Differ(
        Path(args.output),
        author,
        committer,
        RULES
    )

    # Создаем дифф
    differ.diff(SOURCES)

    print('The diff successful created')
    exit(0)