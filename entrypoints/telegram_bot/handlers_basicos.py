#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

#Internas
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import MensajeInicioUseCase, RegistroNuevoJugadorUseCase, ObtenerSaludoUseCase
from dotenv import load_dotenv

from .dbconfig import db_config
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

load_dotenv()



#INYECCIÓN DE DEPENDENCIAS
repo = MySQLUsuarioRepository(db_config)
mensaje_bienvenida = MensajeInicioUseCase()
registro_use_case = RegistroNuevoJugadorUseCase(repo)
saludo_use_case = ObtenerSaludoUseCase(repo)
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


#HANDLERS
async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_inicio = mensaje_bienvenida.mensaje()
    segundo_mensaje = mensaje_bienvenida.segundo_mensaje()

    await update.message.reply_text(mensaje_inicio)
    await update.message.reply_text(segundo_mensaje)



async def registro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_telegram = str(update.effective_user.id)
    nombre_telegram = update.effective_user.first_name
    
    # 🚀 LLAMADA AL NÚCLEO (Arquitectura Hexagonal en acción)
    # No importa que sea Telegram, el Caso de Uso solo quiere un ID y un nombre.
    mensaje_resultado = registro_use_case.ejecutar(
        id_externo=user_id_telegram, 
        plataforma='telegram', 
        nombre_usuario=nombre_telegram,
        password_usuario="asas"
    )
    
    await update.message.reply_text(mensaje_resultado)


async def saludo(update:Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_telegram = str(update.effective_user.id)
    
    mensaje_saludo = saludo_use_case.ejecutar(id_externo=user_id_telegram, plataforma='telegram')

    await update.message.reply_text(mensaje_saludo)



