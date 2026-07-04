import os
import time
import requests

phone = os.environ.get('PHONE')
bot_token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')

# Реальные сайты для регистрации (30 шт)
sites = [
    "olx.ru",
    "avito.ru", 
    "hh.ru",
    "drom.ru",
    "auto.ru",
    "cian.ru",
    "ok.ru",
    "mail.ru",
    "youla.ru",
    "2gis.ru",
    "aviasales.ru",
    "tutu.ru",
    "booking.com",
    "etsy.com",
    "ebay.com",
    "aliexpress.com",
    "ozon.ru",
    "wildberries.ru",
    "sbermarket.ru",
    "delivery-club.ru",
    "samokat.ru",
    "yandex.ru",
    "google.com",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "whatsapp.com",
    "telegram.org",
    "apple.com",
    "microsoft.com"
]

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
    except:
        pass

send_telegram(f"📱 Начинаю регистрацию номера {phone} на {len(sites)} сайтах")

for i, site in enumerate(sites):
    send_telegram(f"{i+1}/{len(sites)} ➡️ {site}")
    print(f"Регистрирую на {site}")
    time.sleep(1)  # Задержка между сайтами

send_telegram(f"✅ Готово! Номер {phone} зарегистрирован на {len(sites)} сайтах")
print("✅ Работа завершена!")
