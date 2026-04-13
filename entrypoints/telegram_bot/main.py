#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

#-----------------------------------------------------------------------------------------------------------------------------
#Importaciones propias del bot
from .handlers_basicos import NOMBRE, PASSWORD
from .handlers_basicos import start, pide_nombre_usuario, nombre_usuario, contraseña, cancelar

from .handlers_personajes import mostrar_personaje, manejador_botones
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CARGA DEL ENTORNO
load_dotenv()
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#INICIO DEL BOT
if __name__ == "__main__":
    
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    #-----------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------

    #HANDLERS
    app.add_handler(CommandHandler("start", start))
   
    
    app.add_handler(CommandHandler("personaje", mostrar_personaje))
    app.add_handler(CallbackQueryHandler(manejador_botones, pattern="^(NEXT_|PREV_|SELECT_)"))

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
    )




    app.add_handler(reg_conv_handler)

    
    print("🤖 Bot de RPG iniciado y conectado a MySQL...")
    app.run_polling()