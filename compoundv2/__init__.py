import json
import sys
import eth_utils
import pkg_resources

from compoundv2.utils import is_contract_at

from web3 import Web3
from typing import Optional

class Address:

    def __init__(self, address):
        if isinstance(address, Address):
            self.address = address.address
        else:
            self.address = eth_utils.to_checksum_address(address)

    def as_bytes(self) -> bytes:
        return bytes.fromhex(self.address.replace('0x', ''))

    def __str__(self):
        return f"{self.address}"

    def __repr__(self):
        return f"Address('{self.address}')"

    def __hash__(self):
        return self.address.__hash__()

    def __eq__(self, other):
        assert(isinstance(other, Address))
        return self.address == other.address


class Contract:

    @staticmethod
    def _get_contract(web3: Web3, abi: list, address: Address):
        assert(isinstance(web3, Web3))
        assert(isinstance(abi, list))
        assert(isinstance(address, Address))

        if not is_contract_at(web3, address):
            raise Exception(f"No contract found at {address}")

        return web3.eth.contract(abi=abi)(address=address.address)

    @staticmethod
    def _retrieve_abi(package, resource) -> list:
        return json.loads(pkg_resources.resource_string(package, resource))        
