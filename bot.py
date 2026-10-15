import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)

# Render se token lega
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello Aafiya! 🤖💖\n\nMain Live ho gayi!\n\nBhejo kuch bhi - main kaam karungi!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text(f"Aapne bheja: {update.message.text}")
    elif update.message.document:
        await update.message.reply_text("Document mil gaya! ✅")
    elif update.message.sticker:
        await update.message.reply_text("Cute sticker! 😍")
    else:
        await update.message.reply_text("Mil gaya! ✅")

def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN nahi mila! Render me Environment check karo!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    print("Bot starting... Aafiya is Live!")
    app.run_polling()

if __name__ == "__main__":
    main()
