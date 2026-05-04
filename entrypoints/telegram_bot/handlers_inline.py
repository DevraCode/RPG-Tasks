from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

import hashlib

from core.infrastructure.dbconfig import db_config
from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.infrastructure.repositorios.mysql_personajes_repository import MySQLPersonajesRepository
from core.application.use_cases.basico.usuarios_use_cases import UsuarioUsecase
from core.application.use_cases.basico.personajes_use_cases import PersonajeUseCase

repo_usuarios = MySQLUsuarioRepository(db_config)
repo_personajes = MySQLPersonajesRepository(db_config)

usuarios = UsuarioUsecase(repo_usuarios)
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
            
            
            if not query or query in personaje["nombre_personaje"].lower():
            
                resultados.append(
                    InlineQueryResultArticle(
                    id=str(id_personaje),
                    description="Haz clic para enviar este personaje",
                    title=nombre_personaje,
                    thumbnail_url="https://i.postimg.cc/FRMXST6j/rpg-game-(1).png",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{nombre_personaje}"
                    )
                )
                )
            
            
    print(f"Enviando {len(resultados)} resultados a Telegram")
    await update.inline_query.answer(resultados, cache_time=5)