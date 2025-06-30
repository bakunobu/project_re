import os

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'app.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)

class Country(Base):
    __tablename__ = 'country'
    
    id = Column(
        'country_id',
        Integer, primary_key=True
        )
    name = Column(
        'country_name',
        String(256),
        index=True,
        unique=True
        )
    name_lat = Column(
        'country_name_lat',
        String(256),
        index=True,
        unique=True
        )
    
    
class Region(Base):
    __tablename__ = 'region'
    
    id = Column(
        'region_id',
        Integer, primary_key=True
        )
    contry_id = Column(
        'country_id',
        Integer,
        ForeignKey('country.country_id'),
        nullable=False
        )
    name = Column(
        'region_name',
        String(256),
        index=True,
        unique=True
        )
    name_lat = Column(
        'region_name_lat',
        String(256),
        index=True,
        unique=True
        )
    
    
class RegionLvl2(Base):
    __tablename__ = 'region_lvl_2'
    
    id = Column(
        'region_lvl_2_id',
        Integer, primary_key=True
        )
    region_id = Column(
        'region_id',
        Integer,
        ForeignKey('region.region_id'),
        nullable=False
    )
    name = Column(
        'region_lvl_2_name',
        String(256),
        index=True,
        unique=True
        )
    
    name_lat = Column(
        'region_lvl_2_name_lat',
        String(256),
        index=True,
        unique=True
        )
    
    name_short = Column(
        'region_lvl_2_name_short',
        String(64),
        index=True,
        unique=True
        )
    
    

class District(Base):
    __tablename__ = 'district'
    
    id = Column(
        'district_id',
        Integer, primary_key=True
        )
    region_id = Column(
        'region_lvl_2_id',
        Integer,
        ForeignKey('region_lvl_2.region_lvl_2_id'),
        nullable=False
    )
    name = Column(
        'district_name',
        String(256),
        index=True,
        unique=True
        )
    name_lat = Column(
        'district_name_lat',
        String(256),
        index=True,
        unique=True
        )
    
    
class StreetType(Base):
    __tablename__ = 'street_type'
    
    id = Column(
        'street_type_id',
        Integer, primary_key=True
        )
    name = Column(
        'street_type_name',
        String(64),
        index=True,
        unique=True
        )
    
    name_lat = Column(
        'street_type_name_lat',
        String(64),
        index=True,
        unique=True
        )
    
    name_short = Column(
        'street_type_name_short',
        String(8),
        index=True,
        unique=True
        )
    
    name_lat = Column(
        'street_type_name_lat_short',
        String(8),
        index=True,
        unique=True
        )
    
    
class Street(Base):
    __tablename__ = 'street'
    
    id = Column(
        'street_id',
        Integer, primary_key=True
        )
    
    region_lvl_2_id = Column(
        'region_lvl_2_id',
        Integer,
        ForeignKey('region_lvl_2.region_lvl_2_id'),
        nullable=False
    )
    
    street_type_id = Column(
        'street_type_id',
        Integer,
        ForeignKey('street_type.street_type_id'),
        nullable=False
    )
    
    name = Column(
        'street_name',
        String(256),
        index=True,
        unique=True
        )
    
    name_lat = Column(
        'street_name_lat',
        String(256),
        index=True,
        unique=True
        )
    

class ZipCode(Base):
    __tablename__ = 'zip_code'
    
    id = Column(
        'zip_id',
        Integer, primary_key=True
    )
    
    zip_code = Column(
        'zip_code',
        Integer,
        index=True,
        unique=True
        )
    
    
class Building(Base):
    __tablename__ = 'building'
    
    id = Column(
        'building_id',
        Integer, primary_key=True
    )
    
    district_id = Column(
        'district_id',
        Integer,
        ForeignKey('district.district_id'),
        nullable=False
    )
    
    street_id = Column(
        'street_id',
        Integer,
        ForeignKey('street.street_id'),
        nullable=True
    )
    
    
    building = Column(
        'building',
        String(16),
        unique=False,
        nullable=False
        )
    
    corpus = Column(
        'corpus',
        String(16),
        unique=False,
        nullable=True
        )
    
    stroenie = Column(
        'stroenie',
        String(16),
        unique=False,
        nullable=True
        )
    
    id_zip_code = Column(
        'zip_id',
        Integer,
        ForeignKey('zip_code.zip_id'),
        nullable=False
    )
    
    inhabitat_flg = Column(
        'inhabitat_flg',
        Integer,
        nullable=True
    )
    
    nearest_school = Column(
        'school_id',
        Integer,
        ForeignKey('school.school_id'),
        nullable=True
    )
    
    update_dttm = Column(
        'update_dttm',
        Text,
        nullable=True
    )
    
class School(Base):
    __tablename__ = 'school'
    
    id = Column(
        'school_id',
        Integer, primary_key=True
    )
    
    school_name = Column(
        'school_name',
        String(512),
        index=True,
        unique=True
        )
    
    school_name_short = Column(
        'school_name_short',
        String(64),
        index=True,
        unique=True
        )
    

class Filial(Base):
    __tablename__ = 'filial'
    
    id = Column(
        'filial_id',
        Integer, primary_key=True
    )
    main_school_id = Column(
        'school_id',
        Integer,
        ForeignKey('school.school_id'),
        nullable=False
    )
    
    building_id = Column(
        'building_id',
        Integer,
        ForeignKey('building.building_id'),
        nullable=False
    )
    
    filial_name = Column(
        'filial_name',
        String(512),
        index=True,
        unique=True
    )
    
    filial_name_lat = Column(
        'filial_name_lat',
        String(512),
        index=True,
        unique=True
    )
    

class SchoolLink(Base):
    __tablename__ = 'school_link'
    id = Column(
        'record_id',
        Integer, primary_key=True
    )
    
    school_id = Column(
        'school_id',
        Integer,
        ForeignKey('school.school_id'),
        nullable=False
    )
    
    street_id = Column(
        'street_id',
        Integer,
        ForeignKey('street.street_id'),
    )
    
    building = Column(
        'building',
        String(16),
        unique=False,
        nullable=False
        )
    
    corpus = Column(
        'corpus',
        String(16),
        unique=False,
        nullable=True
        )
    
    stroenie = Column(
        'stroenie',
        String(16),
        unique=False,
        nullable=True
        )
    
    update_dt = Column(
        'update_dt',
        Text,
        nullable=True
    )
    
    
metadata_obj = Base.metadata
metadata_obj.create_all(engine)