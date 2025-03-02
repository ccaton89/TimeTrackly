import json
import requests
import time
from telegram import Bot

# --- Config (hardcoded) ---
config = {
"telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
"telegram_chat_id": "YOUR_CHAT_ID",
"blacklisted_coins": [],
"filters": {
"min_volume": 100000,
"max_supply_bundled": False
}
}

# --- Initialize Bot ---
bot = Bot(token=config["telegram_bot_token"])

# --- Token Check Logic ---
def check_token(token_address):
url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
response = requests.get(url)
data = response.json()

if token_address in config["blacklisted_coins"]:
return False, "Blacklisted"

if data["volume"]["h24"] < config["filters"]["min_volume"]:
return False, "Low volume"

return True, "Good token"

# --- Main Loop ---
def main():
while True:
token_address = "EXAMPLE_TOKEN_ADDRESS"
is_good, message = check_token(token_address)
if is_good:
bot.send_message(
chat_id=config["telegram_chat_id"],
text=f"Good token: {token_address}"
)
time.sleep(60)

# --- Start Bot ---
if __name__ == "__main__":
main()

