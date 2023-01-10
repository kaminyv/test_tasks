"""
Скрипт подсчета событий за минуту по паттерну из файла событий
"""
from collections import defaultdict
from typing import List, Dict
from argparse import ArgumentParser
from sys import argv


def _parsed_arguments() -> ArgumentParser:
    """
    Создает аргументы для поиска в командной строке
    :return:
    """
    args_parse = ArgumentParser()
    args_parse.add_argument('-f', '--file',
                            type=str,
                            help='путь к файлу',
                            )
    args_parse.add_argument('-p', '--pattern',
                            type=str,
                            help='паттерн поиска',
                            )

    return args_parse


def _read_file(file_name: str) -> List[str] | None:
    """
    Считываем данные из файла.
    :param file_name: Путь к файлу событий
    :type file_name: str
    :return: Список строк из файла
    """
    file_data = []
    try:
        with open(file_name, 'r') as file:
            file_data = file.readlines()
    except FileNotFoundError as error:
        print(error)

    return file_data


def _count_event(data_file: List[str], pattern: str) -> Dict:
    """
    Считает количество событий по паттерну.
    :param data_file: Данные из файла
    :param pattern: Паттерн для поиска событий. Пример 'NOK'
    :return: Словарь для каждой минуты с количеством событий
    """
    count_event = defaultdict(int)

    for line in data_file:
        if pattern in line:
            count_event[line[1:17]] += 1

    return count_event


def main(file_name: str = 'events.log', pattern: str = 'NOK') -> None:
    """
    Обрабатывает словарь событий
    :param file_name: Путь к файлу событий
    :type file_name: str
    :param pattern: Паттерн для поиска событий. Пример 'NOK'
    :type pattern: str
    :return: Вывод в стандартный поток данных о событиях
    """
    data_file = _read_file(file_name)
    events = _count_event(data_file, pattern)
    for data, count in events.items():
        print(f'[{data}] {pattern} {count}')


if __name__ == '__main__':
    # Получаем аргументы для командной строки
    parsed = _parsed_arguments()

    # Получаем аргументы из командной строки
    argument = parsed.parse_args(argv[1:])

    # Проверяем наличие обязательных аргументов
    if not (argument.file and argument.pattern):
        parsed.error('Параметры -f и -p являются обязательными.')

    main(argument.file, argument.pattern)
