import hashlib as hashlib

# TODO: modify toHash so hash starts with 0
toHash = "hello world"

hash = hashlib.sha256(toHash.encode('utf-8')).hexdigest()

# Hint: use a while loop

print(hash)