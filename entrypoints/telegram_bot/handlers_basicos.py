#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommandScopeChat
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.domain.entidades import CorrespondenciaPlataformas, TiposUsuario, Rango
from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_plataformas_repository import MySQLPlataformasRepository
from core.application.use_cases.basico.basic_use_cases import MensajeInicioUseCase, CrearCuentaUseCase
from core.application.use_cases.basico.usuarios_use_cases import UsuarioUsecase
from core.application.use_cases.basico.plataformas_use_cases import PlataformasUseCase
from core.infrastructure.dbconfig import db_config
from .decoradores import usuario_existe, idioma_elegido

from core.infrastructure.traduccion.traduccion import IDIOMAS_USUARIOS
from core.infrastructure.traduccion.traduccion import traducir
import builtins

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

#INYECCIÓN DE DEPENDENCIAS
repo_usuario = MySQLUsuarioRepository(db_config)
repo_plataformas = MySQLPlataformasRepository(db_config)
mensaje_bienvenida = MensajeInicioUseCase()
crear_cuenta = CrearCuentaUseCase()
usuario = UsuarioUsecase(repo_usuario)
plataformas = PlataformasUseCase(repo_plataformas)



from core.infrastructure.servicios_ia.config_ia import SYSTEM_INSTRUCTION
from core.infrastructure.servicios_ia.cliente_ollama import OllamaClient
from core.infrastructure.servicios_ia.ollama_tools import OllamaTools

tools = OllamaTools()

ia = OllamaClient(
    system_instructions=SYSTEM_INSTRUCTION,
    tools=tools.ollama_tools()
)


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
     
     id_telegram = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]

     if data == "lang_es":
        IDIOMAS_USUARIOS[id_telegram] = "es"
        context.user_data["idioma"] = IDIOMAS_USUARIOS[id_telegram] #Guardamos el idioma elegido en una variable temporal

        builtins._ = lambda texto: texto 
        await query.edit_message_text(text=("Idioma configurado en Español."))
        await context.bot.send_message(chat_id = update.effective_chat.id, text = mensaje_bienvenida.mensaje())
        await context.bot.send_message(chat_id = update.effective_chat.id, text = mensaje_bienvenida.mensaje_registro_telegram())
        await context.bot.set_my_commands(
        commands=[
            ("registro", "Crear una cuenta de héroe"),
            ("vincular", "Vincula una cuenta existente"),
            ("personaje", "Elige un personaje"),
            ("entrenar", "Elige uno de tus personajes y asígnale una tarea para entrenarlo"),
            ("nuevatarea", "Crea una tarea nueva"),
        ],
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )

     elif data == "lang_en":
        IDIOMAS_USUARIOS[id_telegram] = "en"
        context.user_data["idioma"] = IDIOMAS_USUARIOS[id_telegram] #Guardamos el idioma elegido en una variable temporal

        builtins._ = lambda texto: traducir(texto=texto, lang="en")
        await query.edit_message_text(text=("Language set to English."))
        await context.bot.send_message(chat_id = update.effective_chat.id, text = mensaje_bienvenida.mensaje())
        await context.bot.send_message(chat_id = update.effective_chat.id, text = mensaje_bienvenida.mensaje_registro_telegram())
        await context.bot.set_my_commands(
        [
            ("signup", "Create a hero account"),
            ("link", "Link an existing account"),
            ("character", "Choose a character"),
            ("train", "Choose one of your characters and assign a task to train them"),
            ("newtask", "Create a new task"),
        ],
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )
          

