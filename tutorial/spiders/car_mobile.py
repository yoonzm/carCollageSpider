# -*- coding: utf-8 -*-
from multiprocessing.dummy import dict

import scrapy

from tutorial import carService
from tutorial.items import CarBrand, CarType


class CarMobileSpider(scrapy.Spider):
    name = 'car_mobile'
    allowed_domains = ['autohome.com.cn']
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']
    start_urls = ['https://www.autohome.com.cn/car/']

    def start_requests(self):
        # 每次启动前先删除
        carService.delete_all()

        return [
            scrapy.Request('https://m.autohome.com.cn/3941/#pvareaid=103224')
        ]

    def parse(self, response):
        summary_cartype = response.xpath('//div[@class="summary-cartype"]/div')[0]

        categorys = summary_cartype.xpath('div[@class="category "]/text()').extract_first()

        print '类型', categorys

        # for index in range(len(brand_first_words)):
        #
        #     # 首字母
        #     brand_first_word = brand_first_words[index]
        #
        #     # 按字母分类
        #     for sel_brand in div_list_brand.xpath('ul/li/div[@class="item"]'):
        #         car_brand = CarBrand()
        #         car_brand['brandFirstWord'] = brand_first_word
        #         car_brand['brandName'] = sel_brand.xpath('span/text()').extract_first()
        #         # car_brand['brandLogo'] = 'https:' + sel_brand.xpath('img/@src').extract_first()
        #
        #         print '-----------------------------------------', car_brand['brandName'], sel_brand.xpath('img/@src').extract_first()

                # # 保存至远程数据库<carBrand>
                # car_brand_model = carService.save_car_brand(car_brand)
                #
                # # 具体车型 奥迪A3 奥迪A4 ...
                # sel_dd = sel_brand.xpath('dd')
                # type_name = sel_dd.xpath('div[contains(@class, "h3-tit")]/a/text()').extract()
                # type_list = sel_dd.xpath('ul')
                #
                # # 车型分类
                # for index in range(len(type_name)):
                #     for sel_type in type_list[index].xpath('li'):
                #         # 过滤掉class为dashline的
                #         li_class = sel_type.xpath('@class').extract_first()
                #         if li_class == 'dashline':
                #             continue
                #
                #         car_type = CarType()
                #         car_type['brandId'] = car_brand_model.id
                #         car_type['brandName'] = car_brand_model.get('brandName')
                #         car_type['typeName'] = type_name[index]
                #         car_type['name'] = sel_type.xpath('h4/a/text()').extract_first()
                #         car_type['guidePrice'] = sel_type.xpath('div/a[contains(@class, "red")]/text()').extract_first()
                #         car_type['imageStoreUrl'] = 'https:' + sel_type.xpath(
                #             'div/a[contains(@id, "atk_")]/@href').extract_first()
                #         car_type['stopPro'] = False
                #         # 已停产
                #         if sel_type.xpath('div/span[contains(@class, "text-through")]/text()').extract_first() == u'报价':
                #             car_type['stopPro'] = True
                #
                #         request = scrapy.Request(car_type['imageStoreUrl'], callback=self.parse_car_type_image)
                #         request.meta['car_type'] = car_type
                #         yield request

    def parse_car_type_image(self, response):
        car_type = response.meta['car_type']

        image = response.xpath('//li[contains(@class, "vr-item")]/a/img/@src').extract_first()
        car_type['image'] = image
        # print car_type

        # 保存至远程数据库<carType>
        car_type_model = carService.save_car_type(car_type)

