from telegram import BotCommand

async def menu(application):
    commands = [
        BotCommand("registro", "Registrarse en el sistema")
            
    ]

    await application.bot.set_my_commands(commands)

