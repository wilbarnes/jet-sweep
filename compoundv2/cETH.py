import json
import pkg_resources

from typing import Optional
from web3 import Web3

from compoundv2 import account, Address, Contract
from compoundv2.transactor import Transactor

class cETH(Contract):
    """
    Python wrapper for Compound 'Presidio' v2's cETH Solidity Smart Contract
    Mainnet: N/A
    Rinkeby: 0xbed6d9490a7cd81ff0f06f29189160a9641a358f
    """

    abi = Contract._retrieve_abi(__name__, 'abi/cETH.json')

    def __init__(self, web3: Web3, address: Address, sender: Address):
        assert(isinstance(web3, Web3))
        assert(isinstance(address, Address))
        assert(isinstance(sender, Address))

        self.web3 = web3
        self.address = address
        self.sender = sender
        self._contract = self._get_contract(web3, self.abi, address)

    def mint(self, amountToMint):
        function_name = 'mint'

        params = []

        extra_args = dict(
            value = self.web3.toWei(amountToMint, 'ether')
        )

        return Transactor(
            self.web3, 
            self.address, 
            self._contract, 
            function_name,
            params,
            extra_args
        )

    def redeem(self, amountToRedeem):
        function_name = 'redeem'

        params = []
        params.append(int(amountToRedeem))

        return Transactor(
            self.web3,
            self.address,
            self._contract,
            function_name,
            params
        )

    def balanceOf(self, addressToCheck):
        """
        Retrieve balance of address provided
        """
        return self._contract.call().balanceOf(str(addressToCheck))

    def supplyRatePerBlock(self):
        """
        Retrieve the current supply rate as an unsigned integer
        scaled by 1e18
        """
        return self._contract.call().supplyRatePerBlock()

    def exchangeRateCurrent(self):
        """
        Retrieve the current exchange rate as an unsigned integer
        scaled by 1e18
        """
        return self._contract.call().exchangeRateCurrent()
