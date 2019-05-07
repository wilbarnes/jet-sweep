import os
from eth_account import Account
from web3 import Web3
from typing import Optional

def private_key_to_account(web3: Web3):
    private_key = os.environ['ETH_PRIVATE_KEY']
    account = Account.privateKeyToAccount(private_key)
    return account
