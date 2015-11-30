# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class DoubancrawlPipeline(object):

    collection_name = 'books'

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db  = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db  = crawler.settings.get('MONGO_DATABASE','douban')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)

        self.db = self.client[self.mongo_db]
        self.db.authenticate('hackingwu','wu123456')

    def close_spider(self,spider):
        self.client.close()


    def process_item(self, item, spider):
        item = dict(item)
        item_findby_isbn_num = self.db[self.collection_name].count({"name":item.get('name')})
        if item_findby_isbn_num ==  0:
            self.db[self.collection_name].insert(dict(item))
        return item
