import logging

import pymongo
import pymongo.errors

from library_spider import settings


class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        self.db = self.client[settings.MONGODB_DB]
        self.collection = self.db[settings.MONGODB_COLLECTION]
        # self.collection.create_index([('id', pymongo.ASCENDING)], unique=True)

    def process_item(self, item, spider):
        book_item = dict(item)
        try:
            if self.collection.find_one({'id': book_item['id']}):
                logging.log(logging.INFO, '该书已存在👌')
            else:
                try:
                    self.collection.update_one(
                        book_item, {'$set': book_item}, upsert=True)
                    logging.log(logging.INFO, '添加到Mongo中了😃')
                except pymongo.errors.WriteError:
                    logging.log(logging.INFO, '该书不存在😢')
        except KeyError:
            logging.log(logging.INFO, '该书不存在😢')
        return item
