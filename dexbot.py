import requests
import sqlite3
import time
import os
from datetime import datetime
from questionary import select, confirm

class DexBot:
    def __init__(self):
        self.db_name = "crypto_bot.db"
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS coins
                     (address TEXT PRIMARY KEY, symbol TEXT, last_checked TIMESTAMP)''')
        conn.commit()
        conn.close()

    def _get_menu_choice(self):
        return select(
            "What would you like to do?",
            choices=[
                "Add Coin to Watchlist",
                "Check Rug Status",
                "Analyze Prices",
                "Exit"
            ]).ask()

    def _get_coin_info(self):
        address = input("Enter token contract address: ").strip()
        symbol = input("Enter token symbol: ").strip().upper()
        return address, symbol

    def check_rug_status(self, address):
        try:
            data = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}").json()
            
            print("\n🔍 Analyzing Token:")
            print(f"📈 Price: ${data['pairs'][0]['priceUsd']}")
            print(f"💧 Liquidity: ${data['pairs'][0]['liquidity']['usd']}")
            print(f"🔄 Buy/Sell Tax: {self._calculate_tax(data['pairs'][0])}%")
            
            if self._is_risky(data):
                print("🚨 HIGH RISK DETECTED! Possible rug pull!")
            else:
                print("✅ Appears safe (basic checks passed)")
                
        except Exception as e:
            print(f"Error checking coin: {str(e)}")

    def _calculate_tax(self, pair_data):
        try:
            buy_tax = (1 - (pair_data['buyTax'] or 0))*100
            sell_tax = (pair_data['sellTax'] or 0)*100
            return max(buy_tax, sell_tax)
        except:
            return "Unknown"

    def _is_risky(self, data):
        pair = data['pairs'][0]
        return (
            pair['liquidity']['usd'] < 10000 or
            pair['priceUsd'] == 0 or
            pair['dexId'] not in ['uniswap', 'pancakeswap']
        )

    def run(self):
        while True:
            choice = self._get_menu_choice()
            
            if choice == "Add Coin to Watchlist":
                address, symbol = self._get_coin_info()
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO coins VALUES (?, ?, ?)",
                         (address, symbol, datetime.now()))
                conn.commit()
                conn.close()
                print("✅ Coin added to watchlist!")

            elif choice == "Check Rug Status":
                address = input("Enter contract address: ").strip()
                self.check_rug_status(address)

            elif choice == "Analyze Prices":
                print("\n📊 Price Analysis Coming Soon!")
                time.sleep(1)

            elif choice == "Exit":
                if confirm("Really quit?").ask():
                    print("👋 Goodbye!")
                    break

if __name__ == "__main__":
    os.system('clear')
    print("""
    ░██████╗░██╗░░██╗███████╗
    ██╔════╝░██║░░██║██╔════╝
    ██║░░██╗░███████║█████╗░░
    ██║░░╚██╗██╔══██║██╔══╝░░
    ╚██████╔╝██║░░██║███████╗
    ░╚═════╝░╚═╝░░╚═╝╚══════╝
    Crypto Safety Check Bot v1.0
    """)
    
    bot = DexBot()
    bot.run()
