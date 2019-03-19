# -*- coding: utf-8 -*-
import scrapy

from library_spider.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['202.119.228.6:8080']
    # start_urls = ['http://202.119.228.6:8080/opac/item.php?marc_no=' + '%10d' % id
    #               for id in range(1, 10000000)]
    start_urls = ['http://202.119.228.6:8080/opac/item.php?marc_no=0000802345']

    def parse(self, response):
        items = []

        for each in response.xpath('//dl[@class="booklist"]'):
            item = BookItem()
            key = each.xpath('dt/text()').extract()
            value = each.xpath('dd/a/text()').extract() + each.xpath('dd/text()').extract()
            print(key, value)
            # pass

