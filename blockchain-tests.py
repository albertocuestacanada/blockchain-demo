"""
This module are the unit tests for blockchain.py
"""

import unittest
import json
from blockchain import *


class BlockTests(unittest.TestCase):

    def test_Block(self):
        self.assertIsInstance(Block(), Block)

    def test_block_print(self):
        block = Block()
        block_print = "Nonce: 0\n" \
                      "Miner: \n" \
                      "Previous block:\n" \
                      "\n" \
                      "Signature:\n"
        self.assertEqual(block_print, block.__str__())

    def test_empty_block_json(self):
        block = Block()
        block_as_dict = {"Previous": "",
                         "Miner": "",
                         "Signature": "",
                         "Nonce": "0"}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))

    def test_first_block_json(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        block_as_dict = {"Previous": "",
                         "Miner": "miner",
                         "Signature": "04b6674ff8443ec7da8a0fe39c189b0319f6cc419f55fbb9e4ae85b67f0169cb",
                         "Nonce": "7"}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))

    def test_second_block_json(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        miner.set_blockchain(Blockchain(block, zeros=1))
        block = Block()
        miner.sign_block(block, zeros=1)
        block_as_dict = {"Previous": "04b6674ff8443ec7da8a0fe39c189b0319f6cc419f55fbb9e4ae85b67f0169cb",
                         "Miner": "miner",
                         "Signature": "081ee104b7bcbe721b0158404a8fe7f79cabe579c3779368ebea15580a9d54fa",
                         "Nonce": "5"}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))

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
        blockchain.blocks = {}
        blockchain_as_dict = {"Blocks": [],
                              "Zeros": "1",
                              "Last": "04b6674ff8443ec7da8a0fe39c189b0319f6cc419f55fbb9e4ae85b67f0169cb",
                              "First": "04b6674ff8443ec7da8a0fe39c189b0319f6cc419f55fbb9e4ae85b67f0169cb"}
        self.assertDictEqual(blockchain_as_dict, json.loads(blockchain.json()))

    def test_blockchain_two_blocks_json(self):
        block = Block()
        miner = Miner('miner')
        miner.sign_block(block, zeros=1)
        blockchain = Blockchain(block, zeros=1)
        miner.set_blockchain(blockchain)
        block = Block()
        miner.sign_block(block, zeros=1)
        blockchain.append(block)
        blockchain.blocks = {}
        blockchain_as_dict = {"Blocks": [],
                              "Zeros": "1",
                              "Last": "081ee104b7bcbe721b0158404a8fe7f79cabe579c3779368ebea15580a9d54fa",
                              "First": "04b6674ff8443ec7da8a0fe39c189b0319f6cc419f55fbb9e4ae85b67f0169cb"}
        self.assertDictEqual(blockchain_as_dict, json.loads(blockchain.json()))


if __name__ == '__main__':
    unittest.main()
