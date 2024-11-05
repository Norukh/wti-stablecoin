import time
import requests
import json


infura_url = "https://arbitrum-sepolia.infura.io/v3/617c65d94c2b42d6a5845e2ebc63928a"

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
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def poll_blockchain():
    while True:
        print("Polling for the latest block...")
        latest_block = get_latest_block()
        if latest_block is not None:
            print(f"Latest Block Number: {latest_block}")
        else:
            print("Failed to get the latest block number.")
        time.sleep(5)


if __name__ == '__main__':
    print("Starting polling script...")
    poll_blockchain()
