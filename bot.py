from dotenv import load_dotenv
import os
import requests
from flask import Flask, request

# Carica variabili da .env
load_dotenv()

app = Flask(__name__)

# Variabili ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Endpoint per UptimeRobot
@app.route('/', methods=['GET'])
def home():
    return 'Bot attivo!'

# Funzione per inviare messaggi Telegram
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

# Webhook da TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Ricevuto webhook:", data)

    if data:
        msg = f"Segnale ricevuto:\nSymbol: {data.get('symbol')}\nAction: {data.get('side')}\nType: {data.get('type')}"
        send_telegram_message(msg)

    return '', 200

# Avvio server Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)