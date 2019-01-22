# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest

class  Spider(scrapy.Spider):
    name = 'sohuBrand'
    allowed_domains = ['sohu.com']
    start_urls = [
        'http://weizhang.auto.sohu.com/db/rootBrands'
    ]

    def parse(self, response):
        json_response = json.loads(response.body)
        brands = json_response['brands']

        item = {}
        item['tag'] = 'sohu_brand'
        for single_brand in brands:
            for brand in single_brand['brands']:
                item['sohu_id'] = brand['id']
                item['name']    = brand['name']
                # print item
                yield item.copy()