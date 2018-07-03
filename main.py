from block import Block

blockchain = []

# Genesis Block
blockchain.append(Block(0, 0, "hello world", 0, 0))


nonce = 0
data = "new block!"
block = #TODO: get the last block in the blockchain, and call nextBlock on it
while not block.validate():
    nonce = nonce + 1
    block = #TODO: get the last block in the blockchain, and call nextBlock on it

# TODO: Append the newly mined block to the blockchain
# TODO: Repeat this infinitely

block.print()