# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import json
from locale import str

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    page = scrapy.Field()
    title = scrapy.Field()
    reply = scrapy.Field()


# ------------------------------------ car ----------------------------------------

# 品牌
class CarBrand(scrapy.Item):
    brandFirstWord = scrapy.Field()
    brandName = scrapy.Field()
    brandLogo = scrapy.Field()


# 车型
class CarType(scrapy.Item):
    brandId = scrapy.Field()
    brandName = scrapy.Field()
    typeName = scrapy.Field()
    name = scrapy.Field()
    guidePrice = scrapy.Field()
    stopPro = scrapy.Field()
    imageStoreUrl = scrapy.Field()
    image = scrapy.Field()

# class CarItem(scrapy.Item):
#     carName = scrapy.Field()
#     carWord = scrapy.Field()
#     carLogo = scrapy.Field()
#     types = scrapy.Field()
#
# # 各厂家
# class CarType(scrapy.Item):
#     name = scrapy.Field()
#     modelTypes = scrapy.Field()
#
# # 车型
# class CarModel(scrapy.Item):
#     name = scrapy.Field()
#     guidePrice = scrapy.Field()
#     detailUrl = scrapy.Field()
