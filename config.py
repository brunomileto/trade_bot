import logging.config
from datetime import datetime
import logging
import time

API_KEY_TEST = ''
SECRET_KEY_TEST = ''
API_KEY = ""
SECRET_KEY = ""
API_TEST_URL = 'https://testnet.binance.vision/api'
TODAY = datetime.now().date().strftime("%d_%m_%y")


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(f'scripts/trades_of_{TODAY}.log'),
              logging.StreamHandler()],
    format='[%(asctime)s] [%(filename)s] [%(funcName)s] [MESSAGE] [%(message)s]',
    datefmt='%d/%m/%Y %I:%M:%S %p')

logging.basicConfig(
    level=logging.ERROR,
    handlers=[logging.FileHandler(f'scripts/trades_of_{TODAY}.log'),
              logging.StreamHandler()],
    format='[%(asctime)s] [%(filename)s] [%(funcName)s] [MESSAGE] [%(message)s]',
    datefmt='%d/%m/%Y %I:%M:%S %p')

LOGGER = logging.getLogger()
