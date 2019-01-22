# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import Request

from sohu.model import SohuBrand, SohuCompany, SohuSeries, session


class SohuSeriesSpider(scrapy.Spider):
    name = "sohuSeries"
    allowed_domains = ['sohu.com']

    def start_requests(self):
        for sohu_company in session.query(SohuCompany):
            sohu_vehicle_brand_id = sohu_company.sohu_brand.sohu_id
            sohu_brand_id = sohu_company.sohu_vehicle_brand_id

            url = 'http://weizhang.auto.sohu.com/db/rootBrands/'+ str(sohu_vehicle_brand_id) +'/brandModels'
            yield Request(url,
                          meta={'sohu_brand_id': sohu_brand_id, 'sohu_company_id': sohu_company.id},
                          callback=self.parse)


    def parse(self, response):
        sohu_brand_id = response.meta['sohu_brand_id']
        sohu_company_id = response.meta['sohu_company_id']
        json_response = json.loads(response.body)
        brand_models = json_response['brandModels']

        item = {}
        item['tag'] = 'sohu_series'
        for sohu_series in brand_models:
            for series in sohu_series['models']:
                item['sohu_id'] = series['id']
                item['name'] = series['name']
                item['sohu_product_company_id'] = sohu_company_id
                item['sohu_brand_id'] = sohu_brand_id

                yield item.copy()