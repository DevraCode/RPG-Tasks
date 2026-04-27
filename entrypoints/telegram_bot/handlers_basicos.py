#IMPORTACIONES
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Externas
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import hashlib

#-----------------------------------------------------------------------------------------------------------------------------

#Internas
from core.domain.models import CorrespondenciaPlataformas, TiposUsuario, Rango
from core.infrastructure.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases import MensajeInicioUseCase, CrearCuentaUseCase, BuscarPorIdExternoUseCase, RegistrarUsuarioUsecase
from .dbconfig import db_config
from .decoradores import usuario_registrado, usuario_inactivo

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

#INYECCIÓN DE DEPENDENCIAS
repo_usuario = MySQLUsuarioRepository(db_config)
mensaje_bienvenida = MensajeInicioUseCase()
crear_cuenta = CrearCuentaUseCase()
buscar_por_id_externo_use_case = BuscarPorIdExternoUseCase(repo_usuario)
registrar_usuario_use_case = RegistrarUsuarioUsecase(repo_usuario)


#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#HANDLERS
async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_inicio = mensaje_bienvenida.mensaje()

    await update.message.reply_text(mensaje_inicio)
    await update.message.reply_text(f"Utiliza el comando /registro para crear una cuenta o /iniciarsesion para iniciar sesión")
    

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#CONVERSATION HANDLERS

#REGISTRO
#-----------------------------------------------------------------------------------------------------------------------------
NOMBRE, PASSWORD, EMAIL = range(3)

@usuario_registrado # Comprueba si el usuario existe o no en la bd
@usuario_inactivo # Comprueba que el usuario esté o no inactivo por alguna razón
async def pide_nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    pide_usuario = crear_cuenta.nombre_usuario()

    await context.bot.send_message(chat_id=chat_id, text=pide_usuario + f". Puedes cancelar en cualquier momento con /cancelar")
    return NOMBRE

#----------------------------------------------------------------------------------------

async def nombre_usuario (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre_usuario'] = update.message.text.strip().lower()

    usuario_en_bd = repo_usuario.buscar_usuario_en_bd(context.user_data['nombre_usuario'])
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

    registrar_usuario_use_case.registrar_usuario(
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