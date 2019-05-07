from web3 import Web3

def is_contract_at(web3: Web3, address):
    code = web3.eth.getCode(address.address)
    return (code is not None) and (code != "0x") and (code != "0x0") and (code != b"\x00") and (code != b"")
