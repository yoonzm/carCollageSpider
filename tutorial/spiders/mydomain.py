# -*- coding: utf-8 -*-
import json

import scrapy
import leancloud

from tutorial import carService

leancloud.init("Guv8NmYGL7M0xjass3x4Afzi-gzGzoHsz", "zbmTkdFb5AIGLvSeWUc3O72W")


class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['baidu.com']
    start_urls = [
        'https://www.baidu.com',
    ]

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)

        carService.delete_all()
        # TestObject = leancloud.Object.extend('TestObject')
        # test_object = TestObject()
        # test_object.set('words', "Hello World!")
        # test_object.save()
        # self.parse2('', test_object)

        # TestObject = leancloud.Object.extend('TestObject')
        # query = leancloud.Query(TestObject)
        # query.limit(1000)
        # query_result = query.find()
        #
        # for index,item in enumerate(query_result):
        #     title = item.get('carName')
        #
        #     self.log('carName: %s---------------------------------------------' % title)
        #     self.log('index: %s---------------------------------------------' % index)
        #
        #
        # pass

    def parse2(self, response, test_object):
        print 'oId', test_object.id, test_object.get('words')
