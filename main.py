from datetime import datetime
from config import API_KEY, SECRET_KEY, API_KEY_TEST, SECRET_KEY_TEST, API_TEST_URL, LOGGER
from account import MyAccount
from asset import Asset
from trade import Trade


def run():
    LOGGER.info('INITIALIZING...')
    bot = Trade(asset_main='BNB', asset_pair='USDT', minimum_order_len=10, isTest=True,
                api_key=API_KEY_TEST, secret_key=SECRET_KEY_TEST, interval_to_work=1, limit_data=202)
    while True:
        LOGGER.info('GETTING CANDLE DATA')
        bot.get_candle_asset_data()
        LOGGER.info('CALCULATING INDICATORS')
        bot.calculate_indicators()
        LOGGER.info('CHECKING TENDENCY')
        bot.check_asset_tendency_lvl_easy()
        LOGGER.info('SAVING INDICATORS')
        bot.save_indicators_data()
        if bot.tendency in ['UP', 'DOWN']:
            LOGGER.info('MAKING AN ORDER')
            bot.make_market_order_entry_position()
            LOGGER.info('CHECKING ORDER STATUS')
            bot.check_order_made_status()
            if bot.order_made_status in ['FILLED', 'PARTIALLY_FILLED']:
                LOGGER.info('ORGANIZING ORDER INFO')
                bot.organize_order_made()
                LOGGER.info('GETTING OUT OF CURRENT POSITION')
                bot.get_out_current_position()
            else:
                LOGGER.info(f'ORDER {bot.order_made_status.upper()}')
                LOGGER.info(
                    f'TRYING AGAIN IN {bot.interval_to_work} MINUTE(S)')
                bot.wait_to_run_again()

        else:
            bot.bot_status = 'STAND_BY'
            LOGGER.info('ORDER NOT EXECUTED!')
            LOGGER.info(f'TRYING AGAIN IN {bot.interval_to_work} MINUTE(S)')
            bot.wait_to_run_again()


run()
