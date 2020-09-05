from binance.client import Client
import logging.config
from datetime import datetime
import logging


API_KEY_TEST = 'VdBnQ9rM60MqELvvII4m7Pi6SBk06Urt6AAG2ixMTdX5maagTWrjZlr3MIaHsW9c'
SECRET_KEY_TEST = 'n1owlwcLarcLQNkJgwG8fdrjKgjuuE8aWiCVJcIJygLTPkHGBwPJMVO34yAJMaqK'
API_KEY = "T8OAWzBGVHVJokT6nHxP6Eqo0HNGkl9xgK79TmUXtbQhCI1M2rXwzA4E9C7rSTyI"
SECRET_KEY = "x6BUKF8D9tCEOT0ZyeME0Nchglngudw7HcVD7qzB1uy7BN0c7tUZJGbJDXFrJKD2"
API_TEST_URL = 'https://testnet.binance.vision/api'


class MyAccount:

    INTERVAL_ONE_M = Client.KLINE_INTERVAL_1MINUTE
    INTERVAL_FIVE_M = Client.KLINE_INTERVAL_5MINUTE
    INTERVAL_FIFTEEN_M = Client.KLINE_INTERVAL_15MINUTE
    INTERVAL = [INTERVAL_ONE_M, INTERVAL_FIVE_M, INTERVAL_FIFTEEN_M]

    def __init__(self, minimum_order_len, api_key, secret_key, isTest):
        self.client = Client(api_key=api_key, api_secret=secret_key)
        if isTest is True:
            self.client.API_URL = 'https://testnet.binance.vision/api'
        self.account = self.client.get_account()
        self.aceptable_loss = 0.1
        self.max_trade_taxes = 0.001
        self.minimum_order_len = minimum_order_len
        self.bot_status = 'STAND_BY'

    def reverse_list(self, data_list):
        rev = data_list_param[::-1]
        return rev

    def dict_timestamp_to_time(self, data_dict, field_time_name):
        data_dict[field_time_name] = datetime.fromtimestamp(
            data_dict[field_time_name]/1000)
        return data_dict


class Asset(MyAccount):
    def __init__(self, asset_main, asset_pair, minimum_order_len, api_key, secret_key, isTest, interval='5', limit_data=202):
        super().__init__(minimum_order_len, api_key, secret_key, isTest)
        self.asset_main = asset_main.upper()
        self.asset_pair = asset_pair.upper()
        self.symbol = self.asset_main + self.asset_pair
        self.interval = self.INTERVAL_ONE_M
        # self.interval = self.interval[0]
        self.limit_data = limit_data
        # self.asset_candle_data_list = None
        self.tendency = None
        self.actual_price = None
        self.candle_data_list = []
        self.close_price_list = []
        self.close_volume_list = []
        self.my_init_asset_trade_balance = self.get_account_asset_balance(
            self.asset_pair)
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
        self.data_list_for_dict_print = ['self.mm8_now', 'self.mm8_before', ' self.mm10_now', 'self.mm10_before',
                                         'self.mm20_now', 'self.mm20_before', 'self.mm50_now', 'self.mm50_before',                                                    'self.mm200_now', 'self.mm200_before', 'self.close_now', 'self.close_before',                                                'self.volume_now', 'self.volume_before']
        self.data_dict_for_print = {}
        for var in self.data_list_for_dict_print:
            self.data_dict_for_print[var] = eval(var)

    def get_current_asset_value(self):
        ticker_data = self.client.get_symbol_ticker(symbol=self.symbol)
        self.actual_price = round(float(ticker_data['price']), 3)

    def get_account_asset_balance(self, asset):
        for balance in range(len(self.account['balances'])):
            if self.account['balances'][balance]['asset'] == asset:
                return round(float(self.account['balances'][balance]['free']), 4)

    def get_candle_asset_data(self):
        self.candle_data_list = self.reverse_list(
            client.get_klines(symbol=self.symbol, interval=self.interval))
        return

    def mm_now(self, period):
        numbers_series = pd.Series(self.close_price_list)
        windows = numbers_series.rolling(period_number)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        without_nans = moving_averages_list[period_number - 1:]
        return round(without_nans[0], 3)

    def mm_before(self, period):
        numbers_series = pd.Series(self.close_price_list)
        windows = numbers_series.rolling(period_number)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        without_nans = moving_averages_list[period_number - 1:]
        return round(without_nans[1], 3)

    def create_close_list(self):
        data = self.get_candle_asset_data()
        for index in range(1, len(data)):
            self.close_price_list.append(float(data[index][4]))
            self.close_volume_list.append(float(data[index][5]))

    def calculate_indicators(self):
        self.create_close_price_list()
        self.create_close_volume_list()
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
        else:
            self.tendency = 'STAND'
            return


