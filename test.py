import campcoin_api as campcoin
import simplejson as json

transactions = [campcoin.Transaction("123", "123", 1)]
block = campcoin.Block(0, json.dumps(transactions), 0, 0, 0)

campcoin = campcoin.CampCoin("https://campcoin.herokuapp.com")

t = campcoin.getCurrentBlock()

print(t)

r = campcoin.postBlock(block)
print(r)