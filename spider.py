import requests
from bs4 import BeautifulSoup

url = 'http://202.119.228.6:8080/opac/item.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
data = {
    'marc_no': '0000784563'
}

html = requests.get(url, headers=headers, params=data)
html.encoding = 'utf-8'

soup = BeautifulSoup(html.text, 'lxml')


def get_book_attributions(bs=soup):
    items = bs.find_all(class_='booklist')
    attr_list = []
    attr_dict = {}
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


print(get_book_attributions())

