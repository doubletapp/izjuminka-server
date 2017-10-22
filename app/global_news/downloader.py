# -*- coding: utf-8 -*

from pymongo import MongoClient
from utils import BaseTask
from datetime import datetime
import feedparser
from urllib.request import Request, urlopen
import copy
import pymorphy2

connection = MongoClient('localhost', 27017)
dbmain = connection.news


class Downloader(BaseTask):
    name = 'downloader'

    def __init__(self, sources):
        self.sources = sources

    def execute(self):
        for source in sources:
            try:
                self.download_source(source)
            except Exception as ex:
                print(ex)

    def download_source(self, source):
        for rss in source['rss']:
            raw_data = self.download_rss(source, rss)
            if raw_data:
                print(raw_data[0]["source"])
                dbmain.raw_data.insert(raw_data)
            rss['last_update'] = datetime.utcnow()

        dbmain.sources.save(source)





if __name__ == '__main__':
    sources = dbmain.sources.find()
    task = Downloader(sources)
    task.start()