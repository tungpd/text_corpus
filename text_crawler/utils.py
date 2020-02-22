
import leveldb
from scrapy.spiders import CrawlSpider
import logging

import scrapy
from text_crawler import settings
from boilerpy3 import extractors
from text_crawler.items import Article
import re
import hashlib
import time

class LevelDbSet(object):

    def __init__(self, db):
        self.db = leveldb.LevelDB(db, create_if_missing=True)
    def __contains__(self, item):
        try:
            self.db.Get(item)
            return True
        except Exception:
            return False
    def add(self, item):
        self.db.Put(item, b"")

class LevelDbCounter:
    def __init__(self, db):
        self.db = leveldb.LevelDB(db, create_if_missing=True)
    def get(self, key):
        c = -1
        try:
            c = int(self.db.Get(key))
        except Exception as e:
            import traceback
            logging.error(traceback.format_exe())
        return c

    def set(self, key, value):
        self.db.Put(key, str(value).encode('utf8'))
    def has_key(self, key):
        try:
            v = self.db.Get(key)
            return True
        except Exception:
            return False


class TextSpider(CrawlSpider):
    allowed_url_pattern = r''
    excluded_url_pattern = r''
    custom_settings = {
        'DEPTH_LIMIT': 10
    }
    sha256 = hashlib.sha256()


    def __init__(self):
        super(TextSpider, self).__init__()
        self.visited_urls = LevelDbSet(settings.VISITED_URLS_DB + "/" + self.name)

    def parse_article(self, response):
        url = response.url
        self.sha256.update(url.encode('utf8'))
        url_h = self.sha256.hexdigest().encode('utf8')
        if url_h not in self.visited_urls:
            body = response.text
            extractor = extractors.ArticleExtractor()
            extracted_text = extractor.get_content(body)
            self.visited_urls.add(url_h)
            yield Article(content=extracted_text, url=url, source=self.name, create_time=str(time.time()))
