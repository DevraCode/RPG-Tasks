from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext
import hashlib

from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases import VincularIdExternoUseCase


from .dbconfig import db_config

repo = MySQLUsuarioRepository(db_config)
vincular_id_externo_use_case = VincularIdExternoUseCase(repo)


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INSERTAR TAREAS
NOMBRE_TAREA, INSERTAR_TAREA = range(2)