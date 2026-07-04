import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('REPO')

user_data = {}

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' not in data:
        return 'OK', 200
    
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '').strip()
    
    if text == '/start':
        send_message(chat_id, "📱 Отправь номер телефона в формате:\n`79000357876`")
        return 'OK', 200
    
    if text.isdigit() and 10 <= len(text) <= 11:
        user_data[chat_id] = {'phone': text}
        send_message(chat_id, "⏱️ На сколько минут? (1-10)")
        return 'OK', 200
    
    if text.isdigit() and 1 <= int(text) <= 10:
        phone = user_data.get(chat_id, {}).get('phone')
        if not phone:
            send_message(chat_id, "❌ Сначала отправь номер!")
            return 'OK', 200
        
        minutes = int(text)
        
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
                "time": str(minutes),
                "chat_id": str(chat_id)
            }
        }
        
        r = requests.post(url, json=data, headers=headers)
        
        if r.status_code == 204:
            send_message(chat_id, f"✅ Регистрация {phone} запущена на {minutes} минут!")
        else:
            send_message(chat_id, "❌ Ошибка запуска")
        
        del user_data[chat_id]
        return 'OK', 200
    
    send_message(chat_id, "❌ Отправь номер в формате: `79000357876`")
    return 'OK', 200

def send_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