class Trade(Asset, MyAccount):
    def __init__(self, minimum_order_len, api_key, secret_key, isTest, asset_main, asset_pair, interval='5', limit_data=202):
        super().__init__(asset_main, asset_pair,
                         minimum_order_len, api_key, secret_key, isTest)
        self.order_quantity = None
        self.order_made = None
        self.order_made_id = None
        self.order_made_status = None
        self.order_made_time = None
        self.order_executed = None
        self.order_executed_quantity = None
        self.order_executed_side = None
        self.order_executed_price = None
        self.order_executed_id = None
        self.profit_status = 'STANDING'
        self.stop = round(
            self.my_init_asset_trade_balance * self.aceptable_loss, 3)
        self.taxes_order_executed = None
        self.profit_check_value = None

    def make_market_order_entry_position(self):
        if self.tendency == 'STAND':
            return
        else:
            self.order_quantity = round(
                self.minimum_order_len/self.actual_price, 3)

            if self.tendency == 'UP':
                self.oder_made = self.client.order_market_buy(
                    symbol=self.symbol, quantity=self.order_quantity)

            if self.tendency == 'DOWN':
                self.oder_made = self.client.order_market_sell(
                    symbol=self.symbol, quantity=self.order_quantity)

            self.order_made = self.dict_timestamp_to_time(
                self.order_made, 'transactTime')
            self.order_made_id = self.order_made['orderId']
            self.order_made_status = self.order_made['status']
            self.order_made_time = self.order_made['transactTime']

    def make_market_order_out_position(self):
        if self.profit_status == 'STANDING':
            return
        elif self.profit_status == 'LOSING':
            if self.bot_status == 'BOUGHT':
                self.order_made = self.client.order_market_sell(
                    symbol=self.symbol, quantity=self.order_executed_quantity)
            if self.bot_status == 'SOLD':
                self.order_made = self.client.order_market_buy(
                    symbol=self.symbol, quantity=self.order_executed_quantity)

        elif self.profit_status == 'WINNING':
            if self.tendency == 'DOWN' and self.bot_status == 'BOUGHT':
                self.order_made = self.client.order_market_sell(
                    symbol=self.symbol, quantity=self.order_executed_quantity)
            if self.tendency == 'UP' and self.bot_status == 'LOSING':
                self.order_made = self.client.order_market_buy(
                    symbol=self.symbol, quantity=self.order_executed_quantity)
        self.order_made = self.dict_timestamp_to_time(
            self.order_made, 'transactTime')
        self.order_made_id = self.order_made['orderId']
        self.order_made_status = self.order_made['status']
        self.order_made_time = self.order_made['transactTime']

    def check_order_made_status(self):
        while True:
            order = self.client.get_order(
                symbol=self.symbol, orderId=self.order_made_id)
            status = order['status']
            if self.order_made_time + timedelta(minutes=5) < datetime.now():
                if status == 'PARTIALLY_FILLED':
                    if self.order_made_time + timedelta(minutes=20) < datetime.now():
                        self.order_made_status = status
                        self.order_executed = order
                        return
                if status == 'NEW':
                    self.client.cancel_order(
                        symbol=self.symbol, orderId=self.order_made_id)
            if status in ['FILLED', 'CANCELED', 'REJECTED', 'EXPIRED']:
                self.order_made_status = status
                self.order_executed = order
                return

    def organize_order_made(self):
        self.order_executed_side = self.order_executed['side']
        self.order_executed_id = self.order_executed['orderId']

        self.order_executed_quantity = float(
            self.order_executed['executedQty'])

        if len(self.order_made['fills']) > 0:
            self.order_executed_price = float(
                self.order_executed['fills'][0]['price'])
        else:
            self.order_executed_price = float(self.order_executed['price'])

        self.taxes_order_executed = round(
            self.order_executed_price * self.max_trade_taxes, 3)

        if self.order_executed_side == 'BUY':
            self.bot_status = 'BOUGHT'
        if self.order_executed_side == 'SELL':
            self.bot_status = 'SOLD'

    def check_profit_status(self):
        self.profit_check_value = round(
            self.actual_price * self.order_executed_quantity, 3) - self.taxes_current_price

        if self.bot_status == 'BOUGHT':
            if self.profit_check_value > round(self.minimum_order_len + self.stop, 3):
                self.profit_status = 'WINNING'
            elif self.profit_check_value < round(self.minimum_order_len - self.stop, 3):
                self.profit_status = 'LOSING'
            else:
                self.profit_status = 'STANDING'

        if self.bot_status == 'SOLD':
            if self.profit_check_value < round(self.minimum_order_len - self.stop, 3):
                self.profit_status = 'WINNING'
            elif self.profit_check_value > round(self.minimum_order_len + self.stop, 3):
                self.profit_status = 'LOSING'
            else:
                self.profit_status = 'STANDING'

    def get_out_current_position(self):
        while True:
            self.get_current_asset_value()
            self.taxes_current_price = round(
                self.actual_price * self.max_trade_taxes, 3)
            self.check_profit_status()
            self.calculate_indicators()
            self.check_asset_tendency_lvl_easy()
            self.make_market_order_out_position()
            self.check_order_made_status()
            if self.order_made_status in ['FILLED', 'PARTIALLY_FILLED']:
                return


def run():
    while True:
        bot = Trade(asset_main='BNB', asset_pair='USDT', minimum_order_len=0.1, isTest=True,
                    api_key=API_KEY_TEST, secret_key=SECRET_KEY_TEST, interval=1, limit_data=202)
        bot.get_candle_asset_data()
        bot.calculate_indicators()
        bot.check_asset_tendency_lvl_easy()
        bot.make_market_order_entry_position()
        bot.check_order_made_status()
        if bot.order_made_status not in ['CANCELED', 'REJECTED', 'EXPIRED']:
            bot.organize_order_made()
            bot.get_out_current_position

        # ORDEM CANCELADA, RECOMEÇAR
