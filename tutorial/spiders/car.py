# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request

from tutorial import carService
from tutorial.items import CarBrand, CarType, CarModel


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

            request = Request(
                'https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b=' + car_brand['autoHomeId'],
                callback=self.parse_car_type)
            request.meta['car_brand'] = car_brand_model
            yield request

    # 解析车型
    def parse_car_type(self, response):
        car_brand = response.meta['car_brand']

        sellTypes = json.loads(response.body)['result']['sellSeries']
        allTypes = json.loads(response.body)['result']['allSellSeries']

        # 更新brand type 数量
        update_car_brand = CarBrand()
        update_car_brand['objectId'] = car_brand.id
        sell_type_count = 0
        all_type_count = 0

        # 在售
        sellAutoHomeIds = []  # 记录在售的ids
        for type_item in sellTypes:
            items = type_item['SeriesItems']
            sell_type_count += len(items)
            for item in items:
                sellAutoHomeIds.append(item['id'])

                print '-------------------------sellAutoHomeIds', sellAutoHomeIds

        # TODO 在所有的中过滤并标记出在售的
        # 所有
        for type_item in allTypes:
            items = type_item['SeriesItems']
            all_type_count += len(items)
            for item in items:
                on_sale = sellAutoHomeIds.count(item['id']) != 0
                yield self.save_car_type(car_brand, type_item, item, on_sale)

        update_car_brand['sellTypeCount'] = sell_type_count
        update_car_brand['allTypeCount'] = all_type_count
        carService.update_car_brand(update_car_brand)

    # 保存车型
    def save_car_type(self, car_brand, type_item, item, on_sale):
        car_type = CarType()
        car_type['brandId'] = car_brand.id
        car_type['brandName'] = car_brand.get('brandName')

        car_type['typeName'] = type_item['name']

        car_type['autoHomeId'] = item['id']
        car_type['name'] = item['name']
        car_type['maxPrice'] = item['maxprice']
        car_type['minPrice'] = item['minprice']
        car_type['image'] = 'https:' + item['seriesPicUrl']
        car_type['onSale'] = on_sale

        car_type_model = carService.save_car_type(car_type)

        request = Request(
            'https://m.autohome.com.cn/' + str(car_type['autoHomeId']) + '/#pvareaid=103224',
            callback=self.parse_car_model)
        request.meta['car_type'] = car_type_model
        return request

    # 各个配置
    def parse_car_model(self, response):
        car_type = response.meta['car_type']

        models = response.xpath('//div[@class="summary-cartype"]/div')[0]

        categorys = models.xpath('div[contains(@class, "category")]/text()').extract()
        lists = models.xpath('ul')

        print '长度对比', len(categorys), len(lists)

        for index in range(len(categorys)):
            for item in lists:
                car_model = CarModel()
                car_model['autoHomeId'] = item.xpath('li/@data-modelid').extract_first()
                car_model['brandId'] = car_type.get('brandId')
                car_model['brandName'] = car_type.get('brandName')
                car_model['typeId'] = car_type.id
                car_model['typeName'] = car_type.get('typeName')
                car_model['category'] = categorys[index]
                car_model['name'] = item.xpath('li/a/text()').extract_first()
                price_sel = item.xpath('li/div[@class="price"]')
                car_model['guidePrice'] = price_sel.xpath(
                    'span[@class="guide"]/strong/text()').extract_first()
                car_model['realityPrice'] = price_sel.xpath(
                    'span[@class="reality"]/strong/text()').extract_first()

                car_model_model = carService.save_car_model(car_model)

        # print '-------------------------------', categorys
