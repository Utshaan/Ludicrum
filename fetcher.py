from rich.console import Console
from rich.table import Table
import requests
from bs4 import BeautifulSoup


def get_show_ID(search):

    console = Console()

    soup = BeautifulSoup(requests.get(f'https://www.imdb.com/find?q={search}').text, 'html.parser')

    l = soup.find('table', class_='findList').findAll('td', class_='result_text')

    table = Table(title="Show Info")
    table.add_column("No.", justify='right', style="cyan", no_wrap=True, header_style='red')
    table.add_column("Name", style="magenta")
    table.add_column("ID", justify="center", style="green")

    for index,td in enumerate(l):
        table.add_row(str(index+1)+'.', td.text, td.findAll('a')[-1].attrs['href'])
    
    console.print(table)

    pick = input('\nPick index from table: ')
    return l[int(pick)-1].findAll('a')[-1].attrs['href'][7:-1]
    

x = '+'.join(input('Search: ').strip())

get_show_ID(x)