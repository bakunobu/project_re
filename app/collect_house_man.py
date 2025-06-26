import os
import sqlite3

import re

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Session
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

import urllib

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

from bs4 import BeautifulSoup
from parser import get_building_info
from transliterate import translit
from tqdm import tqdm

from db import Street, Building


basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'app.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)


script_dir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(script_dir, "app.db")

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# 1
cursor.execute('SELECT * FROM zip_code')
codes = cursor.fetchall()
zip_codes = {x[1]:x[0] for x in codes}

# 2 
cursor.execute('SELECT district_name, district_id FROM district')
distrs = cursor.fetchall()
districts = {x[0]:x[1] for x in distrs}

cursor.execute('SELECT district_name, region_lvl_2_id FROM district')
distrs_main = cursor.fetchall()
districts_main  = {x[0]:x[1] for x in distrs}

cursor.execute('SELECT street_type_name, street_type_id  FROM street_type')
str_types = cursor.fetchall()
street_types = {x[0]:x[1] for x in str_types}
str_type_filter = r'({})'.format('|'.join(street_types.keys()))
connection.close()

streets = [
    # 'http://mosopen.ru/street/472',
    # 'http://mosopen.ru/street/1291',
    # 'http://mosopen.ru/street/3930',
    # 'http://mosopen.ru/street/3945',
    # 'http://mosopen.ru/street/1575',
    # 'http://mosopen.ru/street/6791',
    # 'http://mosopen.ru/street/8120',
    # 'http://mosopen.ru/street/15858',
    # 'http://mosopen.ru/street/15857',
    # 'http://mosopen.ru/street/15856',
    'http://mosopen.ru/street/15855',
    'http://mosopen.ru/street/16584',
    'http://mosopen.ru/street/16585',
    'http://mosopen.ru/street/16583',
    'http://mosopen.ru/street/17620',
    'http://mosopen.ru/street/18540',
    'http://mosopen.ru/street/18544',
    'http://mosopen.ru/street/19822',
    'http://mosopen.ru/street/20112',
    'http://mosopen.ru/street/20106',
    'http://mosopen.ru/street/20107',
    'http://mosopen.ru/street/22422',
    'http://mosopen.ru/street/22545',
    'http://mosopen.ru/street/23355',
    'http://mosopen.ru/street/23356',
    'http://mosopen.ru/street/23360',
    'http://mosopen.ru/street/93045',
    'http://mosopen.ru/street/26635',
    'http://mosopen.ru/street/28860',
    'http://mosopen.ru/street/29276',
    'http://mosopen.ru/street/30410',
    'http://mosopen.ru/street/30473'    
]

visited = []
visited_streets = []

for street in tqdm(streets):
    if street in visited:
        continue
    visited.append(street)
    try:
        html = urlopen(street)
    except HTTPError as e:
        print(street, 'HTTPError')
        print(e)
        continue
    except URLError as e:
        print(street, 'URLError')
        print(e)
        continue
    
    else:
        with Session(autoflush=False, bind=engine) as session:
            street_id = street.split('/')[-1]
            re_expr = r'http://address.mosopen.ru/{}[-0-9]+'.format(street_id)
            bsObj = BeautifulSoup(html.read(), 'html.parser')
            links = bsObj.find_all('a', href=re.compile(re_expr))
            for link in tqdm(links):
                house_info = get_building_info(link.attrs['href'])
                print(house_info)
                try:
                    zip_code = zip_codes.get(int(house_info['Индекс']), -1)
                except KeyError:
                    zip_code = -1
                
                building_info = Building(
                    district_id=districts.get(house_info['Район'], -1),
                    street_id=int(street_id),
                    building=house_info['дом'],
                    corpus=house_info['корпус'],
                    stroenie=house_info['строение'],
                    id_zip_code = zip_code,
                    inhabitat_flg=None,
                    nearest_school=None
                )
                session.add(building_info)
                session.commit()
                
                if street_id not in visited_streets:
                    visited_streets.append(street_id)

                    try:
                        street_type = re.search(
                          str_type_filter,
                          house_info['Улица'].lower()
                          ).group(0)
                    except:
                        street_type = ''
                        
                    street_type_id = street_types.get(street_type, -1)
                    street_name = house_info['Улица']
                    street_region = districts_main.get(house_info['Район'], -1)
                    
                    
                    street_info = Street(
                      id=int(street_id),
                      region_lvl_2_id=street_region,
                      street_type_id=street_type_id,
                      name=street_name,
                      name_lat=translit(
                        house_info['Улица'],
                        'ru',
                        reversed=True),
                      )
                    session.add(street_info)
                    session.commit()


        
    