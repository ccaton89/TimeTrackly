import time
from web3 import Web3
from solana.rpc.api import Client
from telegram import Bot

class TradingBot:
    def __init__(self):
        # Public RPC endpoints (no API keys needed)
        self.eth_rpc = "https://cloudflare-eth.com"  # Ethereum
        self.sol_rpc = "https://api.mainnet-beta.solana.com"  # Solana
        self.base_rpc = "https://mainnet.base.org"  # Base
        
        # Initialize blockchain connections
        self.eth_web3 = Web3(Web3.HTTPProvider(self.eth_rpc))
        self.sol_client = Client(self.sol_rpc)
        
        # Telegram setup
        self.tg_bot = Bot(token="7690402847:AAEGI2SbIEQIwUT5uyJmmoApQidfX3cW5ck")
        self.chat_id = "6428406707"

    def check_eth_balance(self, address: str) -> float:
        """Check ETH balance for a given address"""
        balance_wei = self.eth_web3.eth.get_balance(address)
        return self.eth_web3.from_wei(balance_wei, 'ether')

    def check_sol_balance(self, address: str) -> float:
        """Check SOL balance for a given address"""
        balance_lamports = self.sol_client.get_balance(address)['result']['value']
        return balance_lamports / 1e9  # Convert lamports to SOL

    def send_telegram_message(self, message: str):
        """Send a message via Telegram"""
        self.tg_bot.send_message(chat_id=self.chat_id, text=message)

    def run(self):
        """Main bot loop"""
        self.send_telegram_message("Trading bot started!")
        
        while True:
            # Example: Check balances
            eth_balance = self.check_eth_balance("0x2a98be6e8720965b489c0aa6f2b21c2aecf384c3")
            sol_balance = self.check_sol_balance("9ju26i5ePKJ2AoBh6GnvVTqbZ1EEj4t13KGjTA9kyj1S")
            
            # Send update
            self.send_telegram_message(
                f"ETH Balance: {eth_balance}\n"
                f"SOL Balance: {sol_balance}"
            )
            
            # Wait 1 minute before checking again
            time.sleep(60)

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
