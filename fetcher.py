import requests
from rich import print
from bs4 import BeautifulSoup
import platform

# x = '+'.join(input().split())

scrapi = 'https://torrentapi.org/pubapi_v2.php'

def _get_user_agent():
    uname = '; '.join(platform.uname())
    pyver = platform.python_version()
    return f'Ludicrum/0.1.0 ({uname}) python {pyver}'

params_token = {'get_token': 'get_token', 'app_id': 'Ludicrum'}
headers_token = {'user-agent': _get_user_agent()}

session = requests.Session()
request = requests.Request('Get', scrapi, params=params_token, headers=headers_token)
preq = request.prepare()
response = session.send(preq)
response.raise_for_status()

token = response
print(token.json()['token'])

params_query = {
    'mode': 'search',
    'token': token.json()['token']
}



# r = requests.get(f'https://rarbgprx.org/torrents.php?search={x}').text
# soup = BeautifulSoup(r, 'html.parser')

# print(soup.prettify())

