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

    # TODO: Create a print statement to display the block nicely
    def print(self):
        return
