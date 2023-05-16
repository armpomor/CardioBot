from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot):
    """
    Deletes the main menu
    """
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')
