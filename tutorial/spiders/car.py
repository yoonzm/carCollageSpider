# -*- coding: utf-8 -*-
import json
from multiprocessing.dummy import dict

import scrapy

from tutorial import carService
from tutorial.items import CarBrand, CarType

class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['autohome.com.cn']
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']
    start_urls = ['https://www.autohome.com.cn/car/']

    def start_requests(self):
        # 每次启动前先删除
        carService.delete_all()

        pages = []
        for i in range(97, 123):
            page = scrapy.Request('https://www.autohome.com.cn/grade/carhtml/' + chr(i).upper() + '.html')
            pages.append(page)
        return pages

    def parse(self, response):
        # 首字母
        brand_first_word = response.url.replace('https://www.autohome.com.cn/grade/carhtml/', '').replace('.html', '')

        # 按字母分类
        for sel_brand in response.xpath('//dl'):
            car_brand = CarBrand()
            car_brand['autoHomeId'] = sel_brand.xpath('@id').extract_first()
            car_brand['brandFirstWord'] = brand_first_word
            car_brand['brandName'] = sel_brand.xpath('dt/div/a/text()').extract_first()
            car_brand['brandLogo'] = 'https:' + sel_brand.xpath('dt/a/img/@src').extract_first()

            # print '-----------------------------------', car_brand['autoHomeId']

            # # 保存至远程数据库<carBrand>
            car_brand_model = carService.save_car_brand(car_brand)

            request = scrapy.Request(
                'https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b=' + car_brand['autoHomeId'],
                callback=self.parse_car_type)
            request.meta['car_brand'] = car_brand_model
            yield request

    # 解析车型
    def parse_car_type(self, response):
        car_brand = response.meta['car_brand']

        sellTypes = json.loads(response.body)['result']['sellSeries']
        allTypes = json.loads(response.body)['result']['allSellSeries']

        # 所有
        for type_item in allTypes:
            items = type_item['SeriesItems']
            for item in items:
                self.save_car_type(car_brand, type_item, item, True)

        # 在售
        for type_item in sellTypes:
            items = type_item['SeriesItems']
            for item in items:
                self.save_car_type(car_brand, type_item, item, False)

    # 保存车型
    def save_car_type(self, car_brand, type_item, item, stop_pro):
        car_type = CarType()
        car_type['brandId'] = car_brand.id
        car_type['brandName'] = car_brand.get('brandName')

        car_type['typeName'] = type_item['name']

        car_type['autoHomeId'] = item['id']
        car_type['name'] = item['name']
        car_type['maxPrice'] = item['maxprice']
        car_type['minPrice'] = item['minprice']
        car_type['image'] = 'https:' + item['seriesPicUrl']
        car_type['stopPro'] = stop_pro

        car_type_model = carService.save_car_type(car_type)

        request = scrapy.Request(
            'https://m.autohome.com.cn/' + car_type['autoHomeId'] + '/#pvareaid=103224',
            callback=self.parse_car_model)
        request.meta['car_type'] = car_type_model
        yield request


    def parse_car_model(self, response):
        car_type = response.meta['car_type']

        models = response.xpath('//div[@class="summary-cartype"]/div')[0]

        categorys = models.xpath('div[contains(@class, "category")]/text()').extract()
        lists = models.xpath('ul')

        for index in range(len(categorys)):
            for item in lists[index]:
                category = categorys[index]
                name = lists[index].xpath('li/a/text()').extract_first()
                id = lists[index].xpath('li/@data-modelid').extract_first()
                guide = lists[index].xpath('li/div(@class="price")/span(@class="guide")/strong/text()').extract_first()
                reality = lists[index].xpath('li/div(@class="price")/span(@class="reality")/strong/text()').extract_first()

        print '-------------------------------', categorys