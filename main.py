from block import Block

nonce = 0
block = Block(0, nonce, "hello world", 0)

while not block.validate():
    nonce = nonce + 1
    block = Block(0, nonce, "hello world", 0)

block.print()