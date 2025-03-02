import time
from web3 import Web3
import configparser
from telegram import Bot

class TradingBot:
    def __init__(self):
        self.config = self._load_config()
        self.w3 = Web3(Web3.HTTPProvider(self.config['SETTINGS']['rpc_url']))
        self.tg_bot = Bot(token=self.config['SETTINGS']['telegram_token'])
        self.chat_id = self.config['SETTINGS']['chat_id']

    def _load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def send_telegram_message(self, message: str):
        self.tg_bot.send_message(chat_id=self.chat_id, text=message)

    def analyze_and_trade(self):
        while True:
            # Example: Send a test message
            self.send_telegram_message("Bot is running and analyzing the market!")
            time.sleep(60)  # Wait 1 minute before checking again

if __name__ == "__main__":
    bot = TradingBot()
    bot.send_telegram_message("Trading bot started!")
    bot.analyze_and_trade()
