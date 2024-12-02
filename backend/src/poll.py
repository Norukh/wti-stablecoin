import time
import logging
import schedule

from rebalancer import rebalance_pool, rebalance_liquidity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def adjust_oil_value(adjustment):
    url = "http://flask:5000/oil"
    payload = {"adjustment": adjustment}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Exception occurred: {e}")


def collateral_management():
    print("Collateral management...")
    rebalance_liquidity()


if __name__ == '__main__':
    logger.info("Starting WTIST backend...")

    logger.info("Schedule cron jobs...")
    schedule.every(2).minutes.do(rebalance_pool)
    schedule.every().hour.do(collateral_management)

    rebalance_pool()

    while True:
        schedule.run_pending()
        time.sleep(1)
