import re
from functools import partial
from multiprocessing import Pool
from time import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


def get_category_page(category):
    url = 'http://202.119.228.6:8080/browse/cls_browsing_book.php'
    data = {
        's_doctype': 'all',
        'cls': category
    }

    html = requests.get(url, headers=HEADERS, params=data)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    try:
        text = str(soup.select('.numstyle font[color=black]'))
        return int(re.search(r'\d+', text).group())
    except AttributeError:
        return 1


def get_book_ids(category, page):
    print(page)
    url = 'http://202.119.228.6:8080/browse/cls_browsing_book.php'
    data = {
        's_doctype': 'all',
        'cls': category,
        'page': page
    }

    html = requests.get(url, headers=HEADERS, params=data)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')

    items = soup.select('.list_books span')
    return re.findall(r'\d{10}', str(items))


def get_all_books(category):
    book_ids = []
    page = get_category_page(category)
    for i in range(page):
        print(i + 1)
        book_ids += get_book_ids(category, i + 1)
    return book_ids


def get_book_html(book_id):
    url = 'http://202.119.228.6:8080/opac/item.php'
    book_data = {
        'marc_no': str(book_id)
    }
    book_html = requests.get(url, headers=HEADERS, params=book_data)
    book_html.encoding = 'utf-8'
    return book_html.text


def get_book_attributions(book_id):
    book_soup = BeautifulSoup(get_book_html(book_id), 'lxml')
    items = book_soup.find_all(class_='booklist')
    attr_list = []
    attr_dict = {'id': book_id}
    for item in items:
        text = item.get_text()
        if text == '':
            continue
        if text[0] == '\n':
            attr_list.append(text[1:-1].split('\n'))
        else:
            attr = text.split('\n')
            attr.append('')
            attr_list.append(attr)
    for attr in attr_list:
        attr_dict[attr[0]] = attr[1]
    return attr_dict


def get_book_ids_in_category(cate):
    pool = Pool(64)
    page = get_category_page(cate)
    get = partial(get_book_ids, cate)
    raw_data = pool.map(get, range(1, page + 1))
    pool.close()
    pool.join()

    result = []
    for item in raw_data:
        if isinstance(item, list):
            for i in item:
                result.append(i)
        else:
            result.append(item)
    print(result)
    return result


def get_latest_book_ids(day=3, category='ALL', type='ALL', location='ALL'):

    url = 'http://202.119.228.6:8080/newbook/newbook_cls_book.php'
    # 总馆00 密集书库 01
    data = {
        'back_days': str(day),
        's_doctype': type,
        'cls': category,
        'loca_code': location
    }

    html = requests.get(url=url, headers=HEADERS, params=data)
    soup = BeautifulSoup(html.text, 'lxml')

    items = soup.select('.list_books span')
    return re.findall(r'\d{10}', str(items))


if __name__ == '__main__':
    ts = time()
    # start_pool()
    # get_book_ids_in_category('B8')
    print(get_latest_book_ids())
    print(time() - ts)
