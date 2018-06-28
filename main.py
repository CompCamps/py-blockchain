import datetime as date
from block import *    

def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", 0, "0")

def next_block(last_block, nonce):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, nonce, this_hash)

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

for i in range(10):
    beginTimestamp = date.datetime.now()
    nonce = 0
    block_to_add = next_block(previous_block, nonce)
    while (block_to_add.hash[:4] != "0000"):
        nonce += 1
        block_to_add = next_block(previous_block, nonce)
    blockchain.append(block_to_add)
    time_taken = date.datetime.now() - beginTimestamp
    print block_to_add.nonce
    print "Took " + str(time_taken.total_seconds())
    previous_block = block_to_add

for i in range(10):
    blockchain[i].display()
