import os
from fastapi import FastAPI, Request
import telegram

# ===============================
# إعدادات أساسية
# ===============================

TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telegram.Bot(token=TOKEN)
app = FastAPI()

# ===============================
# نص الترحيب الرسمي
# ===============================

WELCOME_TEXT = """
🤖 Warith AI Assistant

مساعد ذكي للطلاب والتقنيين
إجابات فورية • شرح مبسّط • دعم 24/7

📚 أقدر أساعدك في:
• البرمجة
• التكنولوجيا
• الذكاء الاصطناعي
• الشرح والدراسة

👤 المطوّر:
Warith Al-Awadi
"""

# ===============================
# فحص أن الخدمة تعمل
# ===============================

@app.get("/")
async def root():
    return {
        "ok": True,
        "service": "Warith AI Assistant",
        "status": "running",
        "mode": "webhook"
    }

# ===============================
# Webhook Telegram
# ===============================

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text or ""

        # /start
        if text.startswith("/start"):
            bot.send_message(
                chat_id=chat_id,
                text=WELCOME_TEXT
            )
            return {"ok": True}

        # أي رسالة أخرى
        bot.send_message(
            chat_id=chat_id,
            text=f"""
🧠 Warith AI Assistant

وصلني سؤالك:
{text}

✍️ اكتب أي سؤال تقني أو دراسي وسأساعدك فورًا.
"""
        )

    return {"ok": True}
