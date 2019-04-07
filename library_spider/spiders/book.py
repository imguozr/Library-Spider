# -*- coding: utf-8 -*-

import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['202.119.228.6:8080']
    start_urls = ['http://202.119.228.6:8080/opac/item.php?marc_no=' + '%010d' % id
                  for id in range(1, 10000000)]

    def parse(self, response):
        book_dict = {}

        for each in response.xpath('//dl[@class="booklist"]'):
            # 属性名
            try:
                text = each.xpath('dt/text()').extract()[0]
                if '豆瓣' not in text:
                    key = text.split(':')[0]
                else:
                    key = text.split('：')[0]
            except IndexError:
                continue
            # 属性值
            try:
                value = each.xpath('dd/a/text()').extract()[0] + each.xpath('dd/text()').extract()[0]
            except IndexError:
                value = each.xpath('dd/text()').extract_first() or each.xpath('dd/a/text()').extract_first()
            if not value:
                continue

            if key in book_dict:
                if isinstance(book_dict.get(key), list):
                    book_dict[key] = book_dict.get(key) + [value]
                else:
                    book_dict[key] = [book_dict.get(key)] + [value]
            else:
                if key == '题名/责任者':
                    book_dict['题名'] = value.split('/')[0]
                elif key == 'ISBN及定价':
                    book_dict['ISBN'] = value.split('/')[0]
                    book_dict['定价'] = value.split('/')[1]
                else:
                    book_dict[key] = value

            if book_dict != {}:
                bool_url = response.url
                book_id = bool_url.split('=')[1]
                book_dict['id'] = book_id
            else:
                return None

        return book_dict
