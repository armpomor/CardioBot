"""
Module for turning the bot into maintenance mode
"""

import logging
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.types import Message
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from config.get_settings import config

logger = logging.getLogger(__name__)

# Router for bot maintenance mode
maintenance_router = Router()
# Install filters for this router
maintenance_router.message.filter(
    MagicData(F.maintenance_mode.is_(config.tg_bot.data["MODE"]))
)
maintenance_router.callback_query.filter(
    MagicData(F.maintenance_mode.is_(config.tg_bot.data["MODE"]))
)


@maintenance_router.message()
async def any_message(message: Message, i18n: TranslatorRunner):
    """
    Handler intercepts all messages if MODE is True
    """
    await message.answer(i18n.service_mode(), show_alert=True)


@maintenance_router.callback_query()
async def any_callback(message: Message, i18n: TranslatorRunner):
    """
    The handler intercepts all callbacks, if MODE is True
    """
    await message.answer(i18n.service_mode(), show_alert=True)
