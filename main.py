import datetime as date
from block import *

blockchain = [createGenesisBlock()]
previousBlock = blockchain[0]

# Attempts to mine a new block
def mine():
    nonce = 0
    newBlock = nextBlock(previousBlock, "test", nonce)
    while (newBlock.hash[:4] != "0000"):
        nonce += 1
        newBlock = nextBlock(previousBlock, "test", nonce)
    return newBlock

# Mine 10 blocks
for i in range(10):
    beginTimestamp = date.datetime.now()

    newBlock = mine()
    blockchain.append(newBlock)
    previousBlock = newBlock

    time_taken = date.datetime.now() - beginTimestamp
    print "-- New block mined! --"
    print "Took " + str(time_taken.total_seconds())
    newBlock.display()