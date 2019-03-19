# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    isbn = scrapy.Field()
    price = scrapy.Field()
    cluster_item = scrapy.Field()  # 丛编项
    subject = scrapy.Field()
    category = scrapy.Field()
    author_notes = scrapy.Field()  # 题名责任附注
    version_notes = scrapy.Field()  # 版本附注
    Bibliographic_notes = scrapy.Field()  # 书目附注
    abstract = scrapy.Field()  # 提要文摘附注
    douban_description = scrapy.Field()  # 豆瓣简介

