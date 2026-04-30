#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from functools import wraps
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from core.infrastructure.repositorios.mysql_plataformas_repository import MySQLPlataformasRepository
from core.application.use_cases import UsuarioUsecase, PersonajeUseCase, PlataformasUseCase


from .dbconfig import db_config

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INYECCIÓN DE DEPENDENCIAS
repo_usuarios = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)
repo_plataformas = MySQLPlataformasRepository(db_config)

usuario = UsuarioUsecase(repo_usuarios)
personaje = PersonajeUseCase(repo_personajes, repo_usuarios)
plataformas = PlataformasUseCase(repo_plataformas)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Comprueba que exista el usuario y que tenga la sesion activa
#Si existe y tiene la sesión activa no podrá volver a registrarse o volver la vincular una cuenta hasta que cierre sesión
def usuario_existe(func):
    @wraps(func)
    async def usuario_registrado(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]

        nombre_usuario = usuario.buscar_id_externo_usuario(id_externo)
        sesion = plataformas.usuario_activo(id_externo)

        if id_externo and sesion == True:
            await update.message.reply_text(
                f"Ya estás registrado como {nombre_usuario.nombre_usuario.capitalize()}. Cierra la sesión o inicia sesión con otro usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return usuario_registrado


#Comprueba si el usuario existe o tiene cerrada la sesión
#Si no existe, no tiene vinculada una cuenta o no tiene abierta la sesión, no podrá usar los comandos de personajes ni tareas
def usuario_no_existe_o_sesion_cerrada(func):
    @wraps(func)
    async def comprobacion(update,context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]

        id_usuario = usuario.buscar_id_externo_usuario(id_externo)
        sesion = plataformas.usuario_activo(id_externo)

        if not id_usuario or not id_externo or sesion == False:
            await update.message.reply_text(
                f"Debes registrarte o vincular una cuenta primero"
            )
            return
        
        return await func(update, context, *args, **kwargs)
    return comprobacion




#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Límite de personajes del usuario
def limite_personajes(func):
    @wraps(func)
    async def id_personaje(update, context, *args, **kwargs):
        id_telegram = str(update.effective_user.id)
        id_externo = hashlib.sha256(id_telegram.encode()).hexdigest()[:8]
        id_interno = usuario.buscar_id_externo_usuario(id_externo)
        

        personaje_elegido_id = personaje.vincular_id_personaje_con_usuario(id_externo)
        total_personajes = personaje.limite_personajes_usuario(id_interno.id_usuario)
        
        
        if personaje_elegido_id and personaje_elegido_id.get("id_personaje") is not None and total_personajes == False:
            await update.message.reply_text(
                "Has llegado al límite de 5 personajes por usuario"
            )
            return 
        
        return await func(update, context, *args, **kwargs)
    return id_personaje

