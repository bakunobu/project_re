from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

from parser import get_building_info


http_url = 'http://mosopen.ru/street/16790'

#http_url = 'http://mosopen.ru/street/80'

html = urlopen(http_url)

street_suffix = http_url.split('/')[-1]

re_expr = r'http://address.mosopen.ru/{}[-0-9]+'.format(street_suffix)

bsObj = BeautifulSoup(html.read(), 'html.parser')

links = bsObj.find_all('a', href=re.compile(re_expr))
for i, link in enumerate(links):
    print(i, end='->')
    print(get_building_info(link.attrs['href']))
    


# print(bsObj)