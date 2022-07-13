#tixati api work here 
import requests
import urllib3
import json
from rich import print
from rich.console import Console
from rich.table import Table, Column
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

class TixatiAPI():
    def __init__(self) -> None:
        with open('config.json', 'r') as f:
            file = json.load(f)
            self.port = file['port']
            self.username = file['username']
        
        self.target_site = f"https://localhost:{self.port}"
        self.session = requests.Session()
        self.session.verify= False
    
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
    
    def get_homestats(self):
        html_table = self.soup.find('table', class_="homestats")
        returntable = Table(title=html_table.attrs['class'][0].upper(), expand=True, header_style="#bb546a",border_style="#395013", title_style='cyan', padding=0)

        for heading in html_table.find_all('th'):
            returntable.add_column(heading.text, justify="center")
        
        mini_tables = [Table(Column(), Column(justify="right"), expand=True, box= None, show_header=False) for _ in range(3)]

        for row in html_table.find_all('tr')[1:]:
            l = row.find_all('td')
            for i,data in enumerate(l):
                mini_tables[i].add_row(data.next.text, data.next.next.text)
            
        returntable.add_row(mini_tables[0], mini_tables[1], mini_tables[2])
        return returntable


client = TixatiAPI()

client.auth()
scraper = RequestScraper(client.get_home())
console.print(scraper.get_homestats())