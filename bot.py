import os
import requests
from fastapi import FastAPI, Request

# =====================
# إعدادات
# =====================
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

WELCOME_TEXT = """
🤖 Warith AI Assistant

مساعد ذكي للطلاب والتقنيين
إجابات فورية • شرح مبسّط • دعم 24/7

👤 المطوّر:
Warith Al-Awadi
"""

app = FastAPI()

# =====================
# إرسال رسالة
# =====================
def send_message(chat_id: int, text: str):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# =====================
# Root (لـ Render)
# =====================
@app.get("/")
def root():
    return {"status": "Warith AI Assistant is running"}

# =====================
# Webhook
# =====================
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(chat_id, WELCOME_TEXT)
        else:
            send_message(
                chat_id,
                f"📩 رسالتك:\n{text}\n\n🤖 سأجيبك قريبًا بإذن الله"
            )

    return {"ok": True}
