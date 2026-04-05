#IMPORTACIONES
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#Externas
import discord
from discord.ext import commands
#----------------------------------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
#----------------------------------------------------------------------------------------------------------------

#Locales
from core.infrastructure.mysql_repository import MySQLUsuarioRepository
from core.application.use_cases import RegistroNuevoJugadorUseCase, ObtenerSaludoUseCase
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)


db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}


repo = MySQLUsuarioRepository(db_config)
registro_use_case = RegistroNuevoJugadorUseCase(repo)
saludo_use_case = ObtenerSaludoUseCase(repo)

saludo_use_case = ObtenerSaludoUseCase(repo)



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id_discord = message.author.id
    nombre_usuario_discord = message.author.name

    registro_use_case.ejecutar(
        id_externo=str(user_id_discord), 
        plataforma='discord', 
        nombre_sugerido=nombre_usuario_discord
    )

    await bot.process_commands(message)


    
@bot.command()
async def hello(ctx):
    # 'ctx' (contexto) contiene todo: autor, canal, id, etc.
    user_id_discord = str(ctx.author.id)

    mensaje_saludo = saludo_use_case.ejecutar(id_externo=user_id_discord, plataforma='discord')

    
    await ctx.send(mensaje_saludo)  

bot.run(DISCORD_TOKEN)
