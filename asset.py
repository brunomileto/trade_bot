from datetime import datetime
from config import LOGGER
from account import MyAccount, client_production
import pandas as pd


class Asset(MyAccount):
    def __init__(self, asset_main, asset_pair, minimum_order_len, api_key, secret_key, isTest, interval_to_work, limit_data=202):
        super().__init__(minimum_order_len=minimum_order_len, api_key=api_key, secret_key=secret_key, isTest=isTest,
                         interval_to_work=interval_to_work)
        self.asset_main = asset_main.upper()
        self.asset_pair = asset_pair.upper()
        self.symbol = self.asset_main + self.asset_pair
        LOGGER.info(f'SYMBOL: {self.symbol}')
        self.candle_interval = self.interval_to_work
        self.interval = self.define_candle_interval()
        self.limit_data = limit_data
        self.tendency = None
        self.actual_price = None
        self.candle_data_list = []
        self.close_price_list = []
        self.close_volume_list = []
        self.my_init_asset_trade_balance = self.get_account_asset_balance(
            self.asset_pair)
        LOGGER.info(
            f'QUANTITY OF {self.asset_main}= {self.get_account_asset_balance(self.asset_main)}')
        LOGGER.info(
            f'QUANTITY OF {self.asset_pair}= {self.my_init_asset_trade_balance}')
        self.current_operated_asset_quantity = None
        self.mm8_now = None
        self.mm8_before = None
        self.mm10_now = None
        self.mm10_before = None
        self.mm20_now = None
        self.mm20_before = None
        self.mm50_now = None
        self.mm50_before = None
        self.mm200_now = None
        self.mm200_before = None
        self.close_now = None
        self.close_before = None
        self.volume_now = None
        self.volume_before = None
        self.taxes_current_price = None
        self.data_list_for_dict_print = ['self.tendency', 'self.mm8_now', 'self.mm8_before', ' self.mm10_now', 'self.mm10_before',
                                         'self.mm20_now', 'self.mm20_before', 'self.mm50_now', 'self.mm50_before',
                                         'self.mm200_now', 'self.mm200_before', 'self.close_now', 'self.close_before',
                                         'self.volume_now', 'self.volume_before']
        self.data_dict_for_print = {}

    def save_indicators_data(self):
        for var in self.data_list_for_dict_print:
            self.data_dict_for_print[var] = eval(var)
        self.dict_to_log(self.data_dict_for_print)

    def get_current_asset_value(self):
        ticker_data = client_production.get_symbol_ticker(symbol=self.symbol)
        self.actual_price = round(float(ticker_data['price']), 3)
        LOGGER.info(f'ACTUAL ASSET PRICE: {self.actual_price}')

    def get_account_asset_balance(self, asset):
        for balance in range(len(self.account['balances'])):
            if self.account['balances'][balance]['asset'] == asset:
                return round(float(self.account['balances'][balance]['free']), 4)

    def get_candle_asset_data(self):
        self.candle_data_list.clear()
        self.candle_data_list = self.reverse_list(
            client_production.get_klines(symbol=self.symbol, interval=self.interval))
        return

    def mm_now(self, period):
        numbers_series = pd.Series(self.close_price_list)
        windows = numbers_series.rolling(period)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        without_nans = moving_averages_list[period - 1:]
        return round(without_nans[0], 3)

    def mm_before(self, period):
        numbers_series = pd.Series(self.close_price_list)
        windows = numbers_series.rolling(period)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        without_nans = moving_averages_list[period - 1:]
        return round(without_nans[1], 3)

    def create_close_list(self):
        self.close_price_list.clear()
        self.close_volume_list.clear()
        for index in range(1, len(self.candle_data_list)):
            self.close_price_list.append(
                float(self.candle_data_list[index][4]))
            self.close_volume_list.append(
                float(self.candle_data_list[index][5]))

    def calculate_indicators(self):
        self.create_close_list()
        self.mm8_now = self.mm_now(8)
        self.mm8_before = self.mm_before(8)
        self.mm10_now = self.mm_now(10)
        self.mm10_before = self.mm_before(10)
        self.mm20_now = self.mm_now(20)
        self.mm20_before = self.mm_before(20)
        self.mm50_now = self.mm_now(50)
        self.mm50_before = self.mm_before(50)
        self.mm200_now = self.mm_now(200)
        self.mm200_before = self.mm_before(200)
        self.close_now = self.close_price_list[0]
        self.close_before = self.close_price_list[1]
        self.volume_now = self.close_volume_list[0]
        self.volume_before = self.close_volume_list[1]
        self.actual_price = self.close_now

    def check_asset_tendency_lvl_easy(self):
        if self.mm20_now > self.mm20_before:
            if self.close_now > self.close_before:
                self.tendency = 'UP'
                return
        if self.mm20_now < self.mm20_before:
            if self.close_now < self.close_before:
                self.tendency = 'DOWN'
                return
        self.tendency = 'STAND'
        return
