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
from .handlers_basicos import NOMBRE, PASSWORD, EMAIL, PEDIR_NOMBRE, PEDIR_PASSWORD
from .handlers_basicos import start, interaccion_ia, pide_nombre_usuario, nombre_usuario, contraseña, email, cancelar, vincular, obtener_username, obtener_password

from .handlers_personajes import SELECCIONANDO_CLASE, PREGUNTAR_NOMBRE, SELECCIONANDO, ASIGNAR_TAREA
from .handlers_personajes import mostrar_personaje, manejador_botones, obtener_nombre_personaje, lista_personajes_usuarios, manejador_lista_personajes, asignar_tarea

from .handlers_tareas import INSERTAR_TAREA
from .handlers_tareas import preguntar_nombre_tarea, crear_tarea

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interaccion_ia))
    
    
   
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #CONVERSATION HANDLERS
    reg_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("registro", pide_nombre_usuario)],
        states={
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre_usuario)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, contraseña)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)]
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
    allow_reentry=True 
    )

    vin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("vincular", vincular)],
        states={
            PEDIR_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_username)],
            PEDIR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_password)]
            
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        per_message=False,
        per_chat=True,
        allow_reentry=True 
    )

    tarea_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("nuevatarea", preguntar_nombre_tarea)],
        states={
            INSERTAR_TAREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, crear_tarea)],
            
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        per_message=False,
        per_chat=True,
        allow_reentry=True 
    )




    app.add_handler(reg_conv_handler)
    app.add_handler(personaje_conv_handler)
    app.add_handler(entrenar_personaje_conv_handler)
    app.add_handler(vin_conv_handler)
    app.add_handler(tarea_conv_handler)

    
    print("🤖 Bot de RPG iniciado y conectado a MySQL...")
    app.run_polling()