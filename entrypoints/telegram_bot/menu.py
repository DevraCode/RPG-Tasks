from telegram import BotCommand

async def menu(application):
    commands = [
        BotCommand("registro", "Registrarse en el sistema"),
        BotCommand("personaje", "Elige un personaje"),
            
    ]

    await application.bot.set_my_commands(commands)

