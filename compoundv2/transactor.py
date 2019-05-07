import os
import eth_utils
from eth_account import Account
from typing import Optional
from web3 import Web3
from compoundv2 import Address

class Transactor:
    """
    Generic wrapper for transactions, raw and from web3.eth.defaultAccount

    """
    def __init__(self, 
                 web3: Web3,
                 sender: Address,
                 contract: Optional[object],
                 function_name: Optional[str],
                 params: Optional[list] = None,
                 extra_args: Optional[dict] = None):

        assert(isinstance(web3, Web3))
        assert(isinstance(sender, Address))
        assert(isinstance(contract, Optional[object]))
        #assert(isinstance(function_name, Optional[str]))
        #assert(isinstance(params, Optional[list]))
        #assert(isinstance(extra_args, Optional[dict]))

        self.web3 = web3
        self.sender = sender
        self.contract = contract
        self.function_name = function_name
        self.params = params
        self.extra_args = extra_args

    def _get_receipt(self, transaction_hash: str):
        raw_receipt = self.web3.eth.getTransactionReceipt(transaction_hash)

        if raw_receipt is not None and raw_receipt['blockNumber'] is not None:
            receipt = Receipt(raw_receipt)
            return receipt
        else:
            return None

    def _get_function(self):
        if '(' in self.function_name:
            func = self.contract.get_function_by_signature(self.function_name)
        else:
            func = self.contract.get_function_by_name(self.function_name)

        return func

    def send_raw_transaction(self, **kwargs):
        if os.environ['ETH_PRIVATE_KEY']:
            from_account_priv = os.environ.get('ETH_PRIVATE_KEY')
            from_account = Account.privateKeyToAccount(from_account_priv)
            
        else: 
            from_account = self.web3.eth.defaultAccount

        nonce_dict = dict(nonce = self.web3.eth.getTransactionCount(from_account.address))
        gas_price_dict = dict(gasPrice = self.web3.eth.gasPrice)
        extra_dict = self.extra_args

        contract_func = self.contract.functions[self.function_name]

        if self.extra_args is not None:
            build_raw_tx = contract_func(*self.params).buildTransaction(
                dict(
                    chainId     = 4,
                    **nonce_dict,
                    **gas_price_dict,
                    gas         = 170000,
                    **self.extra_args
                )
            )

        else:
            build_raw_tx = contract_func(*self.params).buildTransaction(
                dict(
                    chainId     = 4,
                    **nonce_dict,
                    **gas_price_dict,
                    gas         = 170000
                )
            )

        signed_raw_tx = self.web3.eth.account.signTransaction(
            build_raw_tx, 
            private_key = from_account_priv
        )
        
        send_tx = self.web3.eth.sendRawTransaction(signed_raw_tx.rawTransaction)
        tx_receipt = self.web3.eth.waitForTransactionReceipt(send_tx)

        return tx_receipt

class Receipt:
    """
    Generic wrapper for an Ethereum transaction receipt

    """

    def __init__(self, receipt):
        self.raw_receipt = receipt
        self.transaction_hash = receipt['transactionHash']
        self.gas_used = receipt['gasUsed']
        self.result = None
        
    def logs(self):
        return self.raw_receipt['logs']
