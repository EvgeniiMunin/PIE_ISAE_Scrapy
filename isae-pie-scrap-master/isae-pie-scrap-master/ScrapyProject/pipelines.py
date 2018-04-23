
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo

import random

# Imports for Postgres
from sqlalchemy.orm import sessionmaker
from ScrapyProject.models import NewsArticles, db_connect, create_table

class PostgresPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()

        #insert a random Tag
        item['tag'] = random.choice([
            'plasma', 'plasma',
            'SSTO',
            'liquid',
            'solid', 'solid', 'solid'
            ])

        article = NewsArticles(**item)

        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item




class MongoPipeline(object):

    collection_name = 'newsarticles'
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        self.db[self.collection_name].insert(dict(item))
        logging.debug("Post added to MongoDB")
        return item

