from rich import print
import requests
import platform


uname = '; '.join(platform.uname())
pyver = platform.python_version()

header = {'user-agent': f'rarbgapi/0.532.0 ({uname}) python {pyver}'}

param = {'get_token': 'get_token', 'app_id': 'rarbgapi'}

session = requests.Session() 
req = requests.Request('Get', 'http://torrentapi.org/pubapi_v2.php', headers=header, params=param)
preq = req.prepare()
resp = session.send(preq)
resp.raise_for_status()

print(resp)

class Ludicrum():

    APP_ID = 'rarbgapi'

    def __init__(self) -> None:
        self._token = None
        self._scrape_site = "http://torrentapi.org/pubapi_v2.php"
    
    def user_agent(self) -> str:
        username = '; '.join(platform.uname())
        python_version = platform.python_version()
        return f'{self.APP_ID}/0.5.0 ({username}) python {python_version}'
    
    def token(self):
        params = {
            'get_token': 'get_token'
        }
        return self.requests('Get', self._scrape_site, params)
    
    def query(self, mode, **kwargs):
        params = {
            'mode': mode,
            'token': self.token
        }

        if 'extended_response' in kwargs:
            params['format'] = 'json_extended' \
                if kwargs['extended_response'] else 'json'
            del kwargs['extended_response']
        
        if 'categories' in kwargs:
            params['category'] = ';'.join(
                [str(c) for c in kwargs['categories']])
            del kwargs['categories']
        
        for key, value in kwargs.items():
            if key not in [
                'sort', 'limit', 'search_string', 'search_imdb', 'search_tvdb', 'search_themoviedb',
            ]:
                raise ValueError(f'unsupported parameter {key}')
            
            if value in None:
                continue

            params[key] = value
        
        return self.requests('Get', self._scrape_site, params)

    def requests(self, method, url, params={}):
        params.update({
            'app_id': self.APP_ID
        })

        headers = {'user-agent': self.user_agent()}

        session = requests.Session()
        request = requests.Request(method, url, params=params, headers=headers)
        prequest = req.prepare()
        response = session.send(prequest)
        response.raise_for_status()
        return response


client = Ludicrum()
client.
