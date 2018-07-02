import hashlib as hasher
from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
import simplejson as json

from block import *
from transaction import Transaction

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

template_dir = os.path.abspath('./frontend')
app = Flask(__name__, template_folder=template_dir, static_url_path=template_dir)
client = MongoClient(os.getenv("MONGO_URL"),
                      username=os.getenv("MONGO_USERNAME"),
                      password=os.getenv("MONGO_PASSWORD"),
                      authSource=os.getenv("MONGO_AUTHSOURCE"),
                      authMechanism='SCRAM-SHA-1')

db = client.campcoin
prefix = "decaf0"

#genesis block
#db.blocks.insert_one(createGenesisBlock().__dict__)

def getBlockchain():
    blockchain = []
    blocks = db.blocks.find()
    for block in blocks:
        b = Block(block['index'], block['transactions'], block['nonce'], block['previousHash'], block['hash'])
        blockchain.append(b)
    return blockchain
    
def findTransactions():
    transactions = []
    for transaction in db.transactions.find():
        t = Transaction(transaction['sender'], transaction['reciever'], transaction['amount'], transaction['signature'])
        transactions.append(t)
    return transactions

def getBalance(public_key):
    balance = 0
    blockchain = getBlockchain()
    for block in blockchain:
        for transaction in json.loads(block.transactions):
            if (transaction["reciever"] == public_key):
                balance = balance + transaction["amount"]
            if (transaction["sender"] == public_key):
                balance = balance - transaction["amount"]

    return balance

def getPendingBalance(public_key):
    balance = 0
    transactions = findTransactions()
    for transaction in transactions:
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

@app.route('/')
def indexRoute():
    return render_template("index.html")
    
@app.route('/transactions')
def transactionsRoute():
    return render_template("transactions.html")

@app.route('/balance')
def balanceRoute():
    return render_template("balance.html")

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('frontend', path)

@app.route('/api/balance')
def balance():
    key = request.args.get('public_key')
    balance = getBalance(key) + getPendingBalance(key)
    return str(balance)

@app.route('/api/chain')
def chain():
    blockchain = getBlockchain()
    return jsonify(blockchain)

@app.route("/api/current")
def current():
    blockchain = getBlockchain()
    return jsonify(blockchain[-1])

@app.route("/api/prefix")
def getPrefix():
    return prefix

@app.route("/api/mine", methods=['POST'])
def mine():
    global db

    previousBlock = getBlockchain()[-1]
    transactions = findTransactions()

    req = request.get_json()
    block = Block(req["index"], req["transactions"], req["nonce"], previousBlock.hash, req["hash"])
    if not block.validate(prefix):
        return jsonify({"error": "Invalid hash"}), 400

    transactionStringArr = []
    for transaction in json.loads(block.transactions):
        transactionObject = Transaction(transaction["sender"], transaction["reciever"], transaction["amount"], transaction["signature"])
        if not transaction["sender"] == "MINER":
            if not transactionObject.verifyTransaction(transactionObject.sender):
                return jsonify({"error": "Bad Transaction in block"}), 400
            for trans in transactions:
                if trans.signature == transactionObject.signature:
                    db.transactions.delete_one({ "signature": transactionObject.signature })
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
    
    insertBlock = Block(block.index, block.transactions, block.nonce, block.previousHash, block.hash)
    db.blocks.insert_one(insertBlock.__dict__)

    print("--New block successfully mined!--")
    print("Transactions:")
    for tStr in transactionStringArr:
        print(tStr)
    print("----------------")
    print("")
    return jsonify({"message": "New block successfully mined!"}), 200

@app.route("/api/transactions", methods=['POST'])
def createTransaction():
    req = request.get_json()
    transactionObject = Transaction(req["sender"], req["reciever"], req["amount"], req["signature"])
    if not transactionObject.verifyTransaction(transactionObject.sender):
        return jsonify({"error": "Bad Transaction"}), 400

    if not hasSufficentFunds(transactionObject.sender, transactionObject.amount):
        return jsonify({"error": "Insufficient Balance"}), 400

    db.transactions.insert_one(transactionObject.__dict__)
    return jsonify({"response": "Transaction Posted"})

@app.route("/api/transactions", methods=['GET'])
def getTransactions():
    transactions = findTransactions()
    return jsonify(transactions)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
