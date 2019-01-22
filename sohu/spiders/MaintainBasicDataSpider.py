# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request
from sohu.model import SohuBrand, SohuCompany, SohuSeries, SohuType, SohuMaintenanceInformation, MaintainBasicData, session

class MaintainBasicDataSpider(scrapy.Spider):
    name = 'basicData'
    allowed_domains = ['sohu.com']
   
    def start_requests(self):
        for sohu_series in session.query(SohuSeries):
            sohu_series_id = sohu_series.sohu_id
            link = sohu_series.sohu_company.link

            subdomain_prefix =  re.findall(r'\/\/[a-zA-z]{1,}[\-]?[0-9]*\.', link)
            if subdomain_prefix != None and len(subdomain_prefix) > 0:
                subdomain = subdomain_prefix[0].replace('//', '').replace('.', '')

                for sohu_type in sohu_series.sohu_types:
                    sohu_type_id = sohu_type.sohu_id
                    sohu_vehicle_type_id = sohu_type.id

                    url = 'http://db.auto.sohu.com/'+ str(subdomain) +'/'+ str(sohu_series_id) +'/'+ str(sohu_type_id) +'/maintenance.html'

                    yield Request(url,
                            meta={'sohu_vehicle_type_id': sohu_vehicle_type_id, 'sohu_type_id': sohu_type_id},
                            callback=self.parse)

        
    def parse(self, response):
        sohu_vehicle_type_id = response.meta['sohu_vehicle_type_id']
        sohu_type_id = response.meta['sohu_type_id']
        sel  = Selector(response)
        
        item = {}
        item['tag'] = 'basic_data'
        item['sohu_vehicle_type_id'] = sohu_vehicle_type_id

        #刹车油
        brake_oil = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[2]/tbody/tr[4]/td[3]')
        if brake_oil is None or len(brake_oil) <= 0:
            return

        item['brake_oil_usage'] = 0
        brake_oil_text  = brake_oil.xpath('.//text()').extract()
        if len(brake_oil_text) != 0:
            brake_oil_usage = re.findall(r'[1-9]\d?[L|升|个|支]|[0-9]{1,}[.][0-9]*?[L|升|个|支]', brake_oil_text[0])
            if len(brake_oil_usage) != 0:
                brake = re.findall(r'[1-9]\d?|[0-9]{1,}[.][0-9]*?', brake_oil_usage[0])
                item['brake_oil_usage'] = int(brake[0]) * 1000


        #机油(全合成机油)
        oil = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[2]/tbody/tr[1]/td[6]')
        if oil is None or len(oil) <= 0:
            return

        item['oil_usage'] = 0
        oil_text  = oil.xpath('.//text()').extract()
        if len(oil_text) != 0:
            oil_usage = re.findall(r'[1-9]\d?[L|升|个|支]|[0-9]{1,}[.][0-9]*?[L|升|个|支]', oil_text[0])
            if len(oil_usage) != 0:
                oil = re.findall(r'[1-9]\d?|[0-9]{1,}[.][0-9]*?', oil_usage[0])
                item['oil_usage'] =int( oil[0]) * 1000


        #转向助力油
        steering_oil = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[2]/tbody/tr[5]/td[3]')
        if steering_oil is None or len(steering_oil) <= 0:
            return

        item['steering_oil_usage'] = 0
        steering_oil_usage_text  = steering_oil.xpath('.//text()').extract()
        if len(steering_oil_usage_text) != 0:
            steering_oil_usage = re.findall(r'[1-9]\d?[L|升|个|支]|[0-9]{1,}[.][0-9]*?[L|升|个|支]', steering_oil_usage_text[0])
            if len(steering_oil_usage) != 0:
                steering = re.findall(r'[1-9]\d?|[0-9]{1,}[.][0-9]*?', steering_oil_usage[0])
                item['steering_oil_usage'] = int(steering[0]) * 1000



        #变速箱油
        transmission_oil = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[2]/tbody/tr[4]/td[6]')
        if transmission_oil is None or len(transmission_oil) <= 0:
            return

        item['transmission_oil_usage'] = 0
        transmission_oil_usage_text  = transmission_oil.xpath('.//text()').extract()
        if len(transmission_oil_usage_text) != 0:
            transmission_oil_usage = re.findall(r'[1-9]\d?[L|升|个|支]|[0-9]{1,}[.][0-9]*?[L|升|个|支]', transmission_oil_usage_text[0])
            if len(transmission_oil_usage) != 0:
                transmission = re.findall(r'[1-9]\d?|[0-9]{1,}[.][0-9]*?', transmission_oil_usage[0])
                item['transmission_oil_usage'] = int(transmission[0]) * 1000


        #火花塞
        spark_plug = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[2]/tbody/tr[5]/td[6]')
        if spark_plug is None or len(spark_plug) <= 0:
            return

        item['spark_plug_num'] = 0
        spark_plug_text  = spark_plug.xpath('.//text()').extract()
        if len(spark_plug_text) != 0:
            spark_plug_num = re.findall(r'[1-9]\d?[L|升|个|支]|[0-9]{1,}[.][0-9]*?[L|升|个|支]', spark_plug_text[0])
            if len(spark_plug_num) != 0:
                num = re.findall(r'[1-9]\d?|[0-9]{1,}[.][0-9]*?', spark_plug_num[0])
                item['spark_plug_num'] = int(num[0])

        # print item
        yield item.copy() 