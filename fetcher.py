import requests
from bs4 import BeautifulSoup
from rich import print, table

# x = input("What do you wanna watch today: ")

# x = x.replace(" ", "+")

# cookies = dict( aby='2', expla='1', expla3='1', gaDts48g='q8h5pp9t', ppu_delay_9ef78edf998c4df1e1636c9a474d9f47='1', ppu_main_9ef78edf998c4df1e1636c9a474d9f47='1', ppu_sub_9ef78edf998c4df1e1636c9a474d9f47='3', skt='FZMSYi9dub', use_alt_cdn='1')

# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'}

# r = requests.get(f"https://rarbgprx.org/torrents.php?search={x}", headers=header, cookies=cookies)

# soup = BeautifulSoup(r.text, features='html.parser')

# print(soup.prettify())

with open("h.html", 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

print(soup.prettify())