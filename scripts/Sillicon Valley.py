# coding=utf-8
"""download tv play from http://www.zimuzu.tv/, change config for another tv play"""
from __future__ import print_function, unicode_literals

import re

# import bs4
import requests
from bs4 import BeautifulSoup

from bgmi.script import ScriptBase

BANGUMI_NAME = 'Sillicon Valley'
UPDATE_TIME = 'Mon'
COVER = 'http://renren.maoyun.tv/ftp/2018/0226/b_8ddd4f8d7fa60f961de34d5b6ab883db.jpg'
RESOURCE_ID = 31801
SEASON = 5


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X)'
                  ' AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}


class Script(ScriptBase):
    class Model(ScriptBase.Model):
        bangumi_name = BANGUMI_NAME
        # this cover may be failure
        cover = COVER
        # due_date = datetime(2017, 10, 1)
        update_time = UPDATE_TIME

    def get_download_url(self):
        """
        for another teleplay, you just need to change `season_to_download` and `resource_id`
        """
        # config
        season_to_download = SEASON
        resource_id = RESOURCE_ID

        # fetch and return dict
        resp = requests.get('http://m.zimuzu.tv/resource/{}'.format(resource_id), headers=HEADERS).content
        soup = BeautifulSoup(resp, 'lxml')

        data = soup.find('div', id='item1mobile')  # type: bs4.Tag
        data = data.find_all('a', class_='aurl')
        regex_expression = re.compile(
            r'http://m\.zimuzu\.tv/resource/item\?rid={}&season=(?P<season>\d+)&episode=(?P<episode>\d+)'.format(resource_id))
        result = {}
        print(data)
        for a_tag in data:
            page_url = a_tag['href'].replace('&amp;', '&')
            re_result = regex_expression.match(page_url)
            if re_result.group('season') == str(season_to_download):
                result[re_result.group('episode')] = page_url

        result = {int(key): page_url_to_magnet(p_url) for key, p_url in result.items()}
        result = {key: value for key, value in result.items() if key and value}
        return result


def page_url_to_magnet(url):
    """get magnet url from url like
    http://m.zimuzu.tv/resource/item?rid=33555&season=3&episode=6

    """
    response = requests.get(url, headers=HEADERS).content
    response = BeautifulSoup(response, 'lxml')
    for li in response.find_all('li', class_="mui-table-view-cell mui-collapse"):
        badge = li.find('span', class_="mui-badge")
        if '中文' in badge.text:
            for link in li.find_all('a', class_='copy'):
                if link['data-url'].startswith('magnet:?xt=urn:btih:'):
                    return link['data-url']


if __name__ == '__main__':
    s = Script()
    r = s.get_download_url()
    from pprint import pprint

    pprint(r)
