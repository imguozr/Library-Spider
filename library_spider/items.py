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
    sub_author = scrapy.Field()  # 个人次要责任者
    carrier = scrapy.Field()  # 载体形态项
    publisher = scrapy.Field()
    isbn = scrapy.Field()
    price = scrapy.Field()
    cluster_item = scrapy.Field()  # 丛编项
    subject = scrapy.Field()  # 学科主题
    category = scrapy.Field()  # 中图法分类号
    author_notes = scrapy.Field()  # 题名责任附注
    publisher_notes = scrapy.Field()  # 出版发行附注
    version_notes = scrapy.Field()  # 版本附注
    bibliographic_notes = scrapy.Field()  # 书目附注
    abstract = scrapy.Field()  # 提要文摘附注
    douban_description = scrapy.Field()  # 豆瓣简介
    other = scrapy.Field()
