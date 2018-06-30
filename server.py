import hashlib as hasher
from flask import Flask, request, jsonify
from pymongo import MongoClient
import simplejson as json
import configparser

from block import *
from transaction import Transaction
from keys import getEncodedKeys

Config = configparser.ConfigParser()
Config.read("config.ini")

app = Flask(__name__)
client = MongoClient(Config["MongoDB"]["url"],
                      username=Config["MongoDB"]["username"],
                      password=Config["MongoDB"]["password"],
                      authSource=Config["MongoDB"]["authsource"],
                      authMechanism='SCRAM-SHA-1')

transactions = []
blockchain = []
db = client.campcoin
blocks = db.blocks.find()
for block in blocks:
    b = Block(block['index'], block['transactions'], block['nonce'], block['hash'])
    blockchain.append(b)

#db.blocks.insert_one(createGenesisBlock().__dict__)
previousBlock = blockchain[-1]

# make transaction endpoint to get pending transctions
# endpoint to post new transaction
# verify new transactions on post
# verify transactions included with mined block

def getBalance(public_key):
    balance = 0
    for block in blockchain:
        for transaction in json.loads(block.transactions):
            if (transaction["reciever"] == public_key):
                balance = balance + transaction["amount"]

    return balance

@app.route('/balance', methods=["POST"])
def balance():
    req = request.get_json()
    return str(getBalance(req["public_key"]))

@app.route('/chain')
def chain():
    global blockchain
    return jsonify(blockchain)

@app.route("/current")
def current():
    global previousBlock
    return jsonify(previousBlock)

@app.route("/mine", methods=['POST'])
def mine():
    global previousBlock
    global db

    req = request.get_json()
    print(req)
    block = Block(req["index"], req["transactions"], req["nonce"], previousBlock.hash, req["hash"])
    if not block.validate():
        return False

    for transaction in json.loads(block.transactions):
        transactionObject = Transaction(transaction["sender"], transaction["reciever"], transaction["amount"], transaction["signature"])
        if not transaction["sender"] == "MINER" and not transactionObject.verifyTransaction(transactionObject.sender):
            return False
    
    insertBlock = Block(block.index, block.transactions, block.nonce, block.hash)
    db.blocks.insert_one(insertBlock.__dict__)
    blockchain.append(block)
    previousBlock = block

    print(str(block.validate()))
    return str(block.validate())

@app.route("/transaction", methods=['POST'])
def transaction():
    req = request.get_json()



if __name__ == '__main__':
    app.run(debug=True)
