from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from typing import Dict, Any, Union
import re

def get_build_number(build_num:str) -> Dict[str, Union[int, str]]:
    """Parse bilding info to separate parts: building number, corpus and stroenie

    Args:
        build_num (str): _description_

    Returns:
        Dict[str, Union[int, str]]: _description_
    """
    pattern_b1 = r'\d+\w*'
    pattern_k1 = r'к\w+'
    pattern_c1 = r'с\w+'
    build_dict = dict()


    match_b1 = re.search(pattern_b1, build_num)
    
    build_dict['дом']=match_b1.group(0)
    match_k1 = re.search(pattern_k1, build_num)
    if match_k1:
        build_dict['корпус']=match_k1.group(0).replace('к','')
    else:
        build_dict['корпус']=None
    match_c1 = re.search(pattern_c1, build_num)
    if match_c1:
        build_dict['строение']=match_c1.group(0).replace('с','')
    else:
        build_dict['строение']=None

    return build_dict    


def get_building_info(
    http_url: str,
) -> Dict[str, Union[int, str]]:
    """Get building info from mosopen.ru by parsing the HTML page
    """
    try:
        html = urlopen(http_url)
    except HTTPError:
        print('Error: ', HTTPError)
        return {'building_number':0, 'building_name':''}
    except URLError:
        print('Error: ', URLError)
        return {'building_number':0, 'building_name':''}
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    title = bsObj.find('div', attrs={'class': 'house_info_page_first'})
    building = title.p.text.split(':')[1].split(',', 1)[1].strip().replace('.', '').replace('\xa0', ' ')
    str_list = list(
        bsObj.find_all(
            'div',
            attrs={'class': 'contact'}
            )[0].text.split('\n')
        )
    build_info = [x.replace(':', '') for x in str_list if x != '']
    building_dict = get_build_number(building)
    address = dict()
    address.update(building_dict)
    for i in range(0, len(build_info[:8]), 2):
        address[build_info[i]] = build_info[i+1]
    return address

# http_url = 'http://address.mosopen.ru/80-1498'
# print(get_building_info(http_url))
