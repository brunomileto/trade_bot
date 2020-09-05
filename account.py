from binance.client import Client
from datetime import datetime
from config import LOGGER, API_KEY, SECRET_KEY
from pprint import pprint

client_production = Client(api_key=API_KEY, api_secret=SECRET_KEY)


class MyAccount:

    def __init__(self, minimum_order_len, api_key, secret_key, isTest, interval_to_work=5):
        self.client = Client(api_key=api_key, api_secret=secret_key)
        if isTest is True:
            self.client.API_URL = 'https://testnet.binance.vision/api'
        self.account = self.client.get_account()
        LOGGER.info('ACCOUNT DATA: ')
        self.dict_list_dict_to_log(self.account)

        self.interval_to_work = interval_to_work
        self.time_now = None
        self.time_to_run = None
        self.aceptable_loss = 0.1
        self.max_trade_taxes = 0.001
        self.minimum_order_len = minimum_order_len
        self.bot_status = 'STAND_BY'
        self.interval_list = []

    def reverse_list(self, data_list):
        rev = data_list[::-1]
        return rev

    def dict_timestamp_to_time(self, data_dict, field_time_name):
        data_dict[field_time_name] = datetime.fromtimestamp(
            data_dict[field_time_name]/1000)
        return data_dict

    def dict_to_log(self, dict_data):
        for item in dict_data:
            LOGGER.info(f'{item}: {dict_data[item]}')

    def dict_list_dict_to_log(self, dict_list_dict_data):
        for item in dict_list_dict_data:
            try:
                len(item)
                for index in dict_list_dict_data[item]:
                    for item_2 in index:
                        LOGGER.info(
                            f'{item_2}: {index[item_2]}')
            except:
                LOGGER.info(
                    f'{item}: {dict_list_dict_data[item]}')

    def define_candle_interval(self):
        if self.interval_to_work == 1:
            return Client.KLINE_INTERVAL_1MINUTE
        elif self.interval_to_work == 5:
            return Client.KLINE_INTERVAL_5MINUTE
        elif self.interval_to_work == 15:
            return Client.KLINE_INTERVAL_15MINUTE

    def get_time_now(self):
        self.time_now = None
        self.time_now = datetime.now()

    def get_time_to_run(self):
        minute = 0
        self.interval_list.clear()
        self.interval_list.append(minute)

        while minute < 59:
            minute = minute + self.interval_to_work
            self.interval_list.append(minute)
        self.get_time_now()

        for the_minute in self.interval_list:
            if self.time_now.minute < the_minute:
                minute_to_run = the_minute
                break
        self.time_to_run = datetime(
            self.time_now.year, self.time_now.month, self.time_now.day, self.time_now.hour, minute_to_run, 0)

    def wait_to_run_again(self):
        self.get_time_to_run()
        while True:
            if datetime.now() > self.time_to_run:
                break
            else:
                pass
