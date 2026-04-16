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
from core.application.use_cases import SesionIniciadaUseCase, BuscarPorIdExternoUseCase


from .dbconfig import db_config

#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
sesion_iniciada = SesionIniciadaUseCase(repo)
buscar_por_id_externo_use_case = BuscarPorIdExternoUseCase(repo)


#Si el usuario está activo, tabla usuarios.activo = 1
def sesion_activa(func):
    @wraps(func)
    async def sesion_activa_true(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
    
        
        if repo.obtener_estado_sesion(id_externo,nombre_plataforma='telegram'):
            await update.message.reply_text(
                "Ya te has registrado \n"
                "En Telegram solo puedes tener una cuenta por usuario debido a las limitaciones"
            )
            return 

        return await func(update, context, *args, **kwargs)
    return sesion_activa_true




#Si el usuario se ha dado de baja, es decir, en la tabla usuarios.activo = 0
#Útil para usuarios baneados
def id_externo_existente(func):
    @wraps(func)
    async def id_externo_true(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
    
        
        if repo.buscar_por_id_externo(id_externo,nombre_plataforma='telegram'):
            await update.message.reply_text(
                "Este ID de Telegram ya está registrado pero no tiene la sesión activa"
            )
            return 

        
        

        
        return await func(update, context, *args, **kwargs)
    return id_externo_true