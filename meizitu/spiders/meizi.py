# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from meizitu.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/all/']

    # def start_requests(self):
    #     url = 'https://www.mzitu.com/all/'
    #     yield Request(url=url, method='GET', callback=self.main_page)

    def parse(self, response):
        # 取得所有套图地址
        hxs = response.xpath('//p[contains(@class,"url")]/a/@href').extract()
        for url in hxs:
            yield Request(url=url, callback=self.fenye)

    def fenye(self, response):
        # 取得图片路径和标题
        url = response.url
        item = MeizituItem()
        item['img_url'] = response.xpath('//div[@class="main-image"]//img/@src').extract()
        item['title'] = response.xpath('//div[@class="main-image"]//img/@alt').extract_first().strip()
        yield item
        # 取得下方导航条页面路径
        xhs = response.xpath('//div[@class="pagenavi"]/a[6]/@href').extract()
        for url in xhs:
            yield Request(url=url, callback=self.fenye)
            pass