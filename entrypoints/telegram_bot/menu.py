from telegram import BotCommand

async def menu(application):
    commands = []

    await application.bot.set_my_commands(commands)

