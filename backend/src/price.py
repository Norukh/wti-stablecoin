import sqlite3
import requests
import json
from constants import PRICE_FEED_CONTRACT_ADDRESS, AGGREGATOR_INTERFACE_ABI, MAX_INT_64, PRICES_DB_PATH
from web3 import Web3

rpc_url = "https://arb1.arbitrum.io/rpc"
contract_address = PRICE_FEED_CONTRACT_ADDRESS

web3 = Web3(Web3.HTTPProvider(rpc_url))
abi = AGGREGATOR_INTERFACE_ABI

contract = web3.eth.contract(address=contract_address, abi=abi)

def init_db():
    conn = sqlite3.connect(PRICES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            roundId TEXT PRIMARY KEY,
            price BIGINT NOT NULL,
            startedAt TIMESTAMP NOT NULL,
            updatedAt TIMESTAMP NOT NULL,
            answeredInRound TEXT NOT NULL
        )
    ''')
    conn.close()

def get_decimals() -> int:
    if decimals <= 0:
        decimals = contract.functions.decimals().call()
    return decimals

def get_latest_price():
    latest_round_data = contract.functions.latestRoundData().call()
    return {
        "decimals": get_decimals(),
        "price": latest_round_data[1],
    }

def get_historical_price(round_id):
    historical_data = contract.functions.getRoundData(round_id).call()
    return {
        "round_id": historical_data[0],
        "price": historical_data[1],
        "started_at": historical_data[2],
        "updated_at": historical_data[3],
        "answered_in_round": historical_data[4]
    }

def load_historical_data():
    conn = sqlite3.connect(PRICES_DB_PATH)
    cursor = conn.cursor()

    latest_round = contract.functions.latestRoundData().call()
    latest_round_id = latest_round[0]

    num = latest_round_id
    num2 = MAX_INT_64

    phaseId = num >> 64
    aggregator_round_id = num & num2

    first_round_id = latest_round_id - aggregator_round_id + 1

    historical_data = []
    for round_id in range(first_round_id, latest_round_id):
        historical_pr = get_historical_price(round_id)

        print(str(historical_pr["round_id"]), 
            historical_pr["price"], 
            historical_pr["started_at"], 
            historical_pr["updated_at"], 
            str(historical_pr["answered_in_round"]))

        cursor.execute("INSERT OR IGNORE INTO entries (roundId, price, startedAt, updatedAt, answeredInRound) VALUES (?, ?, ?, ?, ?)",
                          (str(historical_pr["round_id"]), 
            historical_pr["price"], 
            historical_pr["started_at"], 
            historical_pr["updated_at"], 
            str(historical_pr["answered_in_round"])))
        conn.commit()


        historical_data.append(historical_pr)

    conn.close()


if __name__ == "__main__":
    init_db()
    load_historical_data()

