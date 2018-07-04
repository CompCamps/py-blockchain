import hashlib as hashlib
import datetime as date

# Block object
class Block:
    # Constructor
    def __init__(self, index, transactions, nonce, previousHash, hash=None, timestamp=None):
        self.index = index
        self.transactions = transactions
        self.nonce = nonce
        self.previousHash = previousHash
        if hash:
            self.hash = hash
        else:
            self.hash = self.hashBlock()
        self.timestamp = timestamp

    def _asdict(self):
        return self.__dict__
  
    # Generate the hash for the new block
    def hashBlock(self):
        hash = hashlib.sha256((
                str(self.transactions) + 
                str(self.nonce) +
                str(self.previousHash)).encode('utf-8'))
        return hash.hexdigest()

    # Prints out information about the block
    def display(self):
        print("Block #: " + str(self.index))
        print("transactions: " + self.transactions)
        print("Nonce: " + str(self.nonce))
        print("Hash: " + self.hash)
        print("Previous Hash: " + self.previousHash)
        print("")
    
    def validate(self, prefix):
        if (self.hash != self.hashBlock()):
            return False
        # if (self.hash[:4] != "0000"):
        #      return False
        if (self.hash[:len(prefix)] != prefix):
            return False
        return True

# Creates the first block with arbitrary hash
def createGenesisBlock():
  return Block(0, "[]", 0, "0")

def nextBlock(lastBlock, transactions, nonce):
    index = lastBlock.index + 1
    return Block(index, transactions, nonce, lastBlock.hash)
