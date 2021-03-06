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
        bangumi_name = 'Mr Robot Season 4'
        cover = 'https://www.333tv.com/wp-content/uploads/2019/08/333tv288022311624311.jpg'
        due_date = datetime(2020, 1, 30)
        update_time = 'Mon'

    def get_download_url(self):
        # fetch and return dict
        resp = requests.get('https://www.333tv.com/50611/').content
        html = bs(resp, 'lxml')

        data = html.find_all(attrs={'id': 'playtab'})

        if not data or len(data) != 3:
            print_error('No data found, maybe the script is out-of-date.', exit_=False)
            return {}

        data = data[1]

        ret = {}
        match_episode = re.compile('第([\d]+)集')
        for row in data.find_all('ul')[2].find_all('li'):
            link = row.a.attrs['href']
            episode = match_episode.findall(row.text)
            if episode:
                ret[int(episode[0])] = link

        return ret


if __name__ == '__main__':
    s = Script()
    print(s.get_download_url())
