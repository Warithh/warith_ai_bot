import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ======================
# CONFIG
# ======================
TOKEN = os.environ.get("TELEGRAM_TOKEN")

WELCOME_TEXT = """
🤖 Warith AI Assistant

مساعد ذكي للطلاب والتقنيين
• إجابات فورية
• شرح مبسّط
• دعم تقني وتعليمي
• يعمل 24/7

👤 المطوّر:
Warith Al-Awadi
"""

# ======================
# APP INIT
# ======================
app = FastAPI()
application = Application.builder().token(TOKEN).build()

# ======================
# HANDLERS
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(
        f"📩 استلمت رسالتك:\n\n{user_text}\n\n✅ البوت يعمل 24/7"
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ======================
# FASTAPI ROUTES
# ======================
@app.get("/")
async def root():
    return {
        "ok": True,
        "service": "Warith AI Assistant",
        "status": "running",
        "mode": "webhook",
    }

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
