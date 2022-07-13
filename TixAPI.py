#tixati api work here 
import requests
import urllib3
import json
from rich import print
from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
username = 'omninight'
console = Console()

class TixatiAPI():
    def __init__(self, username) -> None:
        with open('config.json', 'r') as f:
            file = json.load(f)
            self.port = file['port']
        
        self.target_site = f"https://localhost:{self.port}"
        self.session = requests.Session()
        self.session.verify= False
        self.username = username
    
    def auth(self):
        self.session.auth = requests.auth.HTTPDigestAuth('omninight', 'nimda')
    
    def get_home(self) -> str:
        return self.session.get(f'{self.target_site}/home').text
    
    def get_transfers(self) -> str:
        return self.session.get(f'{self.target_site}/transfers').text
    
    def add_magnet_transfer(self, link):
        self.session.post(f'{self.target_site}/transfers/action', {'addlinktext': link, "addlink": 'add'})

class RequestScraper():
    def __init__(self, text) -> None:
        self.soup = BeautifulSoup(text, 'html.parser')
    
    def get_table(self):
        tables = self.soup.find_all('table')

        table_2_rows = tables[1].find_all('tr')[1:]
        
        table_2 = Table(title=tables[1].attrs['class'][0].upper(), expand=True, header_style="#bb546a",border_style="#395013", title_style='cyan', padding=0)

        for i in tables[1].find_all('th'):
            table_2.add_column(i.text)
        
        mini_tables = [Table() for i in range(3)]
        for table in mini_tables:
            table.add_column('Item')
            table.add_column('Value', justify='right')
            table.expand = True
            table.box = None

        for row in table_2_rows:
            l = row.find_all('td')
            for i,data in enumerate(l):
                mini_tables[i].add_row(data.next.text, data.next.next.text)
            
        table_2.add_row(mini_tables[0], mini_tables[1], mini_tables[2])
        console.print(table_2)


client = TixatiAPI(username)

client.auth()
scraper = RequestScraper(client.get_home())
scraper.get_table()