import datetime as date
import requests as requests
from block import *
from transaction import *
import simplejson as json
import random
from keys import getEncodedKeys

public_key, _ = getEncodedKeys()

#transaction = Transaction("MINER", public_key, 1)
#print(transaction.signature)

#print(transaction.verifyTransaction("/pJ+3b4y3iOwIF+bTqQQT78xeuvoJxSUb3QmHNkpGP61ZbBXjq0cFclTqPI5pevQSniw/1Yz+snqDBCkPbWPRw=="))

# Attempts to mine a new block
def mine(previousBlock):
    nonce = 0
    transactions = []
    transaction = Transaction("MINER", public_key, 1)
    transactions.append(transaction)
    #print(transaction.verifyTransaction(public_key))
    newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)
    while (not newBlock.validate()):
        nonce = random.randint(1, 100000000000)
        newBlock = nextBlock(previousBlock, json.dumps(transactions), nonce)
    return newBlock

def getCurrentBlock():
    req = requests.get('http://localhost:5000/current').json()
    currentBlock = Block(req['index'], req['transactions'], req['nonce'], req['previousHash'], req['hash'])
    return currentBlock

def submitNewBlock(newBlock):
    print(json.dumps(newBlock))
    req = requests.post('http://localhost:5000/mine', json=newBlock)
    print(req)

while(1):
    beginTimestamp = date.datetime.now()
    newBlock = mine(getCurrentBlock())
    time_taken = date.datetime.now() - beginTimestamp
    print("Took " + str(time_taken.total_seconds()))
    submitNewBlock(newBlock)

# # Mine 10 blocks
# for i in range(10):
#     beginTimestamp = date.datetime.now()

#     newBlock = mine()
#     blockchain.append(newBlock)
#     previousBlock = newBlock

#     time_taken = date.datetime.now() - beginTimestamp

#     print("-- New block mined! --")
#     print("Took " + str(time_taken.total_seconds()))
#     newBlock.display()