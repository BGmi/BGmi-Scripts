import feedparser
import requests
from bgmi.script import ScriptBase
import re


class Script(ScriptBase):
    class Model(ScriptBase.Model):
        bangumi_name = '生活大爆炸S12'
        cover = 'http://tu.jstucdn.com/ftp/2018/1023/b_863118231740caaf847a935ddab3fd5d.jpg'
        update_time = 'Mon'

    def get_download_url(self):
        # fetch and return dict
        res = {}
        resp = requests.get('http://diaodiaode.me/rss/feed/11005')
        feeds = feedparser.parse(resp.text)
        for item in feeds['entries']:
            if 'magnet' in item:
                res[self.parse_episode(item['title'])] = item['magnet']
            print(item['title'])
        return res

    @staticmethod
    def parse_episode(title: str) -> int:
        """
        解析美剧集数

        Args:
            title: 美剧title

        Returns:
            int: episode for this title

        """
        m = re.findall(r'S12E(\d+)', title)
        if m:
            return int(m[0])
        return 0


if __name__ == '__main__':
    print(Script().get_download_url())
