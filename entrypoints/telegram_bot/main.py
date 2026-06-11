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
from telegram.ext import CallbackContext, InlineQueryHandler, TypeHandler, PicklePersistence
#-----------------------------------------------------------------------------------------------------------------------------
#Importaciones propias del bot
from .handlers_basicos import NOMBRE, PASSWORD, EMAIL, PEDIR_NOMBRE, PEDIR_PASSWORD
from .handlers_basicos import start, manejador_start, interaccion_ia, pide_nombre_usuario, nombre_usuario, contraseña, email, cancelar, vincular, obtener_username, obtener_password

from .handlers_personajes import SELECCIONANDO_CLASE, PREGUNTAR_NOMBRE, SELECCIONANDO, ASIGNAR_TAREA, ENTRENAR, COMPLETAR, TEMPORIZADOR
from .handlers_personajes import mostrar_personaje, manejador_botones, obtener_nombre_personaje, lista_personajes_usuarios, manejador_lista_personajes, asignar_tarea, entrenar, completar_tarea, teclado_minutos, manejador_minutos

from .handlers_tareas import INSERTAR_TAREA
from .handlers_tareas import preguntar_nombre_tarea, crear_tarea, lista_tareas

from .handlers_inline import inline_handler, manejador_stats

from .menu import menu

from core.infrastructure.traduccion.traduccion import traducir
import builtins
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CARGA DEL ENTORNO
load_dotenv()
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

persistencia = PicklePersistence(filepath="rpg_data_telegram.pickle")

if __name__ == "__main__":
    
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).post_init(menu).persistence(persistencia).build()

    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #HANDLERS

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tareas", lista_tareas))
    app.add_handler(InlineQueryHandler(inline_handler))

    #He puesto expresiones regulares para que no se intercepten los data query de los botones entre los comandos
    app.add_handler(CallbackQueryHandler(manejador_start, pattern=r"^lang_"))
    app.add_handler(CallbackQueryHandler(manejador_stats, pattern=r"^stats_"))
    
    
    
    
   
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

    reg_conv_handler_en = ConversationHandler(
        entry_points=[CommandHandler("signup", pide_nombre_usuario)],
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
        ASIGNAR_TAREA: [CallbackQueryHandler(asignar_tarea)],
        ENTRENAR: [CallbackQueryHandler(entrenar)],
        COMPLETAR: [CallbackQueryHandler(completar_tarea)],
        TEMPORIZADOR: [CallbackQueryHandler(manejador_minutos)],
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

    vin_conv_handler_en = ConversationHandler(
        entry_points=[CommandHandler("link", vincular)],
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
    app.add_handler(reg_conv_handler_en)
    app.add_handler(personaje_conv_handler)
    app.add_handler(entrenar_personaje_conv_handler)
    app.add_handler(vin_conv_handler)
    app.add_handler(vin_conv_handler_en)
    app.add_handler(tarea_conv_handler)


    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interaccion_ia))

    
    print("Bot Iniciado")
    app.run_polling()