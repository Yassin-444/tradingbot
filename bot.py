from dotenv import load_dotenv
import os
import requests
import csv
from flask import Flask, request
from datetime import datetime

# Carica variabili da .env
load_dotenv()

# Configurazioni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)

# Invia un messaggio Telegram testuale
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Errore invio Telegram:", e)

# Registra segnale nel file CSV con timestamp
def log_signal(symbol, side, order_type):
    file_exists = os.path.isfile("log.csv")
    with open("log.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "side", "type"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, symbol, side, order_type])

# Homepage test (es. per UptimeRobot)
@app.route('/', methods=['GET'])
def home():
    return 'Bot attivo!'

# Webhook da TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Ricevuto webhook:", data)

    symbol = data.get("symbol")
    side = data.get("side")
    order_type = data.get("type")

    if symbol and side and order_type:
        msg = f"Segnale ricevuto:\nSymbol: {symbol}\nAction: {side}\nType: {order_type}"
        send_telegram_message(msg)
        log_signal(symbol, side, order_type)
        return '', 200
    else:
        print("Segnale incompleto ricevuto.")
        return 'Bad Request', 400

# Comando Telegram per ricevere log.csv
@app.route('/telegram/log', methods=['GET'])
def send_log_file():
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        with open("log.csv", "rb") as file:
            requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID
            }, files={
                "document": file
            })
        return 'Log inviato su Telegram', 200
    except Exception as e:
        print("Errore invio log:", e)
        return 'Errore invio log', 500

# Avvia il bot
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)