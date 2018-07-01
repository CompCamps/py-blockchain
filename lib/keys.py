from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import base64

def generateKeys():
    # SECP256k1 is the Bitcoin elliptic curve
    private_key = SigningKey.generate(curve=SECP256k1) 
    public_key = private_key.get_verifying_key()

    file_out = open("private.pem", "wb")
    file_out.write(private_key.to_pem())

    file_out = open("public.pem", "wb")
    file_out.write(public_key.to_pem())

    print(base64.b64encode(private_key.to_string()))
    print(str(base64.b64encode(public_key.to_string()), "utf-8"))

def genPubKey():
    private_key = SigningKey.generate(curve=SECP256k1) 
    public_key = private_key.get_verifying_key()

    print(str(base64.b64encode(public_key.to_string()), "utf-8"))

def getKeys():
    public_key = {}
    private_key = {}
    try:
        public_key = VerifyingKey.from_pem(open("public.pem").read())
        private_key = SigningKey.from_pem(open("private.pem").read())
    except:
        generateKeys()
        public_key = VerifyingKey.from_pem(open("public.pem").read())
        private_key = SigningKey.from_pem(open("private.pem").read())
    return public_key, private_key

def getEncodedKeys():
    public_key, private_key = getKeys()
    return str(base64.b64encode(public_key.to_string()), "utf-8"), str(base64.b64encode(private_key.to_string()), "utf-8")

# sign data with a private key
def signData(data):
    _, private_key = getKeys()
    encoded = data.encode('utf8')
    signature = private_key.sign(encoded)
    return signature

# verifty message with public key and signature
def verifyData(data, public_key_string, signature):
    public_key = VerifyingKey.from_string(base64.b64decode(public_key_string), curve=SECP256k1)
    encoded = data.encode('utf8')
    try:
        public_key.verify(signature, encoded)
        return True
    except BadSignatureError:
        return False

#genPubKey()
# sig = signData("test")
# print(verifyData("test", "/pJ+3b4y3iOwIF+bTqQQT78xeuvoJxSUb3QmHNkpGP61ZbBXjq0cFclTqPI5pevQSniw/1Yz+snqDBCkPbWPRw==", sig))