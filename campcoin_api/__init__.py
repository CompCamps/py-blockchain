
import requests
import urllib
from block import Block
from transaction import Transaction

class CampCoin:
    def __init__(self, server):
        self.server = server

    def postBlock(self, block):
        req = requests.post(self.server + '/api/mine', json=block)
        if req.status_code == 200:
            return True
        else:
            print(req.json()["error"])
            return False

    def postTransaction(self, transaction):
        req = requests.post(self.server + '/api/transactions', json=transaction)
        if req.status_code == 200:
            return True
        else:
            print(req.json()["error"])
            return False

    def getBalance(self, public_key):
        key = {'public_key': public_key}
        req = requests.get(self.server + '/api/balance?' + urllib.parse.urlencode(key))
        if req.status_code == 200:
            return req.text
        else:
            return False

    def getCurrentBlock(self):
        req = requests.get(self.server + '/api/current').json()
        currentBlock = Block(req['index'], req['transactions'], req['nonce'], req['previousHash'], req['hash'])
        return currentBlock

    def getCurrentTransactions(self):
        req = requests.get(self.server + '/api/transactions')
        transactions = []
        for trans in req.json():
            transactions.append(Transaction(trans['sender'], trans['reciever'], trans['amount'], trans['signature']))
        return transactions