import os
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from dotenv import load_dotenv
from constants import LIQUIDITY_POOL_ABI, SWAP_ROUTER_ABI
import json

# Load environment variables
load_dotenv()

# Arbitrum Sepolia network configuration
PROVIDER_URL = os.getenv("PROVIDER_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Contract addresses
SWAP_ROUTER_02_ADDRESS = os.getenv("SWAP_ROUTER_02_ADDRESS")  # Address of your SwapRouter02
WTIST_TOKEN_ADDRESS = os.getenv("WTIST_TOKEN_ADDRESS")
USDC_ADDRESS = os.getenv("USDC_ADDRESS")
POOL_ADDRESS = os.getenv("POOL_ADDRESS")  # Address of your liquidity pool


# Initialize Web3
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Account
account = Account.from_key(PRIVATE_KEY)

# SwapRouter ABI
swaprouter_contract = w3.eth.contract(address=SWAP_ROUTER_02_ADDRESS, abi=SWAP_ROUTER_ABI)

# Liquidity Pool ABI
pool_contract = w3.eth.contract(address=POOL_ADDRESS, abi=LIQUIDITY_POOL_ABI)

# Function to get the price ratio from pool reserves
def get_price_ratio():
    try:
        reserve_wtist = #Replace with the correct index from your pool's ABI
        reserve_usdc = #Replace with the correct index from your pool's ABI
        if reserve_usdc == 0:
            return float('inf')
        ratio = reserve_wtist / reserve_usdc
        return ratio
    except Exception as e:
        print(f"Error getting price ratio: {e}")
        return None


# Function to swap tokens using SwapRouter02
def swap_tokens(amountIn, tokenIn, tokenOut, poolFee, amountOutMinimum=0, sqrtPriceLimitX96=0):
    try:
        nonce = w3.eth.getTransactionCount(account.address)

        #Encode the path correctly for ExactInputSingle
        transaction = swaprouter_contract.functions.ExactInputSingle(
            {
                'tokenIn': tokenIn,
                'tokenOut': tokenOut,
                'fee': poolFee, #Remember that this is a uint24
                'recipient': account.address,
                'deadline': w3.eth.getBlock('latest')['timestamp'] + 60,
                'amountIn': amountIn,
                'amountOutMinimum': amountOutMinimum, # Usually should be set to a non-zero value to prevent slippage
                'sqrtPriceLimitX96': sqrtPriceLimitX96 # Usually set to 0 for no limit
            }
        ).buildTransaction({
            'chainId': 421614,
            'from': account.address,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price,
            'gas': 3000000,  #Increased gas limit, might need to increase it even further
        })


        signed_txn = w3.eth.account.signTransaction(transaction, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(f"Swap transaction hash: {w3.toHex(tx_hash)}")
        w3.eth.waitForTransactionReceipt(tx_hash)

    except Exception as e:
        print(f"Error swapping tokens: {e}")


# Rebalance function (simplified)
def rebalance_pool():
    ratio = get_price_ratio()
    if ratio is not None:
        target_ratio = 1 / 69
        tolerance = 0.1
        deviation = abs(ratio - target_ratio) / target_ratio

        if deviation > tolerance:
            print(f"Price ratio deviated by {deviation:.2f}. Rebalancing...")
            if ratio > target_ratio * (1 + tolerance):  # Sell WTIST, buy USDC
                amountIn = 10**18  # Placeholder – needs improvement (see explanation below)
                amountOutMinimum = int(0.95 * amountIn * ratio)  # 5% slippage buffer
                swap_tokens(amountIn, WTIST_TOKEN_ADDRESS, USDC_ADDRESS, 3000, amountOutMinimum) #Remember to set poolFee
            else:  # Sell USDC, buy WTIST
                amountIn = 10**6   # Placeholder – needs improvement
                amountOutMinimum = int(0.95 * amountIn / ratio)  # 5% slippage buffer
                swap_tokens(amountIn, USDC_ADDRESS, WTIST_TOKEN_ADDRESS, 3000, amountOutMinimum) #Remember to set poolFee


# Main loop
if __name__ == "__main__":
    while True:
        rebalance_pool()
        time.sleep(60)