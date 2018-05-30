import flask
import blockchain
import os
import socket

app = flask.Flask(__name__)
miner = blockchain.Miner(os.getenv("MINER", "miner"))
block = blockchain.Block()
miner.sign_block(block)
blockchain_ = blockchain.Blockchain(block, zeros=1)
miner.set_blockchain(blockchain_)


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.route("/miner/api/v0.1/blockchain", methods=['GET'])
def get_blockchain():

    return miner.blockchain.json()


@app.route("/miner/api/v0.1/blockchain/first-block", methods=['GET'])
def get_first_block():

    return miner.blockchain.first.json()


@app.route("/miner/api/v0.1/blockchain/last-block", methods=['GET'])
def get_last_block():

    return miner.blockchain.last.json()


@app.route("/miner/api/v0.1/blockchain/block/<string:signature>", methods=['GET'])
def get_block(signature):

    return miner.blockchain.blocks[signature].json()


@app.route("/miner/api/v0.1/blockchain/block", methods=['POST'])
def post_block():
    if not flask.request.json:
        flask.abort(400)
    _block = blockchain.Block()
    _block.nonce = flask.request.json.get('nonce', "")
    _block.miner = flask.request.json.get('miner', "")
    _block.previous = flask.request.json.get('previous', "")
    _block.signature = flask.request.json.get('signature', "")
    miner.blockchain.append(_block)
    return block.json(), 201


@app.route("/")
def hello():

    html = "<h3>Miner: {name}</h3>" \
           "<b>Hostname:</b> {hostname}"
    return html.format(name=os.getenv("MINER", "Unnamed"), hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
