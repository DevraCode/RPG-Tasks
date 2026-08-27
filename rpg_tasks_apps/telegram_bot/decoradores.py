from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

#Impide usar los comandos /registro  y /vincular si el usuario ya está registrado y tiene la sesión activa
def verificar_sesion_activa(func):
    @wraps(func)
    async def usuario_registrado(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        token_usuario = context.user_data.get("token_usuario")
        id_externo_usuario = context.user_data.get("id_externo_usuario")

        if token_usuario and id_externo_usuario:
            await update.message.reply_text("Ya estás registrado y tienes la sesión activa. No es necesario registrarte de nuevo.")
            return
        
        return await func(update, context, *args, **kwargs)
    
    return usuario_registrado

