from requests import Session
from requests.auth import HTTPDigestAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from rich.console import Console
from rich.table import Table, Column
from bs4 import BeautifulSoup

disable_warnings(InsecureRequestWarning)
console = Console()

class TixatiAPI():
    def __init__(self, username, port, password) -> None:
        self.port = port
        self.username = username
        self.target_site = f"https://localhost:{self.port}"
        self.session = Session()
        self.session.verify= False
        self.auth(username, password)
    
    def auth(self, username, password):
        self.session.auth = HTTPDigestAuth(username, password)
    
    def get_home(self) -> str:
        return self.session.get(f'{self.target_site}/home').text
    
    def get_transfers(self) -> str:
        return self.session.get(f'{self.target_site}/transfers').text
    
    def add_magnet_transfer(self, link):
        self.session.post(f'{self.target_site}/transfers/action', {'addlinktext': link, "addlink": 'add'})
    
    def remove_transfer(self, ind):
        name = RequestScraper(self.get_transfers()).soup.find_all(class_='selection')[ind-1].attrs['name']
        self.session.post(f'{self.target_site}/transfers/action', {'remove': "Remove", name: 1, "removeconf": "Remove+Transfers"})
    
    def stop_transfer(self, ind):
        name = RequestScraper(self.get_transfers()).soup.find_all(class_="selection")[ind-1].attrs['name']
        self.session.post(f'{self.target_site}/transfers/action', {'stop': 'Stop', name:1})
    
    def start_transfer(self, ind):
        name = RequestScraper(self.get_transfers()).soup.find_all(class_="selection")[ind-1].attrs['name']
        self.session.post(f'{self.target_site}/transfers/action', {'start': 'Start', name:1})

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