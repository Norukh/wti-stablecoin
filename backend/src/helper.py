import requests
import json
import time

from constants import WTIST_CONTRACT_ADDRESS
from price import get_latest_price
from util import format_units

headers = {
    "Content-Type": "application/json"
}
infura_url = "https://arbitrum-sepolia.infura.io/v3/617c65d94c2b42d6a5845e2ebc63928a"
contract_address = WTIST_CONTRACT_ADDRESS
WTI_rest = 0


def get_block_details(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1
    }
    response = requests.post(
        infura_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['result']
    else:
        print(f"Error getting block details: {response.status_code}")
        print(response.text)
        return None


def get_latest_block():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    response = requests.post(
        infura_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        block_number = int(response_data['result'], 16)
        return block_number
    else:
        print(f"Error getting latest block number: {response.status_code}")
        print(response.text)
        return None


def fetch_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["ethereum"]["usd"]
        else:
            print(f"Error: Failed to fetch ETH price. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"Exception while fetching ETH price: {e}")
    return None


# not used
def read_wti_price():
    arbitrum_rpc_url = "https://arb1.arbitrum.io/rpc"

    chainlink_wti_contract_address = '0x594b919AD828e693B935705c3F816221729E7AE8'
    chainlink_latest_round_data_function_signature = "0xfeaf968c"

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": chainlink_wti_contract_address,
                "data": chainlink_latest_round_data_function_signature
            },
            "latest"  # Use the latest block
        ],
        "id": 1
    }

    # Send the request to the Arbitrum RPC
    response = requests.post(arbitrum_rpc_url, json=payload)
    response_data = response.json()

    # Check if the result exists
    if 'result' not in response_data:
        raise Exception(f"Error fetching WTI price: {response_data}")

    # Get the raw result
    raw_result = response_data['result']

    answer_hex = raw_result[66:130]
    answer = int(answer_hex, 16)

    if answer > (2 ** 255 - 1):
        answer -= 2 ** 256

    wti_price = answer / 10 ** 8
    return wti_price


def poll_blockchain():
    global WTI_rest
    global current_eth_price
    one_minute_ago = int(time.time()) - 60  # Get Unix time for 1 minute ago
    last_block = None
    amount_purchased = 0

    new_eth_price = fetch_eth_price()
    # update eth price to keep correct values (sometimes None)
    if new_eth_price is not None:
        print(f"New ETH price: {new_eth_price}")
        current_eth_price = new_eth_price
    print("Polling for the latest block...")
    latest_block = get_latest_block()

    if latest_block is not None:
        if last_block is None or latest_block > last_block:
            # Iterate over all blocks between last_block and latest_block
            for block_num in range(last_block + 1 if last_block else latest_block, latest_block + 1):
                block_details = get_block_details(block_num)
                if block_details is not None and 'timestamp' in block_details:
                    block_timestamp = int(block_details['timestamp'], 16)
                    # Check if the block is within the last minute
                    if block_timestamp >= one_minute_ago:

                        if 'transactions' in block_details:

                            for tx in block_details['transactions']:
                                if tx['to'] == contract_address:
                                    amount_purchased += int(tx['value'], 16) / (10 ** 18) * current_eth_price
                                if tx['from'] == contract_address:
                                    amount_purchased -= int(tx['value'], 16) / (10 ** 18) * current_eth_price

            last_block = latest_block
            one_minute_ago = int(time.time()) - 60

        latest_wti_price = get_latest_price()
        if latest_wti_price is not None:
            print(f"Latest WTI price: {latest_wti_price}")
            current_wti_price = format_units(latest_wti_price['price'], latest_wti_price['decimals'])
            print(f"Current WTI price: {current_wti_price}")
        else:
            print("Failed to get the latest WTI price.")

        amountoilpurchased = amount_purchased / current_wti_price
        amountoilpurchased += WTI_rest

        WTI_rest = amountoilpurchased % 1
        print(f"WTI rest value: {WTI_rest}")

        return amountoilpurchased
    else:
        print("Failed to get the latest block number.")
        return None
