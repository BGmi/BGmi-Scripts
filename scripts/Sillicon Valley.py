# coding=utf-8
"""download tv play from http://www.zimuzu.tv/, change config for another tv play"""
from __future__ import print_function, unicode_literals

import re

# import bs4
import requests
from bs4 import BeautifulSoup

from bgmi.script import ScriptBase

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
}


class Script(ScriptBase):
    class Model(ScriptBase.Model):
        bangumi_name = 'Sillicon Valley'
        # this cover may be failure
        cover = 'http://renren.maoyun.tv/ftp/2018/0226/b_8ddd4f8d7fa60f961de34d5b6ab883db.jpg'
        # due_date = datetime(2017, 10, 1)
        update_time = 'Mon'

    def get_download_url(self):
        """
        for another teleplay, you just need to change `season_to_download` and `resource_id`
        """
        # config
        season_to_download = 5
        resource_id = 31801

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
            print(page_url)
            re_result = regex_expression.match(page_url)
            print(re_result)
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
