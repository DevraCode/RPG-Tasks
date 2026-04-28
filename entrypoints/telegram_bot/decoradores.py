#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from functools import wraps
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases import IdUsuarioExisteUseCase, ObtenerEstadoSesionUseCase, BuscarPorIdExternoUseCase, VincularIdPersonajeConUsuarioUseCase, LimitePersonajesUsuarioUseCase


from .dbconfig import db_config

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
id_usuario_existe_use_case = IdUsuarioExisteUseCase(repo)



sesion_iniciada = ObtenerEstadoSesionUseCase(repo)
buscar_por_id_externo_use_case = BuscarPorIdExternoUseCase(repo)
vincular_id_personaje_con_usuario_use_case = VincularIdPersonajeConUsuarioUseCase(repo)
limite_personajes_usuario_use_case = LimitePersonajesUsuarioUseCase(repo)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


def usuario_existe(func):
    @wraps(func)
    async def usuario_registrado(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]

        id_usuario = repo.vincular_id_externo_con_interno(id_externo)

        if id_usuario_existe_use_case.id_usuario_existe(id_usuario):
            await update.message.reply_text(
                f"Ya estás registrado. Cierra la sesión o inicia sesión con otro usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return usuario_registrado





#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


def sesion_usuario_iniciada(func):
    @wraps(func)
    async def id_externo_true(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]

        id_usuario = repo.vincular_id_externo_con_interno(id_externo)
        
        if sesion_iniciada.usuario_activo(id_usuario):
            await update.message.reply_text(
                "Ya has iniciado sesión. Cierra sesión o registrate con otro usuario"
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

