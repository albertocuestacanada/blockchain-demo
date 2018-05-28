from flask import Flask
import blockchain
import json
import os
import socket

app = Flask(__name__)
miner = blockchain.Miner(os.getenv("NAME", "world"))
block = blockchain.Block()
miner.sign_block(block)
blockchain_ = blockchain.Blockchain(block, zeros=1)
miner.set_blockchain(blockchain_)


@app.route("/miner/api/v0.1/blockchain/last-block")
def get_last_block():

    return miner.blockchain.blocks[miner.blockchain.last].json()


@app.route("/")
def hello():

    html = "<h3>Miner: {name}</h3>" \
           "<b>Hostname:</b> {hostname}"
    return html.format(name=os.getenv("MINER", "Unnamed"), hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
