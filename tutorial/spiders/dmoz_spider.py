# coding=utf-8
import scrapy

from tutorial.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["car.autohome.com.cn"]
    start_urls = [
        "https://car.autohome.com.cn/pic/series/18.html#pvareaid=103448",
    ]

    def parse(self, response):
        test = response.xpath('//li[contains(@class, "vr-item")]/a/img/@src').extract_first()
        print '---------------------', test
        yield scrapy.Request('https://car.autohome.com.cn/pic/series/18.html#pvareaid=103448', callback=self.parse2)

    def parse2(self, response):
        print '-------------------parse2', response
        yield scrapy.Request('https://car.autohome.com.cn/pic/series/19.html#pvareaid=103447', callback=self.parse3)

    def parse3(self, response):
        print '-------------------parse3', response



