import os
import json
import time
import requests
import threading
from bs4 import BeautifulSoup
from telegram import Bot

PRODUCTS_FILE = "products.json"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=BOT_TOKEN)

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

def scrape_amazon():
    url = "https://www.amazon.es/gp/bestsellers"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    products = []
    for item in soup.select(".zg-grid-general-faceout")[:10]:
        title_tag = item.select_one(".p13n-sc-truncate, ._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        link_tag = item.select_one("a.a-link-normal")
        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.amazon.es" + link_tag["href"]
            products.append({"title": title, "link": link})
    return products

def send_new_products():
    old_products = load_products()
    old_links = {p["link"] for p in old_products}
    new_products = scrape_amazon()

    for product in new_products:
        if product["link"] not in old_links:
            try:
                bot.send_message(chat_id=CHANNEL_ID, text=f"🛒 {product['title']}\n🔗 {product['link']}")
                print(f"✅ Publicado: {product['title']}")
            except Exception as e:
                print(f"❌ Error al enviar mensaje: {e}")

    save_products(new_products)

def loop():
    while True:
        send_new_products()
        time.sleep(600)  # cada 10 minutos

if __name__ == "__main__":
    print("📦 BOT_TOKEN:", "CARGADO" if BOT_TOKEN else "NO DEFINIDO")
    print("📦 CHANNEL_ID:", CHANNEL_ID if CHANNEL_ID else "NO DEFINIDO")

    try:
        bot.send_message(chat_id=CHANNEL_ID, text="Chollebot está en marcha 🚀")
        threading.Thread(target=loop, daemon=True).start()
        while True:
            time.sleep(3600)
    except Exception as e:
        print("❌ Error al iniciar:", e)
