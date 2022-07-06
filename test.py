from time import sleep
import requests
from rich import print, table
from bs4 import BeautifulSoup

class Ludicrum():
    DEFAULT_TRIES = 5
    def __init__(self, username) -> None:
        self.USERNAME = username
        self.SCRAPI = 'https://torrentapi.org/pubapi_v2.php'
        self.HEADER = {'user-agent': f'Ludicrum/0.1.0 {self.USERNAME}'}
        self.APP_ID = 'Ludicrum'
        self.Rsession = requests.Session()
        self.TOKEN = self.token()
        # self.DEFAULT_TRIES = 5
    
    def r(self, params):
        req = requests.Request('Get', self.SCRAPI, params=params, headers=self.HEADER)
        prep = req.prepare()
        resp = self.Rsession.send(prep)
        resp.raise_for_status()

        return resp

    def token(self):
        return self.r({'get_token': 'get_token', 'app_id':self.APP_ID}).json()['token']
    
    def search(self, string, tries=DEFAULT_TRIES):
        params = {
            'app_id': self.APP_ID,
            'mode': 'search',
            'token': self.TOKEN,
            'search_string': string,
            'format': 'json_extended',
            # 'ranked': 0
        }
        response = self.r(params).json()
        error_code = response.get('error_code')
        if error_code and tries > 0:
            match error_code:
                case 20:
                    sleep(2)
                    return self.search(string, tries - 1)
                case _:
                    return error_code
        if not error_code:
            return response
        else:
            print(response)
            return {'torrent_results': ''}

class LudicrousTorrent():
    def __init__(self, info):
        self.title = info['title']
        self.category = info['category']
        self.link = info['download']
        self.seeders = info['seeders']
        self.leechers = info['leechers']
        self.size = round(int(info['size'])/(2**30),2)
        self.published_date = info['pubdate']
        self.episode_info = info['episode_info']
        self.rank = info['ranked']
        self.download = False
        


client = Ludicrum('Omninight')
ask = '+'.join(input("Search: ").split())

# x = requests.get(f'https://thetvdb.com/search?query={ask}')
# soup = BeautifulSoup(x.text, 'html.parser')
# print(soup)
# raise SystemExit


results = client.search(ask)['torrent_results']

datas = [print(f'[yellow]{LudicrousTorrent(result)}[/yellow]') for result in results]


# """{
#         'title': 'Ms.Marvel.S01E05.2160p.DSNP.WEB-DL.DDP5.1.Atmos.DV.MP4.x265-DVSUX[rartv]',
#         'category': 'Movies/TV-UHD-episodes',
#         'download': 'magnet:?xt=urn:btih:33dc4fcdcc078e5b1512fab87d93712d38614cf2&dn=Ms.Marvel.S01E05.2160p.DSNP.WEB-DL.DDP5.1.Atmos.DV.MP4.x265-DV
# SUX%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2860&tr=udp%3A%2F%2F9.rarbg.to%3A2780&tr=udp%3A%2
# F%2Ftracker.tallpenguin.org%3A15770&tr=udp%3A%2F%2Ftracker.slowcheetah.org%3A14780',
#         'seeders': 70,
#         'leechers': 38,
#         'size': 4770025745,
#         'pubdate': '2022-07-06 07:42:57 +0000',
#         'episode_info': {'imdb': 'tt10857164', 'tvrage': None, 'tvdb': '368612', 'themoviedb': '92782'},
#         'ranked': 1,
#         'info_page': 'https://torrentapi.org/redirect_to_info.php?token=ynoq2zfx4p&p=2_8_1_9_8_0_2__33dc4fcdcc'
#     }
# """

