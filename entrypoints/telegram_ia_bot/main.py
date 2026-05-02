from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import os
from dotenv import load_dotenv

from .ollama.handlers_basicos import handle_message

load_dotenv()

token = os.getenv("TELEGRAM_IA_BOT_TOKEN")

if __name__=="__main__":

    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()