import logging
from typing import Any, Awaitable, Callable, Dict, TYPE_CHECKING

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from config.config_data import BANNED

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    """
    We ban users who are in the BANNED list
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        i18n: TranslatorRunner = data.get("i18n")
        logger.info(i18n)

        if event.from_user.id in BANNED:
            return await event.answer(text=i18n.you_banned())

        return await handler(event, data)
