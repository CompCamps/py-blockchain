import hashlib as hasher
import datetime as date

# Block object
class Block:
    # Constructor
    def __init__(self, index, timestamp, data, nonce, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
  
    # Generate the hash for the new block
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + 
                str(self.timestamp) + 
                str(self.data) + 
                str(self.nonce) +
                str(self.previous_hash))
        return sha.hexdigest()

    # Prints out information about the block
    def display(self):
        print "Block #: " + str(self.index)
        print "Data: " + self.data
        print "Hash: " + self.hash
        print "Previous Hash: " + self.previous_hash

# Creates the first block with arbitrary hash
def createGenesisBlock():
  return Block(0, date.datetime.now(), "Genesis Block", 0, "0")

def nextBlock(lastBlock, data, nonce):
    index = lastBlock.index + 1
    timestamp = date.datetime.now()
    hash = lastBlock.hash
    return Block(index, timestamp, data, nonce, hash)