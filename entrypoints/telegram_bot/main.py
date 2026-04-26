#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMedia
from telegram.ext import CallbackContext
#-----------------------------------------------------------------------------------------------------------------------------
#Importaciones propias del bot
from .handlers_basicos import NOMBRE, PASSWORD
from .handlers_basicos import start, pide_nombre_usuario, nombre_usuario, contraseña, cancelar

from .handlers_personajes import SELECCIONANDO_CLASE, PREGUNTAR_NOMBRE, SELECCIONANDO, ASIGNAR_TAREA
from .handlers_personajes import mostrar_personaje, manejador_botones, obtener_nombre_personaje, lista_personajes_usuarios, manejador_lista_personajes, asignar_tarea
from .menu import menu
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CARGA DEL ENTORNO
load_dotenv()
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INICIO DEL BOT
if __name__ == "__main__":
    
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).post_init(menu).build()
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #HANDLERS
    app.add_handler(CommandHandler("start", start))
    #app.add_handler(CommandHandler("listapersonajes", lista_personajes_usuarios))
   
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #CONVERSATION HANDLERS
    reg_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("registro", pide_nombre_usuario)],
        states={
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre_usuario)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, contraseña)] 
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        per_message=False,
        per_chat=True,
        map_to_parent={}, 
        allow_reentry=True 
    )

    personaje_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('personaje', mostrar_personaje)],
    states={
        SELECCIONANDO_CLASE: [CallbackQueryHandler(manejador_botones)],
        PREGUNTAR_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_nombre_personaje)]
    },
    fallbacks=[CommandHandler('cancel', cancelar)],
    per_message=False,
    per_chat=True,
    map_to_parent={}, 
    allow_reentry=True 
    )

    entrenar_personaje_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('entrenar', lista_personajes_usuarios)],
    states={
        SELECCIONANDO: [CallbackQueryHandler(manejador_lista_personajes)],
        ASIGNAR_TAREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, asignar_tarea)]
    },
    fallbacks=[CommandHandler('cancel', cancelar)],
    per_message=False,
    per_chat=True,
    map_to_parent={}, 
    allow_reentry=True 
    )




    app.add_handler(reg_conv_handler)
    app.add_handler(personaje_conv_handler)
    app.add_handler(entrenar_personaje_conv_handler)

    
    print("🤖 Bot de RPG iniciado y conectado a MySQL...")
    app.run_polling()