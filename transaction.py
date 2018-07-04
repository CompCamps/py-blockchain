from lib.keys import signData, verifyData
import base64

class Transaction:
    def __init__(self, sender, reciever, amount, signature=None, timestamp=None):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        if signature==None:
            self.signature = self.signTransaction()
        else:
            self.signature = signature
        self.timestamp = timestamp

    def signTransaction(self):
        signature = signData(str(self.sender) + str(self.reciever) + str(self.amount))
        return base64.b64encode(signature)

    def verifyTransaction(self, public_key_string):
        return verifyData(str(self.sender) + str(self.reciever) + str(self.amount),
                    public_key_string,
                    base64.b64decode(self.signature))

    def _asdict(self):
        return self.__dict__
