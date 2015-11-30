# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubancrawlItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()          #名称
    cover = scrapy.Field()         #封面
    author = scrapy.Field()        #作者
    publishing_house = scrapy.Field()    #出版社
    original_name = scrapy.Field() #原作名
    translator = scrapy.Field()    #译者
    publishing_year = scrapy.Field() #出版年
    page_num = scrapy.Field() #页数
    price = scrapy.Field() #定价
    binding = scrapy.Field() #装帧
    series = scrapy.Field() #丛书
    ISBN = scrapy.Field() #ISBN
    tags = scrapy.Field() #标签
    content_intro = scrapy.Field() #简介
    author_intro = scrapy.Field() #作者简介
    score = scrapy.Field() #评分
    comment_num = scrapy.Field() #评价人数
    pass
