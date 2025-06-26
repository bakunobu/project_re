from db import StreetType, RegionLvl2, District
import re
import os

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Session
from urllib.request import urlopen

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'app.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)


from transliterate import translit
from bs4 import BeautifulSoup

http_url = 'http://mosopen.ru/streets'
html = urlopen(http_url) 
bsObj = BeautifulSoup(html.read(), 'html.parser')
print(bsObj)
# print(bsObj.prettify())
# result = bsObj.find_all('div', attrs={'id': 'regions_by_districts'})



# distrs = {
#     'ЦАО': 1,
#     'СВАО': 2,
#     'СЗАО': 3,
#     'САО': 4,
#     'ВАО': 5,
#     'ЮВАО': 6,
#     'ЮАО': 7,
#     'ЮЗАО': 8,
#     'ЗАО': 9,
#     'ЗелАО': 10,
#     'НАО': 11,
#     'ТАО': 12,
# }

# refs = re.findall(r'\<a\s+href=.*a\>', str(result))

# re_match = r'>[- а-яёА-ЯЁ]+<'

# district_id = None

# with Session(autoflush=False, bind=engine) as session:
#     for ref in refs:
#         text_match = re.search(re_match, str(ref))
#         if text_match:
#             txt = text_match.group(0).replace('<', '').replace('>', '')
#             if txt.isupper() or txt=='ЗелАО':
#                 district_id = distrs.get(txt, -100)
#             else:
#                 new_dist = District(
#                     region_id=district_id,
#                     name=txt,
#                     name_lat=translit(txt, 'ru', reversed=True)
#                 )
#                 session.add(new_dist)
#                 session.commit()


                    
#             region_id=1,
#             name=reg[0],
#             name_lat=translit(reg[0], 'ru', reversed=True),
#             name_short=reg[1],
#             )
#         session.add(new_reg)
#         session.commit()
            
            
            # print(
            #     f"""region_lvl_2_id: {district_id}\ndistrict_name: {txt}\ndistrict_name_lat: {translit(txt, 'ru', reversed=True)}""",
            #     end='\n* * *\n'
            # )
        # print(text_match.group(0).replace('<', '').replace('>', ''))
    

# 
# print(re.findall(r'<a\s\w+</a>(,<br/>|</strong>)\b', str(result)))
# print(result[0].split('\n'))
# print(bsObj)
# result = bsObj.find_all('table', attrs={'class': 'regions_list'})
# print(result)
# # result_obj = BeautifulSoup(result.read(), 'html.parser')

# re_expr_link = r'http://mosopen.ru/region/[a-z]+/streets'
# re_expr_title = r'>[а-яёА-ЯЁ]+<'
# result_txt = re.findall(r'<a\s.+<br/>', str(result))
# print(result_txt)
# links = re.findall(re_expr_link, str(result_txt))
# titles = re.findall(re_expr_title, str(result_txt))
# for link, title in zip(links, titles):
#     print(link, title.replace('<', '').replace('>', ''), sep='->')
    
# links = result_obj.find_all('a', href=re.compile(re_expr))
# for line in result[0]:
#     print(line)
# for i, link in enumerate(links):
#     print(i, end='->')
#     print(link.attrs['title'])
#     print(link.attrs['href'], re.search(r'>[a-z]+<',link.attrs['title']).group(0))


# basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
# 'sqlite:///' + os.path.join(basedir, 'app.db')

# engine = create_engine(SQLALCHEMY_DATABASE_URI)


# regions_lvl_2 = [
#     ('Центральный административный округ', 'ЦАО'),
#     ('Северо-Восточный административный округ', 'СВАО'),
#     ('Северо-Западный административный округ', 'СЗАО'),
#     ('Северный административный округ', 'САО'),
#     ('Восточный административный округ', 'ВАО'),
#     ('Юго-Восточный административный округ', 'ЮВАО'),
#     ('Южный административный округ', 'ЮАО'),
#     ('Юго-Западный административный округ', 'ЮЗАО'),
#     ('Западный административный округ', 'ЗАО'),
#     ('Зеленоградский административный округ', 'ЗелАО'),
#     ('Новомосковский административный округ', 'НАО'),
#     ('Троицкий административный округ', 'ТАО'),
# ]

# with Session(autoflush=False, bind=engine) as session:
#     for reg in regions_lvl_2:
#         new_reg = RegionLvl2(
#             region_id=1,
#             name=reg[0],
#             name_lat=translit(reg[0], 'ru', reversed=True),
#             name_short=reg[1],
#             )
#         session.add(new_reg)
#         session.commit()
    


# street_types = [
#     "аллея",
#     "бульвар",
#     "деревня",
#     "квартал",
#     "линия",
#     "микрорайон",
#     "мост",
#     "набережная",
#     "парк",
#     "переулок",
#     "площадь",
#     "посёлок",
#     "проезд",
#     "проектируемый проезд",
#     "просека",
#     "проспект",
#     "тупик",
#     "шоссе" 
# ]

# with Session(autoflush=False, bind=engine) as session:
#     for street_type in street_types:
#         new_street_type = StreetType(
#             name=street_type,
#             name_lat=translit(street_type, 'ru', reversed=True),
#         )
#         session.add(new_street_type)
#     session.commit()


# examples = [
#     '79, к1, с2',
#     '1',
#     '1, с3',
#     '16А, с211А',
#     '16АС',
#     '35, к3, с5А', 
# ]

# pattern_b1 = r'\d+\w*'
# pattern_k1 = r'к\w+'
# pattern_c1 = r'с\w+'

# for example in examples:
#     print(example)
#     match_b1 = re.search(pattern_b1, example)
#     print(f'дом: {match_b1.group(0)}')
#     match_k1 = re.search(pattern_k1, example)
#     if match_k1:
#         print(f'корпус: {match_k1.group(0)}')
#     match_c1 = re.search(pattern_c1, example)
#     if match_c1:
#         print(f'строение: {match_c1.group(0)}')
        



