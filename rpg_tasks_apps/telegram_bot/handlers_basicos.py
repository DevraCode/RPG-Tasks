#IMPORTACIONES

#Externas
import requests
import hashlib
import secrets
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommandScopeChat
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

#Internas

from .api_url import API_URL

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#Carga de variables de entorno desde el archivo .env
load_dotenv()

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#HANDLERS

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
         [InlineKeyboardButton(text="English", callback_data="lang_en"), InlineKeyboardButton(text="Español", callback_data="lang_es")]
    ]
   
    await context.bot.send_message(chat_id=update.effective_chat.id, text="⚔️ Select your language / Selecciona tu idioma ⚔️", reply_markup=InlineKeyboardMarkup(keyboard))

#Crear manjeador de botones
async def manejador_start(update:Update, context:CallbackContext):
     query = update.callback_query
     data = query.data

     if data == "lang_es":
        await query.edit_message_text(text=("Idioma configurado en Español."))

        try:
            respuesta = requests.get(f"{API_URL}/")
            datos = respuesta.json()
        
            if datos.get("status") == "ok":
                mensaje_inicio = datos.get("data") 
                
                await update.callback_query.answer() 
                
                await update.callback_query.edit_message_text(f"{mensaje_inicio}", 
                                                                parse_mode="Markdown")
            else:
                await update.message.reply_text("Error al iniciar la aplicación. Por favor, inténtalo de nuevo más tarde.")
            
        except requests.exceptions.ConnectionError:
            await update.message.reply_text("No se pudo conectar con el motor del juego. ¿Te has olvidado de encender FastAPI?")

        #Comandos del menú de Telegram para el bot, que se mostrarán en la barra de comandos del chat
        await context.bot.set_my_commands(
        commands=[
            ("registro", "Crear una cuenta de héroe"),
            ("vincular", "Vincula una cuenta existente"),
            ("personaje", "Elige un personaje"),
            ("entrenar", "Elige uno de tus personajes y asígnale una tarea para entrenarlo"),
            ("nuevatarea", "Crea una tarea nueva"),
            ("tareas", "Muestra tu lista de tareas"),
        ],
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )

     elif data == "lang_en":
        await query.edit_message_text(text=("English Translation is not yet available. Please select Español for now."))
        
          
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CONVERSATION HANDLERS

#REGISTRO
#-----------------------------------------------------------------------------------------------------------------------------
NOMBRE, PASSWORD, EMAIL = range(3)


async def pide_nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text= (f"Introduce tu nombre de usuario. Puedes cancelar en cualquier momento con /cancelar"))

    return NOMBRE

#----------------------------------------------------------------------------------------

async def nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_usuario'] = update.message.text.strip().lower() #Guardamos en una variable temporal el nombre de usuario en minúsculas para evitar problemas de mayúsculas/minúsculas

    #Comprobar que el nombre de usuario no esté ya en uso
    usuario_en_bd = requests.get(f"{API_URL}/api/usuarios/verificar-nombre/{context.user_data['nombre_usuario']}")
    if usuario_en_bd.status_code == 400:
            await update.message.reply_text(("Ese nombre de usuario ya está en uso. Por favor, elige otro."))
            return NOMBRE
    else:
        await update.message.reply_text((f"Perfecto, {update.message.text}. " + f"Introduce tu contraseña"))
        return PASSWORD

#----------------------------------------------------------------------------------------
async def contraseña (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password_usuario'] = update.message.text

    await update.message.reply_text((f"De acuerdo. " + f"Introduce tu email. " + f"Recuerda que este email será tu contacto en caso de que olvides tu contraseña."))
    return EMAIL
    
#----------------------------------------------------------------------------------------

async def email (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email_usuario'] = update.message.text

    nombre = context.user_data.get('nombre_usuario')
    password = context.user_data.get('password_usuario')
    
    email = context.user_data.get('email_usuario')
    idioma = context.user_data.get("idioma")

    id_externo = str(update.effective_user.id)
    


    registro = {
        "nombre_usuario": nombre,
        "password_usuario": password,
        "email_usuario": email,
        "rango": "NOVATO",                   
        "tipo_usuario": 0,                   
        "idioma_usuario": idioma,
        "id_plataforma": 3,
        "nombre_plataforma":"TELEGRAM",
        "id_externo_usuario": id_externo
    }

    try:
        await update.message.reply_text(("Procesando tu registro en el Gremio..."))
    
        respuesta = requests.post(f"{API_URL}/api/usuarios/registro", json=registro)
        
        if respuesta.status_code == 201:
            await update.message.reply_text(("Cuenta creada con éxito ¡Bienvenido!"))
        else:
            error_api = respuesta.json().get("detail", "Error interno de la API")
            await update.message.reply_text(f"No se pudo completar el registro: {error_api}")
            
    except requests.exceptions.ConnectionError:
        await update.message.reply_text("Error de conexion")
    
    return ConversationHandler.END

#----------------------------------------------------------------------------------------

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registro cancelado. Puedes volver a empezar con /registro.")
    return ConversationHandler.END

#----------------------------------------------------------------------------------------

PEDIR_NOMBRE, PEDIR_PASSWORD = range(2)


async def vincular(update:Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text((f"Introduce tu nombre de usuario"))
     return PEDIR_NOMBRE

     
async def obtener_username (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre_usuario"] = update.message.text.strip().lower()
    await update.message.reply_text(f"Introduce tu contraseña")
    return PEDIR_PASSWORD

            
async def obtener_password (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["password_usuario"] = update.message.text

    nombre_usuario = context.user_data.get("nombre_usuario")
    password = context.user_data.get('password_usuario')
    password_bytes = f"{password}".encode()
    password_encriptado = hashlib.sha256(password_bytes).hexdigest()[:8]

    vincular = {
         "nombre_usuario": nombre_usuario,
         "password_usuario": password_encriptado,
         "id_plataforma": 3,
         "nombre_plataforma": "TELEGRAM",
         "token_usuario": hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
     }

    try:
        await update.message.reply_text(("Vinculando la cuenta..."))
    
        respuesta = requests.post(f"{API_URL}/api/plataformas/vincular", json=vincular)
        
        if respuesta.status_code == 200:
            await update.message.reply_text(("Cuenta vinculada con éxito ¡Bienvenido!"))
        else:
            error_api = respuesta.json().get("detail", "Error interno de la API")
            await update.message.reply_text(f"No se pudo completar la vinculación de la cuenta: {error_api}")
            
    except requests.exceptions.ConnectionError:
         await update.message.reply_text("Error de conexion")
    
    return ConversationHandler.END
     
     
     
        
     