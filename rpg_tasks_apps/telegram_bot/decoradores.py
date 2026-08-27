from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

#Impide usar los comandos /registro  y /vincular si el usuario ya está registrado y tiene la sesión activa
def verificar_sesion_activa(func):
    @wraps(func)
    async def usuario_registrado(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        token_usuario = context.user_data.get("token_usuario")
        
        if token_usuario:
            await update.message.reply_text("Ya estás registrado. No es necesario registrarte de nuevo.")
            return
        
        return await func(update, context, *args, **kwargs)
    
    return usuario_registrado

#Impide usar los comandos que requieren que el usuario esté registrado y tenga la sesión activa
def verificar_usuario(func):
    @wraps(func)
    async def usuario_existe(update,context, *args, **kwargs):
        token_usuario = context.user_data.get("token_usuario")

        if not token_usuario:
            await update.message.reply_text("No estás registrado o no has iniciado sesión. Por favor, regístrate o inicia sesión primero.")
            return
        
        return await func(update, context, *args, **kwargs)
    return usuario_existe

#Comprueba los permisos del usuario
