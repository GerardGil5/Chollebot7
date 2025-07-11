import os
from telegram import Bot
from telegram.error import TelegramError

# Leer variables de entorno
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print(f"📦 BOT_TOKEN: {'CARGADO' if TOKEN else 'VACÍO'}")
print(f"📦 CHANNEL_ID: {CHANNEL_ID}")

try:
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHANNEL_ID, text="✅ El bot se ha iniciado correctamente.")
    print("✅ Mensaje enviado con éxito")
except TelegramError as e:
    print("❌ Error al enviar el mensaje:")
    print(e)
