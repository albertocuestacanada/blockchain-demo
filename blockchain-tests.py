"""
This module are the unit tests for blockchain.py
"""

import unittest
import json
from blockchain import *


class BlockTests(unittest.TestCase):

    def test_Block(self):
        self.assertIsInstance(Block(), Block)

    def test_Block_print(self):
        block = Block()
        block_print = "Nonce: 0\n" \
                      "Miner: \n" \
                      "Previous block:\n" \
                      "\n" \
                      "Signature:\n"
        self.assertEqual(block_print, block.__str__())

    def test_Block_json(self):
        block = Block()
        block_as_dict = {"Previous": "",
                         "Miner": "",
                         "Signature": "",
                         "Nonce": "0"}
        self.assertDictEqual(block_as_dict, json.loads(block.json()))


if __name__ == '__main__':
    unittest.main()
