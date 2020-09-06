from datetime import datetime
from config import API_KEY, SECRET_KEY, API_KEY_TEST, SECRET_KEY_TEST, API_TEST_URL, LOGGER
from account import MyAccount
from asset import Asset
from trade import Trade


def run():
    LOGGER.info('INITIALIZING...')
    bot = Trade(asset_main='BNB', asset_pair='BTC', minimum_order_len=0.0001, isTest=False,
                api_key=API_KEY, secret_key=SECRET_KEY, interval_to_work=5, limit_data=202)
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
            if ((bot.tendency == 'DOWN' and bot.asset_main_balance > 0) or
                    (bot.tendency == 'UP' and bot.asset_pair_balance > 0)):
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
                LOGGER.info(f'THE TENDENCY IDENTIFIED IS: {bot.tendency}')
                if bot.tendency == 'DOWN':
                    LOGGER.info(
                        f'BUT YOUR QUANTITY OF {bot.asset_main} IS: {bot.asset_main_balance}')
                else:
                    LOGGER.info(
                        f'BUT YOUR QUANTITY OF {bot.asset_pair} IS: {bot.asset_pair_balance}')

                LOGGER.info(
                    f'BECAUSE OF THAT IT WAS NOT POSSIBLE TO MAKE AN ORDER')
                LOGGER.info(
                    f'TRYING AGAIN IN {bot.interval_to_work} MINUTE(S)')
                bot.wait_to_run_again()
        else:
            bot.bot_status = 'STAND_BY'
            LOGGER.info('NO TENDENCY IDENTIFIED!')
            LOGGER.info(f'TRYING AGAIN IN {bot.interval_to_work} MINUTE(S)')
            bot.wait_to_run_again()


run()
