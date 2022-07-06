# from time import sleep
# import requests
# from rich import print
# from bs4 import BeautifulSoup
# import platform

# # x = '+'.join(input().split())

# scrapi = 'https://torrentapi.org/pubapi_v2.php'

# def _get_user_agent():
#     username = 'Omninight'
#     return 'Ludicrum/0.1.0 {username}'

# params_token = {'get_token': 'get_token', 'app_id': 'Ludicrum'}
# headers_token = {'user-agent': _get_user_agent()}

# session = requests.Session()
# request = requests.Request('Get', scrapi, params=params_token, headers=headers_token)
# preq = request.prepare()
# response = session.send(preq)
# response.raise_for_status()

# token = response
# # print(token.json())

# mode = input('What do you wanna do: ')
# search = input('Name the show: ')

# params_query = {
#     'app_id': 'Ludicrum',
#     'mode': mode,
#     'token': token.json()['token'],
#     'search_string': search
# }

# request = requests.Request('Get', scrapi, params=params_query, headers=headers_token)
# preq = request.prepare()
# response = session.send(preq)
# response.raise_for_status()

# print(response.json())
