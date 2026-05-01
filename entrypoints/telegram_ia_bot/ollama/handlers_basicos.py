
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from core.infrastructure.servicios_ia.cliente_ollama import OllamaClient


from core.infrastructure.dbconfig import db_config

from core.infrastructure.servicios_ia.config_ia import SYSTEM_INSTRUCTION

ia = OllamaClient(
    model_name="llama3", 
    system_instruction=SYSTEM_INSTRUCTION 
)



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta_ia = ia.ask(update.message.text)
    
    await update.message.reply_text(respuesta_ia)