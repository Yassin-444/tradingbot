import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = '7666973146:AAGH5wYdSUTGYwpBkoqRf4LRiQpmb_xB8mQ'
TELEGRAM_CHAT_ID = '1937600819'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Errore Telegram:", e)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("Ricevuto webhook:", data)

    # Format del messaggio Telegram
    if data:
        msg = f"Segnale ricevuto:\nSymbol: {data.get('symbol')}\nAction: {data.get('side')}\nType: {data.get('type')}"
        send_telegram_message(msg)

    return '', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)