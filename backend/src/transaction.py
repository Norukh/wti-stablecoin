import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def adjust_oil_value(amount, action):
    url = os.getenv("OIL_API_URL", "http://localhost:5500/")
    payload = {"amount": amount, "action": action}
    try:
        response = requests.post(url + "oil", json=payload)
        if response.status_code == 200:
            logger.info(f"Success: {response.json()}")
        else:
            logger.error(f"Error: {response.status_code}, {response.json()}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
