import json
import os
import pkg_resources

from typing import Optional, List
from web3 import Web3

from compoundv2 import account, Address, Contract

class Comptroller(Contract):
    """
    Python wrapper for Compound 'Presidio' v2's Comptroller Solidity Smart Contract
    """

    abi = Contract._retrieve_abi(__name__, 'abi/Comptroller.json')

    def __init__(self, web3: Web3, address: Address):
        assert(isinstance(web3, Web3))
        assert(isinstance(address, Address))

        self.web3 = web3
        self.address = address.address
        self._contract = self._get_contract(web3, self.abi, address)

    def enter_markets(self, addr: Address, address_one: Address):
        build_tx = self._contract.functions.enterMarkets([addr.address]).buildTransaction({
            'chainId': 4,
            'gas': 170000,
            'gasPrice': self.web3.toWei('1', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(address_one.address)
        })

        signed = self.web3.eth.account.signTransaction(
            build_tx,
            private_key=os.environ['ETH_PRIVATE_KEY']
        )

        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        print(tx_hash)
        
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def get_liquidity(self, addr: Address):
        return self._contract.functions.getAccountLiquidity(addr.address).call()

    def get_assets_in(self, addr: Address) -> List[Address]:
        return self._contract.functions.getAssetsIn(addr.address).call()
        
    def testing(self, addr: Address):
        return self._contract.all_functions()

