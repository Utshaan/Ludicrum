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