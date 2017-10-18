# coding=utf-8
from __future__ import print_function, unicode_literals

import re
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from bgmi.script import ScriptBase
from bgmi.utils import print_error, parse_episode
from bgmi.config import IS_PYTHON3


class Script(ScriptBase):

    class Model(ScriptBase.Model):
        bangumi_name = 'Rick and Morty Season 3'
        cover = 'http://img.itvfans.com/wp-content/uploads/31346.jpg'
        due_date = datetime(2017, 10, 1)
        update_time = 'Wed'

    def get_download_url(self):
        # fetch and return dict
        resp = requests.get('http://www.itvfans.com/fenji/313463.html').text
        html = bs(resp, 'lxml')

        data = html.find(attrs={'id': '31346-3-720p'})

        if not data:
            print_error('No data found, maybe the script is out-of-date.', exit_=False)
            return {}

        ret = {}
        match_episode = re.compile('Rick\.and\.Morty\.S03E(\d+)\.720p')
        for row in data.find_all('a', attrs={'type': 'magnet'}):
            link = row.attrs['href']
            episode = match_episode.findall(link)
            if episode:
                ret[int(episode[0])] = link

        return ret


if __name__ == '__main__':
    s = Script()
    print(s.get_download_url())
