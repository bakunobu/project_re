
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
result = bsObj.find_all('table', attrs={'class': 'table_list'})


refs = re.findall(r'\<a\s+href=.*a\>', str(result))
# print(refs)


with Session(autoflush=False, bind=engine) as session:
    for ref in refs:
        text_match = re.findall(r'/post_code/\d+', str(ref))
        for match in text_match:
            print(match)
            new_zip = ZipCode(zip_code=match.strip('/post_code/'))
            session.add(new_zip)
            session.commit()

