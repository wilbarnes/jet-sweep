import os
import sys
import datetime
import time
import json
import argparse
import configparser

from eth_utils import to_checksum_address
from web3 import Web3

from compoundv2 import Address
from compoundv2.cETH import cETH
from compoundv2.Comptroller import Comptroller

def main():
    """
    Generic scripts for interacting with Compound v2 Presidio
    """

    if args.enter in ('eth', 'Eth', 'ETH'):
        enter_markets_tx = contract_Comptroller.enter_markets(cETH_addr, address_one)
        print(enter_markets_tx)

    elif args.get_assets_in:
        get_assets_call = contract_Comptroller.get_assets_in(address_one)
        print(get_assets_call)

    elif args.get_balance:
        get_balance_call = contract_cETH.balanceOf(address_one.address)
        print(get_balance_call)

    elif args.get_liquidity:
        get_liquidity_call = contract_Comptroller.get_liquidity(address_one)
        print(get_liquidity_call)
        
    elif args.supply and args.eth:
        supply_eth = contract_cETH.mint(args.eth)
        tx = supply_eth.send_raw_transaction()
        print(web3.toHex(tx['transactionHash']))

    elif args.supply_rate:
        supply_rate_call = contract_cETH.supplyRatePerBlock()
        print(supply_rate_call / 1e18)

    elif args.exchange_rate:
        exchange_rate_call = contract_cETH.exchangeRateCurrent()
        print(exchange_rate_call / 1e18)

    elif args.redeem and args.eth:
        redeem_eth = contract_cETH.redeem(args.eth)
        print(redeem_eth)
        tx = redeem_eth.send_raw_transaction()
        print('ETH redeemed.')
        print(web3.toHex(tx['transactionHash']))

    elif args.sweep_overnight and args.eth:
        supply_eth = contract_cETH.mint(args.eth)
        tx = supply_eth.send_raw_transaction()
        get_balance_call = contract_cETH.balanceOf(address_one.address)
        print(get_balance_call)
        time.sleep(60 * 15)
        redeem_eth = contract_cETH.redeem(get_balance_call)
        tx = redeem_eth.send_raw_transaction()
        print('Sweep complete')
        print(web3.toHex(tx['transactionHash']))

    elif args.supply and args.dai:
        print('Supplying dai is not yet implemented.')

    elif args.borrow and args.eth:
        # requires market entry
        print('Borrowing eth is not yet implemented.')

    elif args.borrow and args.dai:
        # requires market entry
        print('Borrowing dai is not yet implemented.')

    else:
        print('Not a valid option.')

if __name__ == "__main__":
    # set config parser and read config variables
    parser = argparse.ArgumentParser('Jet sweep your assets to higher earning contracts')
    config = configparser.ConfigParser()
    config.read('config.ini')

    private_key         = config['ACCOUNT']['PrivateKey']
    address_one         = Address(config['ACCOUNT']['Address'])
    infura_mainnet      = config['PROVIDER']['InfuraMainnet']
    infura_rinkeby      = config['PROVIDER']['InfuraRinkeby']
    infura_secret       = config['PROVIDER']['InfuraProjSecret']

    # compound.finance contracts
    cDAI                = to_checksum_address(config['COMPOUND-CONTRACTS']['cDAI'])
    cETH_addr           = Address(config['COMPOUND-CONTRACTS']['cETH'])
    comptroller_addr    = Address(config['COMPOUND-CONTRACTS']['Comptroller'])
    price_oracle        = to_checksum_address(config['COMPOUND-CONTRACTS']['PriceOracle'])
    stable_interest     = to_checksum_address(config['COMPOUND-CONTRACTS']['StableCoinInterestRateModel'])
    standard_interest   = to_checksum_address(config['COMPOUND-CONTRACTS']['StandardInterestRateModel'])

    # arguments
    parser.add_argument(
        '--supply', 
        dest='supply', 
        action='store_true', 
        help='supply asset'
    )

    parser.add_argument(
        '--borrow', 
        dest='borrow', 
        action='store_true', 
        help='borrow asset'
    )

    parser.add_argument(
        '--redeem', 
        dest='redeem', 
        action='store_true', 
        help='redeem asset'
    )

    parser.add_argument(
        '--supply-rate', 
        dest='supply_rate', 
        action='store_true', 
        help='retrieve supply rate per block'
    )

    parser.add_argument(
        '--exchange-rate', 
        dest='exchange_rate', 
        action='store_true', 
        help='retrieve current exchange rate'
    )

    parser.add_argument(
        '--eth', 
        dest='eth', 
        help='ether'
    )

    parser.add_argument(
        '--dai', 
        dest='dai', 
        help='dai'
    )

    # markets argument group
    markets_grp = parser.add_argument_group(
        title="ENTER/EXIT MARKETS",
        description="commands for entering & exiting markets"
    )

    markets_grp.add_argument(
        '--enter', 
        dest='enter', 
        help='enter specified market'
    )

    # reporting argument group
    reporting_grp = parser.add_argument_group(
        title="REPORTING", 
        description="short form reports of your open positions"
    )

    reporting_grp.add_argument(
        '--get-assets-in', 
        dest        = 'get_assets_in', 
        action      = 'store_true', 
        help        = 'get list of entered markets'
    )

    reporting_grp.add_argument(
        '--get-liquidity',
        dest        = 'get_liquidity',
        action      = 'store_true',
        help        = 'return estimated ether value of account\'s collateral'
    )

    reporting_grp.add_argument(
        '--get-balance-of',
        dest        = 'get_balance',
        action      = 'store_true',
        help        = 'get cToken balance of provided account'
    )

    sweep_grp = parser.add_argument_group(
        title="sweep options for your digital assets",
        description='quick POC for sweeping your ETH into high interest accounts'
    )

    sweep_grp.add_argument(
        '--sweep-overnight',
        dest        = 'sweep_overnight',
        action      = 'store_true',
        help        = 'sweep specified amount of eth to a high interest account once overnight'
    )


    args = parser.parse_args()

    web3 = Web3(Web3.HTTPProvider(infura_rinkeby))
    print('Web3 connected:', web3.isConnected())
    
    contract_cETH = cETH(web3, cETH_addr, address_one)
    contract_Comptroller = Comptroller(web3, comptroller_addr)

    main()
