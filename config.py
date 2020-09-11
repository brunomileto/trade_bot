import logging.config
from datetime import datetime
import logging
import time

API_KEY_TEST = 'VdBnQ9rM60MqELvvII4m7Pi6SBk06Urt6AAG2ixMTdX5maagTWrjZlr3MIaHsW9c'
SECRET_KEY_TEST = 'n1owlwcLarcLQNkJgwG8fdrjKgjuuE8aWiCVJcIJygLTPkHGBwPJMVO34yAJMaqK'
API_KEY = "T8OAWzBGVHVJokT6nHxP6Eqo0HNGkl9xgK79TmUXtbQhCI1M2rXwzA4E9C7rSTyI"
SECRET_KEY = "x6BUKF8D9tCEOT0ZyeME0Nchglngudw7HcVD7qzB1uy7BN0c7tUZJGbJDXFrJKD2"
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
