# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import Request

from sohu.model import SohuBrand, SohuCompany, SohuSeries, session

class SohuTypeSpider(scrapy.Spider):
    name = 'sohuType'
    allowed_domains = ['sohu.com']

    def start_requests(self):
        for sohu_series in session.query(SohuSeries):
            sohu_series_id = sohu_series.sohu_id
            
            #在售
            on_sell_url = 'http://autoapp.auto.sohu.com/api/model/trimList/'+ str(sohu_series_id)
            yield Request(on_sell_url,
                    meta={'sohu_series_id': sohu_series_id},
                    callback=self.parse_types)
            
            #停售年限
            market_out_year_url = 'http://autoapp.auto.sohu.com/api/model/info/'+ str(sohu_series_id)
            yield Request(market_out_year_url,
                    meta={'sohu_series_id': sohu_series_id},
                    callback=self.parse_market_out_types)


    def parse_types(self, response):
        sohu_series_id = response.meta['sohu_series_id']
        on_sell_types = json.loads(response.body)
        if len(on_sell_types) == 0:
            return

        item = {}
        item['tag'] = 'sohu_type'
        for on_sell_type in on_sell_types:
            item['name']  = on_sell_type['nameZh']
            item['year']  = on_sell_type['year']
            item['sohu_id'] = on_sell_type['trimId']
            item['sohu_vehicle_series_id'] = sohu_series_id
           
            yield item.copy()


    def parse_market_out_types(self, response):
        sohu_series_id = response.meta['sohu_series_id']
        market_out_years = json.loads(response.body)
        if len(market_out_years) == 0:
            return

        for year in market_out_years['offSaleYearList']:
            market_out_type_url = 'http://autoapp.auto.sohu.com/api/model/offsaleList/'+ str(sohu_series_id) +'/'+ str(year)

            yield Request(market_out_type_url,
                    meta={'sohu_series_id': sohu_series_id, 'year': year},
                    callback=self.parse_market_out_type)


    def parse_market_out_type(self, response):
        sohu_series_id = response.meta['sohu_series_id']
        year = response.meta['year']
        market_out_types = json.loads(response.body)
        if len(market_out_types) == 0:
            return
        
        item = {}
        item['tag'] = 'sohu_type'
        for market_out_type in market_out_types[year]:
            item['name']  = market_out_type['nameZh']
            item['year']  = year
            item['sohu_id'] = market_out_type['trimId']
            item['sohu_vehicle_series_id'] = sohu_series_id
          
            yield item.copy()