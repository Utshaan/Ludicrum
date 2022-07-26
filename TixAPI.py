#tixati api work here 
import requests
import urllib3
import json
from rich import print
from rich.console import Console
from rich.table import Table, Column
from bs4 import BeautifulSoup
from time import sleep
import os

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
    
    def start_process(self, link):
        pass

class RequestScraper():
    def __init__(self, text) -> None:
        self.soup = BeautifulSoup(text, 'html.parser')
    
    def get_homestats(self):
        html_table = self.soup.find('table', class_="homestats")
        returntable = Table(title=html_table.attrs['class'][0].upper(), expand=True, header_style="#bb546a",border_style="#395013", title_style='cyan', padding=0)

        for heading in html_table.find_all('th'):
            returntable.add_column(heading.text, justify="center")
        
        mini_tables = [Table(Column(), Column(justify="right"), expand=True, box= None, show_header=False, highlight=True) for _ in range(3)]

        for row in html_table.find_all('tr')[1:]:
            l = row.find_all('td')
            for i,data in enumerate(l):
                mini_tables[i].add_row(data.next.text, data.next.next.text)
            
        returntable.add_row(mini_tables[0], mini_tables[1], mini_tables[2])
        return returntable
    
    def get_eventlog(self):
        html_table = self.soup.find('table', class_='eventlogview')
        returntable = Table(Column(), title=html_table.attrs['class'][0].upper(),expand=True, header_style="#bb546a", border_style="#395013", title_style='cyan', padding=0, show_header=False, highlight=True)

        for row in html_table.find_all('tr')[1:]:
            returntable.add_row(row.text[1:-1])

        return returntable
    
    def get_transfers(self):
        html_table = self.soup.find('table', class_='listtable xferslist')
        
        returnable = Table(title=html_table.attrs['class'][0].upper(), expand=True, header_style="#bb546a",border_style="#395013", title_style='cyan', padding=0, highlight=True)

        for heading in html_table.find_all('th'):
            if heading.text:
                returnable.add_column(heading.text)


        data = map(lambda x: 'N/A' if x == '' else x, (td.text.replace('\n', '') for td in html_table.find_all('td')[1:]))

        returnable.add_row(*data)
        
        return returnable


if __name__ == "__main__":
    client = TixatiAPI()

    client.auth()
    scraper_transfers = RequestScraper(client.get_transfers())
    scraper_home = RequestScraper(client.get_home())
    console.print(scraper_home.get_homestats())
    console.print(scraper_home.get_eventlog())
    console.print(RequestScraper(client.get_transfers()).get_transfers())
    while True:
        scrape_old = client.get_transfers()
        sleep(1)
        scrape_new = client.get_transfers()

        if scrape_new != scrape_old:
            os.system('cls')
            console.print(RequestScraper(scrape_new).get_transfers())
        
