# entrypoints/telegram_bot/main.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Importamos nuestras capas del Core e Infraestructura
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import RegistroNuevoJugadorUseCase, ObtenerSaludoUseCase

# 1. Cargamos configuración
load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

# 2. Inyección de Dependencias (Montamos las piezas)
repo = MySQLUsuarioRepository(db_config)
registro_use_case = RegistroNuevoJugadorUseCase(repo)
saludo_use_case = ObtenerSaludoUseCase(repo)

# 3. Handler del comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_telegram = str(update.effective_user.id)
    nombre_telegram = update.effective_user.first_name
    
    # 🚀 LLAMADA AL NÚCLEO (Arquitectura Hexagonal en acción)
    # No importa que sea Telegram, el Caso de Uso solo quiere un ID y un nombre.
    mensaje_resultado = registro_use_case.ejecutar(
        id_externo=user_id_telegram, 
        plataforma='telegram', 
        nombre_sugerido=nombre_telegram
    )
    
    await update.message.reply_text(mensaje_resultado)


async def saludo(update:Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_telegram = str(update.effective_user.id)
    

    mensaje_saludo = saludo_use_case.ejecutar(id_externo=user_id_telegram, plataforma='telegram')

    await update.message.reply_text(mensaje_saludo)



if __name__ == "__main__":
    # 4. Configuración del Bot
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hola", saludo))



    
    print("🤖 Bot de RPG iniciado y conectado a MySQL...")
    app.run_polling()