async def interaccion_ia(update, context):
    mensaje_usuario = update.message.text
    
    if mensaje_usuario.startswith('/'):
        return 

    try:
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await update.message.reply_text("Buscando en los Registros Antiguos... Ten un poco de paciencia, por favor")
        sticker_carga = "./assets/animaciones/carga/animacion_puntos_suspensivos.webm"

        await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=sticker_carga)

        #Llamada a la IA
        respuesta_ia = ia.preguntar(mensaje_usuario)
        
        await update.message.reply_text(respuesta_ia, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error en IA: {e}")
        await update.message.reply_text("Error al buscar en los Registros Antiguos... Puede que hayan sido robados por seres malignos ajenos al Gremio")
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CONVERSATION HANDLERS

#REGISTRO
#-----------------------------------------------------------------------------------------------------------------------------
NOMBRE, PASSWORD, EMAIL = range(3)

@idioma_elegido
@usuario_existe
async def pide_nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    pide_usuario = crear_cuenta.nombre_usuario()

    await context.bot.send_message(chat_id=chat_id, text= _(f"{pide_usuario} Puedes cancelar en cualquier momento con /cancelar"))


    return NOMBRE

#----------------------------------------------------------------------------------------

async def nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_usuario'] = update.message.text.strip().lower()

    usuario_en_bd = usuario.buscar_usuario_por_nombre(context.user_data['nombre_usuario'])
    if usuario_en_bd:
            await update.message.reply_text(_("Ya estás registrado"))
            return ConversationHandler.END
    else:
        pide_contraseña = crear_cuenta.contraseña()

        await update.message.reply_text(_(f"Perfecto, {update.message.text}. " + f"{pide_contraseña}"))
        return PASSWORD

#----------------------------------------------------------------------------------------
async def contraseña (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password_usuario'] = update.message.text

    pide_email = crear_cuenta.email()

    await update.message.reply_text(_(f"De acuerdo. " + f"{pide_email}"))
    return EMAIL
    
#----------------------------------------------------------------------------------------

async def email (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email_usuario'] = update.message.text

    nombre = context.user_data.get('nombre_usuario')
    password = context.user_data.get('password_usuario')
    password_bytes = f"{password}".encode()
    password_encriptado = hashlib.sha256(password_bytes).hexdigest()[:8]
    email = context.user_data.get('email_usuario')
    idioma = context.user_data.get("idioma")

    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]

    usuario.registrar_usuario(
            nombre_usuario=nombre,
            password_usuario=password_encriptado,
            email_usuario=email,
            rango= Rango.novato,
            tipo_usuario=TiposUsuario.USUARIO,
            idioma_usuario= idioma,
            id_plataforma = CorrespondenciaPlataformas.TELEGRAM,
            nombre_plataforma="TELEGRAM",
            id_externo_usuario=id_generado

        )
    
    await update.message.reply_text(_(f"Cuenta creada"))

    return ConversationHandler.END

#----------------------------------------------------------------------------------------

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registro cancelado. Puedes volver a empezar con /registro.")
    return ConversationHandler.END

#----------------------------------------------------------------------------------------

PEDIR_NOMBRE, PEDIR_PASSWORD = range(2)

@usuario_existe
async def vincular(update:Update, context: ContextTypes.DEFAULT_TYPE):
     pide_usuario = crear_cuenta.nombre_usuario()
     await update.message.reply_text(_(f"{pide_usuario}"))
     return PEDIR_NOMBRE

async def obtener_username (update:Update, context: ContextTypes.DEFAULT_TYPE):
     context.user_data["nombre_usuario"] = update.message.text.strip().lower()
     pide_password = crear_cuenta.contraseña()
     await update.message.reply_text(pide_password)
     return PEDIR_PASSWORD

async def obtener_password (update:Update, context: ContextTypes.DEFAULT_TYPE):
     context.user_data["password_usuario"] = update.message.text

     nombre_usuario = context.user_data.get("nombre_usuario")
     password_usuario = context.user_data.get("password_usuario")

     id_plataforma = CorrespondenciaPlataformas.TELEGRAM
     nombre_plataforma = "TELEGRAM"
     id_externo_usuario = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]
     

     usuario_existe = usuario.comprobar_usuario(nombre_usuario, password_usuario)
     id_usuario = usuario_existe.id_usuario

     if usuario_existe:
          
          plataformas.vincular_plataforma(id_plataforma,nombre_plataforma, id_externo_usuario, id_usuario)

          await update.message.reply_text(f"Cuenta vinculada correctamente")
          
          return ConversationHandler.END
     
     else:
          await update.message.reply_text(f"No se encuentra al usuario")
          
          return ConversationHandler.END