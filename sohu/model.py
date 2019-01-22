# -*- coding: utf-8 -*-
import json
import os

from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import settings

Base = declarative_base()

class SohuBrand(Base):
    __tablename__ = 'sohu_vehicle_brands'

    id = Column(BigInteger, primary_key=True)

    sohu_id = Column(BigInteger, index=False, unique=True, nullable=False)

    name = Column(String(64))
    vehicle_brand_id = Column(BigInteger, index=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    sohu_companies = relationship('SohuCompany', backref='sohu_brand', lazy='dynamic')
    sohu_series = relationship('SohuSeries', backref='sohu_brand', lazy='dynamic')


class SohuCompany(Base):
    __tablename__ = 'sohu_vehicle_product_companies'

    id = Column(BigInteger, primary_key=True)

    name = Column(String(64))
    sohu_vehicle_brand_id = Column(BigInteger, ForeignKey('sohu_vehicle_brands.id'))
    link = Column(String(128))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    sohu_series = relationship('SohuSeries', backref='sohu_company', lazy='dynamic')


class SohuSeries(Base):
    __tablename__ = 'sohu_vehicle_serieses'

    id = Column(BigInteger, primary_key=True)

    sohu_id = Column(BigInteger, index=False, unique=True, nullable=False)

    name = Column(String(64))
    sohu_product_company_id = Column(BigInteger, ForeignKey('sohu_vehicle_product_companies.id'))
    sohu_vehicle_brand_id = Column(BigInteger, ForeignKey('sohu_vehicle_brands.id'))
    vehicle_series_id = Column(BigInteger, index=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    sohu_types = relationship('SohuType', backref='sohu_vehicle_series', lazy='dynamic')


class SohuType(Base):
    __tablename__ = 'sohu_vehicle_types'

    id = Column(BigInteger, primary_key=True)

    sohu_id = Column(BigInteger, index=False, unique=True, nullable=False)

    name = Column(String(64))
    sohu_vehicle_series_id = Column(BigInteger, ForeignKey('sohu_vehicle_serieses.id'))
    vehicle_type_id = Column(BigInteger, index=False)
    user_id = Column(BigInteger, index=False)
    year = Column(BigInteger, index=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    sohu_maintenance_informations = relationship('SohuMaintenanceInformation', backref='sohu_type', lazy='dynamic')
    basic_data = relationship('MaintainBasicData', backref='sohu_type', lazy='dynamic')

class SohuMaintenanceInformation(Base):
    __tablename__ = 'maintenance_informations'

    id = Column(BigInteger, primary_key=True)

    sohu_vehicle_type_id = Column(BigInteger, ForeignKey('sohu_vehicle_types.id'))  
    vehicle_type_id = Column(BigInteger, index=False)
    mileage = Column(String(24))          #里程
    oil = Column(Integer)                 #机油
    oil_filter = Column(Integer)          #机滤 
    air_filter = Column(Integer)          #空气滤清器
    cabin_filter = Column(Integer)        #空调滤清器
    fuel_filter = Column(Integer)         #汽油滤清器
    brake_oil = Column(Integer)           #刹车油
    transmission_oil = Column(Integer)    #变速箱油
    steering_oil = Column(Integer)        #转向助力油
    spark_plug = Column(Integer)          #火花塞
    timing_belt = Column(Integer)         #正时皮带
    reference_price = Column(String(24))  #参考价格
    mounth = Column(Integer)              #保养时间

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class MaintainBasicData(Base):
    __tablename__='maintain_basic_data'

    id = Column(BigInteger, primary_key=True)

    sohu_vehicle_type_id = Column(BigInteger, ForeignKey('sohu_vehicle_types.id'))  
    vehicle_type_id = Column(BigInteger, index=False)
    oil_usage = Column(Integer)
    brake_oil_usage = Column(Integer)    
    steering_oil_usage = Column(Integer)
    transmission_oil_usage = Column(Integer)       
    spark_plug_num = Column(Integer) 

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

def get_db_engine():
    engine = create_engine(settings.DB_CONN, echo=settings.DB_DEBUG)

    return engine

engine = get_db_engine()
dbsession = sessionmaker(bind=engine, autoflush=False)
session = dbsession()
Base.metadata.create_all(engine) 