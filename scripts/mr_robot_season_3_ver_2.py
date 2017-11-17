# coding=utf-8

import bs4
import requests
from bs4 import BeautifulSoup

from bgmi.script import ScriptBase

import re

ua = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}


class Script(ScriptBase):
    class Model(ScriptBase.Model):
        bangumi_name = 'Mr Robot Season 3'
        # this cover may be failure
        cover = 'http://175.6.228.3/ftp/2017/1008/b_fc47b982916ac306498010071784b49d.jpg'
        # due_date = datetime(2017, 10, 1)
        update_time = 'Thu'

    def get_download_url(self):
        id = 33555
        # fetch and return dict
        resp = requests.get('http://m.zimuzu.tv/resource/{}'.format(id), headers=ua).content
        soup = BeautifulSoup(resp, 'lxml')

        data = soup.find('div', id='item1mobile')  # type: bs4.Tag
        # data = data.find(class_='panel panel-white')
        data = data.find_all('a', class_='aurl')
        regex_expression = re.compile(
            r'http://m\.zimuzu\.tv/resource/item\?rid={}&season=(?P<season>\d+)&episode=(?P<episode>\d+)'.format(id))
        result = {}
        for a in data:
            page_url = a['href']
            re_result = regex_expression.match(page_url)
            if re_result.group('season') == str(3):
                result[re_result.group('episode')] = page_url

        result = {int(key): page_url_to_magnet(p_url) for key, p_url in result.items()}
        return result


def page_url_to_magnet(url: str):
    r = requests.get(url, headers=ua).content
    r = BeautifulSoup(r, 'lxml')
    for link in r.find_all('a', class_='copy'):
        if link['data-url'].startswith('magnet:?xt=urn:btih:'):
            return link['data-url']


if __name__ == '__main__':
    s = Script()
    s.get_download_url()
