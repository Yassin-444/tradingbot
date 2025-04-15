import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("Ricevuto webhook:", data)
    return '', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render userà questa variabile PORT
    app.run(host='0.0.0.0', port=port)