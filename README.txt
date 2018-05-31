This project attempts to create a simple Blockchain demo using python


--- Running a Miner ---

miner-server.py requires flask.

To run miner-server.py in a local environment:
sudo su
. venv/bin/activate
python3 miner-server.py &

Tu run miner-server.py in a docker container:
docker build -t local-repository:miner-server .
docker run -dp 80:80 local-repository:miner-server


--- Initializing a Miner ---

import blockchain
b = blockchain.Block()   # This will be the first block in the blockchain
m = blockchain.Miner('alberto')             # Choose a name for the miner
m.sign_block(b)                # Find the nonce for the block and sign it
bc = blockchain.Blockchain(b,1)      # Create a blockchain from the block
m.set_blockchain(bc)      # Give the blockchain to the miner, good to go!


--- Miner API ---

GET             http://[hostname]/miner/api/v0.1/blockchain
                Retrieves the miner's blockchain

GET             http://[hostname]/miner/api/v0.1/blockchain/first-block
                Retrieves the first block in the miner's blockchain

GET             http://[hostname]/miner/api/v0.1/blockchain/last-block
                Retrieves the last block in the miner's blockchain

GET             http://[hostname]/miner/api/v0.1/blockchain/block/[signature]
                Retrieves a block with a specific signature from the miner's 
                blockchain

GET             http://[hostname]/miner/api/v0.1/blockchain/tail/[signature]
                Retrieves the miner's blockchain from the block with a certain
                signature

POST            http://[hostname]/miner/api/v0.1/blockchain/block
                Uploads a new signed block to add to the miner's blockchain

POST            http://[hostname]/miner/api/v0.1/transaction
(ToDo)          Uploads a candidate transaction

--- Testing POST block ---
In python3:
import blockchain
import requests
import json
request = requests.get('http://localhost/miner/api/v0.1/blockchain/last-block')
miner = blockchain.Miner('Miner')
block = blockchain.Block()
block.from_json(request.json())
blockchain_ = blockchain.Blockchain(block, zeros=1)
miner.set_blockchain(blockchain_)
block = blockchain.Block(previous=miner.blockchain.last)
miner.sign_block(block)
miner.blockchain.append(block)
block.to_json()
# Haven't got yet requests.post() to work

Execute:
curl -i -H "Content-Type: application/json" -X POST -d [Output from last command] http://localhost:80/miner/api/v0.1/blockchain/block

Return must be:
HTTP/1.0 201 CREATED
Content-Type: text/html; charset=utf-8
Content-Length: 131
Server: Werkzeug/0.14.1 Python/3.5.5
Date: Wed, 30 May 2018 13:27:33 GMT

[Output from block.to_json()]

Test also the blockchain:
curl -i -H "Content-Type: application/json" -X GET http://localhost:80/miner/api/v0.1/blockchain

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 546
Server: Werkzeug/0.14.1 Python/3.5.5
Date: Wed, 30 May 2018 13:31:11 GMT

{"last": "0e6fc956c6203586d05afd7cd9a8c9513c4450116d0742b54eff4074b319b38f", "first": "09e17d31ffc28f4717907bf5d3ff8d7ac02e8cf08e6ee09557b8e872ff489364", "zeros": "1", "blocks": ["{\"miner\": \"Alberto\", \"previous\": \"\", \"nonce\": \"2\", \"signature\": \"09e17d31ffc28f4717907bf5d3ff8d7ac02e8cf08e6ee09557b8e872ff489364\"}", "{\"miner\": \"Alberto\", \"previous\": \"09e17d31ffc28f4717907bf5d3ff8d7ac02e8cf08e6ee09557b8e872ff489364\", \"nonce\": \"14\", \"signature\": \"0e6fc956c6203586d05afd7cd9a8c9513c4450116d0742b54eff4074b319b38f\"}"]}
