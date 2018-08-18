# -*- coding: utf-8 -*-
import json
from multiprocessing.dummy import dict

import scrapy

from tutorial import carService
from tutorial.items import CarBrand, CarType

def format_wan(num):
    return format(float(num)/float(10000),'.2f')

def format_price(min, max):
    return str(format_wan(min)) + '-' + str(format_wan(max)) + '万'

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

        for type_item in allTypes:
            items = type_item['SeriesItems']
            for item in items:
                save_car_type(car_brand, type_item, item, True)

        for type_item in sellTypes:
            items = type_item['SeriesItems']
            for item in items:
                save_car_type(car_brand, type_item, item, False)

def save_car_type(car_brand, type_item, item, stop_pro):
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

    carService.save_car_type(car_type)