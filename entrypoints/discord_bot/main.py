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
from core.application.use_cases import MensajeInicioUseCase, RegistroNuevoJugadorUseCase, ObtenerSaludoUseCase
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
mensaje_bienvenida = MensajeInicioUseCase()

registro_use_case = RegistroNuevoJugadorUseCase(repo)
saludo_use_case = ObtenerSaludoUseCase(repo)


@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

    # 1. Buscamos el canal por nombre en todos los servidores donde esté el bot
    for guild in bot.guilds:
        # Buscamos el canal 'bienvenida' (o el nombre que prefieras)
        channel = discord.utils.get(guild.text_channels, name="pruebas")
        
        # Si no lo encuentra por ese nombre, podemos buscar otro
        if not channel:
            channel = discord.utils.get(guild.text_channels, name="general")

        # 2. Si encontramos el canal y tenemos permiso para escribir
        if channel and channel.permissions_for(guild.me).send_messages:
            mensaje_inicio = mensaje_bienvenida.mensaje()
            segundo_mensaje = mensaje_bienvenida.segundo_mensaje()
            
            # Opcional: Añadir un aviso de que el sistema está en línea
            await channel.send(f"⚠️ **Sistema RPG Tasks Iniciado**\n\n{mensaje_inicio}")
            await channel.send(segundo_mensaje)
            
            # Usamos break si solo quieres que mande el mensaje en el primer servidor que encuentre
            # break

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # IMPORTANTE: Eliminamos el registro de aquí para no saturar la DB
    # Solo procesamos los comandos (como !hello)
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    user_id_discord = str(ctx.author.id)
    # Aquí el usuario ya debería estar registrado por el evento de arriba
    mensaje_saludo = saludo_use_case.ejecutar(id_externo=user_id_discord, plataforma='discord')
    await ctx.send(mensaje_saludo)



bot.run(DISCORD_TOKEN)
