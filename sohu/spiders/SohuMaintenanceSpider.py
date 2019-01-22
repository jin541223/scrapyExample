# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request

from sohu.model import SohuBrand, SohuCompany, SohuSeries, SohuType, SohuMaintenanceInformation, session


class SohuMaintenanceSpider(scrapy.Spider):
    name = 'sohuMaintenance'
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

        tr_list = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[1]/tbody/tr')
        if tr_list is None or len(tr_list) <= 0:
            return

        tr_td_first  = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[1]/tbody/tr[1]/td[@class="bg"]')   
        if tr_td_first is None or len(tr_td_first) == 0:
            return

        tr_td_second = sel.xpath('//*[@id="stm_'+ str(sohu_type_id) +'_L"]/table[1]/tbody/tr[2]/td[@class="bg"]') 
        if tr_td_second is None or len(tr_td_second) == 0:
            return

        td_first  = tr_td_first.xpath('.//text()').extract()
        td_second = tr_td_second.xpath('.//text()').extract()
        if len(td_first) != 0 and len(td_second) != 0:
            td_first  = int(td_first[0].replace('km', ''))
            td_second = int(td_second[0].replace('km', ''))
            mileage_cycle = td_second - td_first
            if mileage_cycle <= 5000:
                time_cycle = 3
            else:
                time_cycle = 6

        # maintenance information
        item = {}
        item['tag'] = 'maintenance_info'

        for tr in tr_list:
            item['sohu_vehicle_type_id'] = sohu_vehicle_type_id
            mileage = tr.xpath('.//td[1]/text()').extract()
            if len(mileage) is 0:
                item['mileage'] = 0 
                item['mounth']  = 0
            else:
                item['mileage'] = mileage[0].replace('km', '')
                item['mounth']  = (((int(item['mileage']) - td_first) / mileage_cycle) + 1) * time_cycle

            oil = tr.xpath('.//td[2]/text()').extract()
            if len(oil) is 0 or re.match('-', oil[0]) is None:
                item['oil'] = 1   
            else:
                item['oil'] = 0

            oil_filter = tr.xpath('.//td[3]/text()').extract()
            if len(oil_filter) is 0 or re.match('-', oil_filter[0]) is None:
                item['oil_filter'] = 1
            else:
                item['oil_filter'] = 0

            air_filter = tr.xpath('.//td[4]/text()').extract()
            if len(air_filter) is 0 or re.match('-', air_filter[0]) is None:
                item['air_filter'] = 1
            else:
                item['air_filter'] = 0

            cabin_filter = tr.xpath('.//td[5]/text()').extract()
            if len(cabin_filter) is 0 or re.match('-', cabin_filter[0]) is None:
                item['cabin_filter'] = 1
            else:
                item['cabin_filter'] = 0

            fuel_filter = tr.xpath('.//td[6]/text()').extract()
            if len(fuel_filter) is 0 or re.match('-', fuel_filter[0]) is None:
                item['fuel_filter'] = 1   
            else:
                item['fuel_filter'] = 0

            brake_oil = tr.xpath('.//td[7]/text()').extract()
            if len(brake_oil) is 0 or re.match('-', brake_oil[0]) is None:
                item['brake_oil'] = 1
            else:
                item['brake_oil'] = 0

            transmission_oil = tr.xpath('.//td[8]/text()').extract()
            if len(transmission_oil) is 0 or re.match('-', transmission_oil[0]) is None:
                item['transmission_oil'] = 1
            else:
                item['transmission_oil'] = 0

            steering_oil = tr.xpath('.//td[9]/text()').extract()
            if len(steering_oil) is 0 or re.match('-', steering_oil[0]) is None:
                item['steering_oil'] = 1
            else:
                item['steering_oil'] = 0

            spark_plug = tr.xpath('.//td[10]/text()').extract()
            if len(spark_plug) is 0 or re.match('-', spark_plug[0]) is None:
                item['spark_plug'] = 1   
            else:
                item['spark_plug'] = 0

            timing_belt = tr.xpath('.//td[11]/text()').extract()
            if len(timing_belt) is 0 or re.match('-', timing_belt[0]) is None:
                item['timing_belt'] = 1
            else:
                item['timing_belt'] = 0

            reference_price = tr.xpath('.//td[12]/text()').extract()
            if len(reference_price) is 0 or reference_price is None:
                item['reference_price'] = 0
            else:
                price = re.findall(r'\d{1,}\.', reference_price[0])
                item['reference_price'] =  int(price[0].replace('.', ''))*100  

            # print item
            yield item.copy()       