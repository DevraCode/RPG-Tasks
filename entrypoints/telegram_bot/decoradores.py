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
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
    
        
        if repo.obtener_estado_sesion(id_externo):
            await update.message.reply_text(
                "Ya tienes una sesión iniciada"
                "En Telegram solo puedes tener una cuenta por Usuario debido a las limitaciones"
            )
            return 

        
        await update.message.reply_text("Genial, vamos a empezar el registro")

        
        return await func(update, context, *args, **kwargs)
    return sesion_activa_true

