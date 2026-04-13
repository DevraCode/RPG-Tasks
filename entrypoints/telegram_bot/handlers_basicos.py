#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

#Internas
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import MensajeInicioUseCase, CrearCuentaUseCase, RegistroNuevoJugadorUseCase
from dotenv import load_dotenv

from .dbconfig import db_config


import hashlib
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

load_dotenv()



#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
mensaje_bienvenida = MensajeInicioUseCase()
crear_cuenta = CrearCuentaUseCase()
registro_use_case = RegistroNuevoJugadorUseCase(repo)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#HANDLERS
async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_inicio = mensaje_bienvenida.mensaje()

    await update.message.reply_text(mensaje_inicio)
    await update.message.reply_text(f"Utiliza el comando /registro para crear una cuenta o /iniciarsesion para iniciar sesión")
    




#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CONVERSATION HANDLERS
NOMBRE, PASSWORD = range(2)

async def pide_nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    pide_usuario = crear_cuenta.nombre_usuario()

    await context.bot.send_message(chat_id=chat_id, text=pide_usuario)
    return NOMBRE


async def nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_usuario'] = update.message.text.strip().lower()

    usuario_en_bd = repo.buscar_usuario_en_bd(context.user_data['nombre_usuario'])
    if usuario_en_bd:
            await update.message.reply_text(f"Ya estás registrado")
            return ConversationHandler.END
    else:
        pide_contraseña = crear_cuenta.contraseña()

        await update.message.reply_text(f"Perfecto, **{update.message.text}**." + f"{pide_contraseña}")
        return PASSWORD

async def contraseña (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password_usuario'] = update.message.text

    nombre = context.user_data.get('nombre_usuario')
    password = context.user_data.get('password_usuario')
    password_bytes = f"{password}".encode()
    password_encriptado = hashlib.sha256(password_bytes).hexdigest()[:8]

    id_externo = str(update.effective_user.id)

    #Se mezcla el id de telegram con el nombre elegido. De esta forma se pueden crear varias cuentas en la misma plataforma
    id_externo_bytes = f"{id_externo}{nombre}".encode()
    nuevo_id_externo = hashlib.sha256(id_externo_bytes).hexdigest()[:8]

    resultado = registro_use_case.ejecutar(
            id_externo=nuevo_id_externo,
            plataforma='telegram',
            nombre_usuario=nombre,
            password_usuario=password_encriptado
        )
    await update.message.reply_text(f"✅ {resultado}")

    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Registro cancelado. Puedes volver a empezar con /registro.")
    return ConversationHandler.END