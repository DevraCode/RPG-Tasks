from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

async def inline_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    #AQUI funcion para buscar al personaje en la BD por nombre

    respuesta = InlineQueryResultArticle(
        id="1",
        title=f"Personaje {query}",
        input_message_content=InputTextMessageContent(
            message_text=f"{query}"
        )
    )

    return respuesta