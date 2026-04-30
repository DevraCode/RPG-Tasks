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
from core.infrastructure.repositorios.mysql_usuario_repository import MySQLUsuarioRepository
from core.application.use_cases import MensajeInicioUseCase, RegistroNuevoJugadorUseCase, ObtenerCatalogoUseCase
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

obtener_catalogo_use_case = ObtenerCatalogoUseCase()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

    
    for guild in bot.guilds:
       
        channel = discord.utils.get(guild.text_channels, name="pruebas")
        
        
        if not channel:
            channel = discord.utils.get(guild.text_channels, name="general")

        
        if channel and channel.permissions_for(guild.me).send_messages:
            mensaje_inicio = mensaje_bienvenida.mensaje()
            segundo_mensaje = "Utiliza el comando !registro para empezar o !iniciarsesion si ya tienes una cuenta"
            
            
            await channel.send(f"⚠️ **Sistema RPG Tasks Iniciado**\n\n{mensaje_inicio}")
            await channel.send(segundo_mensaje)
            
            

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)



@bot.command()
async def elegir_clase(ctx):
    
    catalogo = obtener_catalogo_use_case.ejecutar()
    
    for clave, datos in catalogo.items():
        ruta_archivo = datos["imagen_gif"]
        
        
        archivo_discord = discord.File(ruta_archivo, filename=datos["imagen_gif"])
        embed = discord.Embed(title=f"Clase: {datos['clase']}")
        embed.set_image(url=f"attachment://{datos['imagen_gif']}")
        
        
        await ctx.send(file=archivo_discord, embed=embed)

bot.run(DISCORD_TOKEN)
