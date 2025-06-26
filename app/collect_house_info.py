import os
import sqlite3

import re

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Session
from urllib.request import urlopen
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

"""
  Мне нужно:
  1) идентифкаторы зип-кодов, чтобы мапить их на соответствующую запись для дома
  2) идентификаторы районов, чтобы получать идентфикаторы по названию и писать в таблицу
  3) список улиц, которые я уже обошел (id, название, тип)
  4) список типов улиц, чтобы удалять их из названий
"""
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

# 3
visited_streets = [
    '20115',
    '6090',
    '28780',
    '28790',
    '26040',
    '22525',
    '33426',
    '31435',
    '4220',
    '4230',
    '4200',
    '4213',
    '4211',
    '4201',
    '4198',
    '4120',
    '5890',
]

# 4
cursor.execute('SELECT street_type_name, street_type_id  FROM street_type')
str_types = cursor.fetchall()
street_types = {x[0]:x[1] for x in str_types}
str_type_filter = r'({})'.format('|'.join(street_types.keys()))
connection.close()
# список идентификаторов улиц
re_expr_main = r'http://mosopen.ru/street/[-0-9]+'
for i in tqdm(range(3, 33)):
    with Session(autoflush=False, bind=engine) as session:
        http_url = f'http://mosopen.ru/streets/letter/{i}'
        # html = urlopen(http_url)
        html = opener.open(http_url)
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        street_links = bsObj.find_all('a', href=re.compile(re_expr_main))
        
        for street_link in street_links:
            street_id = street_link.attrs['href'].split('/')[-1]
            print(street_id)
            http_url = street_link.attrs['href']

            html = urlopen(http_url)

            re_expr = r'http://address.mosopen.ru/{}[-0-9]+'.format(street_id)

            bsObj = BeautifulSoup(html.read(), 'html.parser')

            links = bsObj.find_all('a', href=re.compile(re_expr))
            print(links)
            for link in links:
                house_info = get_building_info(link.attrs['href'])
                building_info = Building(
                    district_id=districts.get(house_info['Район'], -1),
                    street_id=int(street_id),
                    building=house_info['дом'],
                    corpus=house_info['корпус'],
                    stroenie=house_info['строение'],
                    id_zip_code = zip_codes.get(int(house_info['Индекс']), -1),
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


