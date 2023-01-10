from datetime import datetime
from requests import get
from time import sleep
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Iterator

DOMAINS = [
    'maria.ru',
    'rose.ru',
    'sina.ru',
]


def fetch_url_data(domain: str) -> Dict:
    """
    Получение данных из домена
    :param domain: доменное имя
    :return: словарь данных для домена
    """
    try:
        resp = get(f'http://{domain}', timeout=60)
        data = resp.json()
    except Exception as error:
        return {'url': domain, 'error': error}
    return {'url': domain, 'data': data['count']}


def get_all_url_data(domains: List[str]) -> Iterator[dict]:
    """
    Асинхронное выполнение запросов для списка доменов
    :param domains: список доменов
    :return: Итератор словарей для доменов
    """
    with ProcessPoolExecutor() as executor:
        response = executor.map(fetch_url_data, domains)
    return response


def main(domains: List[str]) -> None:
    """
    Выводит данные запросов в стандартный поток данных
    :param domains: список доменов
    :return:
    """
    responses = get_all_url_data(domains)
    str_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for item in responses:
        if item.get('error'):
            print(f"{str_datetime} {item.get('url')} {item.get('error')}")
        else:
            print(f"{str_datetime} {item.get('url')} {item.get('count')}")


if __name__ == '__main__':
    while True:
        main(DOMAINS)
        # Интервал между запросами.
        sleep(60)
