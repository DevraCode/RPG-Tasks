
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from core.infrastructure.servicios_ia.cliente_gemini import GeminiService
from core.infrastructure.servicios_ia.gemini_tools import gemini_tools

from core.infrastructure.dbconfig import db_config

token_gemini = os.getenv("GEMINI_API_KEY")


herramientas = gemini_tools(db_config)
ia = GeminiService(
    api_key=token_gemini, 
    model_name="gemini-2.5-flash", 
    tools=herramientas
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta_ia = ia.ask(update.message.text)
    
    await update.message.reply_text(respuesta_ia)