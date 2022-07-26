from ludicrum import Ludicrum, LudicrousTorrent, console
from TixAPI import TixatiAPI, RequestScraper
from time import sleep
from os import system

from json import load
password = input('Enter your password: ')

with open('config.json', 'r') as f:
    file = load(f)
    username = file['username']
    client = Ludicrum(username=username)
    api = TixatiAPI(username=username, port=file['port'], password=password)

process = input("Input process name [add/remove/start/stop/info]: ").lower()

match process:
    case 'add':
        Ludicrum(username=username)
        service_choice = input("Search IMDB or TMDB: ").lower()
        search = input("Search: ")
        results = client.search(search, service=service_choice)["torrent_results"]
        datas = [LudicrousTorrent(result) for result in results]
        console.print(Ludicrum.torrent_table_generator(datas))
        torrent_index = int(input("Pick one: ")) - 1
        api.add_magnet_transfer(datas[torrent_index].link)
    case 'remove':
        ind = int(input("Index of transfer to remove: "))
        api.remove_transfer(ind)
    case 'start':
        ind = int(input("Index of transfer to start: "))
        api.start_transfer(ind)
    case 'stop':
        ind = int(input("Index of transfer to stop: "))
        api.stop_transfer(ind)
    case 'info':
        home_page = api.get_home()
        info_choice = input("What do you want to see [stats/logs/transfers]: ").lower()
        match info_choice:
            case 'stats':
                console.print(RequestScraper(home_page).get_homestats())
            case 'logs':
                console.print(RequestScraper(home_page).get_eventlog())
            case 'transfers':
                console.print(RequestScraper(api.get_transfers()).get_transfers())
                while True:
                    scrape_old = api.get_transfers()
                    sleep(1)
                    scrape_new = api.get_transfers()
                    if scrape_new != scrape_old:
                        system('cls')
                        console.print(RequestScraper(scrape_new).get_transfers())
            case _:
                console.print("Invalid argument")
    case _:
        console.print("Invalid input")