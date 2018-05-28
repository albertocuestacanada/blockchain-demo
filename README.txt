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

POST            http://[hostname]/miner/api/v0.1/transaction
                Uploads a candidate transaction

POST            http://[hostname]/miner/api/v0.1/blockchain/block
                Uploads a new signed block to add to the miner's blockchain



