
import leveldb
from scrapy.spiders import CrawlSpider
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import scrapy
from text_crawler import settings
from boilerpy3 import extractors
from text_crawler.items import Article
import re
import hashlib
import time
from random import randint

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
        'DEPTH_LIMIT': 3
    }

    def __init__(self):
        super(TextSpider, self).__init__()
        self.visited_urls = LevelDbSet(settings.VISITED_URLS_DB + "/" + self.name)

    def process_links(self, links):
        ret_links = []
        for link in links:
            url = link.url
            url_h = hashlib.sha256(url.encode('utf8')).hexdigest().encode('utf8')
            rd = randint(0, 100)
            if url_h in self.visited_urls and rd < 90:
                self.log("visitted url: %s, %s"%(url_h, url))
                continue
            if url_h not in self.visited_urls:
                self.log("not visitted url: %s, %s"%(url_h, url))
            else:
                self.log("radom select visitted_url: %s, %s"%(url_h, url))
            ret_links.append(link)
        return ret_links


    def parse_article(self, response):
        url = response.url
        url_h = hashlib.sha256(url.encode('utf8')).hexdigest().encode('utf8')
        if url_h not in self.visited_urls:
            body = response.text
            extractor = extractors.ArticleExtractor()
            extracted_text = extractor.get_content(body)
            yield Article(content=extracted_text, url=url, source=self.name, create_time=str(time.time()))
            self.visited_urls.add(url_h)
