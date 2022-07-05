from time import sleep
import requests
from rich import print

class Ludicrum():
    DEFAULT_TRIES = 5
    def __init__(self, username) -> None:
        self.USERNAME = username
        self.SCRAPI = 'https://torrentapi.org/pubapi_v2.php'
        self.HEADER = {'user-agent': f'Ludicrum/0.1.0 {self.USERNAME}'}
        self.APP_ID = 'Ludicrum'
        self.Rsession = requests.Session()
        self.TOKEN = self.token()
        self.DEFAULT_TRIES = 5
    
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
            'search_string': string
        }
        response = self.r(params).json()
        error_code = response.get('error_code')
        if error_code and tries > 0:
            match error_code:
                case 20:
                    print('Sitey problem...?')
                    sleep(2**min(tries- 4,0) + 2)
                    return self.search(string, tries - 1)
                case _:
                    print(error_code)
        elif tries < 0:
            raise Exception('Something went wrong')
        else:
            return response


client = Ludicrum('Omninight')
results = client.search('stranger things')['torrent_results']

for result in results:
    name = result['filename']
    category = result['category']
    link = result['download']
    print(name, category, link)


