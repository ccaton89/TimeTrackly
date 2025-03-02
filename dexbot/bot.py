import time
import requests
import yaml
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize Telegram bot
bot = Bot(token=config["telegram"]["token"])
chat_id = config["telegram"]["chat_id"]

# Track historical data for trend analysis
price_history = {}
volume_history = {}

def get_pair_data(chain, pair_address):
    """Fetch DexScreener data with error handling"""
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}"
        response = requests.get(url, timeout=10)
        return response.json().get("pair", {})
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return {}

def analyze_token(pair_data):
    """Advanced Solana token analysis for pumps and whales"""
    alerts = []
    recommendations = []
    
    # Extract metrics
    liquidity = pair_data.get("liquidity", {}).get("usd", 0)
    volume_24h = pair_data.get("volume", {}).get("h24", 0)
    holders = pair_data.get("holders", 0)
    price = pair_data.get("priceUsd", 0)
    price_change_1h = pair_data.get("priceChange", {}).get("h1", 0)
    fdv = pair_data.get("fdv", 0)
    txns_24h = pair_data.get("txns", {}).get("h24", {}).get("count", 0)
    
    # Whale detection
    if txns_24h > 1000 and volume_24h > 1000000:  # High activity
        alerts.append("🐳 WHALE ALERT: High transaction volume (>1M)")
        
    # Pump detection
    if volume_24h > (liquidity * 5):  # Volume 5x liquidity = pump
        alerts.append("🚨 PUMP DETECTED: Volume 5x liquidity")
        
    if price_change_1h > 20:  # 20%+ price increase
        alerts.append("🚀 PUMP IN PROGRESS: Price up 20%+ in 1h")
        
    # High-reward buy signals
    if liquidity > 100000 and volume_24h > 500000:  # Strong base
        if price_change_1h < -10:  # 10%+ dip
            recommendations.append("🔥 BUY OPPORTUNITY: 10%+ dip with strong liquidity")
        elif price_change_1h > 15:  # 15%+ pump
            recommendations.append("💰 TAKE PROFIT: 15%+ pump detected")
            
    # Low-cap gems
    if liquidity < 50000 and volume_24h > 100000:  # Micro-cap with activity
        recommendations.append("💎 LOW-CAP GEM: High volume, low liquidity")

    # Compile report
    analysis = "\n".join(alerts + recommendations)
    return analysis or "✅ No strong signals detected"

def check_pairs():
    """Main monitoring function for Solana tokens"""
    try:
        # Example Solana pairs (replace with your favorites)
        solana_pairs = [
            ("solana", "PAIR_ADDRESS_1"),  # Replace with actual pair address
            ("solana", "PAIR_ADDRESS_2"),  # Add more pairs here
        ]
        
        for chain, pair_address in solana_pairs:
            pair_data = get_pair_data(chain, pair_address)
            
            if not pair_data:
                logger.error(f"Failed to fetch data for {pair_address}")
                continue
                
            analysis = analyze_token(pair_data)
            
            # Send Telegram alert
            message = (
                f"📈 **{pair_data.get('baseToken', {}).get('name', 'Unknown')} Analysis**\n"
                f"• Price: ${pair_data.get('priceUsd', 'N/A')}\n"
import time
import requests
import yaml
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize Telegram bot
bot = Bot(token=config["telegram"]["token"])
chat_id = config["telegram"]["chat_id"]

# Track previous states for trend analysis
price_history = {}
volume_history = {}

def get_pair_data(chain, pair_address):
    """Fetch DexScreener data with error handling"""
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}"
        response = requests.get(url, timeout=10)
        return response.json().get("pair", {})
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return {}

