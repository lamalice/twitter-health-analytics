# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter

class TwitterbotPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonItemPipeline(object):
    def open_spider(self, spider):
        self.file = open("/Users/alicelam/Kstate_Classes/CIS598/twitter-health-analytics/TwitterBot/data/file1.json", 'wb')
        self.file.write(str.encode('['))
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.file.write(str.encode(']'))
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.file.write(str.encode(','))
        return item