import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


def get_book_id(category, page):
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
    book_ids = re.findall(r'\d{10}', str(items))
    return book_ids


def get_book_html(book_id):
    url = 'http://202.119.228.6:8080/opac/item.php'
    book_data = {
        'marc_no': str(book_id)
    }
    book_html = requests.get(url, headers=HEADERS, params=book_data)
    book_html.encoding = 'utf-8'
    return book_html


def get_book_attributions(book_id):
    book_soup = BeautifulSoup(get_book_html(book_id).text, 'lxml')
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
