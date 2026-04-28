#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from functools import wraps
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.mysql_personajes_repository import MySQLPersonajesRepository
from core.infrastructure.mysql_plataformas_repository import MySQLPlataformasRepository
from core.application.use_cases import UsuarioUsecase, PersonajeUseCase, PlataformasUseCase


from .dbconfig import db_config

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INYECCIÓN DE DEPENDENCIAS
repo_usuario = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)
repo_plataformas = MySQLPlataformasRepository(db_config)

usuario = UsuarioUsecase(repo_usuario)
personaje = PersonajeUseCase(repo_personajes)
plataformas = PlataformasUseCase(repo_plataformas)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


def usuario_existe(func):
    @wraps(func)
    async def usuario_registrado(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]

        id_usuario = plataformas.vincular_id_externo_usuario(id_externo)


        if usuario.id_usuario_existe(id_usuario):
            await update.message.reply_text(
                f"Ya estás registrado. Cierra la sesión o inicia sesión con otro usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return usuario_registrado





#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------



#Busca que personaje pertence al usuario
def personaje_elegido(func):
    @wraps(func)
    async def id_personaje(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
        id_interno_obj = usuario.buscar_id_externo_usuario(id_externo,nombre_plataforma='telegram')
        id_interno = id_interno_obj.id_usuario

        personaje_elegido_id = personaje.vincular_id_personaje_con_usuario(id_externo)
        total_personajes = personaje.limite_personajes_usuario(id_interno)
        
        
        if personaje_elegido_id and personaje_elegido_id.get("id_personaje") is not None and total_personajes == False:
            await update.message.reply_text(
                "Has llegado al límite de 5 personajes por usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return id_personaje

