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


# How do I filter the massive error message to show something meaningful?
# For example, 500 is returned if attempting to append a block that doesn't
#  point to the last one in the miner's blockchain, quite a common event.
#@app.errorhandler(500)
#def not_found(error):
#    return flask.make_response(flask.jsonify({'error': 'Not found'}), 500)


@app.route("/miner/api/v0.1/blockchain", methods=['GET'])
def get_blockchain():

    return miner.blockchain.to_json()


@app.route("/miner/api/v0.1/blockchain/first-block", methods=['GET'])
def get_first_block():

    return miner.blockchain.first.to_json()


@app.route("/miner/api/v0.1/blockchain/last-block", methods=['GET'])
def get_last_block():

    return miner.blockchain.last.to_json()


@app.route("/miner/api/v0.1/blockchain/block/<string:signature>", methods=['GET'])
def get_block(signature):

    return miner.blockchain.blocks[signature].to_json()


@app.route("/miner/api/v0.1/blockchain/block", methods=['POST'])
def post_block():
    if not flask.request.json:
        flask.abort(400)
    _block = blockchain.Block()
    _block.from_json(flask.request.json)
    miner.blockchain.append(_block)
    return block.to_json(), 201


@app.route("/")
def hello():

    html = "<h3>Miner: {name}</h3>" \
           "<b>Hostname:</b> {hostname}"
    return html.format(name=os.getenv("MINER", "Unnamed"), hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
