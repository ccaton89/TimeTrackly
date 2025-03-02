import requests
import sqlite3
import time
from datetime import datetime
from questionary import select, confirm, text

class TradingBot:
    def __init__(self):
        self.db_name = "crypto_trading.db"
        self.balance = 1000  # Starting balance in USD
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS trades
                     (id INTEGER PRIMARY KEY,
                      pair TEXT,
                      amount REAL,
                      price REAL,
                      type TEXT,
                      timestamp DATETIME)''')
        conn.commit()
        conn.close()

    def show_menu(self):
        while True:
            choice = select(
                "Crypto Trading Bot",
                choices=[
                    "Analyze Token",
                    "Simulate Trade",
                    "Portfolio",
                    "Trading History",
                    "Exit"
                ]).ask()

            if choice == "Analyze Token":
                self.analyze_token()
            elif choice == "Simulate Trade":
                self.simulate_trade()
            elif choice == "Portfolio":
                self.show_portfolio()
            elif choice == "Trading History":
                self.show_history()
            elif choice == "Exit":
                if confirm("Exit the bot?").ask():
                    print("Happy trading! 👋")
                    break

    def analyze_token(self):
        token = text("Enter token contract address:").ask()
        try:
            data = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{token}").json()
            pair = data['pairs'][0]
            
            print(f"\n📊 {pair['baseToken']['symbol']} Analysis:")
            print(f"Price: ${pair['priceUsd']}")
            print(f"24h Change: {pair['priceChange']['h24']}%")
            print(f"Liquidity: ${pair['liquidity']['usd']}")
            print(f"Volume: ${pair['volume']['h24']}")
            
            if pair['liquidity']['usd'] < 10000:
                print("⚠️ Low liquidity warning!")
            if abs(float(pair['priceChange']['h24'])) > 30:
                print("⚠️ High volatility!")
                
        except Exception as e:
            print(f"Error analyzing token: {str(e)}")

    def simulate_trade(self):
        pair = text("Enter trading pair (e.g., ETH/USDC):").ask()
        amount = float(text("Enter amount in USD:").ask())
        trade_type = select("Trade type:", choices=["Buy", "Sell"]).ask()

        if trade_type == "Buy" and amount > self.balance:
            print("❌ Insufficient funds!")
            return
            
        # Get simulated price
        price = self.get_market_price(pair)
        
        print(f"\n🔔 Executing {trade_type} order:")
        print(f"Pair: {pair}")
        print(f"Amount: ${amount}")
        print(f"Price: ${price}")
        
        if confirm("Confirm trade?").ask():
            self.record_trade(pair, amount, price, trade_type)
            if trade_type == "Buy":
                self.balance -= amount
            else:
                self.balance += amount
            print("✅ Trade executed!")

    def get_market_price(self, pair):
        # Simulate real pricing with 1% random variation
        return 1800 * (1 + (0.01 * (0.5 - (time.time() % 1))))

    def record_trade(self, pair, amount, price, trade_type):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''INSERT INTO trades 
                     (pair, amount, price, type, timestamp)
                     VALUES (?,?,?,?,?)''',
                  (pair, amount, price, trade_type, datetime.now()))
        conn.commit()
        conn.close()

    def show_portfolio(self):
        print(f"\n💼 Portfolio Balance: ${self.balance:.2f}")
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM trades WHERE type='Buy'")
        buys = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM trades WHERE type='Sell'")
        sells = c.fetchone()[0] or 0
        print(f"Total Invested: ${buys - sells:.2f}")

    def show_history(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT 5")
        print("\n📜 Recent Trades:")
        for trade in c.fetchall():
            print(f"{trade[4]} {trade[1]} - ${trade[2]} @ ${trade[3]}")

if __name__ == "__main__":
    print("""
    ┏━━┓┏┓╋┏┓┏━━┓┏┓╋╋┏┓
    ┃┏┓┃┃┃╋┃┃┗┫┣┛┃┃╋╋┃┃
    ┃┗┛┃┃┗━┛┃╋┃┃╋┃┗━┓┃┃
    ┃┏━┛┃┏━┓┃╋┃┃╋┃┏┓┃┃┃
    ┃┃╋╋┃┃╋┃┃┏┫┣┓┃┃┃┣┫┗┓
    ┗┛╋╋┗┛╋┗┛┗━━┛┗┛┗┻┻━┛
    """)
    bot = TradingBot()
    bot.show_menu()
