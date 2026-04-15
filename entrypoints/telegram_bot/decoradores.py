#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from functools import wraps

import hashlib

#Internas
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import SesionIniciadaUseCase


from .dbconfig import db_config

#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
sesion_iniciada = SesionIniciadaUseCase(repo)

def sesion_activa(func):
    @wraps(func)
    async def sesion_activa_true(update, context, *args, **kwargs):

        #Se busca el id de la tabla plataformas que no necesita el nombre de usuario
        #Tiene que ser EXACTAMENTE el mismo id que se crea al registrarse
        palabra_para_encriptar = "TELEGRAM"
        id_telegram = str(update.effective_user.id)
        id_telegram_bytes = f"{id_telegram}{palabra_para_encriptar}".encode()
        id_generado = hashlib.sha256(id_telegram_bytes).hexdigest()[:8]
        
        mensaje_error = sesion_iniciada.usuario_activo(id_generado)
        
        if mensaje_error:
            await update.message.reply_text(mensaje_error)
            return 

        return await func(update, context, *args, **kwargs)
    return sesion_activa_true

