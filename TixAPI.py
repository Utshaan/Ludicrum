#tixati api work here 
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
username = 'omninight'

class TixatiAPI():
    def __init__(self, username) -> None:
        self.target_site = "https://localhost:port"
        self.session = requests.Session()
        self.session.verify= False
        self.username = username
    
    def auth(self):
        self.session.auth = requests.auth.HTTPDigestAuth('omninight', 'nimda')
    
    def get_home(self):
        return self.session.get(f'{self.target_site}/home').text
    
    def get_transfers(self):
        return self.session.get(f'{self.target_site}/transfers').text
    
    def add_magnet_transfer(self, link):
        self.session.post(f'{self.target_site}/transfers/action', {'addlinktext': link, "addlink": 'add'})


dclient = TixatiAPI(username)

dclient.auth()