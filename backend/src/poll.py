import time
import requests
import json
import datetime

infura_url = "https://arbitrum-sepolia.infura.io/v3/617c65d94c2b42d6a5845e2ebc63928a"
contract_address = "0xB4BC5598b3e291188a35086Ef4EF31A951b7C1b2".lower()

headers = {
    "Content-Type": "application/json"
}


def get_latest_block():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    response = requests.post(infura_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        block_number = int(response_data['result'], 16)
        return block_number
    else:
        print(f"Error getting latest block number: {response.status_code}")
        print(response.text)
        return None


def get_block_details(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],  # True to include full transaction objects
        "id": 1
    }
    response = requests.post(infura_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        return response_data['result']
    else:
        print(f"Error getting block details: {response.status_code}")
        print(response.text)
        return None


def poll_blockchain():
    one_minute_ago = int(time.time()) - 60  # Get Unix time for 1 minute ago
    last_block = None

    while True:
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
                            print(f"Block {block_num} is from the last minute, timestamp: {datetime.datetime.utcfromtimestamp(block_timestamp)}")
                            if 'transactions' in block_details:
                                for tx in block_details['transactions']:
                                    # Check if the transaction involves the contract address
                                    if tx.get('to') and tx['to'].lower() == contract_address:
                                        print(f"Transaction involving contract found in block {block_num}:")
                                        print(f"Tx Hash: {tx['hash']}")
                                        print(f"From: {tx['from']}")
                                        print(f"To: {tx['to']}")
                                        print(f"Value: {int(tx['value'], 16) / (10 ** 18)} ETH")
                                        print(f"Value in dollars: {int(tx['value'], 16) / (10 ** 18)*3000}$")

                # Update the last block number polled and current time
                last_block = latest_block
                one_minute_ago = int(time.time()) - 10

        else:
            print("Failed to get the latest block number.")

        time.sleep(10)  # Polling interval


if __name__ == '__main__':
    print("Starting polling script...")
    poll_blockchain()
