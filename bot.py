import os
from fastapi import FastAPI, Request
import telegram
from telegram.constants import ParseMode
from openai import OpenAI

# ====== ENV ======
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY)

WELCOME_TEXT = """
🤖 *Warith AI Assistant*

مساعد ذكي للطلاب والتقنيين 👨‍🎓👩‍💻  
• شرح مبسّط  
• إجابة أي سؤال  
• برمجة • تقنية • دراسة  
• يعمل 24/7 ⏱️  

👤 المطوّر:  
*Warith Al-Awadi*
"""

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)

    if update.message and update.message.text:
        chat_id = update.message.chat.id
        text = update.message.text

        # /start
        if text == "/start":
            bot.send_message(
                chat_id=chat_id,
                text=WELCOME_TEXT,
                parse_mode=ParseMode.MARKDOWN
            )
            return {"ok": True}

        # AI response
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي عربي للطلاب والتقنيين."},
                    {"role": "user", "content": text}
                ]
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = "⚠️ حدث خطأ مؤقت، حاول مرة أخرى."

        bot.send_message(
            chat_id=chat_id,
            text=reply
        )

    return {"ok": True}
