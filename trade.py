from datetime import datetime, timedelta
from config import LOGGER
from account import MyAccount
from asset import Asset
import time


class Trade(Asset, MyAccount):
    def __init__(self, minimum_order_len_asset_main, minimum_order_len_asset_pair, api_key, secret_key, isTest, asset_main, asset_pair, interval_to_work, limit_data=202):
        super().__init__(asset_main=asset_main, asset_pair=asset_pair, secret_key=secret_key, api_key=api_key,
                         minimum_order_len_asset_main=minimum_order_len_asset_main, minimum_order_len_asset_pair=minimum_order_len_asset_pair,
                         interval_to_work=interval_to_work, isTest=isTest, limit_data=limit_data)
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
        self.stop_main = round(
            self.minimum_order_len_asset_main * self.aceptable_loss, 8)
        self.stop_pair = round(
            self.minimum_order_len_asset_pair * self.aceptable_loss, 8)
        self.taxes_order_executed = None
        self.profit_check_value = None
        self.quoteqty = None

    def make_market_order_entry_position(self):
        # self.order_quantity = self.minimum_order_len_asset_main
        # self.order_quantity = round(
        #     self.minimum_order_len_asset_main/self.actual_price, 1)

        LOGGER.info(f'ACTUAL PRICE: {self.actual_price}')

        if self.tendency == 'UP':
            self.order_quantity = self.minimum_order_len_asset_pair
            LOGGER.info(f'ORDER QUANTITY: {self.order_quantity}')

            self.order_made = self.client.order_market_buy(
                symbol=self.symbol, quoteOrderQty=self.order_quantity)

        if self.tendency == 'DOWN':
            self.order_quantity = self.minimum_order_len_asset_main
            LOGGER.info(f'ORDER QUANTITY: {self.order_quantity}')
            self.order_made = self.client.order_market_sell(
                symbol=self.symbol, quantity=self.order_quantity)
        self.order_made = self.dict_timestamp_to_time(
            data_dict=self.order_made, field_time_name='transactTime')

        self.dict_list_dict_to_log(self.order_made)
        time.sleep(5)
        self.order_made_id = self.order_made['orderId']
        self.order_made_status = self.order_made['status']
        self.order_made_time = self.order_made['transactTime']
        LOGGER.info(
            'CHECK IF ORDER MADE DATA WAS PASSED TO RESPECTIVE VARIABLES:')
        LOGGER.info(f'ORDER MADE ID: {self.order_made_id}')
        LOGGER.info(f'ORDER MADE STATUS: {self.order_made_status}')
        LOGGER.info(f'ORDER MADE TIME: {self.order_made_time}')

    def make_market_order_out_position(self):
        if self.profit_status == 'LOSING':
            LOGGER.info('LOSING MONEY!')
            LOGGER.info('EXECUTING ORDER TO GET OUT OF CURRENT POSITION')
            if self.bot_status == 'BOUGHT':
                self.order_made = self.client.order_market_sell(
                    symbol=self.symbol, quantity=self.quoteqty)
            if self.bot_status == 'SOLD':
                self.order_made = self.client.order_market_buy(
                    symbol=self.symbol, quoteOrderQty=self.quoteqty)

            LOGGER.info('ORDER MADE: ')
            self.dict_list_dict_to_log(self.order_made)

        elif self.profit_status == 'WINNING':
            LOGGER.info('WINNING!')
            LOGGER.info(f'CURRENT POSITION: {self.bot_status}')
            LOGGER.info(f'CURRENT TENDENCY: {self.tendency}')

            if self.tendency == 'DOWN' and self.bot_status == 'BOUGHT':
                LOGGER.info('TENDENCY IS AGAINS MY POSITION')
                LOGGER.info('THE MARKET MAY TURN AROUND')
                LOGGER.info('EXECUTING ORDER TO GET OUT OF CURRENT POSITION')
                self.order_made = self.client.order_market_sell(
                    symbol=self.symbol, quantity=self.quoteqty)
            elif self.tendency == 'UP' and self.bot_status == 'LOSING':
                LOGGER.info('TENDENCY IS AGAINS MY POSITION')
                LOGGER.info('THE MARKET MAY TURN AROUND')
                LOGGER.info('EXECUTING ORDER TO GET OUT OF CURRENT POSITION')
                self.order_made = self.client.order_market_buy(
                    symbol=self.symbol, quoteOrderQty=self.quoteqty)
            else:
                self.order_made = None
                LOGGER.info('I MAY CAN STILL WINNING RIGHT NOW!')
                LOGGER.info('STILL IN THIS POSITION')
        time.sleep(5)
        self.order_made = self.dict_timestamp_to_time(
            self.order_made, 'transactTime')
        self.order_made_id = self.order_made['orderId']
        self.order_made_status = self.order_made['status']
        self.order_made_time = self.order_made['transactTime']
        LOGGER.info(
            'CHECK IF ORDER MADE DATA WAS PASSED TO RESPECTIVE VARIABLES:')
        LOGGER.info(f'ORDER MADE ID: {self.order_made_id}')
        LOGGER.info(f'ORDER MADE STATUS: {self.order_made_status}')
        LOGGER.info(f'ORDER MADE TIME: {self.order_made_time}')

    def check_order_made_status(self):
        while True:
            order = self.client.get_order(
                symbol=self.symbol, orderId=self.order_made_id)
            status = order['status']

            LOGGER.info(f'CURRENT ORDER STATUS: {status}')

            if self.order_made_time + timedelta(minutes=5) < datetime.now():
                if status == 'PARTIALLY_FILLED':
                    if self.order_made_time + timedelta(minutes=20) < datetime.now():
                        self.order_made_status = status
                        self.order_executed = order
                        if order['side'] == 'BUY':
                            self.bot_status = 'BOUGHT'
                        if order['side'] == 'SELL':
                            self.bot_status = 'SOLD'
                        return
                if status == 'NEW':
                    self.client.cancel_order(
                        symbol=self.symbol, orderId=self.order_made_id)
            if status in ['FILLED', 'CANCELED', 'REJECTED', 'EXPIRED']:
                self.order_made_status = status
                self.order_executed = order
                if status == 'FILLED':
                    if order['side'] == 'BUY':
                        self.bot_status = 'BOUGHT'
                    if order['side'] == 'SELL':
                        self.bot_status = 'SOLD'
                return
            LOGGER.info('WAITING 30 SECONDS TO CHECK ORDER AGAIN')
            time.sleet(30)

    def organize_order_made(self):
        self.order_executed = self.order_made
        LOGGER.info('SHOWING AGAIN, ORDER DATA: ')
        self.dict_list_dict_to_log(self.order_executed)

        self.order_executed_side = self.order_executed['side']

        if self.order_executed_side == 'SELL':
            self.bot_status = 'SOLD'
        elif self.order_executed_side == 'BUY':
            self.bot_status = 'BOUGHT'

        self.order_executed_id = self.order_executed['orderId']
        self.quoteqty = round(
            float(self.order_executed['cummulativeQuoteQty']), 8)
        self.order_executed_quantity = float(
            self.order_executed['executedQty'])

        if len(self.order_made['fills']) > 0:
            self.order_executed_price = float(
                self.order_made['fills'][0]['price'])
        else:
            self.order_executed_price = float(self.order_executed['price'])

        # self.taxes_order_executed = round(
        #     self.order_executed_price * self.max_trade_taxes, 8)
        # LOGGER.info(f'TAXES FOR EXECUTED ORDER: {self.order_executed_price}')

    def check_profit_status_bought_position(self):
        LOGGER.info('CHECKING PROFIT STATUS FOR BOUGHT POSITION')

        self.profit_check_value = round(
            self.actual_price * self.quoteqty, 6) - round(
            ((self.actual_price * self.quoteqty) * self.max_trade_taxes), 6)

        position_bought_winnin = round(
            self.order_executed_quantity + self.stop_pair, 6)
        position_bought_losing = round(
            self.order_executed_quantity - self.stop_pair, 6)

        LOGGER.info(f'PROFIT CHECK VALUE: {self.profit_check_value}')

        LOGGER.info(f'VALUES OF STOP TO CHECK OF:')

        LOGGER.info(
            f'POSITION BOUGHT/WINNING: {position_bought_winnin}')
        LOGGER.info(
            f'POSITION BOUGHT/LOSING: {position_bought_losing}')

        if self.profit_check_value > position_bought_winnin:
            self.profit_status = 'WINNING'
        elif self.profit_check_value < position_bought_losing:
            self.profit_status = 'LOSING'
        else:
            self.profit_status = 'STANDING'

    def check_profit_status_sold_position(self):
        LOGGER.info('CHECKING PROFIT STATUS FOR SOLD POSITION')
        self.profit_check_value = round(
            self.quoteqty / self.actual_price, 6) - round(
            ((self.quoteqty / self.actual_price) * self.max_trade_taxes), 6)

        position_sold_winnin = round(
            self.order_executed_quantity - self.stop_main, 6)
        position_sold_losing = round(
            self.order_executed_quantity + self.stop_main, 6)

        LOGGER.info(f'PROFIT CHECK VALUE: {self.profit_check_value}')

        LOGGER.info(f'VALUES OF STOP TO CHECK OF:')

        LOGGER.info(
            f'POSITION SOLD/WINNING: {position_sold_winnin}')
        LOGGER.info(
            f'POSITION SOLD/LOSING: {position_sold_losing}')

        if self.profit_check_value < position_sold_winnin:
            self.profit_status = 'WINNING'
        elif self.profit_check_value > position_sold_losing:
            self.profit_status = 'LOSING'
        else:
            self.profit_status = 'STANDING'

    def check_profit_status(self):
        if self.bot_status == 'BOUGHT':
            self.check_profit_status_bought_position()

        if self.bot_status == 'SOLD':
            self.check_profit_status_sold_position()

        LOGGER.info(f'PROFIT STATUS: {self.profit_status}')

    def get_out_current_position(self):
        while True:
            LOGGER.info('GETTING CURRENT VALUE OF THE ASSET')
            self.get_current_asset_value()

            LOGGER.info('CHECKING PROFIT STATUS')

            self.check_profit_status()

            LOGGER.info('CALCULATING INDICATORS')

            self.calculate_indicators()

            LOGGER.info('CHECKING TENDENCY')

            self.check_asset_tendency_lvl_easy()

            LOGGER.info('INDICATORS DATA TO GET OUT OF CURRENT POSITION')

            self.save_indicators_data()

            if self.profit_status in ['LOSING', 'WINNING']:
                LOGGER.info('MAKING THE ORDER')

                self.make_market_order_out_position()

                if self.order_made is not None:

                    # LOGGER.info('CHECKING ORDER STATUS')

                    # self.check_order_made_status()
                    if self.order_made_status in ['FILLED', 'PARTIALLY_FILLED']:
                        self.organize_order_made()
                        LOGGER.info(f'OUT OF POSITION: {self.bot_status}')
                        self.bot_status = 'STAND_BY'
                        return
                    else:
                        LOGGER.info('ORDER NOT EXECUTED')
                        LOGGER.info(
                            f'WAITING {self.interval_to_work} MINUTE(S), TO TRY TO GET OUT AGAIN')
                        self.wait_to_run_again()
                else:
                    LOGGER.info(
                        f'TRYING AGAIN IN {self.interval_to_work} MINUTE(S)')
                    self.wait_to_run_again()
            else:
                LOGGER.info('NOT WINNING OR LOSING YET')
                LOGGER.info(
                    f'CHECKING AGAIN IN {self.interval_to_work} MINUTE(S)')
                self.wait_to_run_again()
