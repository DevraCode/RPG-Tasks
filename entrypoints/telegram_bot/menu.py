from telegram import BotCommand

async def menu(application):
    commands = [
        BotCommand("registro", "Registrarse en el sistema"),
        BotCommand("vincular", "Vincula una cuenta existente"),
        BotCommand("personaje", "Elige un personaje"),
        BotCommand("entrenar", "Elige uno de tus personajes y asígnale una tarea para entrenarlo"),
        BotCommand("nuevatarea", "Crea una tarea nueva"),
            
    ]

    await application.bot.set_my_commands(commands)

