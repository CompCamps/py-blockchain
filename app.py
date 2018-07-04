import hashlib as hasher
from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
import simplejson as json
import time
import datetime

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

def utc_to_local(dt):
    return dt - datetime.timedelta(seconds = 21600)

def getBlockchain():
    blockchain = []
    blocks = db.blocks.find()
    for block in blocks:
        b = Block(block['index'], block['transactions'], block['nonce'], block['previousHash'], block['hash'], utc_to_local(block['_id'].generation_time))
        blockchain.append(b)
    return blockchain
    
def findTransactions():
    transactions = []
    for transaction in db.transactions.find():
        t = Transaction(transaction['sender'], transaction['reciever'], transaction['amount'], transaction['signature'], utc_to_local(transaction['_id'].generation_time))
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

def subtractPendingBalance(public_key):
    balance = 0
    transactions = findTransactions()
    for transaction in transactions:
        if (transaction.sender == public_key):
            balance = balance - transaction.amount

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

@app.route('/stats')
def statsRoute():
    return render_template("stats.html")
    
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
    balance = getBalance(key) + subtractPendingBalance(key)
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
    
    if transactionObject.sender == transactionObject.reciever:
        return jsonify({"error": "You cannot send yourself coins!"}), 400

    if transactionObject.amount <= 0:
        return jsonify({"error": "Must send at least 1 coin"}), 400

    if (len(str(transactionObject.__dict__)) > 500):
        return jsonify({"error": "Transaction Object exceeds maximum bytes"}), 400 

    db.transactions.insert_one(transactionObject.__dict__)
    return jsonify({"response": "Transaction Posted"})

@app.route("/api/transactions", methods=['GET'])
def getTransactionsToMine():
    # Get up to two transactions per block
    transactions = findTransactions()[0:2]
    return jsonify(transactions)

@app.route('/api/balances')
def getAllBalances():
    balances = {}
    blockchain = getBlockchain()
    for block in blockchain:
        for transaction in json.loads(block.transactions):
            try:
                balances[transaction["reciever"]] = balances[transaction["reciever"]] + transaction["amount"]
            except:
                balances[transaction["reciever"]] = transaction["amount"]

            try:
                balances[transaction["sender"]] = balances[transaction["sender"]] - transaction["amount"]
            except:
                balances[transaction["sender"]] = 0 - transaction["amount"]

    del balances["MINER"]
    del balances["123"] # test key
    return jsonify(balances)

@app.route("/api/transactions/pending")
def getPendingTransactions():
    transactions = findTransactions()
    return jsonify(transactions)

@app.route('/api/transactions/mined')
def getAllTransactions():
    transactions = []
    blockchain = getBlockchain()
    for block in blockchain:
        for transaction in json.loads(block.transactions):
            if (transaction['sender'] != "MINER"):
                trans = Transaction(transaction['sender'], transaction['reciever'], transaction['amount'], transaction['signature'], block.timestamp)
                transactions.append(trans)

    return jsonify(transactions)

@app.route('/api/stats/blocksPerHour')
def getBlocksPerHour():
    blockchain = getBlockchain()
    stats = {}
    for block in blockchain:
        day = block.timestamp.strftime('%d')
        hour = block.timestamp.strftime('%H')
        try:
            stats[day][hour] = stats[day][hour] + 1
        except:
            try:
                stats[day][hour] = 1
            except:
                stats[day] = {}
                stats[day][hour] = 1
    del stats['30']
    return jsonify(stats)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
