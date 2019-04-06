# -*- coding: utf-8 -*-

import scrapy

from library_spider.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['202.119.228.6:8080']
    start_urls = ['http://202.119.228.6:8080/opac/item.php?marc_no=' + '%010d' % id
                  for id in range(1700, 10000000)]
    # start_urls = ['http://202.119.228.6:8080/opac/item.php?marc_no=0010805345']

    def parse(self, response):
        book_dict = {}

        book_item = BookItem()

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

        # print(book_dict)
        if book_dict == {}:
            return None
        else:
            bool_url = response.url
            book_id = bool_url.split('=')[1]
            book_item['id'] = book_id

            for key in book_dict:
                if key == '题名':
                    book_item['title'] = book_dict[key]
                elif key == '出版发行项':
                    book_item['publisher'] = book_dict[key]
                elif key == '个人责任者':
                    book_item['author'] = book_dict[key]
                elif key == '个人次要责任者':
                    book_item['sub_author'] = book_dict[key]
                elif key == 'ISBN':
                    book_item['isbn'] = book_dict[key]
                elif key == '定价':
                    book_item['price'] = book_dict[key]
                elif key == '载体形态项':
                    book_item['carrier'] = book_dict[key]
                elif key == '丛编项':
                    book_item['cluster_item'] = book_dict[key]
                elif key == '学科主题':
                    book_item['subject'] = book_dict[key]
                elif key == '中图法分类号':
                    book_item['category'] = book_dict[key]
                elif key == '题名责任附注':
                    book_item['author_notes'] = book_dict[key]
                elif key == '版本附注':
                    book_item['version_notes'] = book_dict[key]
                elif key == '出版发行附注':
                    book_item['publisher_notes'] = book_dict[key]
                elif key == '书目附注':
                    book_item['bibliographic_notes'] = book_dict[key]
                elif key == '提要文摘附注':
                    book_item['abstract'] = book_dict[key]
                elif key == '豆瓣简介':
                    book_item['douban_description'] = book_dict[key]

            return book_item
