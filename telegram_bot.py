import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('MY_GITHUB_TOKEN')
REPO = os.environ.get('REPO')

# Храним временные данные пользователей
user_data = {}

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' not in data:
        return 'OK', 200
    
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '').strip()
    
    # ===== КОМАНДА /START =====
    if text == '/start':
        send_message(chat_id, "📱 Отправь номер телефона в формате:\n`79000357876`")
        user_data[chat_id] = {'step': 'phone'}
        return 'OK', 200
    
    # ===== ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВЁЛ НОМЕР =====
    if text.isdigit() and 10 <= len(text) <= 11:
        # Проверяем, что пользователь на шаге "phone"
        if chat_id in user_data and user_data[chat_id].get('step') == 'phone':
            user_data[chat_id]['phone'] = text
            user_data[chat_id]['step'] = 'time'
            send_message(chat_id, "⏱️ На сколько минут? (от 1 до 10)")
        else:
            send_message(chat_id, "❌ Напиши /start сначала")
        return 'OK', 200
    
    # ===== ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВЁЛ ВРЕМЯ =====
    if text.isdigit() and 1 <= int(text) <= 10:
        # Проверяем, что пользователь на шаге "time" и есть номер
        if chat_id in user_data and user_data[chat_id].get('step') == 'time':
            phone = user_data[chat_id]['phone']
            minutes = int(text)
            
            send_message(chat_id, f"✅ Запускаю регистрацию {phone} на {minutes} минут!")
            send_message(chat_id, f"📱 СМС придут на твой телефон в течение {minutes} минут")
            
            # Запускаем GitHub Actions
            url = f"https://api.github.com/repos/{REPO}/actions/workflows/run.yml/dispatches"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "ref": "main",
                "inputs": {
                    "phone": phone,
                    "time": str(minutes)
                }
            }
            
            r = requests.post(url, json=data, headers=headers)
            
            if r.status_code != 204:
                send_message(chat_id, "❌ Ошибка запуска. Попробуй позже")
            
            # Очищаем данные пользователя
            del user_data[chat_id]
        else:
            send_message(chat_id, "❌ Сначала отправь номер через /start")
        return 'OK', 200
    
    # ===== ЕСЛИ НЕПОНЯТНЫЙ ТЕКСТ =====
    send_message(chat_id, "❌ Отправь номер в формате:\n`79000357876`\nИли нажми /start")
    return 'OK', 200

# ===== ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ =====
def send_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        })
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
