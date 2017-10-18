# coding=utf-8
from __future__ import print_function, unicode_literals

import re
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from bgmi.script import ScriptBase
from bgmi.utils import print_error


class Script(ScriptBase):

    class Model(ScriptBase.Model):
        bangumi_name = 'Mr Robot Season 3'
        cover = 'http://www.meijuxz.com/Uploads/vod/2017-10-13/59e02649ee585.jpg'
        # due_date = datetime(2017, 10, 1)
        update_time = 'Thu'

    def get_download_url(self):
        # fetch and return dict
        resp = requests.get('http://www.dyjihe.com/download/567f/magnet.html').content
        html = bs(resp, 'lxml')

        data = html.find_all(attrs={'class': 'thunder-deal'})

        if not data:
            print_error('No data found, maybe the script is out-of-date.', exit_=False)
            return {}

        ret = {}
        match_episode = re.compile('第([\d]+)集')
        for row in data:
            link = row.attrs['data-link']
            episode = match_episode.findall(row.text)
            if episode:
                ret[int(episode[0])] = link

        return ret


if __name__ == '__main__':
    s = Script()
    print(s.get_download_url())
