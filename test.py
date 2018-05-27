import blockchain
b = blockchain.Block()
m = blockchain.Miner('alberto')
m.sign_block(b)
bc = blockchain.Blockchain(b,1)
m.set_blockchain(bc)
b2 = blockchain.Block()
m.sign_block(b2)
bc.append(b2)

