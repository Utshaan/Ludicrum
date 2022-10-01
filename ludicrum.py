from time import sleep
from requests import Session, Request, get, request
from rich import print
from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup

console = Console()


class Ludicrum:
    DEFAULT_TRIES = 5

    def __init__(self, username) -> None:
        self.USERNAME = username
        self.SCRAPI = "https://torrentapi.org/pubapi_v2.php"
        self.HEADER = {"user-agent": f"Ludicrum/0.1.0 {self.USERNAME}"}
        self.APP_ID = "Ludicrum"
        self.Rsession = Session()
        self.TOKEN = self.token()

    def r(self, params):
        req = Request("Get", self.SCRAPI, params=params, headers=self.HEADER)
        prep = req.prepare()
        resp = self.Rsession.send(prep)
        resp.raise_for_status()

        return resp

    def token(self):
        return self.r({"get_token": "get_token", "app_id": self.APP_ID}).json()["token"]

    @staticmethod
    def get_IMDB_ID(search):
        soup = BeautifulSoup(
            get(f"https://www.imdb.com/find", params={"q": search}).text, "html.parser"
        )
        data = list(map(lambda td: (td.text, td.findAll("a")[-1].attrs["href"][7:-1]) , soup.find("table", class_="findList").findAll("td", class_="result_text")))
        
        return Ludicrum.pick_ID(data)
    
    @staticmethod
    def get_TVDB_ID(search):
        pass

    @staticmethod
    def get_THE_MOVIE_DB_ID(search):
        response = request("GET", "https://www.themoviedb.org/search", headers={"user-agent": "Ludicrum/0.1.0"}, params={"query":search})
        soup = BeautifulSoup(
            response.text, "html.parser"
        )
        data = list(map(lambda td: (td.text, td.attrs["href"].split("/")[-1]), soup.find(class_="results flex").findAll(class_="result")[1::2]))

        return Ludicrum.pick_ID(data)

    @staticmethod
    def pick_ID(data):

        table = Table(title="Show Info")
        table.add_column(
            "No.", justify="right", style="cyan", header_style="red"
        )
        table.add_column("Name", style="magenta")
        table.add_column("ID", justify="center", style="green")

        for index, info in enumerate(data):
            NAME, ID = info
            table.add_row(
                str(index + 1) + ".", NAME, ID
            )

        console.print(table)

        pick = input("\nPick index from table: ")
        return data[int(pick) - 1][1]

    def search(self, string, service="IMDB", tries=DEFAULT_TRIES):
        params = {
            "app_id": self.APP_ID,
            "mode": "search",
            "token": self.TOKEN,
            "format": "json_extended",
            # 'ranked': 0
        }

        if service == "imdb":
            params["search_imdb"] = Ludicrum.get_IMDB_ID(string)
        elif service == "tmdb":
            params["search_themoviedb"] = Ludicrum.get_THE_MOVIE_DB_ID(string)

        response = self.r(params).json()
        error_code = response.get("error_code")
        if error_code and tries > 0:
            match error_code:
                case 20:
                    sleep(2)
                    return self.search(string, tries - 1)
                case 10:
                    console.print("[bold red]NOT THERE!!![/bold red]")
                    raise SystemExit
                case _:
                    return response
        if not error_code:
            return response
        else:
            print(response)
            return {"torrent_results": ""}

    def search_text(self, string, tries=DEFAULT_TRIES):
        params = {
            "app_id": self.APP_ID,
            "mode": "search",
            "token": self.TOKEN,
            "format": "json_extended",
            "search_string": string,
            'category': "27;28;40;53;32"
        }

        response = self.r(params).json()
        error_code = response.get("error_code")
        if error_code and tries > 0:
            match error_code:
                case 20:
                    sleep(2)
                    return self.search(string, tries - 1)
                case 10:
                    console.print("[bold red]NOT THERE!!![/bold red]")
                    raise SystemExit
                case _:
                    return response
        if not error_code:
            return response
        else:
            print(response)
            return {"torrent_results": ""}
    
    def torrent_table_generator(datas):
        torrent_table = Table(
            title="Table of Torrents",
            header_style="#bb546a",
            expand=True,
            border_style="#395013",
        )
        torrent_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
        torrent_table.add_column("Name", style="#00e5d3")
        torrent_table.add_column("Size", style="yellow", justify="right")
        torrent_table.add_column("S", style="green", justify="right")
        torrent_table.add_column("L", style="#e35b00")

        for index, data in enumerate(datas):
            torrent_table.add_row(
                str(index + 1), data.title, data.size, str(data.seeders), str(data.leechers)
            )

        return torrent_table


class LudicrousTorrent:
    def __init__(self, info):
        self.info = info
        self.title = info["title"]
        self.category = info["category"]
        self.link = info["download"]
        self.seeders = info["seeders"]
        self.leechers = info["leechers"]
        self.size = (
            str(round(int(info["size"]) / (2**30), 2)) + " GB"
            if info["size"] > 1073741824
            else str(round(int(info["size"]) / (2**20), 2)) + " MB"
        )
        self.published_date = info["pubdate"]
        self.episode_info = info["episode_info"]
        self.rank = info["ranked"]
        self.download = False