def analyze_token(pair_data):
    """Advanced rug detection and trading signals"""
    alerts = []
    recommendations = []
    
    # Extract metrics
    liquidity = pair_data.get("liquidity", {}).get("usd", 0)
    volume_24h = pair_data.get("volume", {}).get("h24", 0)
    holders = pair_data.get("holders", 0)
    price = pair_data.get("priceUsd", 0)
    price_change_1h = pair_data.get("priceChange", {}).get("h1", 0)
    fdv = pair_data.get("fdv", 0)
    
    # Track historical data
    pair_address = pair_data.get("pairAddress", "default")
    current_time = time.time()
    
    # Rug-pull detection (RED FLAGS)
    if liquidity < 50000:  # $50K liquidity floor
        alerts.append("🚨 EXTREME RISK: Liquidity < $50K (High rug probability)")
    elif liquidity < 100000:
        alerts.append("⚠️ WARNING: Liquidity < $100K (Possible micro-cap)")
        
    if volume_24h > (liquidity * 3):  # Volume 3x liquidity = pump
        alerts.append("🚨 PUMP DETECTED: Volume 3x liquidity")
        
    if holders < 150:
        alerts.append("⚠️ CENTRALIZATION: <150 holders")
        
    if fdv > (liquidity * 100):  # FDV 100x liquidity = overvalued
        alerts.append("🚨 OVERVALUED: FDV 100x liquidity")

    # Trading signals (GREEN FLAGS)
    if liquidity > 500000 and volume_24h > 1000000:  # Strong base
        if price_change_1h < -15:
            recommendations.append("🔥 BUY OPPORTUNITY: 15%+ dip with strong liquidity")
        elif price_change_1h > 25:
            recommendations.append("💰 TAKE PROFIT: 25%+ pump detected")
            
    # Whale watching
    if volume_24h > 5000000 and abs(price_change_1h) > 30:
        alerts.append("🐳 WHALE ALERT: Massive price move with high volume")

    # Compile report
    analysis = "\n".join(alerts + recommendations)
    return analysis or "✅ No strong signals detected"

def check_pairs():
    """Main monitoring function"""
    try:
        # Example: Check ETH/USDC Uniswap v3
        pair_data = get_pair_data("ethereum", "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")
        
        if not pair_data:
            logger.error("Failed to fetch pair data")
            return
            
        analysis = analyze_token(pair_data)
        
        # Send Telegram alert
        message = (
            "📈 **Pair Analysis**\n"
            f"• Price: ${pair_data.get('priceUsd', 'N/A')}\n"
            f"• 1h Change: {pair_data.get('priceChange', {}).get('h1', 0):.2f}%\n"
            f"• Liquidity: ${pair_data.get('liquidity', {}).get('usd', 0):,.0f}\n"
            f"• Volume 24h: ${pair_data.get('volume', {}).get('h24', 0):,.0f}\n\n"
            f"**Alerts**\n{analysis}"
        )
        
        bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown"
        )
        logger.info("Analysis sent to Telegram")
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")

# Run every 3 minutes for real-time tracking
scheduler = BlockingScheduler()
scheduler.add_job(check_pairs, 'interval', minutes=3)
scheduler.start()
import os
import requests
import yaml
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize Telegram bot
bot = Bot(token=config["telegram"]["token"])
chat_id = config["telegram"]["chat_id"]

# DexScreener API functions
def get_pair_data(chain_id, pair_address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain_id}/{pair_address}"
    response = requests.get(url)
    return response.json()

def analyze_token(pair_data):
    # Basic analysis example
    liquidity = pair_data["liquidity"]["usd"]
    volume_24h = pair_data["volume"]["h24"]
    
    if volume_24h > 100000 and liquidity < 50000:
        return "⚠️ Low liquidity alert!"
    return "✅ Looks safe"

# Main bot logic
def check_pairs():
    # Example: Check Uniswap ETH/USDC pair
    pair_data = get_pair_data("ethereum", "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")
    analysis = analyze_token(pair_data)
    
    # Send Telegram alert
    bot.send_message(
        chat_id=chat_id,
        text=f"📊 Pair Analysis:\n{analysis}\nLiquidity: ${pair_data['liquidity']['usd']}"
    )

# Schedule checks every 5 minutes
scheduler = BlockingScheduler()
scheduler.add_job(check_pairs, 'interval', minutes=5)
scheduler.start()
