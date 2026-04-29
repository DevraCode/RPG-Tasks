from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext
import hashlib

from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.mysql_tareas_repository import MySQLTareasRepository
from core.infrastructure.mysql_plataformas_repository import MySQLPlataformasRepository
from core.application.use_cases import UsuarioUsecase, TareasUseCase, PlataformasUseCase


from .dbconfig import db_config

repo_usuarios = MySQLUsuarioRepository(db_config)
repo_tareas = MySQLTareasRepository(db_config)
repo_plataformas = MySQLPlataformasRepository(db_config)
usuarios = UsuarioUsecase(repo_usuarios)
tareas = TareasUseCase(repo_tareas)
plataformas = PlataformasUseCase(repo_plataformas)


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INSERTAR TAREAS
INSERTAR_TAREA = range(1)

async def preguntar_nombre_tarea(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Introduce el nombre de la tarea")
    return INSERTAR_TAREA


async def crear_tarea(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre_tarea"] = update.message.text

    id_externo = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
    id_usuario = plataformas.vincular_id_externo_usuario(id_externo)
    nombre_tarea = context.user_data.get("nombre_tarea")

    nueva_tarea = tareas.insertar_tarea(id_usuario, nombre_tarea)

    await update.message.reply_text(nueva_tarea)


    return ConversationHandler.END



