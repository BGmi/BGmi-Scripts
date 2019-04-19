import base64

import requests
from bgmi.script import ScriptBase

HEADER = {
    'Host': 'a.allappapi.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.12.1',
}
ACCESS_KEY = base64.decodebytes(b'NTE5ZjljYWI4NWM4MDU5ZDE3NTQ0OTQ3azM2MWE4Mjc=').decode()

print(ACCESS_KEY)


def get_params(**kwargs):
    p = {
        'g': 'api/v2',
        'accesskey': ACCESS_KEY,
        'client': 2,
    }
    p.update(kwargs)
    return p


class Script(ScriptBase):
    rid = '11005'
    season = 12

    class Model(ScriptBase.Model):
        bangumi_name = '生活大爆炸S12'
        cover = 'http://tu.jstucdn.com/ftp/2018/1023/b_863118231740caaf847a935ddab3fd5d.jpg'
        update_time = 'Tue'

    def get_download_url(self):
        # fetch and return dict
        res = {}
        for season in self.get_season_json(self.rid)['data']['season']:
            if season['season'] == self.season:
                for episode in season['episode']:
                    resp = requests.get(
                        'http://a.allappapi.com/index.php',
                        params=get_params(
                            a='resource_item',
                            id=self.rid,
                            season=season['season'],
                            episode=episode
                        ),
                        headers=HEADER
                    )
                    for item in resp.json()['data']['item_list']:
                        if item.get('format') == 'MP4' or item.get("format_tip") == "中文字幕版":
                            for link in item['files']:
                                if link['way'] == '2':
                                    res[episode] = link['address']

        return res

    @staticmethod
    def get_season_json(rid):
        return requests.get(
            'http://a.allappapi.com/index.php',
            params=get_params(a='resource', g='api/v2', rid=rid, m='index'),
            headers=HEADER,
        ).json()


if __name__ == '__main__':
    from pprint import pprint
    pprint(Script().get_download_url())
