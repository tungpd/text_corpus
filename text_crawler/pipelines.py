# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os
import logging
import leveldb
from text_crawler import utils
from text_crawler import settings
from datetime import datetime
from scrapy.exporters import JsonLinesItemExporter
import pathlib

class TextCrawlerPipeline(object):

    def open_spider(self, spider):
        self.db = leveldb.LevelDB(settings.ARTICLE_DB + '/' + spider.name)
        self.counters = utils.LevelDbCounter(settings.ARTICLE_COUNTERS_DB + '/' + spider.name)

    def process_item(self, item, spider):
        id = 0
        if self.counters.has_key(item['source']):
            id = self.counters.get(item['source'])
            self.counters.set(item['source'], id + 1)
        else:
            self.counters.set(item['source'], 1)

        print('write item to levelDB with key: ' + str(id))
        self.db.Put(str(id).encode('utf8'), item['content'])
        return item


class TextCrawlerJsonPipeline(object):
    export_root_dir = settings.EXPORT_ROOT_DIR
    exporters_dict = {}

    def open_spider(self, spider):
        self.exporters_dict[spider.name] = {}


    def close_spider(self, spider):
        self._close_exporter(spider.name)

    def _close_exporter(self, spider_name):
        for exporter in self.exporters_dict[spider_name].values():
            exporter.finish_exporting()
        self.exporters_dict[spider_name] = {}

    def process_item(self, item, spider):
        spider_name = spider.name
        exporter = self._exporter_for_item(item, spider_name)
        exporter.export_item(item)
        return item

    def _exporter_for_item(self, item, spider_name):
        create_time = int(float(item['create_time'])/86400)*86400
        dt = datetime.fromtimestamp(create_time)
        exporter_dir = os.path.join(self.export_root_dir, spider_name, str(dt.year), str(dt.month))
        pathlib.Path(exporter_dir).mkdir(parents=True, exist_ok=True)
        exporter_file_name = os.path.join(exporter_dir, str(dt.day))
        if create_time not in self.exporters_dict[spider_name]:
            self._close_exporter(spider_name)
            logging.info("start new exporter, saved to: %s", exporter_file_name)
            f = open(exporter_file_name, 'ab')
            exporter = JsonLinesItemExporter(f, ensure_ascii=False)
            exporter.start_exporting()
            self.exporters_dict[spider_name][create_time] = exporter
        logging.info("export to: %s", exporter_file_name)
        return self.exporters_dict[spider_name][create_time]



