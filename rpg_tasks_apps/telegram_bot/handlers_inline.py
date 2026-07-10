from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext, CallbackQueryHandler

import hashlib

from rpg_tasks.infrastructure.dbconfig import db_config
from rpg_tasks.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from rpg_tasks.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from rpg_tasks.core.application.use_cases.usuarios_use_cases import UsuarioUseCase
from rpg_tasks.core.application.use_cases.personajes_use_cases import PersonajeUseCase

repo_usuarios = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)

usuarios = UsuarioUseCase(repo_usuarios)
personajes = PersonajeUseCase(repo_personajes, repo_usuarios)

async def inline_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.inline_query.query.strip().lower()

    id_externo = hashlib.sha256(str(update.effective_user.id).encode()).hexdigest()[:8]

    usuario_objeto = usuarios.buscar_id_externo_usuario(id_externo)

    id_usuario = usuario_objeto.id_usuario

    print(f"Buscando personajes para el ID interno: {id_usuario}")

    try:
        lista_personajes = personajes.lista_personajes_usuario(id_usuario)
        print(f"Personajes encontrados: {len(lista_personajes)}")
    except Exception as e:
        print(f"Error en DB: {e}")
        return

    resultados = []

    for personaje in lista_personajes:
            nombre_personaje = personaje.get('nombre_personaje', 'Sin nombre')
            id_personaje = personaje.get('id_personaje')

            keyboard = [
                 [InlineKeyboardButton(text="Ver Personaje", callback_data=f"stats_{id_personaje}")]
            ]
            
            if not query or query in personaje["nombre_personaje"].lower():
            
                resultados.append(
                    InlineQueryResultArticle(
                    id=str(id_personaje),
                    description="Haz clic para enviar este personaje",
                    title=nombre_personaje,
                    thumbnail_url="https://i.postimg.cc/FRMXST6j/rpg-game-(1).png",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{nombre_personaje}"
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                )
            
            
    print(f"Enviando {len(resultados)} resultados a Telegram")
    await update.inline_query.answer(resultados, cache_time=5)


async def manejador_stats(update:Update, context:ContextTypes.DEFAULT_TYPE):
         query = update.callback_query
         await query.answer()

         data = query.data.split("_")
         id_personaje = int(data[1])

         personaje = personajes.buscar_personaje_por_id(id_personaje)
         print(f"📦 Resultado obtenido: {personaje}")


         if personaje is None:
            print(f"ERROR: No se encontró el personaje con ID {id_personaje}")
            await context.bot.edit_message_text(
                inline_message_id=query.inline_message_id,
                text="❌ Error: El personaje ya no existe en la base de datos."
            )
            return


         mensaje_stats = (
            f"*{personaje['nombre_personaje']}*\n\n"
            f"Clase: {personaje['clase']}\n"
            f"Nivel: {personaje['nivel']}\n"
            f"EXP: {personaje['exp']}\n"
            
            
        )

         await context.bot.edit_message_text(
            inline_message_id=query.inline_message_id,
            text=mensaje_stats,
            parse_mode="Markdown"
            )

         