import os
import json
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)

def load_products():
    try:
        with open("products.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

def load_user_prefs():
    try:
        with open("user_prefs.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading user prefs: {e}")
        return {}

if __name__ == "__main__":
    print("Bot is running...")
    products = load_products()
    prefs = load_user_prefs()
    bot.send_message(chat_id=CHANNEL_ID, text="Chollebot está en marcha 🚀")