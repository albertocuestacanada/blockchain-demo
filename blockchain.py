"""
This library implements a basic version of a blockchain structure and a
cryptocurrency that uses it.
"""

__author__ = "Alberto Cuesta Canada"

import hashlib
import warnings
import json

'''One Block in a Blockchain.'''


class Block:

    # The blocks are built empty, the correctness of the block will only be
    # verified when adding it to a blockchain.
    def __init__(self):
        self.nonce = 0
        self.miner = ''
        self.previous = ''
        self.signature = ''

    # Return a print-friendly string representation of the block.
    def __str__(self):
        return "" \
               + "Nonce: " + str(self.nonce) + "\n" \
               + "Miner: " + self.miner + "\n" \
               + "Previous block:\n" + self.previous + "\n" \
               + "Signature:\n" + self.signature
#               + self.transactions \

    # Return a json representation of the block
    def json(self):
        return json.dumps({
            "Nonce": str(self.nonce),
            "Miner": self.miner,
            "Previous": self.previous,
            "Signature": self.signature
        })

    # Set the signature of the block into the sha256 digest of its string
    # representation.
    def sign(self):
        hash_ = hashlib.sha256()
        flat_block = "" \
            + str(self.nonce) \
            + self.miner \
            + self.previous
        hash_.update(flat_block.encode())
        self.signature = hash_.hexdigest()


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
        if block.previous != "":
            raise ValueError(
                'The block passed as first points to other block'
            )
        self.blocks = {block.signature: block}
        self.first = block
        self.last = block
        self.zeros = zeros

    # Return a json representation of the blockchain
    def json(self):
        return json.dumps({
            "First": self.first.signature,
            "Last": self.last.signature,
            "Zeros": str(self.zeros),
            "Blocks": [block.json() for block in self.blocks.values()]
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

        # Check the signature of the block has enough leading zeros
        block.sign()
        if int(block.signature[:self.zeros]) != 0:
            raise ValueError

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
    # The block must have no nonce and no signature before operation.
    # After signing the block will have the name of the miner as the
    # creation, a nonce and a signature. If the signing process is cancelled
    # the creation, nonce and signature attributes of the block must be set to
    # None before trying to sign it again.
    # If previous is set to None this method creates the first block of a
    # blockchain
    def sign_block(self, block, zeros=1):
        if not isinstance(block, Block):
            raise TypeError(
                'The object passed for signing was not a block'
            )
        if block.nonce is not 0:
            raise ValueError(
                'The nonce for the block is not zero'
            )
        if block.signature is not "":
            raise ValueError(
                'The signature for block is not empty'
            )
        if block.miner is not "":
            raise ValueError(
                'The miner for block is not empty'
            )

        block.nonce = 1
        block.miner = self.name
        if not self.blockchain:
            warnings.warn('This miner does not have a blockchain - '
                          'Creating the first block for one')
        else:
            block.previous = self.blockchain.last.signature

        while True:                   # Might want to implement a safety limit
            block.sign()
            try:
                if int(block.signature[:zeros]) == 0:
                    break
            except ValueError:
                pass
            block.nonce += 1
        return block
