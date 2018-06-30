import hashlib as hasher
from flask import Flask, request, jsonify
from pymongo import MongoClient
import simplejson as json
import os

from block import *
from transaction import Transaction
from keys import getEncodedKeys

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URL"),
                      username=os.getenv("MONGO_USERNAME"),
                      password=os.getenv("MONGO_PASSWORD"),
                      authSource=os.getenv("MONGO_AUTHSOURCE"),
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
            if (transaction["sender"] == public_key):
                balance = balance - transaction["amount"]

    return balance

def getPendingBalance(public_key):
    balance = 0
    for transaction in transactions:
        print(transaction)
        if (transaction.reciever == public_key):
                balance = balance + transaction.amount
        if (transaction.sender == public_key):
            balance = balance - transaction.amount

    return balance

def hasSufficentFunds(public_key, amount):
    balance = getBalance(public_key) + getPendingBalance(public_key)
    if (balance >= amount):
        return True
    return False

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
    block = Block(req["index"], req["transactions"], req["nonce"], previousBlock.hash, req["hash"])
    if not block.validate():
        return jsonify({"error": "Invalid hash"}), 400

    transactionStringArr = []
    for transaction in json.loads(block.transactions):
        transactionObject = Transaction(transaction["sender"], transaction["reciever"], transaction["amount"], transaction["signature"])
        if not transaction["sender"] == "MINER":
            if not transactionObject.verifyTransaction(transactionObject.sender):
                return jsonify({"error": "Bad Transaction in block"}), 400
            for trans in transactions:
                if trans.signature == transactionObject.signature:
                    print(trans.signature)
                    transactions.remove(trans)
                    break
            else:
                trans = None
            if trans == None:
                return jsonify({"error": "Bad Transaction in block"}), 400
        elif transaction["sender"] == "MINER":
            print("New block attempt by [" + transactionObject.reciever + "]")
            if transactionObject.amount != 1:
                return jsonify({"error": "Bad Transaction in block"}), 400

        transactionStringArr.append(str(transactionObject.amount) + " coin(s) " + transactionObject.sender + " --> " + transactionObject.reciever)
    
    insertBlock = Block(block.index, block.transactions, block.nonce, block.hash)
    db.blocks.insert_one(insertBlock.__dict__)
    blockchain.append(block)
    previousBlock = block

    print("--New block successfully mined!--")
    print("Transactions:")
    for tStr in transactionStringArr:
        print(tStr)
    print("----------------")
    print("")
    return jsonify({"message": "New block successfully mined!"}), 200

@app.route("/transactions", methods=['POST'])
def createTransaction():
    req = request.get_json()
    transactionObject = Transaction(req["sender"], req["reciever"], req["amount"], req["signature"])
    if not transactionObject.verifyTransaction(transactionObject.sender):
        return jsonify({"error": "Bad Transaction"}), 400

    if not hasSufficentFunds(transactionObject.sender, transactionObject.amount):
        return jsonify({"error": "Insufficient Balance"}), 400

    transactions.append(transactionObject)
    return jsonify({"response": "Transaction Posted"})

@app.route("/transactions", methods=['GET'])
def getTransactions():
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
