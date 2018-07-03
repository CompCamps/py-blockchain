from block import Block
import requests

blockchain = []

# Genesis Block

# TODO: Make a request to the campcoin API to get the current block in the chain and use as our genesis block
# The campcoin API endpoint is https://campcoin.herokuapp.com/api/current

while 1:
    nonce = 0
    data = "new block!"
    block = blockchain[-1].nextBlock(nonce, data)
    while not block.validate():
        nonce = nonce + 1
        block = blockchain[-1].nextBlock(nonce, data)

    blockchain.append(block)
    block.print()