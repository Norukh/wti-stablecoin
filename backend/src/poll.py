import time
import logging
import schedule

from rebalancer import rebalance_pool
from helper import poll_blockchain
from transaction import adjust_oil_value


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def collateral_management():
    print("Collateral management...")
    amount_oil_purchased = poll_blockchain()

    if amount_oil_purchased is not None and amount_oil_purchased != 0:
        logger.info(f"Amount of oil purchased: {amount_oil_purchased}")

        action = None
        if amount_oil_purchased > 0:
            action = "BUY"
        else:
            action = "SELL"

        adjust_oil_value(amount_oil_purchased, action)


if __name__ == '__main__':
    logger.info("Starting WTIST backend...")

    logger.info("Schedule cron jobs...")
    schedule.every().minutes.do(rebalance_pool)
    schedule.every().minutes.do(collateral_management)

    rebalance_pool()
    collateral_management()

    while True:
        schedule.run_pending()
        time.sleep(1)
