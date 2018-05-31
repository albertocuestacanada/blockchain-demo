"""
This module are the unit tests for blockchain.py
"""

import unittest
import json
from blockchain import *


class BlockTests(unittest.TestCase):

    def test_Block(self):
        self.assertIsInstance(Block(), Block)

    def test_Block_timestamp_check(self):
        with self.assertRaises(ValueError):
            Block(timestamp=int(time.time()) - (2*60*60 + 1))

    def test_block_print(self):
        block = Block()
        timestamp = str(int(time.time()))
        block.timestamp = timestamp
        block_print = "nonce: \n" \
                      "timestamp: " + timestamp + "\n" \
                      "previous:\n" \
                      "\n" \
                      "signature:\n"
        self.assertEqual(block_print, block.__str__())

    def test_empty_block_json(self):
        block = Block()
        timestamp = str(int(time.time()))
        block.timestamp = timestamp
        block_as_dict = {"previous": "",
                         "timestamp": timestamp,
                         "signature": "",
                         "nonce": ""}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))

    def test_first_block_json(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        block_as_dict = {"previous": "",
                         "timestamp": block.timestamp,
                         "signature": block.signature,
                         "nonce": block.nonce}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))

    def test_second_block_json(self):
        block1 = Block()
        miner = Miner('miner')
        miner.sign_block(block1, zeros=1)
        miner.set_blockchain(Blockchain(block1, zeros=1))
        block2 = Block(previous=block1)
        miner.sign_block(block2, zeros=1)
        block2_as_dict = {"previous": block1.signature,
                         "timestamp": block2.timestamp,
                         "signature": block2.signature,
                         "nonce": block2.nonce}
        self.assertDictEqual(block2_as_dict, json.loads(block2.json()))

    def test_Blockchain(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        blockchain = Blockchain(block, zeros=1)
        self.assertIsInstance(blockchain, Blockchain)

    def test_blockchain_one_block_json(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        blockchain = Blockchain(block, zeros=1)
        self.assertEqual(len(blockchain.blocks), 1)
        blockchain.blocks = {}
        blockchain_as_dict = {"blocks": [],
                              "zeros": "1",
                              "last": block.signature,
                              "first": block.signature}
        self.assertDictEqual(blockchain_as_dict, json.loads(blockchain.json()))

    def test_blockchain_two_blocks_json(self):
        block1 = Block()
        miner = Miner('miner')
        miner.sign_block(block1, zeros=1)
        blockchain = Blockchain(block1, zeros=1)
        miner.set_blockchain(blockchain)
        block2 = Block(previous=block1)
        miner.sign_block(block2, zeros=1)
        blockchain.append(block2)
        self.assertEqual(len(blockchain.blocks),2)
        blockchain.blocks = {}
        blockchain_as_dict = {"blocks": [],
                              "zeros": "1",
                              "last": block2.signature,
                              "first": block1.signature}
        self.assertDictEqual(blockchain_as_dict, json.loads(blockchain.json()))


if __name__ == '__main__':
    unittest.main()
