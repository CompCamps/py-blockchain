import hashlib as hashlib

class Block:
    def __init__(self, index, nonce, data, previousHash, hash=None):
        self.index = index
        self.nonce = nonce
        self.data = data
        self.previousHash = previousHash
        self.hash = self.hashBlock()

    # Takes all the block fields and combines them into one big string
    # then hashes that string
    def hashBlock(self):
        hash = hashlib.sha256((
            str(self.index) +
            str(self.nonce) +
            str(self.data) + 
            str(self.previousHash)).encode('utf-8')).hexdigest()
        return hash

    # Checks if the block hash begins with a desired value (000)
    def validate(self):
        if self.hash[:3] != "000":
            return False
        return True

    # Prints the block to the screen
    def print(self):
        print("Block #: " + str(self.index))
        print("Nonce: " + str(self.nonce))
        print("Data: " + str(self.data))
        print("Previous Hash: " + str(self.previousHash))
        print("Hash: " + str(self.hash))

    # Returns the block that comes after this block
    def nextBlock(self, nonce, data):
        return Block(self.index + 1, nonce, data, self.hash)