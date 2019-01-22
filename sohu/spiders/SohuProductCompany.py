# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import Request
from sohu.model import SohuBrand, session

class  SohuProductCompanySpider(scrapy.Spider):
    name = 'sohuCompany'
    allowed_domains = ['sohu.com']
    start_urls = [
        'http://db.auto.sohu.com/'
    ]
   
    def parse(self, response):
        sel = Selector(response)
        brands = sel.xpath('//*[@id="daquan_top"]/div[2]/div')

        item = {}
        item['tag'] = 'sohu_company'
        for brand in brands:
            image_original  = brand.xpath('.//div/div[1]/a/img/@data-original')
            if len(image_original) > 0:
                src = image_original[0].extract()
                sohu_brand_id = re.findall(r'\/\d{1,}\.', src)
                if len(sohu_brand_id) > 0:
                    sohu_brand_id = sohu_brand_id[0].replace('.', '').replace('/', '')

            companies = brand.xpath('.//div/div/div/a')
            for company in companies:
                link = company.xpath('.//@href')
                name = company.xpath('.//text()')
                item['sohu_vehicle_brand_id'] = sohu_brand_id

                if len(name) > 0:
                    item['link'] = link[0].extract()
                    item['name'] = name[0].extract()

                # print item
                yield item.copy()
