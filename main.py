import datetime as date
import requests
from block import *
from transaction import *
import simplejson as json
import random
from lib.keys import getEncodedKeys
import os
import time
import urllib.parse
from lib.prefix import Prefix

public_key, _ = getEncodedKeys()
server = "https://campcoin.herokuapp.com"
prefix = Prefix()

def mineCycle():
    prefix.fetch()
    try:
        while True:
            newBlock = mine(getCurrentBlock(), getCurrentTransactions())
            submitNewBlock(newBlock)
    except KeyboardInterrupt:
        pass

def mineDebug(previousBlock, transactions):
    os.system('clear')
    print("Status: Currently mining")
    print("Current prefix: " + prefix.get())
    print("Press ctrl+C to return to menu.. ")
    print("")
    print("Previous block: ")
    previousBlock.display()
    print("")

# Attempts to mine a new block
def mine(previousBlock, transactions):
    nonce = 0
    newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)
    mineDebug(previousBlock, transactions)

    beginTimestamp = date.datetime.now()
    while (not newBlock.validate(prefix.get())):
        nonce = random.randint(1, 100000000000)
        newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)

        if ((date.datetime.now() - beginTimestamp).total_seconds() > 5):
            beginTimestamp = date.datetime.now()
            previousBlock = getCurrentBlock()
            transactions = getCurrentTransactions()
            prefix.fetch()
            mineDebug(previousBlock, transactions)
    return newBlock

def getCurrentBlock():
    req = requests.get(server + '/api/current').json()
    currentBlock = Block(req['index'], req['transactions'], req['nonce'], req['previousHash'], req['hash'])
    return currentBlock

def getCurrentTransactions():
    transactions = requests.get(server + '/api/transactions').json()
    transaction = Transaction("MINER", public_key, 1)
    transactions.append(transaction)
    return transactions

def submitNewBlock(newBlock): 
    req = requests.post(server + '/api/mine', json=newBlock)
    newBlock.display()
    if req.status_code == 200:
        print("**Successfully mined block!**")
        time.sleep(5)

def postTransaction(reciever, amount):
    transaction = Transaction(public_key, reciever, amount)
    req = requests.post(server + '/api/transactions', json=transaction)
    return req

def sendCoins():
    os.system('clear')
    reciever = input("Enter address to send coins to: ")
    amount = input("Enter amount to send: ")
    res = postTransaction(reciever, float(amount))
    if res.status_code == 200:
        print("Transaction successfully sent!")
    else:
        print(res.json()["error"])

    input("Press any key to return to menu...")


def checkBalance():
    key = {'public_key': public_key}
    req = requests.get(server + '/api/balance?' + urllib.parse.urlencode(key))
    os.system('clear')
    print("Your public key is: " + public_key)
    print("Your balance is: " + req.text)
    print("")
    input("Press any key to return to menu...")

while(1):
    os.system('clear')
    print("Welcome to Campcoin miner")
    print("")
    print("Select an option:")
    print("(M) Start mining")
    print("(T) Send coins")
    print("(B) Check your balance or view your Public Key")
    print()
    print("Press Ctrl+C to exit")
    print()
    option = input("Enter a selection: ")

    if option == "B":
        checkBalance()

    if option == "M":
        mineCycle()

    if option == "T":
        sendCoins()