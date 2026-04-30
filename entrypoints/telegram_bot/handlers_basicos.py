#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.domain.models import CorrespondenciaPlataformas, TiposUsuario, Rango
from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_plataformas_repository import MySQLPlataformasRepository
from core.application.use_cases import MensajeInicioUseCase, CrearCuentaUseCase, UsuarioUsecase, PlataformasUseCase
from .dbconfig import db_config
from .decoradores import usuario_existe

from core.infrastructure.servicios_ia.cliente_gemini import GeminiService
from core.infrastructure.servicios_ia.gemini_tools import gemini_tools

token_gemini = os.getenv("GEMINI_API_KEY")


herramientas = gemini_tools(db_config)
ia = GeminiService(
    api_key=token_gemini, 
    model_name="gemini-2.5-flash", 
    tools=herramientas
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta_ia = ia.ask(update.message.text)
    
    await update.message.reply_text(respuesta_ia)


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

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#HANDLERS
async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_inicio = mensaje_bienvenida.mensaje()
    await update.message.reply_text(mensaje_inicio)
    await update.message.reply_text(f"Utiliza el comando /registro para crear una cuenta. Si ya tienes cuenta, utiliza el comando /vincular para iniciar sesión")
    

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CONVERSATION HANDLERS

#REGISTRO
#-----------------------------------------------------------------------------------------------------------------------------
NOMBRE, PASSWORD, EMAIL = range(3)

@usuario_existe
async def pide_nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    pide_usuario = crear_cuenta.nombre_usuario()

    await context.bot.send_message(chat_id=chat_id, text=pide_usuario + f". Puedes cancelar en cualquier momento con /cancelar")
    return NOMBRE

#----------------------------------------------------------------------------------------

async def nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_usuario'] = update.message.text.strip().lower()

    usuario_en_bd = usuario.buscar_usuario_por_nombre(context.user_data['nombre_usuario'])
    if usuario_en_bd:
            await update.message.reply_text(f"Ya estás registrado")
            return ConversationHandler.END
    else:
        pide_contraseña = crear_cuenta.contraseña()

        await update.message.reply_text(f"Perfecto, {update.message.text}." + f"{pide_contraseña}")
        return PASSWORD

#----------------------------------------------------------------------------------------
async def contraseña (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password_usuario'] = update.message.text

    pide_email = crear_cuenta.email()

    await update.message.reply_text(f"De acuerdo, {update.message.text}." + f"{pide_email}")
    return EMAIL
    
#----------------------------------------------------------------------------------------

async def email (update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email_usuario'] = update.message.text

    nombre = context.user_data.get('nombre_usuario')
    password = context.user_data.get('password_usuario')
    password_bytes = f"{password}".encode()
    password_encriptado = hashlib.sha256(password_bytes).hexdigest()[:8]
    email = context.user_data.get('email_usuario')

    id_generado = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]

    usuario.registrar_usuario(
            nombre_usuario=nombre,
            password_usuario=password_encriptado,
            email_usuario=email,
            rango= Rango.novato,
            tipo_usuario=TiposUsuario.USUARIO,
            id_plataforma = CorrespondenciaPlataformas.TELEGRAM,
            nombre_plataforma="TELEGRAM",
            id_externo_usuario=id_generado

        )
    
    await update.message.reply_text(f"Cuenta creada")



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
     await update.message.reply_text(pide_usuario)
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