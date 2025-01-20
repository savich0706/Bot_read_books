from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS

# Функция для настройки кнопки МЕНЮ бота
async def set_menu(bot: Bot):
    menu_commands = [BotCommand(
        command=command,
        description=description)
            for command, description in LEXICON_COMMANDS.items()]
    
    await bot.set_my_commands(menu_commands)