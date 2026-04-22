#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from functools import wraps
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import SesionIniciadaUseCase, BuscarPorIdExternoUseCase, VincularIdPersonajeConUsuarioUseCase, LimitePersonajesUsuarioUseCase


from .dbconfig import db_config

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
sesion_iniciada = SesionIniciadaUseCase(repo)
buscar_por_id_externo_use_case = BuscarPorIdExternoUseCase(repo)
vincular_id_personaje_con_usuario_use_case = VincularIdPersonajeConUsuarioUseCase(repo)
limite_personajes_usuario_use_case = LimitePersonajesUsuarioUseCase(repo)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Si el usuario no está registrado
def usuario_no_registrado(func):
    @wraps(func)
    async def usuario_no_existe(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
         
        if not repo.obtener_estado_sesion(id_externo,nombre_plataforma='telegram'):
            await update.message.reply_text(
                "Debes registrarte primero"
            )
            return 

        return await func(update, context, *args, **kwargs)
    return usuario_no_existe

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#Si el usuario está registrado y activo, tabla usuarios.activo = 1
def usuario_registrado(func):
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

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Si el usuario se ha dado de baja, es decir, en la tabla usuarios.activo = 0
#Útil para usuarios baneados
def usuario_inactivo(func):
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


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Busca que personaje pertence al usuario
def personaje_elegido(func):
    @wraps(func)
    async def id_personaje(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
        id_interno_obj = repo.buscar_por_id_externo(id_externo,nombre_plataforma='telegram')
        id_interno = id_interno_obj.id_usuario

        personaje_elegido_id = vincular_id_personaje_con_usuario_use_case.vincular_id_personaje_con_usuario(id_externo)
        total_personajes = limite_personajes_usuario_use_case.limite_personajes_usuario(id_interno)
        
        
        if personaje_elegido_id and personaje_elegido_id.get("id_personaje") is not None and total_personajes == False:
            await update.message.reply_text(
                "Has llegado al límite de 5 personajes por usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return id_personaje

