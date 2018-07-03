import hashlib as hashlib

class Block:
    def __init__(self, index, nonce, data, previousHash, hash=None):
        self.index = index

        # TODO: Add the pieces of a block
        # TODO: 'self.hash' should be a the SHA256 of the block


    # Takes all the block fields and combines them into one big string
    # then hashes that string
    def hashBlock(self):
        hash = hashlib.sha256((
            str(self.index) +

            # TODO: Include the nonce in the hash calculation
            
            str(self.data) + 
            str(self.previousHash)).encode('utf-8')).hexdigest()
        return hash

    # Checks if the block hash begins with a desired value (000)
    def validate(self):
        if self.hash[:3] != "000":
            return False
        return True