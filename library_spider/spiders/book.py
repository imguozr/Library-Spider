# -*- coding: utf-8 -*-

import logging

from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'book'
    redis_key = 'book:start_urls'
    allowed_domains = ['202.119.228.6:8080']

    def parse(self, response):
        book_dict = {}
        bool_url = response.url
        book_id = bool_url.split('=')[1]

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
                    isbn = value.split('/')[0]
                    try:
                        price = value.split('/')[1]
                        if price != '':
                            book_dict['定价'] = price
                    except IndexError:
                        logging.log(logging.INFO, '有第二个ISBN🤯')
                    if 'ISBN' in book_dict:
                        book_dict['ISBN'] = [book_dict.get('ISBN')] + [isbn]
                    else:
                        book_dict['ISBN'] = isbn
                else:
                    book_dict[key] = value

        if book_dict != {}:
            book_dict['id'] = book_id
            logging.log(logging.INFO, '当前爬取对象id: %s ✌️' % book_id)
        else:
            logging.log(logging.INFO, '没有和id: %s 对应的书😢' % book_id)
            return None

        return book_dict
