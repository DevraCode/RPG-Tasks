from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler




from core.application.use_cases import ObtenerCatalogoUseCase

use_case = ObtenerCatalogoUseCase() 
catalogo = use_case.ejecutar()


async def mostrar_personaje(update:Update, context):
    for clave, datos in catalogo.items():
        ruta = datos['imagen']

    await update.effective_chat.send_sticker(sticker=ruta)
    