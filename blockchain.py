"""
This library implements a basic version of a blockchain structure and a
cryptocurrency that uses it.
"""

__author__ = "Alberto Cuesta Canada"

import hashlib
import warnings
import json
import time

'''One Block in a Blockchain.'''


class Block:

    # The blocks will auto-generate a timestamp if not provided with one.
    # The time will be checked to be no more than two hours from current local
    # system time.
    # If no previous is provided this would be a genesis block.
    def __init__(self, nonce='', timestamp='', transactions=[], previous=None):
        self.nonce = nonce
        if timestamp != '':
            if abs(int(timestamp) - int(time.time())) > 2*60*60:
                raise ValueError(
                    'The timestamp provided differs more than two hours from '
                    'the local system time'
                )
            self.timestamp = timestamp
        else:
            self.timestamp = str(int(time.time()))
        self.transactions = transactions
        if previous is None:
            self.previous = ''
        else:
            self.previous = previous.signature
        self.signature = ''

    # Return a print-friendly string representation of the block.
    def __str__(self):
        return '' \
               + 'nonce: ' + self.nonce + '\n' \
               + 'timestamp: ' + self.timestamp + '\n' \
               + 'previous:\n' + self.previous + '\n' \
               + 'signature:\n' + self.signature
#               + self.transactions \

    # Return a json representation of the block
    def to_json(self):
        return json.dumps({
            'nonce': self.nonce,
            'timestamp': self.timestamp,
            'previous': self.previous,
            'signature': self.signature
        })

    # Overwrite the block internals with those of a json dictionary
    def from_json(self, json):

        self.nonce = json['nonce']
        self.timestamp = json['timestamp']
        self.previous = json['previous']
        self.signature = json['signature']

    # Hiding the internal implementation of block nonce variable
    def set_nonce(self, nonce):
        self.nonce = str(nonce)

    # Hiding the internal implementation of block timestamp variable
    def set_timestamp(self, timestamp):
        self.timestamp = str(timestamp)

    # Hiding the internal implementation of block previous variable
    def set_previous(self, previous):
        self.previous = str(previous)

    # Hiding the internal implementation of block signature variable
    def set_signature(self, signature):
        self.signature = str(signature)

    # Set the signature of the block into the sha256 digest of its string
    # representation.
    def sign(self):
        _hash = hashlib.sha256()
        flat_block = '' \
            + self.nonce \
            + self.timestamp \
            + self.previous
        _hash.update(flat_block.encode())
        self.signature = _hash.hexdigest()


'''A Blockchain is nothing more than a dictionary of Blocks referenced by their
signatures, and pointers to the first and last blocks.
'''


class Blockchain:

    # A blockchain is initialized with an initial block
    def __init__(self, block, zeros=1):
        if not isinstance(block, Block):
            raise TypeError(
                'The object passed as first block was not a block'
            )
        if block.previous != '':
            raise ValueError(
                'The block passed as first points to other block'
            )
        self.blocks = {block.signature: block}
        self.first = block
        self.last = block
        self.zeros = zeros

    # Return a json representation of the blockchain
    def to_json(self):
        return json.dumps({
            "first": self.first.signature,
            "last": self.last.signature,
            "zeros": str(self.zeros),
            "blocks": [block.to_json() for block in self.blocks.values()]
        })

    # Appends a valid block to the blockchain
    def append(self, block):
        if not isinstance(block, Block):
            raise TypeError(
                'The object passed for appending was not a block'
            )
        if block.previous != self.last.signature:
            raise ValueError(
                'The block passed for appending does not point to the last'
                ' block in the blockchain'
            )

        # Recalculate the signature of the block and check for leading zeros
        block.sign()
        if int(block.signature[:self.zeros]) != 0:
            raise ValueError(
                'The block does not have enough leading zeros in the signature'
            )

        self.blocks[block.signature] = block
        self.last = block


'''A Miner keeps a blockchain and tries to build more blocks by choosing a set
of transactions and finding a nonce that results in a sha256 signature for the
block with the number of leading zeros stipulated by the blockchain
'''


class Miner:

    # A miner must be initialized with a name
    def __init__(self, name):
        self.name = name
        self.blockchain = None
        return

    # Set the blockchain for this miner
    def set_blockchain(self, blockchain):
        if not isinstance(blockchain, Blockchain):
            raise TypeError(
                'The object passed was not a blockchain'
            )
        self.blockchain = blockchain

    # Searches for a nonce that will make the sha256 digest for the string
    # representation of the block start with the given number of leading zeros.
    def sign_block(self, block, zeros=1):

        _nonce = 1
        while True:                   # Might want to implement a safety limit
            block.set_nonce(_nonce)
            block.sign()
            try:
                if int(block.signature[:zeros]) == 0:
                    break
            except ValueError:
                pass
            _nonce += 1
        return block
