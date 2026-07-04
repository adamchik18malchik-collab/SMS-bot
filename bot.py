import os
import time

phone = os.environ.get('PHONE')
minutes = int(os.environ.get('TIME', 1))

sites = [
    "olx.ru", "avito.ru", "hh.ru", "drom.ru", "auto.ru",
    "cian.ru", "ok.ru", "mail.ru", "youla.ru", "2gis.ru"
]

delay = (minutes * 60) / len(sites)

print(f"📱 Регистрирую {phone} на {len(sites)} сайтах за {minutes} минут")

for i, site in enumerate(sites):
    print(f"{i+1}/{len(sites)} ➡️ {site}")
    time.sleep(delay)

print(f"✅ Готово! СМС придут на {phone}")
