import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

phone = os.environ.get('PHONE')

# Сайты для проверки (добавим ещё позже)
sites = [
    {"url": "https://www.olx.ru", "selector": "input[name='phone']"},
    {"url": "https://www.avito.ru", "selector": "input[name='phone']"},
    {"url": "https://hh.ru", "selector": "input[name='phone']"}
]

# Настройки браузера (без графики)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

print(f"📱 Начинаю регистрацию номера {phone}")

for site in sites:
    try:
        print(f"➡️ Открываю {site['url']}")
        driver.get(site['url'])
        time.sleep(3)
        
        # Ищем поле для номера
        phone_field = driver.find_element(By.CSS_SELECTOR, site['selector'])
        phone_field.clear()
        phone_field.send_keys(phone)
        print(f"   ✅ Номер введён")
        
        # Пытаемся нажать кнопку "Получить код"
        try:
            send_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Получить') or contains(text(), 'Отправить') or contains(text(), 'Далее')]")
            send_btn.click()
            print(f"   ✅ Код запрошен")
        except:
            print(f"   ⚠️ Кнопка не найдена")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Ошибка: {str(e)[:50]}")
        continue

driver.quit()
print("✅ Готово! Проверь телефон — должны прийти СМС")
