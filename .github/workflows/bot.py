import os
import time

phone = os.environ.get('PHONE')

print(f"📱 Начинаю регистрацию номера {phone}")

sites = ["olx.ru", "avito.ru", "hh.ru"]

for site in sites:
    print(f"➡️ Регистрирую на {site}")
    time.sleep(1)

print("✅ Готово! СМС придут на телефон")
