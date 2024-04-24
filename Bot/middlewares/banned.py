from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.config_data import BANNED


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
        if event.from_user.id in BANNED:
            return await event.answer(text="You are banned from the bot!")

        return await handler(event, data)
