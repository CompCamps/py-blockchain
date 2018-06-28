import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, nonce, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
  
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + 
                str(self.timestamp) + 
                str(self.data) + 
                str(self.nonce) +
                str(self.previous_hash))
        return sha.hexdigest()

    def display(self):
        print "Block #: " + str(self.index)
        print "Data: " + self.data
        print "Hash: " + self.hash
        print "Previous Hash: " + self.previous_hash