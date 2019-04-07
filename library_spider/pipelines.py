import pymongo

from library_spider import settings


class LibrarySpiderPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        self.db = self.client[settings.MONGODB_DB]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        book_item = dict(item)
        self.collection.update_one(book_item, {'$set': book_item}, upsert=True)
        return item
