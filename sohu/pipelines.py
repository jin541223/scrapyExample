# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
from datetime import datetime
import time

from model import SohuBrand, SohuCompany, SohuSeries, SohuType, SohuMaintenanceInformation, MaintainBasicData, Base, session

def process_sohu_brand(item, sohu_id):
    sohu_brand = session.query(SohuBrand).filter_by(sohu_id=sohu_id).first()
    if sohu_brand is None:
        sohu_brand = SohuBrand()
        sohu_brand.sohu_id=sohu_id
        sohu_brand.created_at=datetime.now()
        sohu_brand.updated_at=datetime.now()

        sohu_brand.name=item.get('name', '')

        session.merge(sohu_brand)


def process_sohu_company(item):
    sohu_brand = session.query(SohuBrand).filter_by(sohu_id=item.get('sohu_vehicle_brand_id')).first()
    sohu_company = session.query(SohuCompany).filter_by(link=item.get('link')).first()
    if sohu_company is None:
        sohu_company = SohuCompany()
        sohu_company.created_at=datetime.now()
        sohu_company.updated_at=datetime.now()

        sohu_company.name=item.get('name', '')
        sohu_company.link=item.get('link', '')

        sohu_brand.sohu_companies.append(sohu_company)

        session.merge(sohu_brand)


def process_sohu_series(item, sohu_id):
    sohu_brand = session.query(SohuBrand).filter_by(id=item.get('sohu_brand_id')).first()
    sohu_company = session.query(SohuCompany).filter_by(id=item.get('sohu_product_company_id')).first()
    sohu_series = session.query(SohuSeries).filter_by(sohu_id=sohu_id).first()
    if sohu_series is None:
        sohu_series = SohuSeries()
        sohu_series.sohu_id=sohu_id
        sohu_series.created_at=datetime.now()
        sohu_series.updated_at=datetime.now()

        sohu_series.name=item.get('name', '')

        sohu_brand.sohu_series.append(sohu_series)
        sohu_company.sohu_series.append(sohu_series)

        session.merge(sohu_brand)
        session.merge(sohu_company)


def process_sohu_type(item, sohu_id):
    sohu_series = session.query(SohuSeries).filter_by(sohu_id=item.get('sohu_vehicle_series_id')).first()
    sohu_type = session.query(SohuType).filter_by(sohu_id=sohu_id).first()
    if sohu_type is None:
        sohu_type = SohuType()
        sohu_type.sohu_id=sohu_id
        sohu_type.created_at=datetime.now()
        sohu_type.updated_at=datetime.now()

        sohu_type.name=item.get('name', '')
        sohu_type.year=item.get('year', '')

        sohu_series.sohu_types.append(sohu_type)

        session.merge(sohu_series)


def process_maintenance_information(item):
    sohu_type = session.query(SohuType).filter_by(id=item.get('sohu_vehicle_type_id')).first()
    maintenance_information = session.query(SohuMaintenanceInformation).filter_by(sohu_vehicle_type_id=item.get('sohu_vehicle_type_id')).filter_by(mileage=item.get('mileage')).first()

    if maintenance_information is None:
        maintenance_information = SohuMaintenanceInformation()
        maintenance_information.created_at=datetime.now()
        maintenance_information.updated_at=datetime.now()

        maintenance_information.mileage=item.get('mileage', '')
        maintenance_information.oil=item.get('oil', 0)
        maintenance_information.oil_filter=item.get('oil_filter', 0)
        maintenance_information.air_filter=item.get('air_filter', 0)
        maintenance_information.cabin_filter=item.get('cabin_filter', 0)
        maintenance_information.fuel_filter=item.get('fuel_filter', 0)
        maintenance_information.brake_oil=item.get('brake_oil', 0)
        maintenance_information.transmission_oil=item.get('transmission_oil', 0)
        maintenance_information.steering_oil=item.get('steering_oil', 0)
        maintenance_information.spark_plug=item.get('spark_plug', 0)
        maintenance_information.timing_belt=item.get('timing_belt', 0)
        maintenance_information.reference_price=item.get('reference_price', '')
        maintenance_information.mounth=item.get('mounth', '')

        sohu_type.sohu_maintenance_informations.append(maintenance_information)

        session.merge(sohu_type)


def process_maintain_basic_data(item):
    oil_usage = item.get('oil_usage', 0)
    brake_oil_usage = item.get('brake_oil_usage', 0)
    steering_oil_usage = item.get('steering_oil_usage', 0)
    transmission_oil_usage = item.get('transmission_oil_usage', 0)
    spark_plug_num = item.get('spark_plug_num', 0)

    if oil_usage != 0 or brake_oil_usage != 0 or steering_oil_usage != 0 or transmission_oil_usage != 0 or spark_plug_num != 0:
        sohu_type = session.query(SohuType).filter_by(id=item.get('sohu_vehicle_type_id')).first()

        maintain_basic_data = session.query(MaintainBasicData).filter_by(sohu_vehicle_type_id=item.get('sohu_vehicle_type_id')).first()
        if maintain_basic_data is None:
            maintain_basic_data = MaintainBasicData()
            maintain_basic_data.created_at=datetime.now()
            maintain_basic_data.updated_at=datetime.now()

            maintain_basic_data.oil_usage=oil_usage
            maintain_basic_data.brake_oil_usage=brake_oil_usage
            maintain_basic_data.steering_oil_usage=steering_oil_usage
            maintain_basic_data.transmission_oil_usage=transmission_oil_usage
            maintain_basic_data.spark_plug_num=spark_plug_num

            sohu_type.basic_data.append(maintain_basic_data)

            session.merge(sohu_type)


class pipeline(object):
    def process_item(self, item, spider):
        tag = item.get('tag', '')

        if tag == 'sohu_brand':
            process_sohu_brand(item, item.get('sohu_id'))
        elif tag == 'sohu_company':
            process_sohu_company(item)
        elif tag == 'sohu_series':
            process_sohu_series(item, item.get('sohu_id'))
        elif tag == 'sohu_type':
            process_sohu_type(item, item.get('sohu_id'))
        elif tag == 'maintenance_info':
            process_maintenance_information(item)
        elif tag == 'basic_data':
            process_maintain_basic_data(item)
        else:
            return

        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.flush()