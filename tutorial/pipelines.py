# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from multiprocessing.dummy import dict


class TutorialPipeline(object):

    def __init__(self):
        # 使用codecs模块的打开方式，可以指定编码打开，避免很多编码问题
        self.file = codecs.open("items.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False, default=lambda obj: obj.__dict__) + "\n"
        self.file.write(lines + ',')
        return item

    def spider_closed(self, spider):
        self.file.close()
