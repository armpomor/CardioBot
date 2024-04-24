import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from states.states import StartSG

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    """
    We start a new dialogue with the stack reset.
    """
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
