from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route("/")
def home():
    return "Bot is live"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data or "text" not in data["message"]:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a sweet, supportive AI girlfriend named Alina."},
                {"role": "user", "content": text}
            ]
        }
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = "Oops! Something went wrong."

    requests.post(f"{BOT_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
