

import re
import os
from db import ZipCode

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Session
from urllib.request import urlopen
from bs4 import BeautifulSoup


basedir = os.path.abspath(os.path.dirname(__file__))



SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'app.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)

http_url = 'http://mosopen.ru/streets'
html = urlopen(http_url) 
bsObj = BeautifulSoup(html.read(), 'html.parser')
result = bsObj.find_all('div', attrs={'id': 'regions_by_map'})
print(result)

refs = re.findall(r'coords="[,0-9]{3,}"', str(result))
# print(refs)
for ref in refs:
    text_match = re.findall(r'\d{1,}', str(ref))
    print(text_match)
