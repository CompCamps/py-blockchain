import requests

server = "https://campcoin.herokuapp.com"

class Prefix:
    def __init__(self):
        self.fetch()

    def get(self):
        return self.prefix

    def fetch(self):
        req = requests.get(server + '/api/prefix')
        self.prefix = req.text.strip()