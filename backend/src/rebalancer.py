import os
import time
import logging
from typing import Tuple

from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

from constants import SWAP_ROUTER_02_ADDRESS, SWAP_ROUTER_ABI, LIQUIDITY_POOL_CONTRACT_ADDRESS, LIQUIDITY_POOL_ABI, WTIST_CONTRACT_ADDRESS, USDC_CONTRACT_ADDRESS, QUOTER_ADDRESS, QUOTER_ABI
from util import format_units, parse_units, sqrt_price_X96_to_price
from price import get_latest_price

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Arbitrum Sepolia network configuration
PROVIDER_URL = os.getenv("PROVIDER_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
account = Account.from_key(PRIVATE_KEY)

# SwapRouter
swap_contract = web3.eth.contract(
    address=SWAP_ROUTER_02_ADDRESS, abi=SWAP_ROUTER_ABI)

# Liquidity Pool
pool_contract = web3.eth.contract(
    address=LIQUIDITY_POOL_CONTRACT_ADDRESS, abi=LIQUIDITY_POOL_ABI)

# Quoter
quoter_contract = web3.eth.contract(
    address=QUOTER_ADDRESS, abi=QUOTER_ABI)


def swap_tokens(tokenIn, tokenOut, amountIn, poolFee, amountOutMinimum=0, sqrtPriceLimitX96=0):
    try:
        nonce = web3.eth.getTransactionCount(account.address)

        # Encode the path correctly for ExactInputSingle
        transaction = swaprouter_contract.functions.ExactInputSingle(
            {
                'tokenIn': tokenIn,
                'tokenOut': tokenOut,
                'fee': poolFee,  # Remember that this is a uint24
                'recipient': account.address,
                'deadline': w3.eth.getBlock('latest')['timestamp'] + 60,
                'amountIn': amountIn,
                # Usually should be set to a non-zero value to prevent slippage
                'amountOutMinimum': amountOutMinimum,
                'sqrtPriceLimitX96': sqrtPriceLimitX96  # Usually set to 0 for no limit
            }
        ).buildTransaction({
            'chainId': 421614,
            'from': account.address,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price,
            'gas': 3000000,  # Increased gas limit, might need to increase it even further
        })

        signed_txn = w3.eth.account.signTransaction(
            transaction, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(f"Swap transaction hash: {w3.toHex(tx_hash)}")
        w3.eth.waitForTransactionReceipt(tx_hash)

    except Exception as e:
        print(f"Error swapping tokens: {e}")


def rebalance_liquidity():
    pass


def get_quote_price(token_in, token_out, amount_in, pool_fee=10000, sqrt_price_limit_x96=0):
    amount_out_data = quoter_contract.functions.quoteExactInputSingle({
        "tokenIn": token_in,
        "tokenOut": token_out,
        "amountIn": amount_in,
        "fee": pool_fee,
        "sqrtPriceLimitX96": sqrt_price_limit_x96
    }).call()

    amount_out = {
        "amountOut": amount_out_data[0],
        "sqrtPriceX96": amount_out_data[1],
        "initializedTicksCrossed": amount_out_data[2],
        "gasEstimate": amount_out_data[3]
    }

    return sqrt_price_X96_to_price(amount_out["sqrtPriceX96"]), amount_out["amountOut"]


def get_current_pool_ratio():
    slot0 = pool_contract.functions.slot0().call()
    slot0 = {
        "sqrtPriceX96": slot0[0],
        "tick": slot0[1],
        "observationCardinality": slot0[2],
        "observationCardinalityNext": slot0[3],
        "feeProtocol": slot0[4],
        "unlocked": slot0[5]
    }

    logger.info(f"Current slot0: {slot0}")
    return sqrt_price_X96_to_price(slot0["sqrtPriceX96"])


def rebalancing(
        target_ratio,
        token_in,
        token_out,
        token_in_decimals
) -> Tuple[float, float]:
    logger.info(f"Target ratio: {target_ratio}")

    step = 0.1
    amount_in = step
    (quote_price, _) = get_quote_price(token_in,
                                       token_out, parse_units(amount_in, token_in_decimals))
    logger.info(f"Initial quote price: {quote_price}")

    below = False
    above = False

    def plus(x): return x + step
    def minus(x): return x - step
    change = plus

    for i in range(1, 100):
        logger.info("----")
        logger.info("Amount in: " + str(amount_in))
        amount_in = change(amount_in)
        logger.info("Amount in: " + str(amount_in))

        if quote_price < target_ratio:
            below = True
            logger.info(f"Quote price below target ratio: {
                        quote_price}, {target_ratio}")
        else:
            above = True
            logger.info(f"Quote price above target ratio: {
                        quote_price}, {target_ratio}")

        (quote_price, _) = get_quote_price(token_in,
                                           token_out, parse_units(amount_in, token_in_decimals))
        logger.info(f"Quote price: {quote_price}")

        if below and above:
            if change == plus:
                change = minus
            else:
                change = plus
            step = step / 2
            below = False
            above = False

        if abs(quote_price - target_ratio) < 0.001:
            break

    return quote_price, amount_in


def rebalance_pool():
    latest_price = get_latest_price()
    target_ratio = format_units(
        latest_price["price"], latest_price["decimals"])

    logger.info(f"Current WTIST target price ratio: {target_ratio}")

    if target_ratio is not None and target_ratio > 0:
        tolerance = 0.01
        current_ratio = get_current_pool_ratio()

        logger.info(f"Current price ratio: {current_ratio}")

        deviation = abs(current_ratio - target_ratio) / target_ratio
        logger.info(f"Deviation: {deviation:.2%}")

        if deviation > tolerance:
            logger.info(f"*** Deviation above tolerance {tolerance:.2%} ***")
            logger.info(f"Current price ratio: {current_ratio}")
            logger.info(f"Target price ratio: {target_ratio}")
            logger.info(f"Price ratio deviated by {
                        deviation:.2%}. Rebalancing...")

            try:
                # Sell WTIST, buy USDC
                if current_ratio > target_ratio * (1 + tolerance):
                    logger.info("Sell WTIST, buy USDC")

                    (quote_price, amount_in) = rebalancing(target_ratio,
                        WTIST_CONTRACT_ADDRESS, USDC_CONTRACT_ADDRESS, 18)

                    logger.info(f"Final Quote price: {quote_price}")
                    logger.info(f"Final amount in: {amount_in} WTIST")

                # Sell USDC, buy WTIST
                else:
                    logger.info("Sell USDC, buy WTIST")

                    (quote_price, amount_in) = rebalancing(
                        target_ratio, USDC_CONTRACT_ADDRESS, WTIST_CONTRACT_ADDRESS, 6)

                    logger.info(f"Final Quote price: {quote_price}")
                    logger.info(f"Final amount in: {amount_in} USDC")
            except Exception as e:
                logger.error(f"Error rebalancing pool: {e}")
                logger.info("Trying again in 2 minutes...")
