from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_commands import LEXICON_COMMANDS


async def set_menu(bot: Bot):
    """
    Кнопка меню
    """
    menu_commands = [BotCommand(command=command, description=description) for command, description in
                     LEXICON_COMMANDS.items()]
    await bot.set_my_commands(menu_commands)
